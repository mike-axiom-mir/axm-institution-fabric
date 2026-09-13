from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_output_compatibility import (
    EvidenceRequirementAmbiguityError,
    EvidenceRequirementNotFoundError,
    OutputContractAmbiguityError,
    OutputContractNotFoundError,
    PacketLaneContextError,
    RequiredStateSemanticsUnresolvedError,
    preflight_created_output_compatibility,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class CreatedOutputCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self, lane=None):
        lane = copy.deepcopy(lane) if lane is not None else self._fixture("lane.schema.json")
        return lane, self.store.store(lane, "lane.schema.json")

    def _store_base(self, lane_refs, *, revision_id="revision.compatibility.base"):
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["lane_refs"] = list(lane_refs)
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = []
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        return self.store.store(revision, "state-revision.schema.json")

    def _artifact(self, *, artifact_id="artifact.compatibility", artifact_type="kernel_contracts"):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = artifact_id
        artifact["type"] = artifact_type
        artifact["content_ref"] = f"artifact://{artifact_id}"
        artifact["provenance"]["base_state_revision"] = "revision.compatibility.base"
        artifact["evidence_refs"] = []
        return artifact

    def _evidence(self, *, evidence_id, subject_ref, state="automated_tested"):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = "Created-output compatibility regression evidence."
        return evidence

    def _ground_packet(
        self,
        lane=None,
        *,
        evidence_state="automated_tested",
        artifact_type="kernel_contracts",
        unrelated_passing_evidence=False,
    ):
        lane, lane_result = self._store_lane(lane)
        base = self._store_base([lane_result.reference])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.compatibility"
        occupancy["base_state_revision_ref"] = base.reference
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_result = admit_occupancy(self.store, occupancy)

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.compatibility"
        claim["base_state_revision_ref"] = base.reference
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_result.occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_result = open_work_claim(self.store, claim)

        artifact_ref = self.store.store(
            self._artifact(artifact_type=artifact_type), "artifact.schema.json"
        ).reference
        evidence_refs = []
        if unrelated_passing_evidence:
            unrelated_ref = self.store.store(
                self._artifact(
                    artifact_id="artifact.compatibility.unrelated",
                    artifact_type=artifact_type,
                ),
                "artifact.schema.json",
            ).reference
            evidence_refs.append(
                self.store.store(
                    self._evidence(
                        evidence_id="evidence.compatibility.unrelated",
                        subject_ref=unrelated_ref,
                        state="automated_tested",
                    ),
                    "evidence-record.schema.json",
                ).reference
            )
        else:
            evidence_refs.append(
                self.store.store(
                    self._evidence(
                        evidence_id="evidence.compatibility",
                        subject_ref=artifact_ref,
                        state=evidence_state,
                    ),
                    "evidence-record.schema.json",
                ).reference
            )

        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.compatibility"
        packet["base_state_revision_ref"] = base.reference
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_result.claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = evidence_refs
        packet_result = submit_return_packet(self.store, packet)

        return {
            "lane": lane,
            "lane_ref": lane_result.reference,
            "base_ref": base.reference,
            "occupancy_ref": occupancy_result.occupancy_ref,
            "claim_ref": claim_result.claim_ref,
            "artifact_ref": artifact_ref,
            "evidence_refs": tuple(evidence_refs),
            "packet": packet,
            "packet_ref": packet_result.packet_ref,
        }

    def test_single_output_single_required_state_is_satisfied_by_exact_bound_evidence(self) -> None:
        context = self._ground_packet()

        result = preflight_created_output_compatibility(self.store, context["packet_ref"])

        self.assertEqual(result.claim_ref, context["claim_ref"])
        self.assertEqual(result.occupancy_ref, context["occupancy_ref"])
        self.assertEqual(result.lane_ref, context["lane_ref"])
        self.assertEqual(len(result.created_outputs), 1)
        created = result.created_outputs[0]
        self.assertEqual(created.artifact.reference, context["artifact_ref"])
        self.assertEqual(created.output_type, "kernel_contracts")
        self.assertEqual(created.required_state, "automated_tested")
        self.assertTrue(created.satisfied)
        self.assertEqual(
            tuple(item.reference for item in created.satisfying_evidence),
            context["evidence_refs"],
        )

    def test_wrong_bound_state_is_explicitly_unsatisfied_without_state_implication(self) -> None:
        context = self._ground_packet(evidence_state="runtime_tested")

        result = preflight_created_output_compatibility(self.store, context["packet_ref"])

        created = result.created_outputs[0]
        self.assertEqual(created.required_state, "automated_tested")
        self.assertFalse(created.satisfied)
        self.assertEqual(created.satisfying_evidence, ())

    def test_unmatched_passing_evidence_cannot_satisfy_created_output(self) -> None:
        context = self._ground_packet(unrelated_passing_evidence=True)

        result = preflight_created_output_compatibility(self.store, context["packet_ref"])

        self.assertFalse(result.created_outputs[0].satisfied)
        self.assertEqual(result.created_outputs[0].satisfying_evidence, ())
        self.assertEqual(len(result.subject_resolution.unmatched_evidence), 1)

    def test_missing_output_contract_fails_closed(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["outputs"] = []
        context = self._ground_packet(lane)

        with self.assertRaises(OutputContractNotFoundError):
            preflight_created_output_compatibility(self.store, context["packet_ref"])

    def test_duplicate_output_contract_fails_closed_without_array_order_authority(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["outputs"].append(copy.deepcopy(lane["outputs"][0]))
        context = self._ground_packet(lane)

        with self.assertRaises(OutputContractAmbiguityError):
            preflight_created_output_compatibility(self.store, context["packet_ref"])

    def test_missing_evidence_requirement_fails_closed(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["evidence_requirements"] = []
        context = self._ground_packet(lane)

        with self.assertRaises(EvidenceRequirementNotFoundError):
            preflight_created_output_compatibility(self.store, context["packet_ref"])

    def test_duplicate_evidence_requirement_fails_closed_without_array_order_authority(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["evidence_requirements"].append(
            copy.deepcopy(lane["evidence_requirements"][0])
        )
        context = self._ground_packet(lane)

        with self.assertRaises(EvidenceRequirementAmbiguityError):
            preflight_created_output_compatibility(self.store, context["packet_ref"])

    def test_multiple_required_states_fail_closed_without_and_or_or_rank_semantics(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["evidence_requirements"][0]["required_states"] = [
            "implemented",
            "automated_tested",
        ]
        context = self._ground_packet(lane)

        with self.assertRaises(RequiredStateSemanticsUnresolvedError):
            preflight_created_output_compatibility(self.store, context["packet_ref"])

    def test_later_same_logical_lane_cannot_rebind_exact_claim_base_lane(self) -> None:
        context = self._ground_packet()
        later_lane = copy.deepcopy(context["lane"])
        later_lane["purpose"] = "Later same-id lane outside the packet claim base."
        later_ref = self.store.store(later_lane, "lane.schema.json").reference
        self.assertNotEqual(later_ref, context["lane_ref"])

        result = preflight_created_output_compatibility(self.store, context["packet_ref"])

        self.assertEqual(result.lane_ref, context["lane_ref"])
        self.assertNotEqual(result.lane_ref, later_ref)

    def test_direct_stored_packet_lane_mismatch_cannot_launder_another_lane_contract(self) -> None:
        context = self._ground_packet()
        packet = copy.deepcopy(context["packet"])
        packet["id"] = "packet.compatibility.decoy-lane"
        packet["lane_id"] = "lane-decoy"
        packet_ref = self.store.store(packet, "return-packet.schema.json").reference

        with self.assertRaises(PacketLaneContextError):
            preflight_created_output_compatibility(self.store, packet_ref)


if __name__ == "__main__":
    unittest.main()
