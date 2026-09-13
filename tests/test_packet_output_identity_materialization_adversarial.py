from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import (
    canonical_bytes,
    make_immutable_ref,
    parse_json_strict,
)
from axm_institution.packet_output_identity import resolve_return_packet_output_identity
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketOutputIdentityMaterializationAdversarialTests(unittest.TestCase):
    """ADV-038: exact operational views must survive bounded materialization without alias drift."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(self, *, artifact_type: str, content_ref: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = "artifact.adv038"
        artifact["type"] = artifact_type
        artifact["content_ref"] = content_ref
        artifact["provenance"]["source_refs"] = [
            "source://adv038/nested-a",
            "source://adv038/nested-b",
        ]
        artifact["dependency_refs"] = ["artifact://dependency/adv038"]
        artifact["notes"] = ["nested", "materialization"]
        return artifact

    def _evidence(self, *, state: str, claim: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.adv038"
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.adv038"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence)
        packet["changes"] = ["nested materialization continuity probe"]
        packet["uncertainties"] = ["transport support remains intentionally bounded"]
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    def test_adv038_a_builtin_mapping_materialization_is_exact_then_detached(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://adv038-a",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        packet_ref = self._store_packet(self._packet(created=[artifact_ref]))

        result = resolve_return_packet_output_identity(self.store, packet_ref)
        relation = result.created_artifacts[0]
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", relation.value), relation.reference
        )

        materialized = dict(relation.value)
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", materialized), relation.reference,
            "ordinary mapping materialization changed exact artifact meaning",
        )

        materialized["type"] = "decoy_after_materialization"
        self.assertNotEqual(
            make_immutable_ref("artifact.schema.json", materialized), relation.reference
        )
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", relation.value), relation.reference,
            "mutating a detached materialization back-mutated the authoritative exact view",
        )

    def test_adv038_b_materialized_nested_relation_cannot_rebind_exact_packet(self) -> None:
        evidence_a = self._evidence(
            state="automated_tested",
            claim="Exact evidence selected before materialization.",
        )
        evidence_a_ref = self.store.store(
            evidence_a, "evidence-record.schema.json"
        ).reference

        evidence_b = self._evidence(
            state="invalidated",
            claim="Same logical id but different exact evidence decoy.",
        )
        evidence_b_ref = self.store.store(
            evidence_b, "evidence-record.schema.json"
        ).reference
        self.assertNotEqual(evidence_a_ref, evidence_b_ref)

        packet_ref = self._store_packet(self._packet(evidence=[evidence_a_ref]))
        result = resolve_return_packet_output_identity(self.store, packet_ref)
        self.assertEqual(result.evidence_records[0].reference, evidence_a_ref)
        self.assertEqual(
            make_immutable_ref("return-packet.schema.json", result.packet), packet_ref
        )

        materialized_refs = list(result.packet["evidence_refs"])
        self.assertEqual(materialized_refs, [evidence_a_ref])
        materialized_refs[0] = evidence_b_ref

        self.assertEqual(
            result.packet["evidence_refs"][0], evidence_a_ref,
            "detached list materialization rebound the authoritative packet relationship",
        )
        self.assertEqual(
            result.evidence_records[0].reference, evidence_a_ref,
            "same-logical-id decoy acquired authority after nested materialization",
        )
        self.assertEqual(
            make_immutable_ref("return-packet.schema.json", result.packet), packet_ref
        )

    def test_adv038_c_canonical_materialization_round_trip_preserves_nested_exact_identity(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://adv038-c",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence = self._evidence(
            state="runtime_tested",
            claim="Nested exact packet materialization remains reconstructable.",
        )
        evidence_ref = self.store.store(
            evidence, "evidence-record.schema.json"
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_ref], evidence=[evidence_ref])
        )

        result = resolve_return_packet_output_identity(self.store, packet_ref)
        transported = parse_json_strict(canonical_bytes(result.packet).decode("utf-8"))

        self.assertEqual(
            make_immutable_ref("return-packet.schema.json", transported), packet_ref,
            "Stage 2 canonical materialization changed packet exact identity",
        )
        self.assertEqual(transported["artifacts_created"], [artifact_ref])
        self.assertEqual(transported["evidence_refs"], [evidence_ref])
        self.assertEqual(result.created_artifacts[0].reference, artifact_ref)
        self.assertEqual(result.evidence_records[0].reference, evidence_ref)


if __name__ == "__main__":
    unittest.main()
