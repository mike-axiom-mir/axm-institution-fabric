from __future__ import annotations

import copy
import json
import unittest

from axm_institution.packet_mixed_compatibility import preflight_mixed_packet_compatibility
import test_packet_mixed_compatibility as base_tests


class MixedPacketCompatibilityAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-046 continuity attacks for Decision 013 only."""

    def setUp(self) -> None:
        self.fixture = base_tests.MixedPacketCompatibilityTests(
            methodName="test_mixed_packet_projects_both_output_families_from_one_exact_context"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store

    def test_adv046_a_later_same_logical_lane_cannot_rebind_either_output_family(self) -> None:
        context = self.fixture._ground_context()

        later_lane = copy.deepcopy(context["lane"])
        later_lane["evidence_requirements"][0]["required_states"] = ["runtime_tested"]
        later_lane_ref = self.store.store(later_lane, "lane.schema.json").reference
        self.assertNotEqual(later_lane_ref, context["lane_ref"])

        created_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.claim-base-created",
            subject_ref=context["created_ref"],
            state="automated_tested",
        )
        result_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.claim-base-result",
            subject_ref=context["result_ref"],
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[created_evidence_ref, result_evidence_ref],
            packet_id="packet.adv046.claim-base-lane",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertNotEqual(resolved.lane_ref, later_lane_ref)
        self.assertEqual(resolved.created_outputs[0].required_state, "automated_tested")
        self.assertEqual(resolved.modified_results[0].required_state, "automated_tested")
        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertTrue(resolved.modified_results[0].satisfied)

    def test_adv046_b_high_version_superseding_same_logical_created_decoy_stays_separate(self) -> None:
        context = self.fixture._ground_context()
        decoy = self.fixture._output_artifact(
            base_ref=context["base_ref"],
            artifact_id="artifact.modified.result",
            content_ref="artifact://mixed/adv046-high-version-created-decoy",
        )
        decoy["version"] = "999.0"
        decoy["supersedes_ref"] = context["result_ref"]
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(decoy_ref, context["result_ref"])

        decoy_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.high-version-created-decoy",
            subject_ref=decoy_ref,
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created=[decoy_ref],
            evidence_refs=[decoy_evidence_ref],
            packet_id="packet.adv046.high-version-created-decoy",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs[0].artifact.reference, decoy_ref)
        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertEqual(
            resolved.modified_results[0].modification.result_artifact.reference,
            context["result_ref"],
        )
        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())

    def test_adv046_c_evidence_order_cannot_erase_conflict_or_unmatched_state(self) -> None:
        context = self.fixture._ground_context()
        refs = [
            self.fixture._store_evidence(
                evidence_id="evidence.adv046.created-pass",
                subject_ref=context["created_ref"],
                state="automated_tested",
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv046.created-invalidated",
                subject_ref=context["created_ref"],
                state="invalidated",
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv046.result-pass",
                subject_ref=context["result_ref"],
                state="automated_tested",
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv046.result-invalidated",
                subject_ref=context["result_ref"],
                state="invalidated",
            ),
            self.fixture._store_evidence(
                evidence_id="evidence.adv046.prior-unmatched",
                subject_ref=context["prior_ref"],
                state="automated_tested",
            ),
        ]

        first_ref = self.fixture._submit_packet(
            context,
            evidence_refs=refs,
            packet_id="packet.adv046.order-forward",
        )
        reverse_ref = self.fixture._submit_packet(
            context,
            evidence_refs=list(reversed(refs)),
            packet_id="packet.adv046.order-reverse",
        )

        first = preflight_mixed_packet_compatibility(self.store, first_ref)
        reverse = preflight_mixed_packet_compatibility(self.store, reverse_ref)

        for resolved in (first, reverse):
            self.assertTrue(resolved.created_outputs[0].satisfied)
            self.assertTrue(resolved.modified_results[0].satisfied)
            self.assertEqual(
                {item.value.get("state") for item in resolved.created_bindings[0].evidence_records},
                {"automated_tested", "invalidated"},
            )
            self.assertEqual(
                {item.value.get("state") for item in resolved.modified_results[0].subject_evidence},
                {"automated_tested", "invalidated"},
            )
            self.assertEqual(
                {item.evidence.reference for item in resolved.unmatched_evidence},
                {refs[-1]},
            )

    def test_adv046_d_materialized_composite_copies_cannot_mutate_exact_operational_facts(self) -> None:
        context = self.fixture._ground_context()
        created_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.materialize-created",
            subject_ref=context["created_ref"],
        )
        result_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.materialize-result",
            subject_ref=context["result_ref"],
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[created_evidence_ref, result_evidence_ref],
            packet_id="packet.adv046.materialize",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)
        outer_copy = resolved._asdict()
        created_value_copy = dict(resolved.created_outputs[0].artifact.value)
        created_evidence_copy = dict(resolved.created_bindings[0].evidence_records[0].value)
        result_value_copy = dict(
            resolved.modified_results[0].modification.result_artifact.value
        )
        result_evidence_copy = dict(resolved.modified_results[0].subject_evidence[0].value)

        outer_copy["lane_ref"] = "decoy-lane"
        created_value_copy["type"] = "decoy-created-type"
        created_evidence_copy["state"] = "invalidated"
        result_value_copy["type"] = "decoy-result-type"
        result_evidence_copy["state"] = "invalidated"

        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(resolved.created_outputs[0].artifact.value.get("type"), "kernel_contracts")
        self.assertEqual(
            resolved.created_bindings[0].evidence_records[0].value.get("state"),
            "automated_tested",
        )
        self.assertEqual(
            resolved.modified_results[0].modification.result_artifact.value.get("type"),
            "kernel_contracts",
        )
        self.assertEqual(
            resolved.modified_results[0].subject_evidence[0].value.get("state"),
            "automated_tested",
        )

    def test_adv046_e_ordinary_json_transport_of_composite_fails_closed(self) -> None:
        context = self.fixture._ground_context()
        created_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.transport-created",
            subject_ref=context["created_ref"],
        )
        result_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.transport-result",
            subject_ref=context["result_ref"],
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[created_evidence_ref, result_evidence_ref],
            packet_id="packet.adv046.transport",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        with self.assertRaises(TypeError):
            json.dumps(resolved)
        with self.assertRaises(TypeError):
            json.dumps(resolved._asdict())

    def test_adv046_f_unsatisfied_component_remains_fact_not_packet_rejection(self) -> None:
        context = self.fixture._ground_context()
        result_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv046.only-result-satisfied",
            subject_ref=context["result_ref"],
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[result_evidence_ref],
            packet_id="packet.adv046.component-facts-only",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.created_outputs[0].satisfied)
        self.assertTrue(resolved.modified_results[0].satisfied)
        for forbidden in ("accepted", "rejected", "complete", "closed", "satisfied"):
            self.assertFalse(hasattr(resolved, forbidden))


if __name__ == "__main__":
    unittest.main()
