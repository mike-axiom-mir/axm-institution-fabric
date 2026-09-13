from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import make_immutable_ref
from axm_institution.packet_output_identity import resolve_return_packet_output_identity
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketOutputIdentityFreezeBypassAdversarialTests(unittest.TestCase):
    """ADV-036: builtin base-class mutators must not bypass exact-value immutability."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(self, *, artifact_type: str, content_ref: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = "artifact.adv036"
        artifact["type"] = artifact_type
        artifact["content_ref"] = content_ref
        return artifact

    def _evidence(self, *, state: str, claim: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.adv036"
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.adv036"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    @staticmethod
    def _require_base_mutator_cannot_create_ref_drift(
        value,
        mutate,
        *,
        schema_name: str,
        reference: str,
    ) -> None:
        """Accept rejection or preserved exact identity; fail on silent ref/value drift."""

        try:
            mutate(value)
        except (TypeError, AttributeError):
            return

        current_ref = make_immutable_ref(schema_name, value)
        if current_ref != reference:
            raise AssertionError(
                "resolved exact JSON value can be mutated through a builtin base-class "
                f"mutator, drifting from {reference} to {current_ref}"
            )

    def test_adv036_a_builtin_dict_setitem_cannot_bypass_created_artifact_freeze(self) -> None:
        artifact = self._artifact(
            artifact_type="kernel_contracts",
            content_ref="artifact://adv036-a",
        )
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
        packet_ref = self._store_packet(self._packet(created=[artifact_ref]))

        result = resolve_return_packet_output_identity(self.store, packet_ref)
        relation = result.created_artifacts[0]
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", relation.value), relation.reference
        )

        self._require_base_mutator_cannot_create_ref_drift(
            relation.value,
            lambda value: dict.__setitem__(value, "type", "bypassed_after_resolution"),
            schema_name="artifact.schema.json",
            reference=relation.reference,
        )

    def test_adv036_b_builtin_dict_setitem_cannot_bypass_evidence_freeze(self) -> None:
        evidence = self._evidence(
            state="automated_tested",
            claim="Exact evidence state selected before compatibility.",
        )
        evidence_ref = self.store.store(
            evidence, "evidence-record.schema.json"
        ).reference
        packet_ref = self._store_packet(self._packet(evidence=[evidence_ref]))

        result = resolve_return_packet_output_identity(self.store, packet_ref)
        relation = result.evidence_records[0]
        self.assertEqual(
            make_immutable_ref("evidence-record.schema.json", relation.value),
            relation.reference,
        )

        self._require_base_mutator_cannot_create_ref_drift(
            relation.value,
            lambda value: dict.__setitem__(value, "state", "invalidated"),
            schema_name="evidence-record.schema.json",
            reference=relation.reference,
        )

    def test_adv036_c_builtin_list_setitem_cannot_rebind_packet_relationship(self) -> None:
        evidence_a = self._evidence(
            state="automated_tested",
            claim="Exact packet evidence relation.",
        )
        evidence_a_ref = self.store.store(
            evidence_a, "evidence-record.schema.json"
        ).reference

        evidence_b = self._evidence(
            state="invalidated",
            claim="Same logical id but conflicting exact evidence state.",
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

        self._require_base_mutator_cannot_create_ref_drift(
            result.packet,
            lambda value: list.__setitem__(value["evidence_refs"], 0, evidence_b_ref),
            schema_name="return-packet.schema.json",
            reference=packet_ref,
        )

        self.assertEqual(
            result.packet["evidence_refs"][0], result.evidence_records[0].reference
        )


if __name__ == "__main__":
    unittest.main()
