from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Mapping

from axm_institution.identity import ContractValidationError
from axm_institution.lifecycle import admit_occupancy
from axm_institution.resolution import (
    RevisionMemberResolutionError,
    resolve_exact_revision_member,
)
from axm_institution.store import FilesystemObjectStore, ObjectStoreError


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class AliasingProbeStore(FilesystemObjectStore):
    """Deterministically simulate caller mutation at the final occupancy write boundary.

    The production API receives a caller-owned mutable dict. This probe mutates that
    exact dict only after admission has already grounded its base/lane relationship,
    immediately before the real immutable store serializes it. That avoids timing-
    dependent threading while exercising the same input-aliasing failure surface.
    """

    def __init__(self, root: Path, caller_occupancy: dict[str, Any]) -> None:
        super().__init__(root)
        self.caller_occupancy = caller_occupancy
        self.mutated = False

    def store(
        self,
        value: Mapping[str, Any],
        schema_name: str,
        *,
        expected_reference: str | None = None,
    ):
        if schema_name == "occupancy.schema.json" and not self.mutated:
            self.assert_same_object(value)
            self.caller_occupancy["lane_id"] = "lane-decoy"
            self.mutated = True
        return super().store(
            value,
            schema_name,
            expected_reference=expected_reference,
        )

    def assert_same_object(self, value: Mapping[str, Any]) -> None:
        if value is not self.caller_occupancy:
            raise AssertionError(
                "probe expected admit_occupancy to pass the caller-owned object into store()"
            )


class OccupancyAdmissionAdversarialTests(unittest.TestCase):
    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def test_adv_032_a_persisted_occupancy_must_match_grounded_lane_after_input_mutation(self) -> None:
        """A successful admission must preserve the relationship it actually grounded.

        Acceptable repaired outcomes are either:
        - explicit rejection before a contradictory occupancy is persisted; or
        - success using an internal immutable/snapshotted candidate whose lane relation
          remains the one that was verified.

        Returning success while persisting a different caller-mutated ``lane_id`` is
        not acceptable because a replacement occupant cannot reconstruct the returned
        lane relationship from the persisted occupancy.
        """

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)

            # Build the exact base using an ordinary store first so the only adversarial
            # behavior is the mutation of the proposed occupancy at its final write.
            setup_store = FilesystemObjectStore(root)
            lane = self._fixture("lane.schema.json")
            lane_result = setup_store.store(lane, "lane.schema.json")
            base = self._fixture("state-revision.schema.json")
            base["lane_refs"] = [lane_result.reference]
            base_result = setup_store.store(base, "state-revision.schema.json")

            occupancy = self._fixture("occupancy.schema.json")
            occupancy["base_state_revision_ref"] = base_result.reference
            occupancy["lane_id"] = lane["id"]

            store = AliasingProbeStore(root, occupancy)

            try:
                result = admit_occupancy(store, occupancy)
            except (ContractValidationError, RevisionMemberResolutionError, ObjectStoreError):
                # A future repair may choose explicit mutation/identity mismatch failure
                # rather than snapshotting. Either is continuity-safe.
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


if __name__ == "__main__":
    unittest.main()
