from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import IdentityError, make_immutable_ref
from axm_institution.packet_output_identity import resolve_return_packet_output_identity
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketOutputIdentityTransportAdversarialTests(unittest.TestCase):
    """ADV-037: tuple-backed JSON views must not silently change meaning in stdlib JSON."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(self, *, artifact_type: str, content_ref: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = "artifact.adv037"
        artifact["type"] = artifact_type
        artifact["content_ref"] = content_ref
        return artifact

    def _evidence(self, *, state: str, claim: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.adv037"
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.adv037"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    def _require_stdlib_json_transport_is_fail_closed_or_exact(
        self,
        value,
        *,
        schema_name: str,
        reference: str,
    ) -> None:
        """Accept explicit rejection or an exact JSON round-trip; reject silent shape drift."""

        try:
            encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return

        transported = json.loads(encoded)
        try:
            transported_ref = make_immutable_ref(schema_name, transported)
        except IdentityError as exc:
            self.fail(
                "authoritative operational value was accepted by Python stdlib JSON "
                "encoding but transported into a different/non-contract shape instead "
                f"of failing closed: encoded={encoded!r}; error={exc}"
            )

        self.assertEqual(
            transported_ref,
            reference,
            "stdlib JSON transport silently changed exact ref/value meaning",
        )

    def test_adv037_a_created_artifact_json_transport_cannot_silently_retype_mapping(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://adv037-a",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        packet_ref = self._store_packet(self._packet(created=[artifact_ref]))

        result = resolve_return_packet_output_identity(self.store, packet_ref)
        relation = result.created_artifacts[0]
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", relation.value), relation.reference
        )

        self._require_stdlib_json_transport_is_fail_closed_or_exact(
            relation.value,
            schema_name="artifact.schema.json",
            reference=relation.reference,
        )

    def test_adv037_b_packet_nested_exact_relation_survives_or_rejects_json_transport(self) -> None:
        evidence_a = self._evidence(
            state="automated_tested",
            claim="Exact evidence relation selected before compatibility.",
        )
        evidence_a_ref = self.store.store(
            evidence_a, "evidence-record.schema.json"
        ).reference

        evidence_b = self._evidence(
            state="invalidated",
            claim="Same logical id but conflicting exact evidence instance.",
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

        self._require_stdlib_json_transport_is_fail_closed_or_exact(
            result.packet,
            schema_name="return-packet.schema.json",
            reference=packet_ref,
        )

        self.assertEqual(
            result.packet["evidence_refs"][0],
            result.evidence_records[0].reference,
            "same-logical-id decoy acquired authority around the operational adapter",
        )


if __name__ == "__main__":
    unittest.main()
