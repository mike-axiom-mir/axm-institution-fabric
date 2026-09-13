from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ImmutableReferenceError, make_immutable_ref
from axm_institution.resolution import (
    RevisionMemberAmbiguityError,
    RevisionMemberConfigurationError,
    RevisionMemberNotFoundError,
    resolve_exact_revision_member,
)
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
)


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class ExactRevisionMemberResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_revision_with(self, member_field: str, member_refs: list[str]):
        revision = self._fixture("state-revision.schema.json")
        revision[member_field] = member_refs
        return self.store.store(revision, "state-revision.schema.json")

    def test_resolves_exact_lane_instance_from_exact_base(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])

        resolved = resolve_exact_revision_member(
            self.store,
            revision_result.reference,
            "lane_refs",
            "lane",
            lane["id"],
        )

        self.assertEqual(resolved.reference, lane_result.reference)
        self.assertEqual(resolved.value, lane)
        self.assertFalse(revision_result.referenced_members_verified)

    def test_zero_logical_id_match_fails_explicitly(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])

        with self.assertRaises(RevisionMemberNotFoundError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "lane",
                "lane-does-not-exist",
            )

    def test_two_exact_instances_with_same_logical_id_are_ambiguous(self) -> None:
        first = self._fixture("lane.schema.json")
        second = copy.deepcopy(first)
        second["purpose"] = "A second exact instance with the same persistent lane id."

        first_result = self.store.store(first, "lane.schema.json")
        second_result = self.store.store(second, "lane.schema.json")
        self.assertNotEqual(first_result.reference, second_result.reference)

        revision_result = self._store_revision_with(
            "lane_refs", [first_result.reference, second_result.reference]
        )

        with self.assertRaises(RevisionMemberAmbiguityError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "lane",
                first["id"],
            )

    def test_occupancy_family_uses_the_same_exact_base_primitive(self) -> None:
        occupancy = self._fixture("occupancy.schema.json")
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        revision_result = self._store_revision_with(
            "occupancy_refs", [occupancy_result.reference]
        )

        resolved = resolve_exact_revision_member(
            self.store,
            revision_result.reference,
            "occupancy_refs",
            "occupancy",
            occupancy["id"],
        )

        self.assertEqual(resolved.reference, occupancy_result.reference)
        self.assertEqual(resolved.value, occupancy)

    def test_work_claim_family_uses_the_same_exact_base_primitive(self) -> None:
        claim = self._fixture("work-claim.schema.json")
        claim_result = self.store.store(claim, "work-claim.schema.json")
        revision_result = self._store_revision_with("claim_refs", [claim_result.reference])

        resolved = resolve_exact_revision_member(
            self.store,
            revision_result.reference,
            "claim_refs",
            "work-claim",
            claim["id"],
        )

        self.assertEqual(resolved.reference, claim_result.reference)
        self.assertEqual(resolved.value, claim)

    def test_wrong_kind_for_membership_family_fails_configuration(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])

        with self.assertRaises(RevisionMemberConfigurationError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "occupancy",
                lane["id"],
            )

    def test_unknown_membership_family_fails_configuration(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])

        with self.assertRaises(RevisionMemberConfigurationError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "newest_lane_refs",
                "lane",
                lane["id"],
            )

    def test_missing_exact_member_propagates_object_not_found(self) -> None:
        lane = self._fixture("lane.schema.json")
        missing_ref = make_immutable_ref("lane.schema.json", lane)
        revision_result = self._store_revision_with("lane_refs", [missing_ref])

        with self.assertRaises(ObjectNotFoundError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "lane",
                lane["id"],
            )

    def test_missing_nonmatching_member_is_not_silently_skipped(self) -> None:
        target = self._fixture("lane.schema.json")
        target_result = self.store.store(target, "lane.schema.json")
        missing = copy.deepcopy(target)
        missing["id"] = "lane-unrelated-missing"
        missing_ref = make_immutable_ref("lane.schema.json", missing)
        revision_result = self._store_revision_with(
            "lane_refs", [target_result.reference, missing_ref]
        )

        with self.assertRaises(ObjectNotFoundError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "lane",
                target["id"],
            )

    def test_corrupt_exact_member_propagates_corruption_failure(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])
        self.store._object_path(lane_result.reference).write_bytes(b"{}")

        with self.assertRaises(ObjectCorruptionError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "lane_refs",
                "lane",
                lane["id"],
            )

    def test_noncanonical_base_reference_is_rejected_before_lookup(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")
        revision_result = self._store_revision_with("lane_refs", [lane_result.reference])
        noncanonical = revision_result.reference.replace(
            "revision.fixture.0001", "revision%2Efixture.0001"
        )

        with self.assertRaises(ImmutableReferenceError):
            resolve_exact_revision_member(
                self.store,
                noncanonical,
                "lane_refs",
                "lane",
                lane["id"],
            )

    def test_non_revision_base_kind_is_rejected(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")

        with self.assertRaises(RevisionMemberConfigurationError):
            resolve_exact_revision_member(
                self.store,
                lane_result.reference,
                "lane_refs",
                "lane",
                lane["id"],
            )


if __name__ == "__main__":
    unittest.main()
