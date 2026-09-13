from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError, make_immutable_ref
from axm_institution.lifecycle import admit_occupancy
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


class OccupancyAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_base(self, lane_refs: list[str]):
        revision = self._fixture("state-revision.schema.json")
        revision["lane_refs"] = lane_refs
        return self.store.store(revision, "state-revision.schema.json")

    def _occupancy_for(self, base_ref: str, lane_id: str):
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane_id
        return occupancy

    def _state_revision_files(self) -> list[Path]:
        root = self.store.objects_dir / "state-revision"
        return list(root.rglob("*.json")) if root.exists() else []

    def test_admission_persists_exact_occupancy_and_returns_exact_base_lane(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])

        before_revisions = self._state_revision_files()
        result = admit_occupancy(self.store, occupancy)
        after_revisions = self._state_revision_files()

        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertTrue(result.created)
        self.assertEqual(self.store.load(result.occupancy_ref, "occupancy.schema.json"), occupancy)
        self.assertEqual(
            result.occupancy_ref,
            make_immutable_ref("occupancy.schema.json", occupancy),
        )
        self.assertEqual(before_revisions, after_revisions)
        self.assertEqual(len(after_revisions), 1)

    def test_re_admission_is_idempotent_without_successor_revision(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])

        first = admit_occupancy(self.store, occupancy)
        second = admit_occupancy(self.store, occupancy)

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.occupancy_ref, second.occupancy_ref)
        self.assertEqual(first.lane_ref, second.lane_ref)
        self.assertEqual(len(self._state_revision_files()), 1)

    def test_same_logical_lane_twice_in_exact_base_is_ambiguous(self) -> None:
        first = self._fixture("lane.schema.json")
        second = copy.deepcopy(first)
        second["purpose"] = "Second exact lane instance with the same logical id."
        first_result = self.store.store(first, "lane.schema.json")
        second_result = self.store.store(second, "lane.schema.json")
        base_result = self._store_base([first_result.reference, second_result.reference])
        occupancy = self._occupancy_for(base_result.reference, first["id"])

        with self.assertRaises(RevisionMemberAmbiguityError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_zero_lane_match_fails_before_occupancy_persistence(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, "lane-missing")

        with self.assertRaises(RevisionMemberNotFoundError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_newer_same_id_lane_elsewhere_cannot_override_exact_base(self) -> None:
        base_lane = self._fixture("lane.schema.json")
        base_lane_result = self.store.store(base_lane, "lane.schema.json")
        base_result = self._store_base([base_lane_result.reference])

        newer_lane = copy.deepcopy(base_lane)
        newer_lane["purpose"] = "Later same-id lane stored outside the exact entry base."
        newer_lane_result = self.store.store(newer_lane, "lane.schema.json")
        self.assertNotEqual(base_lane_result.reference, newer_lane_result.reference)

        occupancy = self._occupancy_for(base_result.reference, base_lane["id"])
        result = admit_occupancy(self.store, occupancy)

        self.assertEqual(result.lane_ref, base_lane_result.reference)
        self.assertNotEqual(result.lane_ref, newer_lane_result.reference)

    def test_missing_exact_lane_member_fails_through_real_store_path(self) -> None:
        lane = self._fixture("lane.schema.json")
        missing_lane_ref = make_immutable_ref("lane.schema.json", lane)
        base_result = self._store_base([missing_lane_ref])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])

        with self.assertRaises(ObjectNotFoundError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_corrupt_exact_lane_member_fails_through_real_store_path(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        self.store._object_path(lane_result.reference).write_bytes(b"{}")
        occupancy = self._occupancy_for(base_result.reference, lane["id"])

        with self.assertRaises(ObjectCorruptionError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_missing_exact_base_fails_before_occupancy_persistence(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision = self._fixture("state-revision.schema.json")
        revision["lane_refs"] = [lane_result.reference]
        missing_base_ref = make_immutable_ref("state-revision.schema.json", revision)
        occupancy = self._occupancy_for(missing_base_ref, lane["id"])

        with self.assertRaises(ObjectNotFoundError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_noncanonical_base_reference_is_rejected_before_store_mutation(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["base_state_revision_ref"] = base_result.reference.replace(
            "revision.fixture.0001", "revision%2Efixture.0001"
        )

        with self.assertRaises(ContractValidationError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_wrong_kind_base_reference_is_rejected_by_occupancy_contract(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["base_state_revision_ref"] = lane_result.reference
        occupancy["lane_id"] = lane["id"]

        with self.assertRaises(ContractValidationError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())

    def test_actor_and_capability_refs_do_not_become_lane_selection_authority(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])

        decoy = copy.deepcopy(lane)
        decoy["id"] = "lane-decoy"
        decoy["purpose"] = "Stored decoy that is not a member of the exact base."
        self.store.store(decoy, "lane.schema.json")

        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["actor_ref"] = "lane-decoy"
        occupancy["capability_ref"] = "lane-decoy"

        result = admit_occupancy(self.store, occupancy)
        self.assertEqual(result.lane_ref, lane_result.reference)

    def test_claim_ids_remain_snapshot_data_and_do_not_open_claims(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["claim_ids"] = ["claim.not-opened.by-admission"]

        result = admit_occupancy(self.store, occupancy)
        reloaded = self.store.load(result.occupancy_ref, "occupancy.schema.json")

        self.assertEqual(reloaded["claim_ids"], ["claim.not-opened.by-admission"])
        self.assertFalse((self.store.objects_dir / "work-claim").exists())

    def test_invalid_occupancy_contract_fails_before_any_occupancy_write(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        base_result = self._store_base([lane_result.reference])
        occupancy = self._occupancy_for(base_result.reference, lane["id"])
        occupancy["ended_at"] = "2026-09-13T03:30:00Z"
        occupancy["status"] = "active"

        with self.assertRaises(ContractValidationError):
            admit_occupancy(self.store, occupancy)

        self.assertFalse((self.store.objects_dir / "occupancy").exists())


if __name__ == "__main__":
    unittest.main()
