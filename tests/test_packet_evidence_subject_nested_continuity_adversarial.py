from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.packet_evidence_subject import resolve_return_packet_evidence_subjects
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ReturnPacketEvidenceSubjectNestedContinuityAdversarialTests(unittest.TestCase):
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
        artifact["provenance"]["base_state_revision"] = "revision.adv040"
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
        packet["id"] = "packet.adv040"
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
            "exact relation reference/value pair drifted after resolution",
        )

    def test_adv040_a_nested_artifact_relation_reference_cannot_drift_after_subject_resolution(self) -> None:
        """The repaired outer NamedTuple must not hide a mutable nested exact relation.

        Subject binding returns an artifact relation whose reference/value pair is expected
        to remain exact. If the nested relation can be reassigned through
        ``object.__setattr__``, a later consumer can see artifact B's exact ref beside
        artifact A's already-grounded immutable value even though the outer binding itself
        is physically non-assignable.
        """

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv040-a"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv040-b"),
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

        try:
            object.__setattr__(relation, "reference", artifact_b_ref)
        except (AttributeError, TypeError):
            return

        self._assert_relation_matches_store(relation, "artifact.schema.json")

    def test_adv040_b_nested_evidence_relation_value_cannot_launder_an_unrelated_subject(self) -> None:
        """A bound nested evidence relation must keep its exact ref/value identity.

        The outer subject-binding wrapper may be immutable while its contained
        ``ExactPacketRelation`` remains a frozen dataclass that can be rewritten through
        ``object.__setattr__``. Replacing only the bound relation's value with unrelated
        exact evidence would recreate Decision 008 evidence laundering beneath the repaired
        outer wrapper.
        """

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv040-bound"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv040-other"),
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
        self.assertEqual(bound.reference, evidence_a_ref)
        self.assertEqual(bound.value["subject_ref"], artifact_a_ref)
        self.assertEqual(unrelated.reference, evidence_b_ref)
        self.assertEqual(unrelated.value["subject_ref"], artifact_b_ref)
        self._assert_relation_matches_store(bound, "evidence-record.schema.json")

        try:
            object.__setattr__(bound, "value", unrelated.value)
        except (AttributeError, TypeError):
            return

        self._assert_relation_matches_store(bound, "evidence-record.schema.json")
        self.assertEqual(
            bound.value["subject_ref"],
            binding.artifact.reference,
            "nested evidence value drift made unrelated exact evidence appear bound",
        )

    def test_adv040_c_nested_output_identity_evidence_set_cannot_drop_packet_evidence(self) -> None:
        """The nested lower-layer identity result must stay aligned with the exact packet.

        The repaired top-level subject projection retains ``output_identity`` from the
        already-canonical packet-output resolver. If that nested frozen dataclass can have
        its evidence tuple reassigned, a later occupant sees a different exact evidence set
        than the immutable packet actually names while the outer subject result remains
        unchanged.
        """

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv040-set"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv040-set-other"),
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

        try:
            object.__setattr__(
                result.output_identity,
                "evidence_records",
                (result.output_identity.evidence_records[0],),
            )
        except (AttributeError, TypeError):
            return

        self.assertEqual(
            tuple(relation.reference for relation in result.output_identity.evidence_records),
            expected_evidence_refs,
            "nested output-identity projection dropped exact packet evidence after proof",
        )


if __name__ == "__main__":
    unittest.main()
