from __future__ import annotations

import json
import unittest

from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    PacketIntegrationEligibilityReason,
    PacketReportedFacts,
    ResolvedPacketIntegrationEligibility,
)


class Decision024EligibilityTransportAdversarialTests(unittest.TestCase):
    def test_adv059_a_named_fact_transport_must_not_silently_become_positional_array(self) -> None:
        """Ordinary JSON transport must fail closed or preserve the named fact surface.

        Decision 024 requires one deterministic *named* packet-level fact whose exact
        packet/base/claim/lane/output identities, outcome, reasons, and reported packet
        facts remain explicit. A positional JSON array silently discards those field
        names and makes reconstruction depend on hidden Python tuple ordering.

        Failing closed is acceptable. An explicit keyed transport is also acceptable.
        Silent sequence transport is not.
        """

        resolved = ResolvedPacketIntegrationEligibility(
            packet_ref="axmref:v1:return-packet:packet.adv059-a:-:sha256:" + "1" * 64,
            base_state_revision_ref=(
                "axmref:v1:state-revision:revision.adv059-a:-:sha256:" + "2" * 64
            ),
            claim_ref="axmref:v1:work-claim:claim.adv059-a:-:sha256:" + "3" * 64,
            lane_ref="axmref:v1:lane:lane-02:-:sha256:" + "4" * 64,
            created_output_refs=(
                "axmref:v1:artifact:artifact.adv059-a:-:sha256:" + "5" * 64,
            ),
            unmatched_evidence_refs=(),
            eligibility_outcome=ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
            reasons=(
                PacketIntegrationEligibilityReason(
                    code="first_slice_conditions_grounded",
                    artifact_ref=None,
                    required_state=None,
                    observed_states=(),
                    related_refs=(
                        "axmref:v1:artifact:artifact.adv059-a:-:sha256:" + "5" * 64,
                    ),
                ),
            ),
            packet_reported_facts=PacketReportedFacts(
                uncertainties=("explicit uncertainty",),
                failures_or_blockers=("explicit blocker",),
                downstream_effects=("explicit downstream effect",),
                requested_followup=("explicit followup",),
            ),
        )

        try:
            encoded = json.dumps(resolved)
        except TypeError:
            return

        transported = json.loads(encoded)
        self.assertIsInstance(
            transported,
            dict,
            "Decision 024 named eligibility fact silently serialized as an anonymous "
            "positional sequence; transport must fail closed or preserve field names",
        )
        self.assertEqual(
            transported.get("eligibility_outcome"),
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertIn("packet_ref", transported)
        self.assertIn("reasons", transported)
        self.assertIn("packet_reported_facts", transported)


if __name__ == "__main__":
    unittest.main()
