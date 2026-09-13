from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable, Mapping

from axm_institution.identity import ContractValidationError
from axm_institution.lifecycle import admit_occupancy
from axm_institution.resolution import (
    RevisionMemberResolutionError,
    resolve_exact_revision_member,
)
from axm_institution.store import FilesystemObjectStore, ObjectStoreError


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class FinalWriteMutationStore(FilesystemObjectStore):
    """Mutate only caller-owned input at the final occupancy write boundary.

    The value passed by production to ``store()`` is deliberately left untouched. A
    continuity-safe implementation may publish a detached function-owned candidate or
    fail closed after detecting drift. An aliased implementation will instead expose
    the caller mutation in durable state.
    """

    def __init__(
        self,
        root: Path,
        caller_occupancy: dict[str, Any],
        mutator: Callable[[dict[str, Any]], None],
    ) -> None:
        super().__init__(root)
        self.caller_occupancy = caller_occupancy
        self.mutator = mutator
        self.mutated = False

    def store(
        self,
        value: Mapping[str, Any],
        schema_name: str,
        *,
        expected_reference: str | None = None,
    ):
        if schema_name == "occupancy.schema.json" and not self.mutated:
            self.mutator(self.caller_occupancy)
            self.mutated = True
        return super().store(
            value,
            schema_name,
            expected_reference=expected_reference,
        )


class OccupancyAdmissionAdversarialTests(unittest.TestCase):
    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _setup_lane_and_base(self, root: Path):
        setup_store = FilesystemObjectStore(root)
        lane = self._fixture("lane.schema.json")
        lane_result = setup_store.store(lane, "lane.schema.json")
        base = self._fixture("state-revision.schema.json")
        base["lane_refs"] = [lane_result.reference]
        base_result = setup_store.store(base, "state-revision.schema.json")
        return setup_store, lane, lane_result, base_result

    def test_adv_032_a_persisted_occupancy_must_match_grounded_lane_after_input_mutation(self) -> None:
        """A successful admission must preserve the lane relation it grounded."""

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            _, lane, _, base_result = self._setup_lane_and_base(root)

            occupancy = self._fixture("occupancy.schema.json")
            occupancy["base_state_revision_ref"] = base_result.reference
            occupancy["lane_id"] = lane["id"]

            store = FinalWriteMutationStore(
                root,
                occupancy,
                lambda caller: caller.__setitem__("lane_id", "lane-decoy"),
            )

            try:
                result = admit_occupancy(store, occupancy)
            except (ContractValidationError, RevisionMemberResolutionError, ObjectStoreError):
                return

            persisted = store.load(result.occupancy_ref, "occupancy.schema.json")
            self.assertEqual(
                persisted["lane_id"],
                lane["id"],
                "admission returned success but persisted a lane_id that was never grounded",
            )
            resolved = resolve_exact_revision_member(
                store,
                persisted["base_state_revision_ref"],
                "lane_refs",
                "lane",
                persisted["lane_id"],
            )
            self.assertEqual(
                resolved.reference,
                result.lane_ref,
                "returned lane_ref must be reconstructable from the exact persisted occupancy",
            )

    def test_adv_032_b_base_ref_mutation_cannot_rebind_successful_admission(self) -> None:
        """Final-write mutation of the exact base must not rebind the grounded lane."""

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            setup_store, lane, lane_result, base_result = self._setup_lane_and_base(root)

            decoy_lane = copy.deepcopy(lane)
            decoy_lane["name"] = f"{decoy_lane['name']} decoy"
            decoy_lane_result = setup_store.store(decoy_lane, "lane.schema.json")
            self.assertNotEqual(lane_result.reference, decoy_lane_result.reference)

            decoy_base = self._fixture("state-revision.schema.json")
            decoy_base["lane_refs"] = [decoy_lane_result.reference]
            decoy_base_result = setup_store.store(decoy_base, "state-revision.schema.json")
            self.assertNotEqual(base_result.reference, decoy_base_result.reference)

            occupancy = self._fixture("occupancy.schema.json")
            occupancy["base_state_revision_ref"] = base_result.reference
            occupancy["lane_id"] = lane["id"]

            store = FinalWriteMutationStore(
                root,
                occupancy,
                lambda caller: caller.__setitem__(
                    "base_state_revision_ref", decoy_base_result.reference
                ),
            )

            try:
                result = admit_occupancy(store, occupancy)
            except (ContractValidationError, RevisionMemberResolutionError, ObjectStoreError):
                return

            persisted = store.load(result.occupancy_ref, "occupancy.schema.json")
            self.assertEqual(
                persisted["base_state_revision_ref"],
                base_result.reference,
                "admission returned success but persisted a base that was never grounded",
            )
            resolved = resolve_exact_revision_member(
                store,
                persisted["base_state_revision_ref"],
                "lane_refs",
                "lane",
                persisted["lane_id"],
            )
            self.assertEqual(resolved.reference, lane_result.reference)
            self.assertEqual(
                resolved.reference,
                result.lane_ref,
                "returned lane_ref must remain derivable from the persisted exact base",
            )

    def test_adv_032_c_nonrelationship_identity_mutation_cannot_change_published_candidate(self) -> None:
        """Proof-to-write continuity covers the exact occupancy, not only lane fields."""

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            setup_store, lane, _, base_result = self._setup_lane_and_base(root)

            occupancy = self._fixture("occupancy.schema.json")
            occupancy["base_state_revision_ref"] = base_result.reference
            occupancy["lane_id"] = lane["id"]
            original_candidate = copy.deepcopy(occupancy)
            original_actor_ref = occupancy["actor_ref"]

            store = FinalWriteMutationStore(
                root,
                occupancy,
                lambda caller: caller.__setitem__(
                    "actor_ref", f"{original_actor_ref}-decoy"
                ),
            )

            try:
                result = admit_occupancy(store, occupancy)
            except (ContractValidationError, RevisionMemberResolutionError, ObjectStoreError):
                return

            persisted = store.load(result.occupancy_ref, "occupancy.schema.json")
            self.assertEqual(
                persisted["actor_ref"],
                original_actor_ref,
                "successful admission published caller identity drift after grounding",
            )
            expected = setup_store.store(original_candidate, "occupancy.schema.json")
            self.assertEqual(
                result.occupancy_ref,
                expected.reference,
                "returned occupancy_ref must name the same exact candidate admitted before mutation",
            )


if __name__ == "__main__":
    unittest.main()
