from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_artifact_provenance import ArtifactProducerLaneMismatchError
from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    NOT_ELIGIBLE_CONFLICTING_SUBJECT_EVIDENCE,
    NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
    UNSUPPORTED_DEPENDENCY_POLICY,
    UNSUPPORTED_MODIFIED_OUTPUT_SLICE,
    preflight_packet_integration_eligibility,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class PacketIntegrationEligibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _prior_artifact(self):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.1"
        artifact["id"] = "artifact.eligibility.prior"
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.1"
        artifact["content_ref"] = "artifact://eligibility/prior"
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-claim",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _output_artifact(
        self,
        *,
        base_ref: str,
        artifact_id: str = "artifact.eligibility.created",
        content_ref: str = "artifact://eligibility/created",
        schema_version: str = "0.2",
        producer_lane_id: str = "lane-02",
        dependency_refs=(),
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = schema_version
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = schema_version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": producer_lane_id,
            "base_state_revision_ref": base_ref,
            "source_refs": ["source://decision024/preserved"],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = list(dependency_refs)
        artifact.pop("supersedes_ref", None)
        return artifact

    def _evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str = "automated_tested",
    ):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = "Decision 024 exact subject-bound evidence."
        return evidence

    def _store_base(self, lane_ref: str, prior_ref: str) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.eligibility.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = [prior_ref]
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = ["Decision 024 bounded eligibility fixture."]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self.store.store(
            self._prior_artifact(), "artifact.schema.json"
        ).reference
        base_ref = self._store_base(lane_ref, prior_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.eligibility"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.eligibility"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        created_ref = self.store.store(
            self._output_artifact(base_ref=base_ref),
            "artifact.schema.json",
        ).reference
        result_ref = self.store.store(
            self._output_artifact(
                base_ref=base_ref,
                artifact_id="artifact.eligibility.modified-result",
                content_ref="artifact://eligibility/modified-result",
            ),
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
            "result_ref": result_ref,
        }

    def _store_evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str = "automated_tested",
    ) -> str:
        return self.store.store(
            self._evidence(
                evidence_id=evidence_id,
                subject_ref=subject_ref,
                state=state,
            ),
            "evidence-record.schema.json",
        ).reference

    def _submit_packet(
        self,
        context,
        *,
        created=None,
        modified=None,
        evidence_refs=(),
        packet_id: str = "packet.eligibility",
        uncertainties=None,
        failures_or_blockers=None,
        downstream_effects=None,
        requested_followup=None,
        changes=None,
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = (
            [context["created_ref"]] if created is None else list(created)
        )
        packet["artifacts_modified"] = [] if modified is None else list(modified)
        packet["evidence_refs"] = list(evidence_refs)
        if uncertainties is not None:
            packet["uncertainties"] = list(uncertainties)
        if failures_or_blockers is not None:
            packet["failures_or_blockers"] = list(failures_or_blockers)
        if downstream_effects is not None:
            packet["downstream_effects"] = list(downstream_effects)
        if requested_followup is not None:
            packet["requested_followup"] = list(requested_followup)
        if changes is not None:
            packet["changes"] = list(changes)
        return submit_return_packet(self.store, packet).packet_ref

    def _eligible_packet(self, context, *, packet_id="packet.eligibility.happy"):
        evidence_ref = self._store_evidence(
            evidence_id=f"evidence.{packet_id}",
            subject_ref=context["created_ref"],
        )
        return self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id=packet_id,
        )

    def test_exact_created_output_packet_is_eligible_candidate(self) -> None:
        context = self._ground_context()
        packet_ref = self._eligible_packet(context)

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertEqual(resolved.packet_ref, packet_ref)
        self.assertEqual(resolved.base_state_revision_ref, context["base_ref"])
        self.assertEqual(resolved.claim_ref, context["claim_ref"])
        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(resolved.created_output_refs, (context["created_ref"],))
        for forbidden in ("accepted", "closed", "integrated", "current"):
            self.assertFalse(hasattr(resolved, forbidden))

    def test_missing_required_evidence_is_not_eligible(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[],
            packet_id="packet.eligibility.missing-evidence",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(resolved.reasons[0].code, "required_subject_evidence_unsatisfied")

    def test_wrong_state_only_is_unsatisfied_not_promoted(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.wrong-state",
            subject_ref=context["created_ref"],
            state="invalidated",
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.wrong-state",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(resolved.reasons[0].observed_states, ("invalidated",))

    def test_required_plus_different_state_is_conflict_not_ranked(self) -> None:
        context = self._ground_context()
        pass_ref = self._store_evidence(
            evidence_id="evidence.eligibility.pass",
            subject_ref=context["created_ref"],
        )
        invalidated_ref = self._store_evidence(
            evidence_id="evidence.eligibility.invalidated",
            subject_ref=context["created_ref"],
            state="invalidated",
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[pass_ref, invalidated_ref],
            packet_id="packet.eligibility.conflict",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_CONFLICTING_SUBJECT_EVIDENCE,
        )
        self.assertEqual(resolved.reasons[0].code, "conflicting_subject_evidence_state")
        self.assertEqual(
            resolved.reasons[0].observed_states,
            ("automated_tested", "invalidated"),
        )

    def test_unmatched_evidence_cannot_satisfy_output(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.unmatched",
            subject_ref="artifact.eligibility.created",
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.unmatched",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(resolved.unmatched_evidence_refs, (evidence_ref,))

    def test_same_logical_id_different_exact_artifact_evidence_cannot_satisfy(self) -> None:
        context = self._ground_context()
        alternate_ref = self.store.store(
            self._output_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.eligibility.created",
                content_ref="artifact://eligibility/alternate-exact-instance",
            ),
            "artifact.schema.json",
        ).reference
        self.assertNotEqual(alternate_ref, context["created_ref"])
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.same-logical-other-exact",
            subject_ref=alternate_ref,
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.same-logical-other-exact",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(resolved.unmatched_evidence_refs, (evidence_ref,))

    def test_modified_packet_is_explicitly_outside_first_slice(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": context["result_ref"],
                }
            ],
            packet_id="packet.eligibility.modified",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(resolved.eligibility_outcome, UNSUPPORTED_MODIFIED_OUTPUT_SLICE)
        self.assertEqual(resolved.reasons[0].code, "modified_outputs_present")
        self.assertEqual(resolved.reasons[0].related_refs, (context["result_ref"],))

    def test_nonempty_exact_dependency_is_explicitly_unsupported(self) -> None:
        context = self._ground_context()
        dependent_ref = self.store.store(
            self._output_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.eligibility.with-dependency",
                content_ref="artifact://eligibility/with-dependency",
                schema_version="0.3",
                dependency_refs=[context["prior_ref"]],
            ),
            "artifact.schema.json",
        ).reference
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.with-dependency",
            subject_ref=dependent_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created=[dependent_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.with-dependency",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(resolved.eligibility_outcome, UNSUPPORTED_DEPENDENCY_POLICY)
        self.assertEqual(resolved.reasons[0].artifact_ref, dependent_ref)
        self.assertEqual(resolved.reasons[0].related_refs, (context["prior_ref"],))

    def test_producer_lane_mismatch_fails_through_existing_provenance_preflight(self) -> None:
        context = self._ground_context()
        mismatched_ref = self.store.store(
            self._output_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.eligibility.bad-producer",
                content_ref="artifact://eligibility/bad-producer",
                producer_lane_id="lane-01",
            ),
            "artifact.schema.json",
        ).reference
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.bad-producer",
            subject_ref=mismatched_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created=[mismatched_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.bad-producer",
        )

        with self.assertRaises(ArtifactProducerLaneMismatchError):
            preflight_packet_integration_eligibility(self.store, packet_ref)

    def test_packet_reported_uncertainty_failure_downstream_and_followup_remain_visible(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.eligibility.reported-facts",
            subject_ref=context["created_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.eligibility.reported-facts",
            uncertainties=["uncertainty remains open"],
            failures_or_blockers=["blocker remains visible"],
            downstream_effects=["downstream effect remains visible"],
            requested_followup=["follow up explicitly"],
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertEqual(
            resolved.packet_reported_facts.uncertainties,
            ("uncertainty remains open",),
        )
        self.assertEqual(
            resolved.packet_reported_facts.failures_or_blockers,
            ("blocker remains visible",),
        )
        self.assertEqual(
            resolved.packet_reported_facts.downstream_effects,
            ("downstream effect remains visible",),
        )
        self.assertEqual(
            resolved.packet_reported_facts.requested_followup,
            ("follow up explicitly",),
        )

    def test_repeated_identical_exact_input_returns_identical_named_fact(self) -> None:
        context = self._ground_context()
        packet_ref = self._eligible_packet(
            context,
            packet_id="packet.eligibility.repeatable",
        )

        first = preflight_packet_integration_eligibility(self.store, packet_ref)
        second = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(first, second)

    def test_evidence_array_order_and_packet_narrative_do_not_control_disposition(self) -> None:
        context = self._ground_context()
        first_evidence = self._store_evidence(
            evidence_id="evidence.eligibility.order-a",
            subject_ref=context["created_ref"],
        )
        second_evidence = self._store_evidence(
            evidence_id="evidence.eligibility.order-b",
            subject_ref=context["created_ref"],
        )
        first_packet = self._submit_packet(
            context,
            evidence_refs=[first_evidence, second_evidence],
            packet_id="packet.eligibility.order-a",
            changes=["actor/founder/schedule/CI/branch/Git narrative A"],
        )
        second_packet = self._submit_packet(
            context,
            evidence_refs=[second_evidence, first_evidence],
            packet_id="packet.eligibility.order-b",
            changes=["actor/founder/schedule/CI/branch/Git narrative B"],
        )

        first = preflight_packet_integration_eligibility(self.store, first_packet)
        second = preflight_packet_integration_eligibility(self.store, second_packet)

        self.assertEqual(
            first.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertEqual(first.eligibility_outcome, second.eligibility_outcome)
        self.assertEqual(first.reasons, second.reasons)

    def test_source_metadata_is_preserved_without_becoming_disposition_authority(self) -> None:
        context = self._ground_context()
        before = self.store.load(context["created_ref"], "artifact.schema.json")
        packet_ref = self._eligible_packet(
            context,
            packet_id="packet.eligibility.source-preservation",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)
        after = self.store.load(context["created_ref"], "artifact.schema.json")

        self.assertEqual(
            resolved.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertEqual(before, after)
        self.assertEqual(
            after["provenance"]["source_refs"],
            ["source://decision024/preserved"],
        )

    def test_empty_created_slice_is_not_eligible(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            created=[],
            evidence_refs=[],
            packet_id="packet.eligibility.no-created-output",
        )

        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)

        self.assertEqual(
            resolved.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(resolved.reasons[0].code, "created_output_required")


if __name__ == "__main__":
    unittest.main()
