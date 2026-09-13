from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_dependency_context_membership import (
    preflight_dependency_context_membership,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class DependencyContextMembershipTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _historical_artifact(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        version: str = "0.1",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.1"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-decision-015",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _store_historical(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        version: str = "0.1",
    ) -> str:
        return self.store.store(
            self._historical_artifact(
                artifact_id=artifact_id,
                content_ref=content_ref,
                version=version,
            ),
            "artifact.schema.json",
        ).reference

    def _store_base(self, lane_ref: str, artifact_refs) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.dependency.context.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = list(artifact_refs)
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [
            "Decision 015 classifies exact dependency context without validity policy."
        ]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self, *, extra_base_artifact_refs=()):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self._store_historical(
            artifact_id="artifact.modified",
            content_ref="artifact://decision015/prior",
        )
        base_ref = self._store_base(
            lane_ref,
            [prior_ref, *extra_base_artifact_refs],
        )

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.dependency.context"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.dependency.context"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
        }

    def _store_output(
        self,
        context,
        *,
        artifact_id: str,
        content_ref: str,
        dependency_refs=(),
        version: str = "0.3",
        supersedes_ref: str | None = None,
        source_refs=(),
    ) -> str:
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.3"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": context["base_ref"],
            "source_refs": list(source_refs),
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = list(dependency_refs)
        if supersedes_ref is None:
            artifact.pop("supersedes_ref", None)
        else:
            artifact["supersedes_ref"] = supersedes_ref
        return self.store.store(artifact, "artifact.schema.json").reference

    def _store_evidence(self, *, evidence_id: str, subject_ref: str) -> str:
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 015 compatibility fixture evidence."
        return self.store.store(evidence, "evidence-record.schema.json").reference

    def _submit_packet(
        self,
        context,
        *,
        created_refs=(),
        modified_result_ref: str | None = None,
        evidence_refs=(),
        packet_id: str,
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = list(created_refs)
        packet["artifacts_modified"] = (
            []
            if modified_result_ref is None
            else [
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": modified_result_ref,
                }
            ]
        )
        packet["evidence_refs"] = list(evidence_refs)
        return submit_return_packet(self.store, packet).packet_ref

    def test_exact_dependency_member_of_claim_base_is_classified_by_exact_ref(self) -> None:
        dependency_ref = self._store_historical(
            artifact_id="artifact.base.dependency",
            content_ref="artifact://decision015/base-dependency",
        )
        context = self._ground_context(extra_base_artifact_refs=[dependency_ref])
        output_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.base",
            content_ref="artifact://decision015/consumer-base",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision015.base",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision015.base",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        fact = resolved.created_outputs[0].dependencies[0]

        self.assertEqual(fact.dependency.reference, dependency_ref)
        self.assertTrue(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)
        self.assertEqual(resolved.claim_base.reference, context["base_ref"])

    def test_same_logical_id_different_exact_ref_does_not_count_as_base_membership(self) -> None:
        base_ref = self._store_historical(
            artifact_id="artifact.same-logical",
            content_ref="artifact://decision015/base-version",
            version="0.1",
        )
        context = self._ground_context(extra_base_artifact_refs=[base_ref])
        exact_dependency_ref = self._store_historical(
            artifact_id="artifact.same-logical",
            content_ref="artifact://decision015/different-exact-version",
            version="9.9",
        )
        output_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.same-logical",
            content_ref="artifact://decision015/consumer-same-logical",
            dependency_refs=[exact_dependency_ref],
            supersedes_ref=base_ref,
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision015.same-logical",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision015.same-logical",
        )

        fact = preflight_dependency_context_membership(
            self.store, packet_ref
        ).created_outputs[0].dependencies[0]

        self.assertEqual(fact.dependency.reference, exact_dependency_ref)
        self.assertFalse(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)

    def test_created_output_dependency_is_classified_without_base_promotion(self) -> None:
        context = self._ground_context()
        producer_ref = self._store_output(
            context,
            artifact_id="artifact.packet.created.producer",
            content_ref="artifact://decision015/packet-created-producer",
        )
        consumer_ref = self._store_output(
            context,
            artifact_id="artifact.packet.created.consumer",
            content_ref="artifact://decision015/packet-created-consumer",
            dependency_refs=[producer_ref],
        )
        producer_evidence = self._store_evidence(
            evidence_id="evidence.decision015.created.producer",
            subject_ref=producer_ref,
        )
        consumer_evidence = self._store_evidence(
            evidence_id="evidence.decision015.created.consumer",
            subject_ref=consumer_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[consumer_ref, producer_ref],
            evidence_refs=[consumer_evidence, producer_evidence],
            packet_id="packet.decision015.created-output",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        consumer = next(
            item for item in resolved.created_outputs if item.artifact.reference == consumer_ref
        )
        fact = consumer.dependencies[0]

        self.assertFalse(fact.in_claim_base)
        self.assertTrue(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)

    def test_modified_result_dependency_is_classified_without_cross_family_laundering(self) -> None:
        context = self._ground_context()
        result_ref = self._store_output(
            context,
            artifact_id="artifact.packet.modified.producer",
            content_ref="artifact://decision015/packet-modified-producer",
        )
        consumer_ref = self._store_output(
            context,
            artifact_id="artifact.packet.modified.consumer",
            content_ref="artifact://decision015/packet-modified-consumer",
            dependency_refs=[result_ref],
        )
        result_evidence = self._store_evidence(
            evidence_id="evidence.decision015.modified.producer",
            subject_ref=result_ref,
        )
        consumer_evidence = self._store_evidence(
            evidence_id="evidence.decision015.modified.consumer",
            subject_ref=consumer_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[consumer_ref],
            modified_result_ref=result_ref,
            evidence_refs=[consumer_evidence, result_evidence],
            packet_id="packet.decision015.modified-result",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        fact = resolved.created_outputs[0].dependencies[0]

        self.assertFalse(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertTrue(fact.in_packet_modified_result)

    def test_exact_external_dependency_remains_explicit_without_validity_decision(self) -> None:
        context = self._ground_context()
        external_ref = self._store_historical(
            artifact_id="artifact.external.dependency",
            content_ref="artifact://decision015/external",
        )
        output_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.external",
            content_ref="artifact://decision015/consumer-external",
            dependency_refs=[external_ref],
            source_refs=[context["prior_ref"]],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision015.external",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision015.external",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        fact = resolved.created_outputs[0].dependencies[0]

        self.assertEqual(fact.dependency.reference, external_ref)
        self.assertFalse(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)
        for forbidden in (
            "dependencies_valid",
            "dependencies_closed",
            "accepted",
            "rejected",
            "complete",
            "closed",
            "satisfied",
        ):
            self.assertFalse(hasattr(resolved, forbidden))

    def test_same_exact_packet_target_can_preserve_both_output_family_facts(self) -> None:
        context = self._ground_context()
        shared_ref = self._store_output(
            context,
            artifact_id="artifact.packet.shared-output",
            content_ref="artifact://decision015/shared-output",
        )
        consumer_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.shared-output",
            content_ref="artifact://decision015/consumer-shared-output",
            dependency_refs=[shared_ref],
        )
        shared_evidence = self._store_evidence(
            evidence_id="evidence.decision015.shared-output",
            subject_ref=shared_ref,
        )
        consumer_evidence = self._store_evidence(
            evidence_id="evidence.decision015.shared-consumer",
            subject_ref=consumer_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[consumer_ref, shared_ref],
            modified_result_ref=shared_ref,
            evidence_refs=[consumer_evidence, shared_evidence],
            packet_id="packet.decision015.shared-contexts",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        consumer = next(
            item for item in resolved.created_outputs if item.artifact.reference == consumer_ref
        )
        fact = consumer.dependencies[0]

        self.assertFalse(fact.in_claim_base)
        self.assertTrue(fact.in_packet_created)
        self.assertTrue(fact.in_packet_modified_result)

    def test_empty_dependency_arrays_preserve_context_without_closure_claim(self) -> None:
        context = self._ground_context()
        output_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.empty",
            content_ref="artifact://decision015/consumer-empty",
            dependency_refs=[],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision015.empty",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision015.empty",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs[0].dependencies, ())
        self.assertEqual(resolved.modified_results, ())
        self.assertEqual(
            resolved.dependency_identity.created_outputs[0].artifact.reference,
            output_ref,
        )

    def test_dependency_order_does_not_change_each_exact_membership_fact(self) -> None:
        base_dependency_ref = self._store_historical(
            artifact_id="artifact.order.base",
            content_ref="artifact://decision015/order-base",
        )
        context = self._ground_context(extra_base_artifact_refs=[base_dependency_ref])
        external_ref = self._store_historical(
            artifact_id="artifact.order.external",
            content_ref="artifact://decision015/order-external",
        )
        output_ref = self._store_output(
            context,
            artifact_id="artifact.consumer.order",
            content_ref="artifact://decision015/consumer-order",
            dependency_refs=[external_ref, base_dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision015.order",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision015.order",
        )

        facts = preflight_dependency_context_membership(
            self.store, packet_ref
        ).created_outputs[0].dependencies
        by_ref = {fact.dependency.reference: fact for fact in facts}

        self.assertFalse(by_ref[external_ref].in_claim_base)
        self.assertTrue(by_ref[base_dependency_ref].in_claim_base)
        self.assertEqual(set(by_ref), {external_ref, base_dependency_ref})


if __name__ == "__main__":
    unittest.main()
