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


class ReturnPacketEvidenceSubjectAdversarialTests(unittest.TestCase):
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
        artifact["provenance"]["base_state_revision"] = "revision.adv039"
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
        packet["id"] = "packet.adv039"
        packet["artifacts_created"] = list(created)
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = list(evidence)
        return packet

    def _store_packet(self, packet):
        return self.store.store(packet, "return-packet.schema.json").reference

    @staticmethod
    def _assert_bound_subjects_are_exact(result) -> None:
        for binding in result.created_artifact_bindings:
            for evidence in binding.evidence_records:
                if evidence.value["subject_ref"] != binding.artifact.reference:
                    raise AssertionError(
                        "subject-binding result drifted after resolution: evidence "
                        f"{evidence.reference!r} now appears under artifact "
                        f"{binding.artifact.reference!r} even though its exact subject is "
                        f"{evidence.value['subject_ref']!r}"
                    )

    @staticmethod
    def _assert_evidence_partition_is_complete(result) -> None:
        expected = [relation.reference for relation in result.output_identity.evidence_records]
        observed = [
            evidence.reference
            for binding in result.created_artifact_bindings
            for evidence in binding.evidence_records
        ] + [item.evidence.reference for item in result.unmatched_evidence]
        if sorted(observed) != sorted(expected):
            raise AssertionError(
                "subject-binding result no longer partitions the exact packet evidence; "
                f"expected {expected!r}, observed {observed!r}"
            )

    def test_adv039_a_binding_wrapper_cannot_launder_unrelated_exact_evidence_after_resolution(self) -> None:
        """A frozen-looking binding must not be rebindable through object.__setattr__.

        The durable packet and exact evidence remain correct in this attack. The only
        mutation is to the operational subject-binding result handed to the next stage.
        A successful mutation would recreate the exact unrelated-evidence laundering
        Decision 008 was introduced to prevent.
        """

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv039-a"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv039-b"),
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
            self._packet(created=[artifact_a_ref], evidence=[evidence_a_ref, evidence_b_ref])
        )
        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)

        binding = result.created_artifact_bindings[0]
        unrelated = result.unmatched_evidence[0].evidence
        self.assertEqual(binding.artifact.reference, artifact_a_ref)
        self.assertEqual(tuple(item.reference for item in binding.evidence_records), (evidence_a_ref,))
        self.assertEqual(unrelated.reference, evidence_b_ref)
        self._assert_bound_subjects_are_exact(result)

        try:
            object.__setattr__(binding, "evidence_records", (unrelated,))
        except (AttributeError, TypeError):
            return

        self._assert_bound_subjects_are_exact(result)

    def test_adv039_b_explicit_unmatched_evidence_cannot_disappear_from_operational_result(self) -> None:
        """Explicit unmatched evidence is continuity state, not disposable presentation.

        Later consumers may not silently turn an exact-but-unrelated packet evidence record
        into absence merely because the returned dataclass is only shallowly frozen.
        """

        artifact_a_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv039-unmatched"),
            "artifact.schema.json",
        ).reference
        artifact_b_ref = self.store.store(
            self._artifact(artifact_id="artifact.b", content_ref="artifact://adv039-other"),
            "artifact.schema.json",
        ).reference
        evidence_b_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.unmatched",
                subject_ref=artifact_b_ref,
                state="invalidated",
                claim="This exact evidence is not about packet-created artifact A.",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_a_ref], evidence=[evidence_b_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        self.assertEqual(len(result.unmatched_evidence), 1)
        self._assert_evidence_partition_is_complete(result)

        try:
            object.__setattr__(result, "unmatched_evidence", ())
        except (AttributeError, TypeError):
            return

        self._assert_evidence_partition_is_complete(result)

    def test_adv039_c_conflicting_same_logical_evidence_states_remain_explicit(self) -> None:
        """Subject binding must preserve conflict without inventing state precedence."""

        artifact_ref = self.store.store(
            self._artifact(artifact_id="artifact.conflict", content_ref="artifact://adv039-conflict"),
            "artifact.schema.json",
        ).reference
        evidence_implemented_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.conflict",
                subject_ref=artifact_ref,
                state="implemented",
                claim="Same logical evidence id, implemented exact instance.",
            ),
            "evidence-record.schema.json",
        ).reference
        evidence_invalidated_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.conflict",
                subject_ref=artifact_ref,
                state="invalidated",
                claim="Same logical evidence id, conflicting invalidated exact instance.",
            ),
            "evidence-record.schema.json",
        ).reference
        self.assertNotEqual(evidence_implemented_ref, evidence_invalidated_ref)

        packet_ref = self._store_packet(
            self._packet(
                created=[artifact_ref],
                evidence=[evidence_invalidated_ref, evidence_implemented_ref],
            )
        )
        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        binding = result.created_artifact_bindings[0]

        self.assertEqual(
            {relation.reference for relation in binding.evidence_records},
            {evidence_implemented_ref, evidence_invalidated_ref},
        )
        self.assertEqual(
            {relation.value["state"] for relation in binding.evidence_records},
            {"implemented", "invalidated"},
        )
        self.assertEqual(result.unmatched_evidence, ())
        self._assert_bound_subjects_are_exact(result)
        self._assert_evidence_partition_is_complete(result)

    def test_adv039_d_noncanonical_exact_like_subject_cannot_gain_exact_standing(self) -> None:
        """A malformed axmref-looking string must remain explicit unmatched evidence."""

        artifact_ref = self.store.store(
            self._artifact(artifact_id="artifact.a", content_ref="artifact://adv039-noncanonical"),
            "artifact.schema.json",
        ).reference
        noncanonical_subject = artifact_ref.replace(":artifact.a:", ":%61rtifact.a:", 1)
        self.assertNotEqual(noncanonical_subject, artifact_ref)

        evidence_ref = self.store.store(
            self._evidence(
                evidence_id="evidence.noncanonical",
                subject_ref=noncanonical_subject,
                state="implemented",
                claim="Exact-looking but noncanonical subject must not bind.",
            ),
            "evidence-record.schema.json",
        ).reference
        packet_ref = self._store_packet(
            self._packet(created=[artifact_ref], evidence=[evidence_ref])
        )

        result = resolve_return_packet_evidence_subjects(self.store, packet_ref)
        self.assertEqual(result.created_artifact_bindings[0].evidence_records, ())
        self.assertEqual(len(result.unmatched_evidence), 1)
        self.assertEqual(result.unmatched_evidence[0].subject_ref, noncanonical_subject)
        self.assertEqual(result.unmatched_evidence[0].reason, "non_exact_subject")
        self._assert_evidence_partition_is_complete(result)


if __name__ == "__main__":
    unittest.main()
