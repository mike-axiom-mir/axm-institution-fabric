from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import make_immutable_ref
from axm_institution.resolution import (
    RevisionMemberAmbiguityError,
    resolve_exact_revision_member,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class Lane03ExactRevisionMemberAdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_revision(self, **member_fields):
        revision = self._fixture("state-revision.schema.json")
        for field, refs in member_fields.items():
            revision[field] = list(refs)
        return self.store.store(revision, "state-revision.schema.json")

    def test_lane_success_is_invariant_under_member_array_reordering(self) -> None:
        target = self._fixture("lane.schema.json")
        other = copy.deepcopy(target)
        other["id"] = "lane-03"
        other["name"] = "Institutional Continuity / Adversarial Systems Specialist"
        other["purpose"] = "Challenge continuity assumptions without becoming merge authority."

        target_result = self.store.store(target, "lane.schema.json")
        other_result = self.store.store(other, "lane.schema.json")

        forward = self._store_revision(
            lane_refs=[target_result.reference, other_result.reference]
        )
        reverse = self._store_revision(
            lane_refs=[other_result.reference, target_result.reference]
        )

        forward_resolved = resolve_exact_revision_member(
            self.store, forward.reference, "lane_refs", "lane", target["id"]
        )
        reverse_resolved = resolve_exact_revision_member(
            self.store, reverse.reference, "lane_refs", "lane", target["id"]
        )

        self.assertNotEqual(forward.reference, reverse.reference)
        self.assertEqual(forward_resolved.reference, target_result.reference)
        self.assertEqual(reverse_resolved.reference, target_result.reference)
        self.assertEqual(forward_resolved.value, target)
        self.assertEqual(reverse_resolved.value, target)

    def test_lane_ambiguity_is_invariant_under_member_array_reordering(self) -> None:
        first = self._fixture("lane.schema.json")
        second = copy.deepcopy(first)
        second["purpose"] = "Second exact instance sharing the same logical lane id."
        other = copy.deepcopy(first)
        other["id"] = "lane-03"
        other["name"] = "Institutional Continuity / Adversarial Systems Specialist"
        other["purpose"] = "Unrelated exact lane instance."

        first_result = self.store.store(first, "lane.schema.json")
        second_result = self.store.store(second, "lane.schema.json")
        other_result = self.store.store(other, "lane.schema.json")

        orders = [
            [first_result.reference, other_result.reference, second_result.reference],
            [second_result.reference, first_result.reference, other_result.reference],
            [other_result.reference, second_result.reference, first_result.reference],
        ]

        for refs in orders:
            revision_result = self._store_revision(lane_refs=refs)
            with self.subTest(order=refs):
                with self.assertRaises(RevisionMemberAmbiguityError):
                    resolve_exact_revision_member(
                        self.store,
                        revision_result.reference,
                        "lane_refs",
                        "lane",
                        first["id"],
                    )

    def test_occupancy_same_logical_id_different_exact_instances_are_ambiguous(self) -> None:
        first = self._fixture("occupancy.schema.json")
        second = copy.deepcopy(first)
        second["actor_ref"] = "fixture:occupant-b"

        first_result = self.store.store(first, "occupancy.schema.json")
        second_result = self.store.store(second, "occupancy.schema.json")
        self.assertNotEqual(first_result.reference, second_result.reference)

        revision_result = self._store_revision(
            occupancy_refs=[first_result.reference, second_result.reference]
        )

        with self.assertRaises(RevisionMemberAmbiguityError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "occupancy_refs",
                "occupancy",
                first["id"],
            )

    def test_work_claim_same_logical_id_different_exact_instances_are_ambiguous(self) -> None:
        first = self._fixture("work-claim.schema.json")
        second = copy.deepcopy(first)
        second["summary"] = "Second exact claim instance sharing the same logical claim id."

        first_result = self.store.store(first, "work-claim.schema.json")
        second_result = self.store.store(second, "work-claim.schema.json")
        self.assertNotEqual(first_result.reference, second_result.reference)

        revision_result = self._store_revision(
            claim_refs=[first_result.reference, second_result.reference]
        )

        with self.assertRaises(RevisionMemberAmbiguityError):
            resolve_exact_revision_member(
                self.store,
                revision_result.reference,
                "claim_refs",
                "work-claim",
                first["id"],
            )

    def test_unreferenced_newer_same_id_object_cannot_override_exact_base_membership(self) -> None:
        base_member = self._fixture("lane.schema.json")
        newer_unreferenced = copy.deepcopy(base_member)
        newer_unreferenced["purpose"] = "Later exact instance deliberately absent from the queried base."

        base_result = self.store.store(base_member, "lane.schema.json")
        newer_result = self.store.store(newer_unreferenced, "lane.schema.json")
        self.assertNotEqual(base_result.reference, newer_result.reference)

        revision_result = self._store_revision(lane_refs=[base_result.reference])
        resolved = resolve_exact_revision_member(
            self.store,
            revision_result.reference,
            "lane_refs",
            "lane",
            base_member["id"],
        )

        self.assertEqual(resolved.reference, base_result.reference)
        self.assertNotEqual(resolved.reference, newer_result.reference)
        self.assertEqual(resolved.value, base_member)

    def test_successful_selected_family_resolution_does_not_imply_global_closure(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_result = self.store.store(lane, "lane.schema.json")

        missing_occupancy = self._fixture("occupancy.schema.json")
        missing_occupancy_ref = make_immutable_ref(
            "occupancy.schema.json", missing_occupancy
        )

        revision_result = self._store_revision(
            lane_refs=[lane_result.reference],
            occupancy_refs=[missing_occupancy_ref],
        )

        resolved = resolve_exact_revision_member(
            self.store,
            revision_result.reference,
            "lane_refs",
            "lane",
            lane["id"],
        )

        self.assertEqual(resolved.reference, lane_result.reference)
        self.assertFalse(revision_result.referenced_members_verified)
        self.assertFalse(hasattr(resolved, "referenced_members_verified"))


if __name__ == "__main__":
    unittest.main()
