from __future__ import annotations

import copy
import unittest

from axm_institution.packet_modified_result_compatibility import (
    preflight_modified_result_compatibility,
)
import test_packet_modified_result_compatibility as base_tests


class ModifiedResultCompatibilityAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-045 continuity attacks for Decision 012 only."""

    def setUp(self) -> None:
        self.fixture = base_tests.ModifiedResultCompatibilityTests(
            methodName="test_exact_result_subject_evidence_satisfies_narrow_contract"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store

    def test_adv045_a_evidence_array_order_cannot_choose_compatibility_standing(self) -> None:
        context = self.fixture._ground_context()
        passing_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.order.pass",
            subject_ref=context["result_ref"],
            state="automated_tested",
        )
        conflicting_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.order.invalidated",
            subject_ref=context["result_ref"],
            state="invalidated",
        )

        first_packet = self.fixture._submit_packet(
            context,
            evidence_refs=[passing_ref, conflicting_ref],
            packet_id="packet.adv045.order.first",
        )
        second_packet = self.fixture._submit_packet(
            context,
            evidence_refs=[conflicting_ref, passing_ref],
            packet_id="packet.adv045.order.second",
        )

        first = preflight_modified_result_compatibility(self.store, first_packet).modified_results[0]
        second = preflight_modified_result_compatibility(self.store, second_packet).modified_results[0]

        self.assertTrue(first.satisfied)
        self.assertTrue(second.satisfied)
        self.assertEqual(
            {item.reference for item in first.subject_evidence},
            {passing_ref, conflicting_ref},
        )
        self.assertEqual(
            {item.reference for item in second.subject_evidence},
            {passing_ref, conflicting_ref},
        )
        self.assertEqual(
            tuple(item.reference for item in first.satisfying_evidence),
            (passing_ref,),
        )
        self.assertEqual(
            tuple(item.reference for item in second.satisfying_evidence),
            (passing_ref,),
        )

    def test_adv045_b_later_high_version_same_logical_decoy_gets_no_authority(self) -> None:
        context = self.fixture._ground_context()
        decoy = self.fixture._result_artifact(
            base_ref=context["base_ref"],
            artifact_id="artifact.modified.result",
            content_ref="artifact://modified/result-high-version-decoy",
        )
        decoy["version"] = "999.0"
        decoy["supersedes_ref"] = context["result_ref"]
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(decoy_ref, context["result_ref"])

        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.high-version-decoy",
            subject_ref=decoy_ref,
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.adv045.high-version-decoy",
        )

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())
        self.assertEqual(len(resolved.unmatched_evidence), 1)
        self.assertEqual(resolved.unmatched_evidence[0].subject_ref, decoy_ref)
        self.assertEqual(
            resolved.unmatched_evidence[0].reason,
            "exact_artifact_not_modified_result",
        )

    def test_adv045_c_supersedes_ref_cannot_turn_prior_evidence_into_result_evidence(self) -> None:
        context = self.fixture._ground_context()
        result = self.fixture._result_artifact(
            base_ref=context["base_ref"],
            artifact_id="artifact.modified.result.supersedes",
            content_ref="artifact://modified/result-supersedes-prior",
        )
        result["supersedes_ref"] = context["prior_ref"]
        context["result_ref"] = self.store.store(result, "artifact.schema.json").reference

        prior_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.prior-pass",
            subject_ref=context["prior_ref"],
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[prior_evidence_ref],
            packet_id="packet.adv045.supersedes-prior",
        )

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())
        self.assertEqual(len(resolved.unmatched_evidence), 1)
        self.assertEqual(resolved.unmatched_evidence[0].evidence.reference, prior_evidence_ref)

    def test_adv045_d_passing_prior_cannot_mask_invalidated_result_in_either_order(self) -> None:
        context = self.fixture._ground_context()
        prior_pass_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.prior-mask",
            subject_ref=context["prior_ref"],
            state="automated_tested",
        )
        result_invalidated_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.result-invalidated",
            subject_ref=context["result_ref"],
            state="invalidated",
        )

        for packet_id, evidence_refs in (
            ("packet.adv045.mask.prior-first", [prior_pass_ref, result_invalidated_ref]),
            ("packet.adv045.mask.result-first", [result_invalidated_ref, prior_pass_ref]),
        ):
            packet_ref = self.fixture._submit_packet(
                context,
                evidence_refs=evidence_refs,
                packet_id=packet_id,
            )
            resolved = preflight_modified_result_compatibility(self.store, packet_ref)
            result = resolved.modified_results[0]

            self.assertFalse(result.satisfied)
            self.assertEqual(
                tuple(item.reference for item in result.subject_evidence),
                (result_invalidated_ref,),
            )
            self.assertEqual(result.satisfying_evidence, ())
            self.assertEqual(
                {item.evidence.reference for item in resolved.unmatched_evidence},
                {prior_pass_ref},
            )

    def test_adv045_e_later_same_logical_lane_contract_cannot_rebind_claim_base(self) -> None:
        context = self.fixture._ground_context()

        later_lane = copy.deepcopy(context["lane"])
        later_lane["evidence_requirements"][0]["required_states"] = ["runtime_tested"]
        later_lane_ref = self.store.store(later_lane, "lane.schema.json").reference
        self.assertNotEqual(later_lane_ref, context["lane_ref"])

        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv045.claim-base-lane",
            subject_ref=context["result_ref"],
            state="automated_tested",
        )
        packet_ref = self.fixture._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.adv045.claim-base-lane",
        )

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)
        result = resolved.modified_results[0]

        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertNotEqual(resolved.lane_ref, later_lane_ref)
        self.assertEqual(result.required_state, "automated_tested")
        self.assertTrue(result.satisfied)


if __name__ == "__main__":
    unittest.main()
