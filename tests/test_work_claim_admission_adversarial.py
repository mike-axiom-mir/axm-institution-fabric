from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import make_immutable_ref
from axm_institution.lifecycle import open_work_claim
from axm_institution.resolution import RevisionMemberAmbiguityError
from axm_institution.store import FilesystemObjectStore, ObjectNotFoundError


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class WorkClaimAdmissionAdversarialTests(unittest.TestCase):
    """Continuity regressions for the bounded work-claim admission slice.

    These witnesses distinguish an exact/schema-valid occupancy object from an
    occupancy whose own entry-base lane relationship is grounded. A generic immutable
    object-store write must not silently substitute for the occupancy-admission
    relationship proof when a later lifecycle step treats that occupancy as operational.
    """

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

    def _store_base(self, lane_refs: list[str], *, revision_id: str):
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["lane_refs"] = lane_refs
        return revision, self.store.store(revision, "state-revision.schema.json")

    def _direct_store_active_occupancy(self, base_ref: str, lane_id: str):
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane_id
        occupancy["status"] = "active"
        occupancy["ended_at"] = None
        return occupancy, self.store.store(occupancy, "occupancy.schema.json")

    def _claim_for(self, base_ref: str, lane_id: str, occupancy_ref: str):
        claim = self._fixture("work-claim.schema.json")
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane_id
        claim["occupancy_ref"] = occupancy_ref
        claim["status"] = "open"
        return claim

    def _claim_files(self) -> list[Path]:
        root = self.store.objects_dir / "work-claim"
        return list(root.rglob("*.json")) if root.exists() else []

    def test_adv_033_a_missing_occupancy_entry_base_cannot_open_claim(self) -> None:
        """Exact-load of occupancy must not erase its own ungrounded entry base."""

        lane, lane_result = self._store_lane()
        _, claim_base = self._store_base(
            [lane_result.reference],
            revision_id="revision.claim-base",
        )

        missing_entry_base = self._fixture("state-revision.schema.json")
        missing_entry_base["id"] = "revision.missing-occupancy-entry-base"
        missing_entry_base["lane_refs"] = [lane_result.reference]
        missing_entry_base_ref = make_immutable_ref(
            "state-revision.schema.json",
            missing_entry_base,
        )

        _, occupancy_result = self._direct_store_active_occupancy(
            missing_entry_base_ref,
            lane["id"],
        )
        claim = self._claim_for(
            claim_base.reference,
            lane["id"],
            occupancy_result.reference,
        )

        with self.assertRaises(ObjectNotFoundError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])

    def test_adv_033_b_ambiguous_occupancy_entry_lane_cannot_open_claim(self) -> None:
        """Claim-base grounding cannot replace occupancy entry-base grounding."""

        lane, first_lane_result = self._store_lane(
            purpose="First exact lane instance for occupancy entry ambiguity."
        )
        second_lane = copy.deepcopy(lane)
        second_lane["purpose"] = "Second exact lane instance with the same logical id."
        second_lane_result = self.store.store(second_lane, "lane.schema.json")
        self.assertNotEqual(first_lane_result.reference, second_lane_result.reference)

        _, occupancy_base = self._store_base(
            [first_lane_result.reference, second_lane_result.reference],
            revision_id="revision.ambiguous-occupancy-entry-base",
        )
        _, occupancy_result = self._direct_store_active_occupancy(
            occupancy_base.reference,
            lane["id"],
        )

        claim_lane = copy.deepcopy(lane)
        claim_lane["purpose"] = "Single exact claim-base lane instance."
        claim_lane_result = self.store.store(claim_lane, "lane.schema.json")
        _, claim_base = self._store_base(
            [claim_lane_result.reference],
            revision_id="revision.clean-claim-base",
        )
        claim = self._claim_for(
            claim_base.reference,
            lane["id"],
            occupancy_result.reference,
        )

        with self.assertRaises(RevisionMemberAmbiguityError):
            open_work_claim(self.store, claim)

        self.assertEqual(self._claim_files(), [])


if __name__ == "__main__":
    unittest.main()
