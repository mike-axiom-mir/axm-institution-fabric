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
        "content_ref": "tests/test_source_live_observation_adversarial_path_dispatch.py",
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


class SourceLiveObservationPathDispatchAdversarialTests(unittest.TestCase):
    def test_adv_058_g_exact_instance_object_path_shadow_cannot_import_external_presence(self):
        """Exact observation must remain grounded in the supplied store's actual root.

        ADV-058-F established that caller-owned ``_verify_existing`` dispatch cannot by
        itself prove ``exact_observed``. The bounded repair now reaches
        ``FilesystemObjectStore._verify_existing(self, ...)`` directly. That base verifier,
        however, still discovers the object through ``self._object_path(reference)``.
        ``_object_path`` is an ordinary method and an exact accepted store instance may
        carry a caller-owned instance shadow for it.

        This fixture keeps the accepted exact store type, leaves ``load_bytes``,
        ``_verify_existing``, and ``schema_dir`` untouched, and keeps the declared target
        absent from the supplied live store. A separate decoy store contains the exact
        canonical target bytes. Only the supplied store's ``_object_path`` is shadowed so
        the base verifier is redirected to that external exact file. Schema/canonical/
        immutable-reference checks can all succeed on the decoy bytes even though the
        target is not present under the supplied store root.

        A truthful Decision 023 observation may fail closed on caller-owned path dispatch
        or report the target not found in the supplied live context. It must not import
        availability from another root and emit ``exact_observed``.
        """

        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as decoy_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            decoy_store = FilesystemObjectStore(decoy_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            stored = decoy_store.store(target, "artifact.schema.json")
            target_ref = stored.reference
            decoy_path = FilesystemObjectStore._object_path(decoy_store, target_ref)
            actual_source_path = FilesystemObjectStore._object_path(source_store, target_ref)

            self.assertTrue(decoy_path.is_file())
            self.assertFalse(actual_source_path.exists())
            self.assertNotEqual(source_store.root, decoy_store.root)

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = decoy_store.store(container, "artifact.schema.json").reference
            path_dispatch_called = False

            def forged_object_path(reference: str):
                nonlocal path_dispatch_called
                path_dispatch_called = True
                self.assertEqual(reference, target_ref)
                return decoy_path

            with mock.patch.object(
                source_store,
                "_object_path",
                side_effect=forged_object_path,
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
                        "caller-shadowed _object_path must not import exact presence from another root",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(path_dispatch_called)
            self.assertFalse(actual_source_path.exists())
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
