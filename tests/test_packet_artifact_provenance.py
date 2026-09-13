from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_artifact_provenance import (
    ArtifactProducerLaneMismatchError,
    ArtifactProvenanceBaseMismatchError,
    ArtifactProvenanceReferenceError,
    ArtifactProvenanceSchemaVersionError,
    preflight_created_artifact_provenance,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class CreatedArtifactProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self):
        lane = self._fixture("lane.schema.json")
        result = self.store.store(lane, "lane.schema.json")
        return lane, result.reference

    def _store_base(
        self,
        lane_ref: str,
        *,
        revision_id: str = "revision.provenance.base",
        uncertainty: str = "Decision 010 provenance base fixture.",
    ) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = []
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [uncertainty]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _artifact_v02(
        self,
        *,
        base_ref: str,
        producer_lane_id: str = "lane-02",
        artifact_id: str = "artifact.provenance",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.2"
        artifact["id"] = artifact_id
        artifact["version"] = "0.2"
        artifact["type"] = "kernel_contracts"
        artifact["content_ref"] = f"artifact://{artifact_id}"
        artifact["provenance"] = {
            "producer_lane_id": producer_lane_id,
            "base_state_revision_ref": base_ref,
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        return artifact

    def _artifact_v01(self, *, base_value: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = "artifact.provenance.historical"
        artifact["type"] = "kernel_contracts"
        artifact["content_ref"] = "artifact://artifact.provenance.historical"
        artifact["provenance"]["producer_lane_id"] = "lane-02"
        artifact["provenance"]["base_state_revision"] = base_value
        artifact["provenance"].pop("base_state_revision_ref", None)
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        return artifact

    def _ground_packet(self, *, artifact) -> dict[str, str]:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.provenance"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.provenance"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference

        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.provenance"
        evidence["subject_ref"] = artifact_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 010 created-artifact provenance fixture."
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference

        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.provenance"
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = [evidence_ref]
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        return {
            "lane_ref": lane_ref,
            "base_ref": base_ref,
            "claim_ref": claim_ref,
            "artifact_ref": artifact_ref,
            "packet_ref": packet_ref,
        }

    def _ground_v02_packet(self, **artifact_overrides) -> dict[str, str]:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.provenance"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.provenance"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        artifact_base_ref = artifact_overrides.pop("base_ref", base_ref)
        artifact = self._artifact_v02(base_ref=artifact_base_ref, **artifact_overrides)
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference

        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.provenance"
        evidence["subject_ref"] = artifact_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 010 created-artifact provenance fixture."
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference

        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.provenance"
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = [evidence_ref]
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        return {
            "lane_ref": lane_ref,
            "base_ref": base_ref,
            "claim_ref": claim_ref,
            "artifact_ref": artifact_ref,
            "packet_ref": packet_ref,
        }

    def test_v02_exact_provenance_base_and_producer_lane_match_claim_context(self) -> None:
        context = self._ground_v02_packet()

        result = preflight_created_artifact_provenance(self.store, context["packet_ref"])

        self.assertEqual(result.claim_ref, context["claim_ref"])
        self.assertEqual(result.claim_base_ref, context["base_ref"])
        self.assertEqual(result.lane_ref, context["lane_ref"])
        self.assertEqual(len(result.created_artifacts), 1)
        created = result.created_artifacts[0]
        self.assertEqual(created.artifact.reference, context["artifact_ref"])
        self.assertEqual(created.provenance_base_ref, context["base_ref"])
        self.assertEqual(created.producer_lane_id, "lane-02")
        self.assertTrue(result.compatibility.created_outputs[0].satisfied)

    def test_historical_v01_artifact_is_not_silently_reinterpreted_as_exact(self) -> None:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref)
        artifact = self._artifact_v01(base_value=base_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.provenance"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref
        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.provenance"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.provenance"
        evidence["subject_ref"] = artifact_ref
        evidence["state"] = "automated_tested"
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.provenance"
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = [evidence_ref]
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        with self.assertRaises(ArtifactProvenanceSchemaVersionError):
            preflight_created_artifact_provenance(self.store, packet_ref)

    def test_same_logical_revision_id_different_exact_ref_cannot_substitute_claim_base(self) -> None:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref, uncertainty="authoritative base")
        decoy_ref = self._store_base(lane_ref, uncertainty="same-id exact decoy")
        self.assertNotEqual(base_ref, decoy_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.provenance"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref
        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.provenance"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref
        artifact = self._artifact_v02(base_ref=decoy_ref)
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.provenance"
        evidence["subject_ref"] = artifact_ref
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.provenance"
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = [evidence_ref]
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        with self.assertRaises(ArtifactProvenanceBaseMismatchError):
            preflight_created_artifact_provenance(self.store, packet_ref)

    def test_exact_but_different_revision_id_cannot_replace_claim_base(self) -> None:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref)
        other_ref = self._store_base(lane_ref, revision_id="revision.provenance.other")
        context = self._ground_packet(artifact=self._artifact_v02(base_ref=other_ref))

        with self.assertRaises(ArtifactProvenanceBaseMismatchError):
            preflight_created_artifact_provenance(self.store, context["packet_ref"])

    def test_producer_lane_mismatch_fails_closed(self) -> None:
        context = self._ground_v02_packet(producer_lane_id="lane-decoy")

        with self.assertRaises(ArtifactProducerLaneMismatchError):
            preflight_created_artifact_provenance(self.store, context["packet_ref"])

    def test_missing_exact_provenance_target_fails_closed(self) -> None:
        missing_ref = (
            "axmref:v1:state-revision:revision.provenance.missing:-:sha256:"
            + "a" * 64
        )
        context = self._ground_v02_packet(base_ref=missing_ref)

        with self.assertRaises(ArtifactProvenanceReferenceError):
            preflight_created_artifact_provenance(self.store, context["packet_ref"])

    def test_wrong_kind_provenance_ref_is_rejected_by_v02_contract(self) -> None:
        artifact = self._artifact_v02(
            base_ref=("axmref:v1:lane:lane-02:-:sha256:" + "b" * 64)
        )

        with self.assertRaises(ContractValidationError):
            self.store.store(artifact, "artifact.schema.json")

    def test_v02_rejects_legacy_base_field_instead_of_accepting_dual_authority(self) -> None:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref)
        artifact = self._artifact_v02(base_ref=base_ref)
        artifact["provenance"]["base_state_revision"] = "revision.provenance.base"

        with self.assertRaises(ContractValidationError):
            self.store.store(artifact, "artifact.schema.json")

    def test_later_same_logical_revision_decoy_does_not_rebind_correct_exact_provenance(self) -> None:
        context = self._ground_v02_packet()
        base = self.store.load(context["base_ref"], "state-revision.schema.json")
        decoy = copy.deepcopy(base)
        decoy["uncertainties"] = ["later same-logical-id decoy"]
        decoy_ref = self.store.store(decoy, "state-revision.schema.json").reference
        self.assertNotEqual(decoy_ref, context["base_ref"])

        result = preflight_created_artifact_provenance(self.store, context["packet_ref"])

        self.assertEqual(result.claim_base_ref, context["base_ref"])
        self.assertEqual(result.created_artifacts[0].provenance_base_ref, context["base_ref"])
        self.assertNotEqual(result.claim_base_ref, decoy_ref)


if __name__ == "__main__":
    unittest.main()
