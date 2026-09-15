from __future__ import annotations

import copy
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from axm_institution.identity import ContractValidationError
from axm_institution.integration_candidate_binding import (
    COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING,
    NON_ACCEPTING_RECEIPT_DECISION,
    RECEIPT_BASE_MISMATCH,
    RECEIPT_PACKET_MISMATCH,
    RECEIPT_PACKET_NOT_ELIGIBLE,
    UNSUPPORTED_MULTI_PACKET_RECEIPT_SLICE,
    preflight_exact_stored_integration_candidate_binding,
)
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    UNSUPPORTED_DEPENDENCY_POLICY,
    preflight_packet_integration_eligibility,
)
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
)


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class IntegrationCandidateBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    @staticmethod
    def _absent_exact_variant(reference: str) -> str:
        replacement = "0" if reference[-1] != "0" else "1"
        return reference[:-1] + replacement

    def _prior_artifact(self):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.1"
        artifact["id"] = "artifact.decision026.prior"
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.1"
        artifact["content_ref"] = "artifact://decision026/prior"
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-claim",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _output_artifact(self, *, base_ref: str, dependency_refs=()):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.2" if not dependency_refs else "0.3"
        artifact["id"] = "artifact.decision026.created"
        artifact["type"] = "kernel_contracts"
        artifact["version"] = artifact["schema_version"]
        artifact["content_ref"] = "artifact://decision026/created"
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": base_ref,
            "source_refs": ["source://decision026/preserved"],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = list(dependency_refs)
        artifact.pop("supersedes_ref", None)
        return artifact

    def _evidence(self, *, subject_ref: str):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.decision026.created"
        evidence["subject_ref"] = subject_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 026 exact subject-bound fixture evidence."
        return evidence

    def _store_base(self, lane_ref: str, prior_ref: str) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.decision026.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = [prior_ref]
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = ["Decision 026 bounded candidate-binding fixture."]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self.store.store(
            self._prior_artifact(), "artifact.schema.json"
        ).reference
        base_ref = self._store_base(lane_ref, prior_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.decision026"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.decision026"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        created_ref = self.store.store(
            self._output_artifact(base_ref=base_ref),
            "artifact.schema.json",
        ).reference
        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
            "created_ref": created_ref,
        }

    def _submit_packet(self, context, *, with_evidence: bool, packet_id: str) -> str:
        evidence_refs = []
        if with_evidence:
            evidence_refs.append(
                self.store.store(
                    self._evidence(subject_ref=context["created_ref"]),
                    "evidence-record.schema.json",
                ).reference
            )

        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = [context["created_ref"]]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = evidence_refs
        return submit_return_packet(self.store, packet).packet_ref

    @staticmethod
    def _root_grounding():
        return [
            {
                "root": "truth",
                "assessment": "grounded",
                "reason": "Exact stored inputs remain explicit facts.",
            },
            {
                "root": "agency_non_domination",
                "assessment": "grounded",
                "reason": "No actor identity grants binding authority.",
            },
            {
                "root": "continuity",
                "assessment": "grounded",
                "reason": "Exact receipt, base, packet, and eligibility facts are reconstructable.",
            },
            {
                "root": "wisdom_before_speed",
                "assessment": "grounded",
                "reason": "The preflight remains read-only and one-packet bounded.",
            },
        ]

    def _receipt(
        self,
        *,
        base_ref: str,
        packet_refs: list[str],
        decision: str = "accepted",
    ):
        return {
            "schema_version": "0.2",
            "id": "receipt.decision026.candidate",
            "base_state_revision_ref": base_ref,
            "packet_refs": list(packet_refs),
            "decision": decision,
            "reasons": ["Decision 026 candidate-binding fixture."],
            "root_grounding": self._root_grounding(),
            "unresolved_conflicts": [],
            "created_at": "2026-09-15T14:20:00Z",
        }

    def _eligible_context_and_packet(self):
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            with_evidence=True,
            packet_id="packet.decision026.eligible",
        )
        self.assertEqual(
            preflight_packet_integration_eligibility(
                self.store, packet_ref
            ).eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        return context, packet_ref

    def test_exact_stored_base_packet_and_accepted_receipt_bind_coherently(self):
        context, packet_ref = self._eligible_context_and_packet()
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        resolved = preflight_exact_stored_integration_candidate_binding(
            self.store, receipt
        )

        self.assertEqual(
            resolved.candidate_binding_outcome,
            COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING,
        )
        self.assertTrue(resolved.base_materialized)
        self.assertTrue(resolved.packet_materialized)
        self.assertEqual(resolved.base_state_revision_ref, context["base_ref"])
        self.assertEqual(resolved.packet_refs, (packet_ref,))
        self.assertIsNotNone(resolved.packet_eligibility)
        self.assertEqual(
            resolved.packet_eligibility.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        for forbidden in (
            "successor_revision_ref",
            "published",
            "integrated",
            "claim_closed",
            "root_approved",
        ):
            self.assertFalse(hasattr(resolved, forbidden))

    def test_well_formed_absent_exact_base_fails_through_store(self):
        context, packet_ref = self._eligible_context_and_packet()
        absent_base = self._absent_exact_variant(context["base_ref"])
        receipt = self._receipt(base_ref=absent_base, packet_refs=[packet_ref])

        with self.assertRaises(ObjectNotFoundError):
            preflight_exact_stored_integration_candidate_binding(self.store, receipt)

    def test_well_formed_absent_exact_packet_fails_without_logical_fallback(self):
        context, packet_ref = self._eligible_context_and_packet()
        absent_same_logical_packet = self._absent_exact_variant(packet_ref)
        receipt = self._receipt(
            base_ref=context["base_ref"],
            packet_refs=[absent_same_logical_packet],
        )

        with self.assertRaises(ObjectNotFoundError):
            preflight_exact_stored_integration_candidate_binding(self.store, receipt)

    def test_corrupt_exact_packet_fails_closed_through_store(self):
        context, packet_ref = self._eligible_context_and_packet()
        path = self.store._object_path(packet_ref)
        path.write_bytes(b" " + path.read_bytes())
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        with self.assertRaises(ObjectCorruptionError):
            preflight_exact_stored_integration_candidate_binding(self.store, receipt)

    def test_reproduced_identity_mismatch_in_stored_packet_fails_closed(self):
        context, packet_ref = self._eligible_context_and_packet()
        alternate_packet = copy.deepcopy(self.store.load(packet_ref))
        alternate_packet["uncertainties"] = [
            "Same logical packet id, different exact stored bytes for Decision 026."
        ]
        alternate_ref = self.store.store(
            alternate_packet, "return-packet.schema.json"
        ).reference
        self.assertNotEqual(alternate_ref, packet_ref)

        target = self.store._object_path(packet_ref)
        target.write_bytes(self.store._object_path(alternate_ref).read_bytes())
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        with self.assertRaises(ObjectCorruptionError):
            preflight_exact_stored_integration_candidate_binding(self.store, receipt)

    def test_same_logical_different_exact_packet_fact_cannot_bind(self):
        context, packet_ref = self._eligible_context_and_packet()
        real_eligibility = preflight_packet_integration_eligibility(self.store, packet_ref)
        decoy_ref = self._absent_exact_variant(packet_ref)
        decoy_eligibility = replace(real_eligibility, packet_ref=decoy_ref)
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        with patch(
            "axm_institution.integration_candidate_binding.preflight_packet_integration_eligibility",
            return_value=decoy_eligibility,
        ):
            resolved = preflight_exact_stored_integration_candidate_binding(
                self.store, receipt
            )

        self.assertEqual(resolved.candidate_binding_outcome, RECEIPT_PACKET_MISMATCH)
        self.assertEqual(resolved.reasons[0].code, "decision024_packet_ref_mismatch")

    def test_same_logical_different_exact_stored_base_is_explicit_mismatch(self):
        context, packet_ref = self._eligible_context_and_packet()
        alternate_base = copy.deepcopy(self.store.load(context["base_ref"]))
        alternate_base["uncertainties"] = [
            "Same logical revision id, different exact Decision 026 instance."
        ]
        alternate_base_ref = self.store.store(
            alternate_base, "state-revision.schema.json"
        ).reference
        self.assertNotEqual(alternate_base_ref, context["base_ref"])

        receipt = self._receipt(base_ref=alternate_base_ref, packet_refs=[packet_ref])
        resolved = preflight_exact_stored_integration_candidate_binding(
            self.store, receipt
        )

        self.assertEqual(resolved.candidate_binding_outcome, RECEIPT_BASE_MISMATCH)
        self.assertEqual(resolved.base_state_revision_ref, alternate_base_ref)
        self.assertEqual(
            resolved.packet_eligibility.base_state_revision_ref,
            context["base_ref"],
        )

    def test_accepted_receipt_cannot_launder_noneligible_packet(self):
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            with_evidence=False,
            packet_id="packet.decision026.noneligible",
        )
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        resolved = preflight_exact_stored_integration_candidate_binding(
            self.store, receipt
        )

        self.assertEqual(resolved.candidate_binding_outcome, RECEIPT_PACKET_NOT_ELIGIBLE)
        self.assertNotEqual(
            resolved.packet_eligibility.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )

    def test_accepted_receipt_cannot_launder_unsupported_packet(self):
        context = self._ground_context()
        dependent_ref = self.store.store(
            self._output_artifact(
                base_ref=context["base_ref"],
                dependency_refs=[context["prior_ref"]],
            ),
            "artifact.schema.json",
        ).reference
        dependent_context = dict(context)
        dependent_context["created_ref"] = dependent_ref
        packet_ref = self._submit_packet(
            dependent_context,
            with_evidence=True,
            packet_id="packet.decision026.unsupported-dependency",
        )
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        resolved = preflight_exact_stored_integration_candidate_binding(
            self.store, receipt
        )

        self.assertEqual(resolved.candidate_binding_outcome, RECEIPT_PACKET_NOT_ELIGIBLE)
        self.assertEqual(
            resolved.packet_eligibility.eligibility_outcome,
            UNSUPPORTED_DEPENDENCY_POLICY,
        )

    def test_nonaccepting_receipt_decisions_never_become_successor_candidates(self):
        context, packet_ref = self._eligible_context_and_packet()

        for decision in (
            "rejected",
            "deferred",
            "repair_requested",
            "partially_integrated",
        ):
            with self.subTest(decision=decision):
                receipt = self._receipt(
                    base_ref=context["base_ref"],
                    packet_refs=[packet_ref],
                    decision=decision,
                )
                resolved = preflight_exact_stored_integration_candidate_binding(
                    self.store, receipt
                )
                self.assertEqual(
                    resolved.candidate_binding_outcome,
                    NON_ACCEPTING_RECEIPT_DECISION,
                )
                self.assertEqual(resolved.receipt_decision, decision)
                self.assertEqual(
                    resolved.packet_eligibility.eligibility_outcome,
                    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
                )

    def test_multiple_packet_refs_are_explicitly_unsupported_without_first_item_selection(self):
        context, packet_ref = self._eligible_context_and_packet()
        second_ref = self._absent_exact_variant(packet_ref)
        receipt = self._receipt(
            base_ref=context["base_ref"],
            packet_refs=[packet_ref, second_ref],
        )

        resolved = preflight_exact_stored_integration_candidate_binding(
            self.store, receipt
        )

        self.assertEqual(
            resolved.candidate_binding_outcome,
            UNSUPPORTED_MULTI_PACKET_RECEIPT_SLICE,
        )
        self.assertIsNone(resolved.base_materialized)
        self.assertIsNone(resolved.packet_materialized)
        self.assertIsNone(resolved.packet_eligibility)
        self.assertEqual(resolved.packet_refs, (packet_ref, second_ref))

    def test_repeated_identical_inputs_produce_identical_named_fact(self):
        context, packet_ref = self._eligible_context_and_packet()
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        first = preflight_exact_stored_integration_candidate_binding(self.store, receipt)
        second = preflight_exact_stored_integration_candidate_binding(
            self.store, copy.deepcopy(receipt)
        )

        self.assertEqual(first, second)
        self.assertEqual(first.reasons, second.reasons)
        self.assertEqual(first.packet_eligibility, second.packet_eligibility)

    def test_hidden_authority_fields_are_not_admitted_into_candidate_binding(self):
        context, packet_ref = self._eligible_context_and_packet()
        receipt = self._receipt(base_ref=context["base_ref"], packet_refs=[packet_ref])

        for field in (
            "current",
            "HEAD",
            "actor",
            "founder",
            "schedule_position",
            "ci_status",
            "branch",
            "git_permission",
        ):
            with self.subTest(field=field):
                widened = copy.deepcopy(receipt)
                widened[field] = "authority"
                with self.assertRaises(ContractValidationError):
                    preflight_exact_stored_integration_candidate_binding(
                        self.store, widened
                    )


if __name__ == "__main__":
    unittest.main()
