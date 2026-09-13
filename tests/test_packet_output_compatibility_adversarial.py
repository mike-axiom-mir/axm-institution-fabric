from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_output_compatibility import preflight_created_output_compatibility
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class CreatedOutputCompatibilityAdversarialTests(unittest.TestCase):
    """ADV-042 continuity probes for the bounded Stage 4 compatibility preflight."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_base(self, lane_refs, *, revision_id: str):
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

    def _artifact(
        self,
        *,
        artifact_id: str,
        artifact_type: str = "kernel_contracts",
        content_suffix: str = "v1",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = artifact_id
        artifact["type"] = artifact_type
        artifact["content_ref"] = f"artifact://{artifact_id}/{content_suffix}"
        artifact["provenance"]["base_state_revision"] = "revision.compatibility.base"
        artifact["evidence_refs"] = []
        return artifact

    def _evidence(self, *, evidence_id: str, subject_ref: str, state: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = "ADV-042 created-output compatibility evidence."
        if state in {
            "compiled",
            "automated_tested",
            "runtime_tested",
            "visually_inspected",
            "playtested",
            "measured",
        }:
            evidence["method"] = "deterministic ADV-042 fixture"
            evidence["source_refs"] = [f"fixture://{evidence_id}"]
        return evidence

    def _admit_occupancy(self, *, base_ref: str, lane_id: str, occupancy_id: str):
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = occupancy_id
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane_id
        occupancy["claim_ids"] = []
        return admit_occupancy(self.store, occupancy)

    def _open_claim(
        self,
        *,
        base_ref: str,
        lane_id: str,
        occupancy_ref: str,
        claim_id: str,
    ):
        claim = self._fixture("work-claim.schema.json")
        claim["id"] = claim_id
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane_id
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        return open_work_claim(self.store, claim)

    def _submit_packet(
        self,
        *,
        base_ref: str,
        lane_id: str,
        claim_ref: str,
        artifact_refs: list[str],
        evidence_refs: list[str],
        packet_id: str,
    ):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane_id
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = list(artifact_refs)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence_refs)
        return submit_return_packet(self.store, packet)

    def _single_lane_claim_context(self, *, prefix: str):
        lane = self._fixture("lane.schema.json")
        lane["purpose"] = f"ADV-042 lane {prefix}."
        lane_result = self.store.store(lane, "lane.schema.json")
        base = self._store_base(
            [lane_result.reference],
            revision_id=f"revision.adv042.{prefix}",
        )
        occupancy = self._admit_occupancy(
            base_ref=base.reference,
            lane_id=lane["id"],
            occupancy_id=f"occupancy.adv042.{prefix}",
        )
        claim = self._open_claim(
            base_ref=base.reference,
            lane_id=lane["id"],
            occupancy_ref=occupancy.occupancy_ref,
            claim_id=f"claim.adv042.{prefix}",
        )
        return lane, lane_result, base, occupancy, claim

    def test_adv042_a_claim_base_contract_wins_over_occupancy_entry_contract(self) -> None:
        entry_lane = self._fixture("lane.schema.json")
        entry_lane["purpose"] = "ADV-042 occupancy-entry version of the lane contract."
        entry_lane["evidence_requirements"][0]["required_states"] = ["implemented"]
        entry_lane_result = self.store.store(entry_lane, "lane.schema.json")
        entry_base = self._store_base(
            [entry_lane_result.reference],
            revision_id="revision.adv042.entry",
        )
        occupancy = self._admit_occupancy(
            base_ref=entry_base.reference,
            lane_id=entry_lane["id"],
            occupancy_id="occupancy.adv042.contract-history",
        )

        claim_lane = self._fixture("lane.schema.json")
        claim_lane["purpose"] = "ADV-042 later claim-base version of the lane contract."
        claim_lane["evidence_requirements"][0]["required_states"] = ["automated_tested"]
        claim_lane_result = self.store.store(claim_lane, "lane.schema.json")
        claim_base = self._store_base(
            [claim_lane_result.reference],
            revision_id="revision.adv042.claim",
        )
        claim = self._open_claim(
            base_ref=claim_base.reference,
            lane_id=claim_lane["id"],
            occupancy_ref=occupancy.occupancy_ref,
            claim_id="claim.adv042.contract-history",
        )

        artifact_ref = self.store.store(
            self._artifact(artifact_id="artifact.adv042.contract-history"),
            "artifact.schema.json",
        ).reference
        evidence_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.contract-history",
                subject_ref=artifact_ref,
                state="automated_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        packet = self._submit_packet(
            base_ref=claim_base.reference,
            lane_id=claim_lane["id"],
            claim_ref=claim.claim_ref,
            artifact_refs=[artifact_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.adv042.contract-history",
        )

        result = preflight_created_output_compatibility(self.store, packet.packet_ref)

        self.assertEqual(result.lane_ref, claim_lane_result.reference)
        self.assertNotEqual(result.lane_ref, entry_lane_result.reference)
        self.assertEqual(result.created_outputs[0].required_state, "automated_tested")
        self.assertTrue(result.created_outputs[0].satisfied)

    def test_adv042_b_same_logical_artifact_decoy_cannot_satisfy_exact_packet_artifact(self) -> None:
        lane, _, base, _, claim = self._single_lane_claim_context(prefix="artifact-decoy")

        authoritative = self._artifact(
            artifact_id="artifact.adv042.same-logical",
            content_suffix="authoritative",
        )
        authoritative_ref = self.store.store(
            authoritative, "artifact.schema.json"
        ).reference
        decoy = copy.deepcopy(authoritative)
        decoy["content_ref"] = "artifact://artifact.adv042.same-logical/later-decoy"
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(authoritative_ref, decoy_ref)

        evidence_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.same-logical-decoy",
                subject_ref=decoy_ref,
                state="automated_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        packet = self._submit_packet(
            base_ref=base.reference,
            lane_id=lane["id"],
            claim_ref=claim.claim_ref,
            artifact_refs=[authoritative_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.adv042.same-logical-decoy",
        )

        result = preflight_created_output_compatibility(self.store, packet.packet_ref)

        created = result.created_outputs[0]
        self.assertEqual(created.artifact.reference, authoritative_ref)
        self.assertFalse(created.satisfied)
        self.assertEqual(created.satisfying_evidence, ())
        self.assertEqual(len(result.subject_resolution.unmatched_evidence), 1)
        self.assertEqual(
            result.subject_resolution.unmatched_evidence[0].subject_ref,
            decoy_ref,
        )

    def test_adv042_c_same_type_artifacts_cannot_cross_launder_exact_evidence(self) -> None:
        lane, _, base, _, claim = self._single_lane_claim_context(prefix="cross-artifact")

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.adv042.a"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.adv042.b"),
            "artifact.schema.json",
        ).reference
        evidence_a_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.a",
                subject_ref=artifact_a_ref,
                state="automated_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.b",
                subject_ref=artifact_b_ref,
                state="runtime_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        packet = self._submit_packet(
            base_ref=base.reference,
            lane_id=lane["id"],
            claim_ref=claim.claim_ref,
            artifact_refs=[artifact_a_ref, artifact_b_ref],
            evidence_refs=[evidence_a_ref, evidence_b_ref],
            packet_id="packet.adv042.cross-artifact",
        )

        result = preflight_created_output_compatibility(self.store, packet.packet_ref)
        by_artifact = {item.artifact.reference: item for item in result.created_outputs}

        self.assertTrue(by_artifact[artifact_a_ref].satisfied)
        self.assertEqual(
            tuple(item.reference for item in by_artifact[artifact_a_ref].satisfying_evidence),
            (evidence_a_ref,),
        )
        self.assertFalse(by_artifact[artifact_b_ref].satisfied)
        self.assertEqual(by_artifact[artifact_b_ref].satisfying_evidence, ())

    def test_adv042_d_conflicting_subject_bound_evidence_remains_explicit(self) -> None:
        lane, _, base, _, claim = self._single_lane_claim_context(prefix="conflict-preservation")

        artifact_ref = self.store.store(
            self._artifact(artifact_id="artifact.adv042.conflict"),
            "artifact.schema.json",
        ).reference
        passing_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.conflict.pass",
                subject_ref=artifact_ref,
                state="automated_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        invalidated_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.adv042.conflict.invalidated",
                subject_ref=artifact_ref,
                state="invalidated",
            ),
            "evidence-record.schema.json",
        ).reference
        packet = self._submit_packet(
            base_ref=base.reference,
            lane_id=lane["id"],
            claim_ref=claim.claim_ref,
            artifact_refs=[artifact_ref],
            evidence_refs=[passing_ref, invalidated_ref],
            packet_id="packet.adv042.conflict",
        )

        result = preflight_created_output_compatibility(self.store, packet.packet_ref)

        created = result.created_outputs[0]
        self.assertTrue(created.satisfied)
        self.assertEqual(
            tuple(item.reference for item in created.satisfying_evidence),
            (passing_ref,),
        )
        bound = result.subject_resolution.created_artifact_bindings[0].evidence_records
        self.assertEqual(
            {item.reference for item in bound},
            {passing_ref, invalidated_ref},
        )
        self.assertEqual(
            {item.value.get("state") for item in bound},
            {"automated_tested", "invalidated"},
        )


if __name__ == "__main__":
    unittest.main()
