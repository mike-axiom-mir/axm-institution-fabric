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
        "content_ref": "tests/test_source_live_observation_adversarial_verifier_guard_drift.py",
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


class SourceLiveObservationVerifierGuardDriftAdversarialTests(unittest.TestCase):
    def test_adv_058_m_verifier_shadow_cannot_remove_guard_and_expose_path_shadow(self):
        """Verifier dispatch must not remove the guard needed by the base verifier path.

        ADV-058-L established that caller-owned ``load_bytes`` dispatch must not remove
        the invocation-local guard before the subsequent base load performs dynamic
        verifier lookup. The current L repair restores that guard after caller load
        dispatch. This adjacent fixture attacks the next verification-critical boundary.

        The declared target is absent from the supplied exact store and exists only in a
        separate decoy store. The supplied instance carries caller-owned
        ``_verify_existing`` and ``_object_path`` shadows. When the guarded verifier
        deliberately exercises the caller verifier shadow, that hook changes only
        ``source_store.__class__`` back to ``FilesystemObjectStore``. The subsequent
        explicit base verifier then resolves ``self._object_path`` after the guard class
        has disappeared, exposing the caller-owned path shadow, which redirects the read
        to the exact object in the decoy root.

        A bounded truthful observer may fail closed on verifier-stage guard drift or
        independently report context-local absence from the supplied store. It must not
        emit ``exact_observed`` by importing exact presence from another root after caller
        verifier dispatch removed the guard relied on by the base verifier.
        """

        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as decoy_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            decoy_store = FilesystemObjectStore(decoy_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            target_ref = decoy_store.store(target, "artifact.schema.json").reference
            source_path = FilesystemObjectStore._object_path(source_store, target_ref)
            decoy_path = FilesystemObjectStore._object_path(decoy_store, target_ref)
            self.assertFalse(source_path.exists())
            self.assertTrue(decoy_path.exists())

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = decoy_store.store(container, "artifact.schema.json").reference
            verifier_shadow_called = False
            path_shadow_called = False

            def remove_guard_in_verifier(reference: str, schema_name: str):
                nonlocal verifier_shadow_called
                verifier_shadow_called = True
                self.assertEqual(reference, target_ref)
                source_store.__class__ = FilesystemObjectStore
                return ({}, b"caller-verifier-result-is-not-authority")

            def redirect_path_after_guard_removal(reference: str):
                nonlocal path_shadow_called
                path_shadow_called = True
                self.assertEqual(reference, target_ref)
                return decoy_path

            with mock.patch.object(
                source_store,
                "_verify_existing",
                side_effect=remove_guard_in_verifier,
            ), mock.patch.object(
                source_store,
                "_object_path",
                side_effect=redirect_path_after_guard_removal,
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
                        "caller-owned verifier dispatch must not remove the invocation guard and expose caller-owned path authority",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(verifier_shadow_called)
            self.assertTrue(path_shadow_called)
            self.assertFalse(source_path.exists())
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
