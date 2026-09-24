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


class Decision026AdversarialContinuityTests(unittest.TestCase):
    """Lane 03 bounded adversarial checks for Decision 026 only."""

    def setUp(self) -> None:
        self.fixture = IntegrationCandidateBindingTests(
            methodName="test_exact_stored_base_packet_and_accepted_receipt_bind_coherently"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_adv_060_a_caller_load_success_cannot_forge_absent_base_materialization(self):
        """Caller-owned ``load`` dispatch must not forge exact base presence.

        Decision 026 requires the receipt base to be materially present through the
        immutable store's exact-load path. The receipt below names a well-formed exact
        base ref whose object is genuinely absent. A function-owned base-class load
        therefore raises ``ObjectNotFoundError``.

        The supplied store instance is otherwise the real ``FilesystemObjectStore``.
        Only that exact instance's ``load`` attribute is shadowed so the absent receipt
        base returns the bytes/value of a different, genuinely stored same-kind base.
        Packet loading and every other load delegate to the canonical base-class path.

        A truthful Decision 026 preflight may fail closed on the caller-owned dispatch,
        or independently exact-load the absent ref and propagate the canonical store
        failure. It must not emit a named fact with ``base_materialized=True`` for an
        exact ref the canonical store cannot load.
        """

        context, packet_ref = self.fixture._eligible_context_and_packet()
        store = self.fixture.store
        self.assertIs(type(store), FilesystemObjectStore)

        absent_base = self.fixture._absent_exact_variant(context["base_ref"])
        with self.assertRaises(ObjectNotFoundError):
            FilesystemObjectStore.load(
                store,
                absent_base,
                "state-revision.schema.json",
            )

        receipt = self.fixture._receipt(
            base_ref=absent_base,
            packet_refs=[packet_ref],
        )
        caller_shadow_used = False

        def forged_load(reference: str, schema_name: str | None = None):
            nonlocal caller_shadow_used
            if reference == absent_base:
                caller_shadow_used = True
                return FilesystemObjectStore.load(
                    store,
                    context["base_ref"],
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
                    resolved.base_materialized,
                    True,
                    "caller-shadowed load success must not forge material presence for an absent exact base",
                )

        self.assertTrue(caller_shadow_used)
        with self.assertRaises(ObjectNotFoundError):
            FilesystemObjectStore.load(
                store,
                absent_base,
                "state-revision.schema.json",
            )


if __name__ == "__main__":
    unittest.main()
