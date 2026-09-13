from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import make_immutable_ref, parse_immutable_ref
from axm_institution.packet_output_identity import (
    ModifiedArtifactIdentityUnresolvedError,
    ReturnPacketOutputIdentityError,
    ReturnPacketRelationKindError,
    resolve_return_packet_output_identity,
)
from axm_institution.store import FilesystemObjectStore, ObjectNotFoundError


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketOutputIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(self, *, artifact_type: str, content_ref: str, base: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = "artifact.same"
        artifact["type"] = artifact_type
        artifact["content_ref"] = content_ref
        artifact["provenance"]["base_state_revision"] = base
        return artifact

    def _evidence(self, *, state: str, claim: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.same"
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), modified=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.output-identity"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = list(modified)
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    def test_exact_created_artifact_and_evidence_ignore_newer_same_id_decoys(self) -> None:
        artifact_a = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://a",
            base="revision.same-logical-id",
        )
        artifact_a_result = self.store.store(artifact_a, "artifact.schema.json")
        artifact_b = self._artifact(
            artifact_type="decoy_type",
            content_ref="artifact://b",
            base="revision.other-exact-instance",
        )
        artifact_b_result = self.store.store(artifact_b, "artifact.schema.json")

        evidence_a = self._evidence(
            state="automated_tested",
            claim="Exact historical evidence selected by the packet.",
        )
        evidence_a_result = self.store.store(evidence_a, "evidence-record.schema.json")
        evidence_b = self._evidence(
            state="invalidated",
            claim="Later same-id evidence must not replace the exact selected record.",
        )
        evidence_b_result = self.store.store(evidence_b, "evidence-record.schema.json")

        packet = self._packet(
            created=[artifact_a_result.reference],
            evidence=[evidence_a_result.reference],
        )
        packet_ref = self._store_packet(packet)
        result = resolve_return_packet_output_identity(self.store, packet_ref)

        self.assertEqual(result.packet_ref, packet_ref)
        self.assertEqual(result.created_artifacts[0].reference, artifact_a_result.reference)
        self.assertEqual(result.created_artifacts[0].value["type"], "kernel_contracts")
        self.assertNotEqual(result.created_artifacts[0].reference, artifact_b_result.reference)
        self.assertEqual(result.evidence_records[0].reference, evidence_a_result.reference)
        self.assertEqual(result.evidence_records[0].value["state"], "automated_tested")
        self.assertNotEqual(result.evidence_records[0].reference, evidence_b_result.reference)

    def test_bare_logical_created_artifact_id_fails_when_identity_becomes_operational(self) -> None:
        packet_ref = self._store_packet(
            self._packet(created=["artifact.same"], evidence=[])
        )
        with self.assertRaisesRegex(ReturnPacketOutputIdentityError, "artifacts_created"):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_bare_logical_evidence_id_fails_when_identity_becomes_operational(self) -> None:
        packet_ref = self._store_packet(
            self._packet(created=[], evidence=["evidence.same"])
        )
        with self.assertRaisesRegex(ReturnPacketOutputIdentityError, "evidence_refs"):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_wrong_kind_created_artifact_and_evidence_refs_fail_explicitly(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://kind",
            base="revision.kind",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence = self._evidence(state="invalidated", claim="Wrong-kind witness.")
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference

        cases = (
            self._packet(created=[evidence_ref], evidence=[]),
            self._packet(created=[], evidence=[artifact_ref]),
        )
        for packet in cases:
            with self.subTest(packet=packet):
                packet_ref = self._store_packet(packet)
                with self.assertRaises(ReturnPacketRelationKindError):
                    resolve_return_packet_output_identity(self.store, packet_ref)

    def test_noncanonical_relationship_refs_fail_through_shared_stage2_parser(self) -> None:
        digest = "1" * 64
        cases = (
            f"axmref:v1:artifact:thing%2Eencoded:v=0.1:sha256:{digest}",
            f"axmref:v1:artifact:%FF:v=0.1:sha256:{digest}",
            f"axmref:v1:artifact:e%CC%81:v=0.1:sha256:{digest}",
            f"axmref:v1:artifact:thing:v=0.1:sha256:{digest}x",
        )
        for reference in cases:
            with self.subTest(reference=reference):
                packet_ref = self._store_packet(
                    self._packet(created=[reference], evidence=[])
                )
                with self.assertRaises(ReturnPacketOutputIdentityError):
                    resolve_return_packet_output_identity(self.store, packet_ref)

    def test_same_logical_artifact_exact_substitution_changes_packet_identity(self) -> None:
        artifact_a = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://identity-a",
            base="revision.a",
        )
        artifact_b = self._artifact(
            artifact_type="different_type",
            content_ref="artifact://identity-b",
            base="revision.b",
        )
        ref_a = make_immutable_ref("artifact.schema.json", artifact_a)
        ref_b = make_immutable_ref("artifact.schema.json", artifact_b)
        self.assertEqual(parse_immutable_ref(ref_a).logical_id, "artifact.same")
        self.assertEqual(parse_immutable_ref(ref_b).logical_id, "artifact.same")
        self.assertNotEqual(ref_a, ref_b)

        packet_a = self._packet(created=[ref_a], evidence=[])
        packet_b = self._packet(created=[ref_b], evidence=[])
        self.assertNotEqual(
            make_immutable_ref("return-packet.schema.json", packet_a),
            make_immutable_ref("return-packet.schema.json", packet_b),
        )

    def test_same_logical_evidence_exact_substitution_changes_packet_identity(self) -> None:
        evidence_a = self._evidence(
            state="automated_tested",
            claim="Exact evidence A.",
        )
        evidence_b = self._evidence(
            state="invalidated",
            claim="Exact evidence B.",
        )
        ref_a = make_immutable_ref("evidence-record.schema.json", evidence_a)
        ref_b = make_immutable_ref("evidence-record.schema.json", evidence_b)
        self.assertEqual(parse_immutable_ref(ref_a).logical_id, "evidence.same")
        self.assertEqual(parse_immutable_ref(ref_b).logical_id, "evidence.same")
        self.assertNotEqual(ref_a, ref_b)

        packet_a = self._packet(created=[], evidence=[ref_a])
        packet_b = self._packet(created=[], evidence=[ref_b])
        self.assertNotEqual(
            make_immutable_ref("return-packet.schema.json", packet_a),
            make_immutable_ref("return-packet.schema.json", packet_b),
        )

    def test_missing_exact_created_artifact_fails_instead_of_falling_back_by_id(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://missing",
            base="revision.missing",
        )
        missing_ref = make_immutable_ref("artifact.schema.json", artifact)
        packet_ref = self._store_packet(self._packet(created=[missing_ref], evidence=[]))
        with self.assertRaises(ObjectNotFoundError):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_missing_exact_evidence_fails_instead_of_falling_back_by_id(self) -> None:
        evidence = self._evidence(state="invalidated", claim="Missing exact evidence.")
        missing_ref = make_immutable_ref("evidence-record.schema.json", evidence)
        packet_ref = self._store_packet(self._packet(created=[], evidence=[missing_ref]))
        with self.assertRaises(ObjectNotFoundError):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_modified_artifact_logical_id_is_explicitly_blocked(self) -> None:
        packet_ref = self._store_packet(
            self._packet(created=[], modified=["artifact.same"], evidence=[])
        )
        with self.assertRaisesRegex(
            ModifiedArtifactIdentityUnresolvedError,
            "exact prior artifact observed.*exact produced artifact result",
        ):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_even_one_exact_modified_artifact_ref_is_insufficient_for_two_sided_change(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://modified-one-side",
            base="revision.modified",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        packet_ref = self._store_packet(
            self._packet(created=[], modified=[artifact_ref], evidence=[])
        )
        with self.assertRaises(ModifiedArtifactIdentityUnresolvedError):
            resolve_return_packet_output_identity(self.store, packet_ref)

    def test_handoff_uncertainty_blocker_and_downstream_fields_survive_unchanged(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://handoff",
            base="revision.handoff",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence = self._evidence(state="invalidated", claim="Handoff evidence.")
        evidence_ref = self.store.store(evidence, "evidence-record.schema.json").reference
        packet = self._packet(created=[artifact_ref], evidence=[evidence_ref])
        packet["uncertainties"] = ["uncertainty one", "uncertainty two"]
        packet["failures_or_blockers"] = ["blocker one"]
        packet["downstream_effects"] = ["downstream one", "downstream two"]
        expected = copy.deepcopy(packet)
        packet_ref = self._store_packet(packet)

        result = resolve_return_packet_output_identity(self.store, packet_ref)

        self.assertEqual(result.packet, expected)
        self.assertEqual(result.packet["uncertainties"], expected["uncertainties"])
        self.assertEqual(
            result.packet["failures_or_blockers"], expected["failures_or_blockers"]
        )
        self.assertEqual(
            result.packet["downstream_effects"], expected["downstream_effects"]
        )


if __name__ == "__main__":
    unittest.main()
