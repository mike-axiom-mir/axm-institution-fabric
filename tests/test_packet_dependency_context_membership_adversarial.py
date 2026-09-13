from __future__ import annotations

import json
import unittest

from axm_institution.packet_dependency_context_membership import (
    preflight_dependency_context_membership,
)
from axm_institution.store import ObjectStoreError
import test_packet_dependency_context_membership as base_tests


class DependencyContextMembershipAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-048 continuity attacks for Decision 015 only."""

    def setUp(self) -> None:
        self.fixture = base_tests.DependencyContextMembershipTests(
            methodName="test_exact_dependency_member_of_claim_base_is_classified_by_exact_ref"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store

    def _submit_created_consumer(
        self,
        context,
        *,
        dependency_refs,
        packet_id: str,
        artifact_id: str,
        content_ref: str,
        source_refs=(),
    ):
        output_ref = self.fixture._store_output(
            context,
            artifact_id=artifact_id,
            content_ref=content_ref,
            dependency_refs=dependency_refs,
            source_refs=source_refs,
        )
        evidence_ref = self.fixture._store_evidence(
            evidence_id=f"evidence.{packet_id}",
            subject_ref=output_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id=packet_id,
        )
        return output_ref, packet_ref

    def test_adv048_a_stale_exact_claim_base_survives_later_same_logical_revision(self) -> None:
        base_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.stale-base-member",
            content_ref="artifact://adv048/stale-base-member",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        _, packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[base_dependency_ref],
            packet_id="packet.adv048.stale-base",
            artifact_id="artifact.adv048.stale-base-consumer",
            content_ref="artifact://adv048/stale-base-consumer",
        )

        later_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.later-base-member",
            content_ref="artifact://adv048/later-base-member",
        )
        later_base_ref = self.fixture._store_base(
            context["lane_ref"], [later_dependency_ref]
        )
        self.assertNotEqual(later_base_ref, context["base_ref"])

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        fact = resolved.created_outputs[0].dependencies[0]

        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(resolved.claim_base.reference, context["base_ref"])
        self.assertTrue(fact.in_claim_base)
        self.assertEqual(fact.dependency.reference, base_dependency_ref)
        self.assertNotEqual(resolved.claim_base.reference, later_base_ref)

    def test_adv048_b_version_supersedes_and_recency_cannot_promote_same_logical_decoy(self) -> None:
        exact_base_member_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.same-logical",
            content_ref="artifact://adv048/base-member",
            version="0.1",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[exact_base_member_ref]
        )

        decoy = self.fixture._historical_artifact(
            artifact_id="artifact.adv048.same-logical",
            content_ref="artifact://adv048/later-decoy",
            version="999.0",
        )
        decoy["supersedes_ref"] = exact_base_member_ref
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(decoy_ref, exact_base_member_ref)

        _, packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[decoy_ref],
            packet_id="packet.adv048.version-decoy",
            artifact_id="artifact.adv048.version-decoy-consumer",
            content_ref="artifact://adv048/version-decoy-consumer",
        )

        fact = preflight_dependency_context_membership(
            self.store, packet_ref
        ).created_outputs[0].dependencies[0]

        self.assertEqual(fact.dependency.reference, decoy_ref)
        self.assertFalse(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)

    def test_adv048_c_base_and_dependency_array_order_do_not_create_precedence(self) -> None:
        first_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.order.first",
            content_ref="artifact://adv048/order-first",
        )
        second_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.order.second",
            content_ref="artifact://adv048/order-second",
        )

        context_ab = self.fixture._ground_context(
            extra_base_artifact_refs=[first_ref, second_ref]
        )
        _, packet_ab = self._submit_created_consumer(
            context_ab,
            dependency_refs=[second_ref, first_ref],
            packet_id="packet.adv048.order-ab",
            artifact_id="artifact.adv048.order-consumer-ab",
            content_ref="artifact://adv048/order-consumer-ab",
        )
        facts_ab = {
            item.dependency.reference: item
            for item in preflight_dependency_context_membership(
                self.store, packet_ab
            ).created_outputs[0].dependencies
        }

        context_ba = self.fixture._ground_context(
            extra_base_artifact_refs=[second_ref, first_ref]
        )
        _, packet_ba = self._submit_created_consumer(
            context_ba,
            dependency_refs=[first_ref, second_ref],
            packet_id="packet.adv048.order-ba",
            artifact_id="artifact.adv048.order-consumer-ba",
            content_ref="artifact://adv048/order-consumer-ba",
        )
        facts_ba = {
            item.dependency.reference: item
            for item in preflight_dependency_context_membership(
                self.store, packet_ba
            ).created_outputs[0].dependencies
        }

        self.assertEqual(set(facts_ab), {first_ref, second_ref})
        self.assertEqual(set(facts_ba), {first_ref, second_ref})
        self.assertTrue(all(item.in_claim_base for item in facts_ab.values()))
        self.assertTrue(all(item.in_claim_base for item in facts_ba.values()))

    def test_adv048_d_same_logical_created_decoy_cannot_cross_launder_modified_result(self) -> None:
        context = self.fixture._ground_context()
        created_decoy_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv048.cross-family",
            content_ref="artifact://adv048/cross-family-created",
        )
        modified_target_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv048.cross-family",
            content_ref="artifact://adv048/cross-family-modified",
        )
        self.assertNotEqual(created_decoy_ref, modified_target_ref)
        consumer_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv048.cross-family-consumer",
            content_ref="artifact://adv048/cross-family-consumer",
            dependency_refs=[modified_target_ref],
        )

        evidence_refs = [
            self.fixture._store_evidence(
                evidence_id="evidence.adv048.cross-family-created",
                subject_ref=created_decoy_ref,
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv048.cross-family-modified",
                subject_ref=modified_target_ref,
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv048.cross-family-consumer",
                subject_ref=consumer_ref,
            ),
        ]
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[consumer_ref, created_decoy_ref],
            modified_result_ref=modified_target_ref,
            evidence_refs=evidence_refs,
            packet_id="packet.adv048.cross-family",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        consumer = next(
            item
            for item in resolved.created_outputs
            if item.artifact.reference == consumer_ref
        )
        fact = consumer.dependencies[0]

        self.assertEqual(fact.dependency.reference, modified_target_ref)
        self.assertFalse(fact.in_packet_created)
        self.assertTrue(fact.in_packet_modified_result)
        self.assertFalse(fact.in_claim_base)

    def test_adv048_e_source_and_evidence_metadata_cannot_promote_external_dependency(self) -> None:
        base_member_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.metadata-base",
            content_ref="artifact://adv048/metadata-base",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_member_ref]
        )
        external_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.metadata-external",
            content_ref="artifact://adv048/metadata-external",
        )
        metadata_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv048.metadata-external",
            subject_ref=external_ref,
        )

        artifact = self.fixture._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.3"
        artifact["id"] = "artifact.adv048.metadata-consumer"
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.3"
        artifact["content_ref"] = "artifact://adv048/metadata-consumer"
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": context["base_ref"],
            "source_refs": [external_ref, base_member_ref],
        }
        artifact["evidence_refs"] = [metadata_evidence_ref]
        artifact["dependency_refs"] = [external_ref]
        artifact.pop("supersedes_ref", None)
        output_ref = self.store.store(artifact, "artifact.schema.json").reference
        packet_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv048.metadata-consumer",
            subject_ref=output_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[packet_evidence_ref],
            packet_id="packet.adv048.metadata",
        )

        fact = preflight_dependency_context_membership(
            self.store, packet_ref
        ).created_outputs[0].dependencies[0]

        self.assertEqual(fact.dependency.reference, external_ref)
        self.assertFalse(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)

    def test_adv048_f_corrupt_exact_claim_base_fails_closed(self) -> None:
        base_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.corrupt-base-member",
            content_ref="artifact://adv048/corrupt-base-member",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        _, packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[base_dependency_ref],
            packet_id="packet.adv048.corrupt-base",
            artifact_id="artifact.adv048.corrupt-base-consumer",
            content_ref="artifact://adv048/corrupt-base-consumer",
        )
        self.store._object_path(context["base_ref"]).write_text("{}", encoding="utf-8")

        with self.assertRaises(ObjectStoreError):
            preflight_dependency_context_membership(self.store, packet_ref)

    def test_adv048_g_missing_exact_claim_base_fails_closed(self) -> None:
        base_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.missing-base-member",
            content_ref="artifact://adv048/missing-base-member",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        _, packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[base_dependency_ref],
            packet_id="packet.adv048.missing-base",
            artifact_id="artifact.adv048.missing-base-consumer",
            content_ref="artifact://adv048/missing-base-consumer",
        )
        self.store._object_path(context["base_ref"]).unlink()

        with self.assertRaises(ObjectStoreError):
            preflight_dependency_context_membership(self.store, packet_ref)

    def test_adv048_h_later_parallel_packet_cannot_rebind_exact_packet_context(self) -> None:
        base_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.parallel-base",
            content_ref="artifact://adv048/parallel-base",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        _, first_packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[base_dependency_ref],
            packet_id="packet.adv048.parallel-first",
            artifact_id="artifact.adv048.parallel-first",
            content_ref="artifact://adv048/parallel-first",
        )

        external_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.parallel-external",
            content_ref="artifact://adv048/parallel-external",
        )
        _, second_packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[external_ref],
            packet_id="packet.adv048.parallel-second",
            artifact_id="artifact.adv048.parallel-second",
            content_ref="artifact://adv048/parallel-second",
        )

        first = preflight_dependency_context_membership(self.store, first_packet_ref)
        second = preflight_dependency_context_membership(self.store, second_packet_ref)

        self.assertEqual(first.packet_ref, first_packet_ref)
        self.assertEqual(second.packet_ref, second_packet_ref)
        self.assertTrue(first.created_outputs[0].dependencies[0].in_claim_base)
        self.assertFalse(second.created_outputs[0].dependencies[0].in_claim_base)
        self.assertNotEqual(
            first.created_outputs[0].artifact.reference,
            second.created_outputs[0].artifact.reference,
        )

    def test_adv048_i_materialization_transport_and_authority_boundaries_remain_explicit(self) -> None:
        base_dependency_ref = self.fixture._store_historical(
            artifact_id="artifact.adv048.materialize-base",
            content_ref="artifact://adv048/materialize-base",
        )
        context = self.fixture._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        output_ref, packet_ref = self._submit_created_consumer(
            context,
            dependency_refs=[base_dependency_ref],
            packet_id="packet.adv048.materialize",
            artifact_id="artifact.adv048.materialize-consumer",
            content_ref="artifact://adv048/materialize-consumer",
        )

        resolved = preflight_dependency_context_membership(self.store, packet_ref)
        output = resolved.created_outputs[0]
        fact = output.dependencies[0]
        outer_copy = resolved._asdict()
        output_copy = output._asdict()
        fact_copy = fact._asdict()
        dependency_value_copy = dict(fact.dependency.value)

        outer_copy["claim_base_ref"] = "state-revision:decoy"
        output_copy["category"] = "modified_result"
        fact_copy["in_claim_base"] = False
        fact_copy["in_packet_created"] = True
        dependency_value_copy["content_ref"] = "artifact://adv048/mutated"

        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(output.category, "created")
        self.assertEqual(output.artifact.reference, output_ref)
        self.assertTrue(fact.in_claim_base)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)
        self.assertEqual(
            fact.dependency.value.get("content_ref"),
            "artifact://adv048/materialize-base",
        )

        with self.assertRaises(TypeError):
            json.dumps(resolved)
        with self.assertRaises(TypeError):
            json.dumps(resolved._asdict())

        for target in (resolved, fact):
            for forbidden in (
                "dependencies_valid",
                "dependencies_closed",
                "accepted",
                "rejected",
                "complete",
                "closed",
                "satisfied",
            ):
                self.assertFalse(hasattr(target, forbidden))


if __name__ == "__main__":
    unittest.main()
