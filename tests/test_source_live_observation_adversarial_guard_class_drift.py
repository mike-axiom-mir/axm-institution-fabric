from __future__ import annotations

import tempfile
import unittest
from unittest import mock

from axm_institution.source_live_observation import (
    SourceLiveObservationError,
    observe_exact_source_live,
)
from axm_institution.store import FilesystemObjectStore


BASE_REF = (
    "axmref:v1:state-revision:revision.observation-base:-:sha256:" + "c" * 64
)


def exact_declaration(target_ref: str) -> dict:
    return {"source_class": "exact_axm_object", "object_ref": target_ref}


def typed_artifact(
    declarations: dict,
    *,
    artifact_id: str = "artifact.observation-container",
    version: str = "1",
) -> dict:
    return {
        "schema_version": "0.4",
        "id": artifact_id,
        "type": "source_live_observation_adversarial_fixture",
        "version": version,
        "content_ref": "tests/test_source_live_observation_adversarial_guard_class_drift.py",
        "provenance": {
            "producer_lane_id": "lane-03",
            "base_state_revision_ref": BASE_REF,
            "source_declarations": declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def target_artifact() -> dict:
    return typed_artifact({}, artifact_id="artifact.observed-target")


class SourceLiveObservationGuardClassDriftAdversarialTests(unittest.TestCase):
    def test_adv_058_l_load_shadow_cannot_remove_invocation_guard_and_expose_forged_verifier(self):
        """Caller dispatch must not be able to remove the guard that grounds verification.

        Decision 023 currently installs an invocation-local ``FilesystemObjectStore``
        subclass whose data descriptors prevent caller-owned ``load_bytes``,
        ``_verify_existing``, ``_object_path``, schema, and location state from becoming
        source-truth authority. The guarded ``load_bytes`` descriptor intentionally calls
        a pre-existing exact-instance ``load_bytes`` shadow first, then invokes the base
        loader so the base path independently decides.

        This fixture keeps the declared target absent from the supplied store. The exact
        instance carries both a caller-owned ``load_bytes`` shadow and a caller-owned
        ``_verify_existing`` shadow. The load shadow does not return bytes as evidence;
        instead, while the observer deliberately executes it, it changes only
        ``source_store.__class__`` back to ``FilesystemObjectStore``. The subsequent
        explicit base ``FilesystemObjectStore.load_bytes(self, ...)`` then performs its
        internal verifier lookup through ``self._verify_existing`` after the guard class
        has been removed, exposing the caller-owned verifier shadow. That shadow can
        return arbitrary bytes without reading the exact object path or reproducing the
        immutable identity.

        A truthful bounded observer may fail closed on invocation-guard drift or report
        context-local absence from an independently grounded base read. It must not emit
        ``exact_observed`` after caller-owned dispatch removed the guard that made the
        later verification path independent.
        """

        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as decoy_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            decoy_store = FilesystemObjectStore(decoy_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            stored = decoy_store.store(target, "artifact.schema.json")
            target_ref = stored.reference
            actual_source_path = FilesystemObjectStore._object_path(source_store, target_ref)
            self.assertFalse(actual_source_path.exists())

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = decoy_store.store(container, "artifact.schema.json").reference
            load_shadow_called = False
            verifier_shadow_called = False

            def remove_invocation_guard(reference: str, schema_name: str | None = None) -> bytes:
                nonlocal load_shadow_called
                load_shadow_called = True
                self.assertEqual(reference, target_ref)
                source_store.__class__ = FilesystemObjectStore
                return b"caller-load-result-is-not-authority"

            def forge_verification(reference: str, schema_name: str):
                nonlocal verifier_shadow_called
                verifier_shadow_called = True
                self.assertEqual(reference, target_ref)
                return ({}, b"caller-forged-unverified-bytes")

            with mock.patch.object(
                source_store,
                "load_bytes",
                side_effect=remove_invocation_guard,
            ), mock.patch.object(
                source_store,
                "_verify_existing",
                side_effect=forge_verification,
            ):
                try:
                    fact = observe_exact_source_live(
                        containing_object_ref=container_ref,
                        containing_value=container,
                        declaration_key="source",
                        store=source_store,
                    )
                except SourceLiveObservationError:
                    pass
                else:
                    self.assertEqual(
                        "not_found_in_live_context",
                        fact.observation_outcome,
                        "caller-owned load dispatch must not remove the invocation guard and expose caller-owned verifier authority",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(load_shadow_called)
            self.assertTrue(verifier_shadow_called)
            self.assertFalse(actual_source_path.exists())
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
