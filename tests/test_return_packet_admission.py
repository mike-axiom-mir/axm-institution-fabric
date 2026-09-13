from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError, make_immutable_ref
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.resolution import RevisionMemberAmbiguityError
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
)


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class FinalWritePacketMutationStore(FilesystemObjectStore):
    """Mutate only caller-owned packet state at the final packet write boundary."""

    def __init__(self, root: Path | str) -> None:
        super().__init__(root)
        self.caller_packet = None
        self.mutation = None

    def store(self, value, schema_name, *, expected_reference=None):
        if (
            schema_name == "return-packet.schema.json"
            and self.caller_packet is not None
            and self.mutation is not None
        ):
            self.mutation(self.caller_packet)
        return super().store(
            value,
            schema_name,
            expected_reference=expected_reference,
        )


class ReturnPacketAdmissionTests(unittest.TestCase):
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
        lane, lane_result = self._store_lane()
        occupancy_base = self._store_base(
            [lane_result.reference], revision_id="revision.packet.occupancy-base"
        )
        occupancy = self._occupancy_for(occupancy_base.reference, lane["id"])
        occupancy_result = admit_occupancy(self.store, occupancy)
        claim_base = self._store_base(
            [lane_result.reference], revision_id="revision.packet.claim-base"
        )
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.occupancy_ref
        )
        claim_result = open_work_claim(self.store, claim)
        return lane, lane_result, occupancy, occupancy_result, claim, claim_result, claim_base

    def test_submit_packet_persists_exact_candidate_and_returns_grounded_identities(self) -> None:
        lane, lane_result, _, occupancy_result, _, claim_result, claim_base = (
            self._ground_open_claim()
        )
        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )

        result = submit_return_packet(self.store, packet)

        self.assertTrue(result.created)
        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertEqual(
            result.packet_ref,
            make_immutable_ref("return-packet.schema.json", packet),
        )
        self.assertEqual(
            self.store.load(result.packet_ref, "return-packet.schema.json"), packet
        )

    def test_re_admitting_same_exact_packet_is_idempotent(self) -> None:
        lane, _, _, _, _, claim_result, claim_base = self._ground_open_claim()
        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )

        first = submit_return_packet(self.store, packet)
        second = submit_return_packet(self.store, packet)

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first, second.__class__(
            packet_ref=second.packet_ref,
            claim_ref=second.claim_ref,
            occupancy_ref=second.occupancy_ref,
            lane_ref=second.lane_ref,
            created=True,
        ))

    def test_missing_corrupt_and_wrong_kind_claim_refs_fail_before_packet_publication(self) -> None:
        lane, lane_result = self._store_lane()
        base = self._store_base([lane_result.reference], revision_id="revision.packet.claim-errors")
        occupancy = self._occupancy_for(base.reference, lane["id"])
        occupancy_result = admit_occupancy(self.store, occupancy)
        claim = self._claim_for(base.reference, lane["id"], occupancy_result.occupancy_ref)

        missing_claim_ref = make_immutable_ref("work-claim.schema.json", claim)
        missing_packet = self._packet_for(base.reference, lane["id"], missing_claim_ref)
        with self.assertRaises(ObjectNotFoundError):
            submit_return_packet(self.store, missing_packet)
        self.assertEqual(self._packet_files(), [])

        claim_result = open_work_claim(self.store, claim)
        self.store._object_path(claim_result.claim_ref).write_bytes(b"{}")
        corrupt_packet = self._packet_for(base.reference, lane["id"], claim_result.claim_ref)
        with self.assertRaises(ObjectCorruptionError):
            submit_return_packet(self.store, corrupt_packet)
        self.assertEqual(self._packet_files(), [])

        wrong_kind_packet = self._packet_for(base.reference, lane["id"], lane_result.reference)
        with self.assertRaises(ContractValidationError):
            submit_return_packet(self.store, wrong_kind_packet)
        self.assertEqual(self._packet_files(), [])

    def test_packet_base_must_equal_exact_claim_base_without_silent_rebase(self) -> None:
        lane, lane_result, _, occupancy_result, _, claim_result, claim_base = (
            self._ground_open_claim()
        )
        later_base = self._store_base(
            [lane_result.reference], revision_id="revision.packet.later-base"
        )
        self.assertNotEqual(claim_base.reference, later_base.reference)
        packet = self._packet_for(later_base.reference, lane["id"], claim_result.claim_ref)

        with self.assertRaises(ContractValidationError):
            submit_return_packet(self.store, packet)

        self.assertEqual(self._packet_files(), [])
        self.assertEqual(result_ref := occupancy_result.occupancy_ref, result_ref)

    def test_packet_lane_must_equal_exact_claim_lane(self) -> None:
        lane, _, _, _, _, claim_result, claim_base = self._ground_open_claim()
        packet = self._packet_for(
            claim_base.reference, "lane-decoy", claim_result.claim_ref
        )

        with self.assertRaises(ContractValidationError):
            submit_return_packet(self.store, packet)

        self.assertEqual(self._packet_files(), [])
        self.assertEqual(lane["id"], "lane-02")

    def test_direct_stored_claim_with_ambiguous_historical_lane_cannot_be_laundered(self) -> None:
        lane, first_lane = self._store_lane()
        _, second_lane = self._store_lane(
            purpose="Second exact instance sharing the same persistent logical lane id."
        )
        claim_base = self._store_base(
            [first_lane.reference, second_lane.reference],
            revision_id="revision.packet.ambiguous-claim-base",
        )
        occupancy_base = self._store_base(
            [first_lane.reference], revision_id="revision.packet.occupancy-clean"
        )
        occupancy = self._occupancy_for(occupancy_base.reference, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.reference
        )
        claim_result = self.store.store(claim, "work-claim.schema.json")
        packet = self._packet_for(claim_base.reference, lane["id"], claim_result.reference)

        with self.assertRaises(RevisionMemberAmbiguityError):
            submit_return_packet(self.store, packet)

        self.assertEqual(self._packet_files(), [])

    def test_exact_claim_occupancy_relation_regrounds_occupancy_entry_base(self) -> None:
        lane, lane_result = self._store_lane()
        missing_entry_revision = self._fixture("state-revision.schema.json")
        missing_entry_revision["id"] = "revision.packet.missing-entry-base"
        missing_entry_revision["lane_refs"] = [lane_result.reference]
        missing_entry_ref = make_immutable_ref(
            "state-revision.schema.json", missing_entry_revision
        )
        occupancy = self._occupancy_for(missing_entry_ref, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")
        claim_base = self._store_base(
            [lane_result.reference], revision_id="revision.packet.valid-claim-base"
        )
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.reference
        )
        claim_result = self.store.store(claim, "work-claim.schema.json")
        packet = self._packet_for(claim_base.reference, lane["id"], claim_result.reference)

        with self.assertRaises(ObjectNotFoundError):
            submit_return_packet(self.store, packet)

        self.assertEqual(self._packet_files(), [])

    def test_later_same_id_claim_occupancy_and_lane_cannot_rebind_exact_relationships(self) -> None:
        lane, entry_lane_result = self._store_lane()
        occupancy_base = self._store_base(
            [entry_lane_result.reference], revision_id="revision.packet.entry"
        )
        occupancy = self._occupancy_for(occupancy_base.reference, lane["id"])
        occupancy["claim_ids"] = ["claim.snapshot.hint"]
        occupancy_result = admit_occupancy(self.store, occupancy)

        claim_lane = copy.deepcopy(lane)
        claim_lane["purpose"] = "Exact later lane instance selected by claim base."
        claim_lane_result = self.store.store(claim_lane, "lane.schema.json")
        decoy_lane, decoy_lane_result = self._store_lane(lane_id="lane-decoy")
        claim_base = self._store_base(
            [decoy_lane_result.reference, claim_lane_result.reference],
            revision_id="revision.packet.claim-exact",
        )
        claim = self._claim_for(
            claim_base.reference, lane["id"], occupancy_result.occupancy_ref
        )
        claim["overlap_with_claim_ids"] = ["claim.report-only"]
        claim_result = open_work_claim(self.store, claim)

        newer_lane = copy.deepcopy(lane)
        newer_lane["purpose"] = "Newer same-id lane outside exact historical bases."
        newer_lane_result = self.store.store(newer_lane, "lane.schema.json")
        later_occupancy = copy.deepcopy(occupancy)
        later_occupancy["actor_ref"] = "fixture:later-occupant"
        later_occupancy_result = self.store.store(later_occupancy, "occupancy.schema.json")
        later_claim = copy.deepcopy(claim)
        later_claim["summary"] = "Later same-id claim decoy."
        later_claim_result = self.store.store(later_claim, "work-claim.schema.json")

        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        result = submit_return_packet(self.store, packet)

        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertNotEqual(result.claim_ref, later_claim_result.reference)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertNotEqual(result.occupancy_ref, later_occupancy_result.reference)
        self.assertEqual(result.lane_ref, claim_lane_result.reference)
        self.assertNotEqual(result.lane_ref, entry_lane_result.reference)
        self.assertNotEqual(result.lane_ref, newer_lane_result.reference)
        self.assertNotEqual(result.lane_ref, decoy_lane_result.reference)
        self.assertEqual(decoy_lane["id"], "lane-decoy")
        self.assertEqual(
            self.store.load(result.claim_ref, "work-claim.schema.json")[
                "overlap_with_claim_ids"
            ],
            ["claim.report-only"],
        )
        self.assertEqual(
            self.store.load(result.occupancy_ref, "occupancy.schema.json")["claim_ids"],
            ["claim.snapshot.hint"],
        )

    def test_local_claim_and_occupancy_status_prerequisites_fail_closed(self) -> None:
        lane, lane_result = self._store_lane()
        base = self._store_base([lane_result.reference], revision_id="revision.packet.status")
        occupancy = self._occupancy_for(base.reference, lane["id"])
        occupancy_result = self.store.store(occupancy, "occupancy.schema.json")

        submitted_claim = self._claim_for(base.reference, lane["id"], occupancy_result.reference)
        submitted_claim["status"] = "submitted"
        submitted_claim_result = self.store.store(
            submitted_claim, "work-claim.schema.json"
        )
        packet = self._packet_for(
            base.reference, lane["id"], submitted_claim_result.reference
        )
        with self.assertRaises(ContractValidationError):
            submit_return_packet(self.store, packet)

        ended_occupancy = copy.deepcopy(occupancy)
        ended_occupancy["status"] = "ended"
        ended_occupancy["ended_at"] = "2026-09-13T08:30:00Z"
        ended_occupancy_result = self.store.store(
            ended_occupancy, "occupancy.schema.json"
        )
        open_claim = self._claim_for(
            base.reference, lane["id"], ended_occupancy_result.reference
        )
        open_claim_result = self.store.store(open_claim, "work-claim.schema.json")
        ended_packet = self._packet_for(
            base.reference, lane["id"], open_claim_result.reference
        )
        with self.assertRaises(ContractValidationError):
            submit_return_packet(self.store, ended_packet)

        self.assertEqual(self._packet_files(), [])

    def test_packet_handoff_fields_survive_exact_persistence_without_extra_authority(self) -> None:
        lane, _, _, _, _, claim_result, claim_base = self._ground_open_claim()
        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        packet["changes"] = ["change one", "change two"]
        packet["artifacts_created"] = ["artifact.created.one", "artifact.created.two"]
        packet["artifacts_modified"] = ["artifact.modified.one"]
        packet["evidence_refs"] = ["evidence.one", "evidence.two"]
        packet["uncertainties"] = ["uncertainty one", "uncertainty two"]
        packet["failures_or_blockers"] = ["blocker one"]
        packet["downstream_effects"] = ["downstream one", "downstream two"]
        packet["requested_followup"] = ["follow up one", "follow up two"]

        result = submit_return_packet(self.store, packet)
        reloaded = self.store.load(result.packet_ref, "return-packet.schema.json")

        for field in (
            "changes",
            "artifacts_created",
            "artifacts_modified",
            "evidence_refs",
            "uncertainties",
            "failures_or_blockers",
            "downstream_effects",
            "requested_followup",
        ):
            self.assertEqual(reloaded[field], packet[field])

    def test_caller_mutation_at_final_write_cannot_change_grounded_packet(self) -> None:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        store = FinalWritePacketMutationStore(Path(tempdir.name))
        self.store = store
        lane, lane_result, _, occupancy_result, _, claim_result, claim_base = (
            self._ground_open_claim()
        )
        packet = self._packet_for(
            claim_base.reference, lane["id"], claim_result.claim_ref
        )
        expected = copy.deepcopy(packet)
        store.caller_packet = packet
        store.mutation = lambda caller: caller.update(
            {
                "lane_id": "lane-decoy",
                "changes": ["caller mutation after grounding"],
            }
        )

        result = submit_return_packet(store, packet)
        persisted = store.load(result.packet_ref, "return-packet.schema.json")

        self.assertEqual(persisted, expected)
        self.assertEqual(result.claim_ref, claim_result.claim_ref)
        self.assertEqual(result.occupancy_ref, occupancy_result.occupancy_ref)
        self.assertEqual(result.lane_ref, lane_result.reference)
        self.assertEqual(packet["lane_id"], "lane-decoy")
        self.assertNotEqual(packet, persisted)


if __name__ == "__main__":
    unittest.main()
