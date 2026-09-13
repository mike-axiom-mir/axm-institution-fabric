from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError, make_immutable_ref
from axm_institution.lifecycle import admit_occupancy, open_work_claim
from axm_institution.resolution import (
    RevisionMemberAmbiguityError,
    RevisionMemberNotFoundError,
)
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
)


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class FinalWriteCallerMutationStore(FilesystemObjectStore):
    """Mutate only caller-owned claim state at the final claim-store boundary."""

    def __init__(self, root: Path | str) -> None:
        super().__init__(root)
        self.caller_claim = None
        self.mutation = None

    def store(self, value, schema_name, *, expected_reference=None):
        if (
            schema_name == "work-claim.schema.json"
            and self.caller_claim is not None
            and self.mutation is not None
        ):
            self.mutation(self.caller_claim)
        return super().store(
            value,
            schema_name,
            expected_reference=expected_reference,
        )


class WorkClaimAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self, *, purpose: str | None = None):
        lane = self._fixture("lane.schema.json")
        if purpose is not None:
            lane["purpose"] = purpose
        return lane, self.store.store(lane, "lane.schema.json")

    def _store_base(self, lane_refs: list[str], *, revision_id: str | None = None):
        revision = self._fixture("state-revision.schema.json")
        revision["lane_refs"] = lane_refs
        if revision_id is not None:
            revision["id"] = revision_id
        return self.store.store(revision, "state-revision.schema.json")

    def _occupancy_for(self, base_ref: str, lane_id: str):
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane_id
        return occupancy

    def _admit_occupancy(self, base_ref: str, lane_id: str, *, occupancy=None):
        candidate = occupancy or self._occupancy_for(base_ref, lane_id)
        result = admit_occupancy(self.store, candidate)
        return candidate, result

    def _claim_for(self, base_ref: str, lane_id: str, occupancy_ref: str):
        claim = self._fixture("work-claim.schema.json")
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane_id
        claim["occupancy_ref"] = occupancy_ref
        return claim

    def _state_revision_files(self) -> list[Path]:
        root = self.store.objects_dir / "state-revision"
        return list(root.rglob("*.json")) if root.exists() else []

    def _claim_files(self) -> list[Path]:
        root = self.store.objects_dir / "work-claim"
        return list(root.rglob("*.json")) if root.exists() else []

    def test_open_claim_persists_exact_candidate_and_returns_exact_dependencies(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)

        before_revisions = self._state_revision_files()
        result = open_work_claim(self.store, claim)
        after_revisions = self._state_revision_files()

        self.assertTrue(result.created)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertEqual(
            result.claim_ref,
            make_immutable_ref("work-claim.schema.json", claim),
        )
        self.assertEqual(self.store.load(result.claim_ref, "work-claim.schema.json"), claim)
        self.assertEqual(before_revisions, after_revisions)
        self.assertEqual(len(after_revisions), 1)

    def test_reopening_same_exact_claim_is_idempotent_without_successor_revision(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)

        first = open_work_claim(self.store, claim)
        second = open_work_claim(self.store, claim)

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.claim_ref, second.claim_ref)
        self.assertEqual(first.occupancy_ref, second.occupancy_ref)
        self.assertEqual(first.lane_ref, second.lane_ref)
        self.assertEqual(len(self._state_revision_files()), 1)

    def test_non_open_claim_status_fails_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)
        claim["status"] = "submitted"

        with self.assertRaises(ContractValidationError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_same_logical_lane_twice_in_exact_claim_base_is_ambiguous(self) -> None:
        lane, first_result = self._store_lane()
        second = copy.deepcopy(lane)
        second["purpose"] = "Second exact lane instance with the same logical id."
        second_result = self.store.store(second, "lane.schema.json")
        base_result = self._store_base([first_result.reference, second_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy_result = admit_occupancy(
            self.store,
            {**occupancy, "lane_id": "lane-missing-for-admission"},
        ) if False else self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.reference)

        with self.assertRaises(RevisionMemberAmbiguityError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_zero_lane_match_in_exact_claim_base_fails_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(base_result.reference, "lane-missing", occupancy_result.reference)

        with self.assertRaises(RevisionMemberNotFoundError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_newer_same_id_lane_elsewhere_cannot_override_exact_claim_base(self) -> None:
        lane, base_lane_result = self._store_lane()
        base_result = self._store_base([base_lane_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])

        newer_lane = copy.deepcopy(lane)
        newer_lane["purpose"] = "Later same-id lane stored outside the exact claim base."
        newer_lane_result = self.store.store(newer_lane, "lane.schema.json")
        self.assertNotEqual(base_lane_result.reference, newer_lane_result.reference)

        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)
        result = open_work_claim(self.store, claim)

        self.assertEqual(result.lane_ref, base_lane_result.reference)
        self.assertNotEqual(result.lane_ref, newer_lane_result.reference)

    def test_missing_exact_occupancy_fails_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        missing_occupancy_ref = make_immutable_ref("occupancy.schema.json", occupancy)
        claim = self._claim_for(base_result.reference, lane["id"], missing_occupancy_ref)

        with self.assertRaises(ObjectNotFoundError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_corrupt_exact_occupancy_fails_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])
        self.store._object_path(occupancy_result.occupancy_ref).write_bytes(b"{}")
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)

        with self.assertRaises(ObjectCorruptionError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_wrong_kind_occupancy_ref_is_rejected_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        claim = self._claim_for(base_result.reference, lane["id"], lane_result.reference)

        with self.assertRaises(ContractValidationError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_exact_occupancy_lane_must_match_claim_lane(self) -> None:
        lane, lane_result = self._store_lane()
        decoy = copy.deepcopy(lane)
        decoy["id"] = "lane-decoy"
        decoy["purpose"] = "Second lane used only to prove occupancy/claim lane mismatch."
        decoy_result = self.store.store(decoy, "lane.schema.json")
        base_result = self._store_base([lane_result.reference, decoy_result.reference])
        _, occupancy_result = self._admit_occupancy(base_result.reference, decoy["id"])
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)

        with self.assertRaises(ContractValidationError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_later_claim_base_need_not_equal_occupancy_entry_base(self) -> None:
        lane, lane_result = self._store_lane()
        occupancy_base = self._store_base([lane_result.reference], revision_id="revision.occupancy-base")
        _, occupancy_result = self._admit_occupancy(occupancy_base.reference, lane["id"])
        claim_base = self._store_base([lane_result.reference], revision_id="revision.claim-base")
        self.assertNotEqual(occupancy_base.reference, claim_base.reference)

        claim = self._claim_for(claim_base.reference, lane["id"], occupancy_result.occupancy_ref)
        result = open_work_claim(self.store, claim)

        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(
            self.store.load(result.claim_ref, "work-claim.schema.json")["base_state_revision_ref"],
            claim_base.reference,
        )

    def test_ended_exact_occupancy_snapshot_cannot_open_claim(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["status"] = "ended"
        occupancy["ended_at"] = "2026-09-13T06:30:00Z"
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.reference)

        with self.assertRaises(ContractValidationError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_snapshot_claim_ids_and_overlap_ids_do_not_become_ownership_authority(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["claim_ids"] = ["claim.unrelated.snapshot"]
        _, occupancy_result = self._admit_occupancy(
            base_result.reference,
            lane["id"],
            occupancy=occupancy,
        )
        claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)
        claim["overlap_with_claim_ids"] = ["claim.reported.overlap"]

        result = open_work_claim(self.store, claim)
        reloaded_claim = self.store.load(result.claim_ref, "work-claim.schema.json")
        reloaded_occupancy = self.store.load(result.occupancy_ref, "occupancy.schema.json")

        self.assertEqual(reloaded_claim["overlap_with_claim_ids"], ["claim.reported.overlap"])
        self.assertEqual(reloaded_occupancy["claim_ids"], ["claim.unrelated.snapshot"])

    def test_later_same_logical_occupancy_cannot_rebind_exact_claim_target(self) -> None:
        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference])
        first_occupancy = self._occupancy_for(base_result.reference, lane["id"])
        first_result = admit_occupancy(self.store, first_occupancy)

        later_occupancy = copy.deepcopy(first_occupancy)
        later_occupancy["actor_ref"] = "fixture:occupant-b"
        later_result = self.store.store(later_occupancy, "occupancy.schema.json")
        self.assertNotEqual(first_result.occupancy_ref, later_result.reference)

        claim = self._claim_for(base_result.reference, lane["id"], first_result.occupancy_ref)
        result = open_work_claim(self.store, claim)

        self.assertEqual(result.occupancy_ref, first_result.occupancy_ref)
        self.assertNotEqual(result.occupancy_ref, later_result.reference)

    def test_missing_exact_base_fails_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        revision = self._fixture("state-revision.schema.json")
        revision["lane_refs"] = [lane_result.reference]
        missing_base_ref = make_immutable_ref("state-revision.schema.json", revision)
        occupancy = self._occupancy_for(missing_base_ref, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(missing_base_ref, lane["id"], occupancy_result.reference)

        with self.assertRaises(ObjectNotFoundError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_wrong_kind_base_reference_is_rejected_before_claim_persistence(self) -> None:
        lane, lane_result = self._store_lane()
        occupancy = self._fixture("occupancy.schema.json")
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(lane_result.reference, lane["id"], occupancy_result.reference)

        with self.assertRaises(ContractValidationError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_caller_mutation_at_final_write_cannot_change_grounded_exact_claim(self) -> None:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        store = FinalWriteCallerMutationStore(Path(tempdir.name))
        self.store = store

        lane, lane_result = self._store_lane()
        base_result = self._store_base([lane_result.reference], revision_id="revision.claim-original")
        _, occupancy_result = self._admit_occupancy(base_result.reference, lane["id"])

        decoy_lane = copy.deepcopy(lane)
        decoy_lane["id"] = "lane-decoy"
        decoy_lane["purpose"] = "Decoy lane for final-write caller mutation."
        decoy_lane_result = store.store(decoy_lane, "lane.schema.json")
        decoy_base = self._store_base([decoy_lane_result.reference], revision_id="revision.claim-decoy")
        decoy_occupancy = self._occupancy_for(decoy_base.reference, decoy_lane["id"])
        decoy_occupancy["id"] = "occupancy.decoy"
        decoy_occupancy_result = admit_occupancy(store, decoy_occupancy)

        caller_claim = self._claim_for(base_result.reference, lane["id"], occupancy_result.occupancy_ref)
        original_claim = copy.deepcopy(caller_claim)
        expected_ref = make_immutable_ref("work-claim.schema.json", original_claim)

        def mutate(claim):
            claim["lane_id"] = decoy_lane["id"]
            claim["base_state_revision_ref"] = decoy_base.reference
            claim["occupancy_ref"] = decoy_occupancy_result.occupancy_ref
            claim["summary"] = "Caller-mutated decoy summary."

        store.caller_claim = caller_claim
        store.mutation = mutate
        result = open_work_claim(store, caller_claim)

        self.assertNotEqual(caller_claim, original_claim)
        self.assertEqual(result.claim_ref, expected_ref)
        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(store.load(result.claim_ref, "work-claim.schema.json"), original_claim)


if __name__ == "__main__":
    unittest.main()
