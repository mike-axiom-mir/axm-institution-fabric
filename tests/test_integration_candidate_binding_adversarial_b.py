from __future__ import annotations

import unittest
from unittest import mock

from axm_institution.integration_candidate_binding import (
    preflight_exact_stored_integration_candidate_binding,
)
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectNotFoundError,
    ObjectStoreError,
)
from test_integration_candidate_binding import IntegrationCandidateBindingTests


class Decision026PacketMaterializationAdversarialTests(unittest.TestCase):
    """Lane 03 bounded adjacent adversarial check after ADV-060-A repair."""

    def setUp(self) -> None:
        self.fixture = IntegrationCandidateBindingTests(
            methodName="test_exact_stored_base_packet_and_accepted_receipt_bind_coherently"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_adv_060_b_caller_load_success_cannot_forge_absent_packet_materialization(self):
        """Caller-owned ``load`` dispatch must not forge exact packet presence.

        ADV-060-A established this boundary for the receipt base. This adjacent check
        stays inside the same Decision 026 materialization fact: the receipt below names
        a well-formed exact packet ref whose object is genuinely absent under the
        canonical ``FilesystemObjectStore.load(...)`` path.

        Only the supplied store instance's ``load`` attribute is shadowed so requests
        for that absent receipt packet return the value of a different genuinely stored
        eligible packet. Every other load delegates to the canonical base-class path.

        A truthful Decision 026 preflight may fail closed on the caller-owned dispatch,
        or independently exact-load the absent packet and propagate the canonical store
        failure. It must not emit ``packet_materialized=True`` for an exact ref the
        canonical store cannot load merely because the caller-controlled dispatch and
        downstream eligibility composition can operate on substituted packet content.
        """

        context, real_packet_ref = self.fixture._eligible_context_and_packet()
        store = self.fixture.store
        self.assertIs(type(store), FilesystemObjectStore)

        absent_packet = self.fixture._absent_exact_variant(real_packet_ref)
        with self.assertRaises(ObjectNotFoundError):
            FilesystemObjectStore.load(
                store,
                absent_packet,
                "return-packet.schema.json",
            )

        receipt = self.fixture._receipt(
            base_ref=context["base_ref"],
            packet_refs=[absent_packet],
        )
        caller_shadow_used = False

        def forged_load(reference: str, schema_name: str | None = None):
            nonlocal caller_shadow_used
            if reference == absent_packet:
                caller_shadow_used = True
                return FilesystemObjectStore.load(
                    store,
                    real_packet_ref,
                    schema_name,
                )
            return FilesystemObjectStore.load(store, reference, schema_name)

        with mock.patch.object(store, "load", side_effect=forged_load):
            try:
                resolved = preflight_exact_stored_integration_candidate_binding(
                    store,
                    receipt,
                )
            except ObjectStoreError:
                pass
            else:
                self.assertIsNot(
                    resolved.packet_materialized,
                    True,
                    "caller-shadowed load success must not forge material presence for an absent exact packet",
                )

        self.assertTrue(caller_shadow_used)
        with self.assertRaises(ObjectNotFoundError):
            FilesystemObjectStore.load(
                store,
                absent_packet,
                "return-packet.schema.json",
            )


if __name__ == "__main__":
    unittest.main()
