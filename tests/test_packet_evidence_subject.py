from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.packet_evidence_subject import (
    EvidenceSubjectKindError,
    resolve_return_packet_evidence_subjects,
)
from axm_institution.packet_output_identity import ModifiedArtifactIdentityUnresolvedError
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketEvidenceSubjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _artifact(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        artifact_type: str = "kernel_contracts",
        evidence_refs=(),
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = artifact_id
        artifact["type"] = artifact_type
        artifact["content_ref"] = content_ref
        artifact["provenance"]["base_state_revision"] = "revision.subject-binding"
        artifact["evidence_refs"] = list(evidence_refs)
        return artifact

    def _evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str = "automated_tested",
        claim: str = "Subject-binding regression evidence.",
    ):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = claim
        return evidence

    def _packet(self, *, created=(), modified=(), evidence=()):
        packet = self._fixture("return-packet.schema.json")
        packet["id"] = "packet.evidence-subject"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = list(modified)
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    def test_exact_subject_binds_only_to_exact_created_artifact(self) -> None:
        artifact_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://subject-a",
            ),
            "artifact.schema.json",
        ).reference
        evidence_ref = self.store.store(
            self._evidence(evidence_id="evidence.a", subject_ref=artifact_ref),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_ref], evidence=[evidence_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        self.assertEqual(len(result.created_artifact_bindings), 1)
        binding = result.created_artifact_bindings[0]
        self.assertEqual(binding.artifact.reference, artifact_ref)
        self.assertEqual(
            tuple(relation.reference for relation in binding.evidence_records),
            (evidence_ref,),
        )
        self.assertEqual(result.unmatched_evidence, ())

    def test_same_logical_artifact_different_exact_ref_does_not_bind(self) -> None:
        artifact_a_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.same",
                content_ref="artifact://exact-a",
            ),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.same",
                content_ref="artifact://exact-b",
            ),
            "artifact.schema.json",
        ).reference
        self.assertNotEqual(artifact_a_ref, artifact_b_ref)
        evidence_ref = self.store.store(
            self._evidence(evidence_id="evidence.same-id", subject_ref=artifact_b_ref),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_a_ref], evidence=[evidence_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        self.assertEqual(result.created_artifact_bindings[0].evidence_records, ())
        self.assertEqual(len(result.unmatched_evidence), 1)
        self.assertEqual(result.unmatched_evidence[0].evidence.reference, evidence_ref)
        self.assertEqual(
            result.unmatched_evidence[0].reason,
            "exact_artifact_not_created_by_packet",
        )

    def test_non_exact_subject_strings_remain_explicitly_unmatched(self) -> None:
        artifact_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://non-exact",
            ),
            "artifact.schema.json",
        ).reference
        subjects = (
            "artifact.a",
            "artifacts/output.json",
            "content://artifact.a",
        )
        evidence_refs = []
        for index, subject in enumerate(subjects):
            evidence_refs.append(
                self.store.store(
                    self._evidence(
                        evidence_id=f"evidence.non-exact-{index}",
                        subject_ref=subject,
                        state="implemented",
                    ),
                    "evidence-record.schema.json",
                ).reference
            )
        packet_ref = self._store_packet(
            self._packet(created=[artifact_ref], evidence=evidence_refs)
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        self.assertEqual(result.created_artifact_bindings[0].evidence_records, ())
        self.assertEqual(
            tuple(item.subject_ref for item in result.unmatched_evidence), subjects
        )
        self.assertTrue(
            all(item.reason == "non_exact_subject" for item in result.unmatched_evidence)
        )

    def test_wrong_kind_exact_subject_fails_closed(self) -> None:
        artifact_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://wrong-kind",
            ),
            "artifact.schema.json",
        ).reference
        objective = self._fixture("objective.schema.json")
        objective["id"] = "objective.subject-decoy"
        objective_ref = self.store.store(objective, "objective.schema.json").reference
        evidence_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.wrong-kind",
                subject_ref=objective_ref,
                state="implemented",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_ref], evidence=[evidence_ref])
        )

        with self.assertRaisesRegex(EvidenceSubjectKindError, "kind 'artifact'"):
            resolve_return_packet_evidence_subjects(self.store, packet_ref)

    def test_unrelated_passing_evidence_cannot_satisfy_created_artifact(self) -> None:
        artifact_a_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://created-a",
                artifact_type="same_type",
            ),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.b",
                content_ref="artifact://unrelated-b",
                artifact_type="same_type",
            ),
            "artifact.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.b",
                subject_ref=artifact_b_ref,
                state="automated_tested",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_a_ref], evidence=[evidence_b_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        self.assertEqual(result.created_artifact_bindings[0].artifact.reference, artifact_a_ref)
        self.assertEqual(result.created_artifact_bindings[0].evidence_records, ())
        self.assertEqual(result.unmatched_evidence[0].subject_ref, artifact_b_ref)

    def test_artifact_evidence_refs_cannot_override_contradictory_exact_subject(self) -> None:
        artifact_b_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.b",
                content_ref="artifact://subject-b",
            ),
            "artifact.schema.json",
        ).reference
        evidence_ref = self.store.store(
            self._evidence(evidence_id="evidence.b", subject_ref=artifact_b_ref),
            "evidence-record.schema.json",
        ).reference
        artifact_a_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://created-a",
                evidence_refs=[evidence_ref],
            ),
            "artifact.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_a_ref], evidence=[evidence_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        self.assertEqual(result.created_artifact_bindings[0].evidence_records, ())
        self.assertEqual(result.unmatched_evidence[0].evidence.reference, evidence_ref)
        self.assertEqual(result.unmatched_evidence[0].subject_ref, artifact_b_ref)

    def test_reversed_packet_evidence_order_does_not_change_subject_binding(self) -> None:
        artifact_a_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.a",
                content_ref="artifact://order-a",
            ),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(
                artifact_id="artifact.b",
                content_ref="artifact://order-b",
            ),
            "artifact.schema.json",
        ).reference
        evidence_a_ref = self.store.store(
            self._evidence(evidence_id="evidence.a", subject_ref=artifact_a_ref),
            "evidence-record.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(evidence_id="evidence.b", subject_ref=artifact_b_ref),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(
                created=[artifact_a_ref, artifact_b_ref],
                evidence=[evidence_b_ref, evidence_a_ref],
            )
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        bound = {
            binding.artifact.reference: {
                relation.reference for relation in binding.evidence_records
            }
            for binding in result.created_artifact_bindings
        }

        self.assertEqual(bound[artifact_a_ref], {evidence_a_ref})
        self.assertEqual(bound[artifact_b_ref], {evidence_b_ref})
        self.assertEqual(result.unmatched_evidence, ())

    def test_modified_artifacts_remain_fail_closed_before_subject_binding(self) -> None:
        packet_ref = self._store_packet(
            self._packet(created=[], modified=["artifact.any"], evidence=[])
        )

        with self.assertRaises(ModifiedArtifactIdentityUnresolvedError):
            resolve_return_packet_evidence_subjects(self.store, packet_ref)


if __name__ == "__main__":
    unittest.main()
