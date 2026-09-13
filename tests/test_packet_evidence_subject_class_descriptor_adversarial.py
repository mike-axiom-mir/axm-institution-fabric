from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.packet_evidence_subject import resolve_return_packet_evidence_subjects
from axm_institution.packet_output_identity import (
    ExactPacketRelation,
    ResolvedReturnPacketOutputIdentity,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketEvidenceSubjectClassDescriptorAdversarialTests(unittest.TestCase):
    """ADV-041: tuple-backed exact wrappers must not gain mutable class-level truth."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(self, *, artifact_id: str, content_ref: str):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["content_ref"] = content_ref
        artifact["provenance"]["base_state_revision"] = "revision.adv041"
        artifact["evidence_refs"] = []
        return artifact

    def _evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str,
        claim: str,
    ):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.adv041"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    def _assert_relation_matches_store(self, relation, schema_name: str) -> None:
        durable_value = self.store.load(relation.reference, schema_name)
        operational_value = dict(relation.value)
        self.assertEqual(
            operational_value,
            durable_value,
            "exact relation reference/value pair drifted through class-level read semantics",
        )

    def test_adv041_a_exact_relation_reference_descriptor_cannot_rebind_existing_result(self) -> None:
        """Class-level field replacement must not rewrite an already-proved exact ref."""

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv041-a"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv041-b"),
            "artifact.schema.json",
        ).reference
        evidence_a_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.a",
                subject_ref=artifact_a_ref,
                state="implemented",
                claim="Evidence explicitly about exact artifact A.",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_a_ref], evidence=[evidence_a_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        relation = result.created_artifact_bindings[0].artifact
        self.assertEqual(relation.reference, artifact_a_ref)
        self._assert_relation_matches_store(relation, "artifact.schema.json")

        original_descriptor = ExactPacketRelation.__dict__["reference"]
        changed = False
        try:
            try:
                setattr(
                    ExactPacketRelation,
                    "reference",
                    property(lambda self: artifact_b_ref),
                )
                changed = True
            except (AttributeError, TypeError):
                return

            self.assertEqual(relation[0], artifact_a_ref)
            self.assertEqual(
                relation.reference,
                artifact_a_ref,
                "class-level descriptor mutation rebound an already-proved exact ref",
            )
            self._assert_relation_matches_store(relation, "artifact.schema.json")
        finally:
            if changed:
                setattr(ExactPacketRelation, "reference", original_descriptor)

    def test_adv041_b_exact_relation_value_descriptor_cannot_launder_unrelated_evidence(self) -> None:
        """Class-level field replacement must not pair an exact ref with another value."""

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv041-bound"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv041-other"),
            "artifact.schema.json",
        ).reference
        evidence_a_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.a",
                subject_ref=artifact_a_ref,
                state="implemented",
                claim="Evidence explicitly about artifact A.",
            ),
            "evidence-record.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.b",
                subject_ref=artifact_b_ref,
                state="automated_tested",
                claim="Passing evidence explicitly about unrelated artifact B.",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(
                created=[artifact_a_ref],
                evidence=[evidence_a_ref, evidence_b_ref],
            )
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        binding = result.created_artifact_bindings[0]
        bound = binding.evidence_records[0]
        unrelated = result.unmatched_evidence[0].evidence
        unrelated_value = unrelated[1]
        self.assertEqual(bound.reference, evidence_a_ref)
        self.assertEqual(bound.value["subject_ref"], artifact_a_ref)
        self.assertEqual(unrelated.reference, evidence_b_ref)
        self.assertEqual(unrelated.value["subject_ref"], artifact_b_ref)
        self._assert_relation_matches_store(bound, "evidence-record.schema.json")

        original_descriptor = ExactPacketRelation.__dict__["value"]
        changed = False
        try:
            try:
                setattr(
                    ExactPacketRelation,
                    "value",
                    property(
                        lambda self: unrelated_value
                        if self[0] == evidence_a_ref
                        else self[1]
                    ),
                )
                changed = True
            except (AttributeError, TypeError):
                return

            self.assertEqual(bound[1]["subject_ref"], artifact_a_ref)
            self.assertEqual(
                bound.value["subject_ref"],
                artifact_a_ref,
                "class-level descriptor mutation laundered unrelated evidence value",
            )
            self._assert_relation_matches_store(bound, "evidence-record.schema.json")
        finally:
            if changed:
                setattr(ExactPacketRelation, "value", original_descriptor)

    def test_adv041_c_output_identity_descriptor_cannot_hide_exact_packet_evidence(self) -> None:
        """Class-level result fields must not hide exact relations from existing results."""

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv041-set"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv041-set-other"),
            "artifact.schema.json",
        ).reference
        evidence_a_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.a",
                subject_ref=artifact_a_ref,
                state="implemented",
                claim="Evidence about packet-created artifact A.",
            ),
            "evidence-record.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.b",
                subject_ref=artifact_b_ref,
                state="invalidated",
                claim="Explicit packet evidence about unrelated artifact B.",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(
                created=[artifact_a_ref],
                evidence=[evidence_a_ref, evidence_b_ref],
            )
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        durable_packet = self.store.load(packet_ref, "return-packet.schema.json")
        expected_evidence_refs = tuple(durable_packet["evidence_refs"])
        self.assertEqual(
            tuple(relation.reference for relation in result.output_identity.evidence_records),
            expected_evidence_refs,
        )

        original_descriptor = ResolvedReturnPacketOutputIdentity.__dict__["evidence_records"]
        changed = False
        try:
            try:
                setattr(
                    ResolvedReturnPacketOutputIdentity,
                    "evidence_records",
                    property(lambda self: (self[3][0],)),
                )
                changed = True
            except (AttributeError, TypeError):
                return

            self.assertEqual(
                tuple(relation.reference for relation in result.output_identity.evidence_records),
                expected_evidence_refs,
                "class-level descriptor mutation hid exact packet evidence after proof",
            )
        finally:
            if changed:
                setattr(
                    ResolvedReturnPacketOutputIdentity,
                    "evidence_records",
                    original_descriptor,
                )


if __name__ == "__main__":
    unittest.main()
