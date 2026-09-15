from __future__ import annotations

import unittest
from unittest import mock

from axm_institution.integration_candidate_binding import (
    COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING,
    preflight_exact_stored_integration_candidate_binding,
)
from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
    preflight_packet_integration_eligibility,
)
from axm_institution.store import FilesystemObjectStore
from test_integration_candidate_binding import IntegrationCandidateBindingTests


class Decision026EligibilityRecomputationAdversarialTests(unittest.TestCase):
    """Lane 03 adjacent Decision 026 check after ADV-060-A/B repairs."""

    def setUp(self) -> None:
        self.fixture = IntegrationCandidateBindingTests(
            methodName="test_exact_stored_base_packet_and_accepted_receipt_bind_coherently"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_adv_060_c_canonical_presence_does_not_bind_caller_substituted_eligibility(self):
        """Decision 024 eligibility must be recomputed from the receipt-named exact bytes.

        The receipt names a real, canonically stored packet that is independently proven
        non-eligible because it carries no required subject evidence. A second packet in
        the same exact base/claim context is independently proven eligible.

        Only the supplied store instance's ``load`` dispatch is shadowed for the
        receipt-named packet so Decision 024 composition sees the eligible packet while
        the canonical base-class exact-load path still sees the actual non-eligible
        receipt packet. ADV-060-A/B repairs establish material presence, but material
        presence alone must not let caller-substituted bytes become the eligibility fact
        for that exact packet ref.

        A truthful Decision 026 preflight may fail closed or preserve the non-eligible
        canonical packet fact. It must not emit a coherent acceptance-candidate binding
        whose nested Decision 024 fact was computed from a different packet's bytes.
        """

        context = self.fixture._ground_context()
        eligible_packet_ref = self.fixture._submit_packet(
            context,
            with_evidence=True,
            packet_id="packet.decision026.adv060c.eligible-decoy",
        )
        real_packet_ref = self.fixture._submit_packet(
            context,
            with_evidence=False,
            packet_id="packet.decision026.adv060c.real-ineligible",
        )

        real_eligibility = preflight_packet_integration_eligibility(
            self.fixture.store,
            real_packet_ref,
        )
        decoy_eligibility = preflight_packet_integration_eligibility(
            self.fixture.store,
            eligible_packet_ref,
        )
        self.assertEqual(
            real_eligibility.eligibility_outcome,
            NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
        )
        self.assertEqual(
            decoy_eligibility.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )

        receipt = self.fixture._receipt(
            base_ref=context["base_ref"],
            packet_refs=[real_packet_ref],
        )
        store = self.fixture.store
        caller_shadow_used = False

        def substituted_load(reference: str, schema_name: str | None = None):
            nonlocal caller_shadow_used
            if reference == real_packet_ref:
                caller_shadow_used = True
                return FilesystemObjectStore.load(
                    store,
                    eligible_packet_ref,
                    schema_name,
                )
            return FilesystemObjectStore.load(store, reference, schema_name)

        with mock.patch.object(store, "load", side_effect=substituted_load):
            try:
                resolved = preflight_exact_stored_integration_candidate_binding(
                    store,
                    receipt,
                )
            except Exception:
                pass
            else:
                self.assertNotEqual(
                    resolved.candidate_binding_outcome,
                    COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING,
                    "canonical presence of the receipt packet must not bind a Decision 024 fact computed from caller-substituted packet bytes",
                )

        self.assertTrue(caller_shadow_used)
        canonical_packet = FilesystemObjectStore.load(
            store,
            real_packet_ref,
            "return-packet.schema.json",
        )
        self.assertEqual(
            canonical_packet["id"],
            "packet.decision026.adv060c.real-ineligible",
        )


if __name__ == "__main__":
    unittest.main()
