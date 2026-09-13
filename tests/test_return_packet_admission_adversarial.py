from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.resolution import RevisionMemberAmbiguityError
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class FinalWriteNestedMutationStore(FilesystemObjectStore):
    """Mutate nested caller packet state only at the final packet publication boundary."""

    def __init__(self, root: Path | str) -> None:
        super().__init__(root)
        self.caller_packet = None

    def store(self, value, schema_name, *, expected_reference=None):
        if schema_name == "return-packet.schema.json" and self.caller_packet is not None:
            self.caller_packet["uncertainties"].append("late caller-only uncertainty")
            self.caller_packet["evidence_refs"].clear()
        return super().store(
            value,
            schema_name,
            expected_reference=expected_reference,
        )


class ReturnPacketAdmissionAdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self, *, lane_id: str = "lane-02", purpose: str | None = None):
        lane = self._fixture("lane.schema.json")
        lane["id"] = lane_id
        if purpose is not None:
            lane["purpose"] = purpose
        return lane, self.store.store(lane, "lane.schema.json")

    def _store_base(self, lane_refs: list[str], *, revision_id: str):
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["lane_refs"] = lane_refs
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["return_packet_refs"] = []
        return self.store.store(revision, "state-revision.schema.json")

    def _occupancy_for(self, base_ref: str, lane_id: str):
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane_id
        occupancy["claim_ids"] = []
        return occupancy

    def _claim_for(self, base_ref: str, lane_id: str, occupancy_ref: str):
        claim = self._fixture("work-claim.schema.json")
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane_id
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        return claim

    def _packet_for(self, base_ref: str, lane_id: str, claim_ref: str):
        packet = self._fixture("return-packet.schema.json")
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane_id
        packet["claim_ref"] = claim_ref
        return packet

    def _packet_files(self) -> list[Path]:
        root = self.store.objects_dir / "return-packet"
        return list(root.rglob("*.json")) if root.exists() else []

    def _ground_open_claim(self):
        lane, entry_lane_result = self._store_lane(
            purpose="Occupancy entry lane instance."
        )
        occupancy_base = self._store_base(
            [entry_lane_result.reference], revision_id="revision.adv034.occupancy-base"
        )
        occupancy = self._occupancy_for(occupancy_base.reference, lane["id"])
        occupancy_result = admit_occupancy(self.store, occupancy)

        claim_lane = copy.deepcopy(lane)
        claim_lane["purpose"] = "Claim-base exact lane instance."
        claim_lane_result = self.store.store(claim_lane, "lane.schema.json")
        claim_base = self._store_base(
            [claim_lane_result.reference], revision_id="revision.adv034.claim-base"
        )
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.occupancy_ref
        )
        claim_result = open_work_claim(self.store, claim)
        return (
            lane,
            entry_lane_result,
            claim_lane_result,
            occupancy,
            occupancy_result,
            claim,
            claim_result,
            claim_base,
        )

    def test_adv034_a_same_logical_revision_id_decoy_cannot_rebase_packet(self) -> None:
        (
            lane,
            _,
            claim_lane_result,
            _,
            occupancy_result,
            _,
            claim_result,
            claim_base,
        ) = self._ground_open_claim()

        later_same_id_lane = copy.deepcopy(lane)
        later_same_id_lane["purpose"] = "Later same-logical-id lane outside the exact claim base."
        later_same_id_lane_result = self.store.store(
            later_same_id_lane, "lane.schema.json"
        )
        decoy_base = self._store_base(
            [later_same_id_lane_result.reference],
            revision_id="revision.adv034.claim-base",
        )
        self.assertNotEqual(decoy_base.reference, claim_base.reference)

        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        result = submit_return_packet(self.store, packet)

        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(result.lane_ref, claim_lane_result.reference)
        self.assertNotEqual(result.lane_ref, later_same_id_lane_result.reference)
        self.assertEqual(
            self.store.load(result.packet_ref, "return-packet.schema.json")[
                "base_state_revision_ref"
            ],
            claim_base.reference,
        )

    def test_adv034_b_ambiguous_occupancy_entry_lane_cannot_be_laundered_by_packet(self) -> None:
        lane, first_lane = self._store_lane(
            purpose="First exact occupancy-entry lane instance."
        )
        _, second_lane = self._store_lane(
            purpose="Second exact occupancy-entry lane instance sharing one logical id."
        )
        occupancy_base = self._store_base(
            [first_lane.reference, second_lane.reference],
            revision_id="revision.adv034.ambiguous-occupancy-base",
        )
        occupancy = self._occupancy_for(occupancy_base.reference, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")

        claim_base = self._store_base(
            [first_lane.reference], revision_id="revision.adv034.clean-claim-base"
        )
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.reference
        )
        claim_result = self.store.store(claim, "work-claim.schema.json")
        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.reference
        )

        with self.assertRaises(RevisionMemberAmbiguityError):
            submit_return_packet(self.store, packet)

        self.assertEqual(self._packet_files(), [])

    def test_adv034_c_later_same_id_closed_snapshots_do_not_gain_recency_authority(self) -> None:
        (
            lane,
            _,
            claim_lane_result,
            occupancy,
            occupancy_result,
            claim,
            claim_result,
            claim_base,
        ) = self._ground_open_claim()

        ended_occupancy = copy.deepcopy(occupancy)
        ended_occupancy["status"] = "ended"
        ended_occupancy["ended_at"] = "2026-09-13T09:00:00Z"
        ended_occupancy_result = self.store.store(
            ended_occupancy, "occupancy.schema.json"
        )

        submitted_claim = copy.deepcopy(claim)
        submitted_claim["status"] = "submitted"
        submitted_claim["occupancy_ref"] = ended_occupancy_result.reference
        submitted_claim_result = self.store.store(
            submitted_claim, "work-claim.schema.json"
        )

        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        result = submit_return_packet(self.store, packet)

        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertNotEqual(result.claim_ref, submitted_claim_result.reference)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertNotEqual(result.occupancy_ref, ended_occupancy_result.reference)
        self.assertEqual(result.lane_ref, claim_lane_result.reference)

    def test_adv034_d_nested_final_write_mutation_cannot_change_grounded_packet(self) -> None:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        store = FinalWriteNestedMutationStore(Path(tempdir.name))
        self.store = store
        (
            lane,
            _,
            claim_lane_result,
            _,
            occupancy_result,
            _,
            claim_result,
            claim_base,
        ) = self._ground_open_claim()

        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        packet["uncertainties"] = ["grounded uncertainty"]
        packet["evidence_refs"] = ["evidence.opaque.one", "evidence.opaque.two"]
        expected = copy.deepcopy(packet)
        store.caller_packet = packet

        result = submit_return_packet(store, packet)
        persisted = store.load(result.packet_ref, "return-packet.schema.json")

        self.assertEqual(persisted, expected)
        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(result.lane_ref, claim_lane_result.reference)
        self.assertEqual(packet["uncertainties"][-1], "late caller-only uncertainty")
        self.assertEqual(packet["evidence_refs"], [])
        self.assertNotEqual(packet, persisted)


if __name__ == "__main__":
    unittest.main()
