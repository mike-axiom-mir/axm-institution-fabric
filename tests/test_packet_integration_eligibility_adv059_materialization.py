from __future__ import annotations

import json
import unittest
from dataclasses import asdict

from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    PacketIntegrationEligibilityReason,
    PacketReportedFacts,
    ResolvedPacketIntegrationEligibility,
)


class Decision024EligibilityMaterializationAdversarialTests(unittest.TestCase):
    def test_adv059_b_nested_named_facts_must_survive_standard_dataclass_materialization(self) -> None:
        """A keyed top-level materialization must not hide nested fact field identity.

        The ADV-059-A repair makes direct ``json.dumps(resolved)`` fail closed, but the
        repaired result is now a dataclass and therefore naturally admits stdlib
        ``dataclasses.asdict`` materialization. Decision 024 requires deterministic named
        reason facts and preserved packet-reported facts. If that keyed top-level
        materialization is then transported as JSON, nested facts must either retain
        their names or transport must fail closed; positional arrays that require hidden
        Python NamedTuple field order are not a reconstructable institutional fact.
        """

        resolved = ResolvedPacketIntegrationEligibility(
            packet_ref="axmref:v1:return-packet:packet.adv059-b:-:sha256:" + "1" * 64,
            base_state_revision_ref=(
                "axmref:v1:state-revision:revision.adv059-b:-:sha256:" + "2" * 64
            ),
            claim_ref="axmref:v1:work-claim:claim.adv059-b:-:sha256:" + "3" * 64,
            lane_ref="axmref:v1:lane:lane-02:-:sha256:" + "4" * 64,
            created_output_refs=(
                "axmref:v1:artifact:artifact.adv059-b:-:sha256:" + "5" * 64,
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
                        "axmref:v1:artifact:artifact.adv059-b:-:sha256:" + "5" * 64,
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
            encoded = json.dumps(asdict(resolved))
        except TypeError:
            return

        transported = json.loads(encoded)
        self.assertIsInstance(transported, dict)
        self.assertEqual(
            transported.get("eligibility_outcome"),
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )

        reasons = transported.get("reasons")
        self.assertTrue(reasons, "materialized Decision 024 fact lost its reason facts")
        self.assertIsInstance(
            reasons[0],
            dict,
            "Decision 024 reason fact silently became a positional array after standard "
            "dataclass materialization + JSON transport; nested reason names must be "
            "preserved or transport must fail closed",
        )
        self.assertIn("code", reasons[0])
        self.assertIn("related_refs", reasons[0])

        reported = transported.get("packet_reported_facts")
        self.assertIsInstance(
            reported,
            dict,
            "Decision 024 packet-reported facts silently became a positional array after "
            "standard dataclass materialization + JSON transport; field names must be "
            "preserved or transport must fail closed",
        )
        self.assertIn("uncertainties", reported)
        self.assertIn("failures_or_blockers", reported)
        self.assertIn("downstream_effects", reported)
        self.assertIn("requested_followup", reported)


if __name__ == "__main__":
    unittest.main()
