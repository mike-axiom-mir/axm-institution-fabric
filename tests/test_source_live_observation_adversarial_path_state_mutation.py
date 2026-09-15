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
        "content_ref": "tests/test_source_live_observation_adversarial_path_state_mutation.py",
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


class SourceLiveObservationPathStateMutationAdversarialTests(unittest.TestCase):
    def test_adv_058_k_object_path_shadow_cannot_rebind_base_path_state_to_import_presence(self):
        """Ignored caller path return values must not retain authority through side effects.

        ADV-058-G established that a caller-owned ``_object_path`` return value may not
        redirect exact observation into another store root. The bounded repair ignores
        that return value and then calls ``FilesystemObjectStore._object_path(self, ...)``.
        The base path implementation, however, derives the path from mutable
        ``self.objects_dir``.

        This fixture keeps the declared target absent from the supplied store and stores
        the exact target only in a separate decoy store. The caller-owned ``_object_path``
        shadow does not return the decoy path. Instead, while being exercised by the
        invocation guard, it mutates only ``source_store.objects_dir`` to the decoy
        store's objects directory. The subsequent function-owned base path call then uses
        that caller-mutated location state and can import the external exact object even
        though the target was absent under the supplied store's entry root.

        A truthful bounded observer may fail closed or report context-local absence. It
        must not emit ``exact_observed`` solely because a caller-owned path hook mutated
        the location state consumed by the supposedly function-owned base path.
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
            original_objects_dir = source_store.objects_dir

            self.assertTrue(decoy_path.is_file())
            self.assertFalse(actual_source_path.exists())
            self.assertNotEqual(source_store.root, decoy_store.root)
            self.assertNotEqual(source_store.objects_dir, decoy_store.objects_dir)

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = decoy_store.store(container, "artifact.schema.json").reference
            path_dispatch_called = False

            def mutate_location_state(reference: str):
                nonlocal path_dispatch_called
                path_dispatch_called = True
                self.assertEqual(reference, target_ref)
                source_store.objects_dir = decoy_store.objects_dir
                return actual_source_path

            try:
                with mock.patch.object(
                    source_store,
                    "_object_path",
                    side_effect=mutate_location_state,
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
                            "caller-shadowed _object_path side effects must not import exact presence from another root",
                        )
                        self.assertEqual("not_found_in_live_context", fact.availability_observation)
                        self.assertEqual("not_obtained", fact.retrieval_observation)
                        self.assertEqual("not_evaluated", fact.integrity_observation)
            finally:
                source_store.objects_dir = original_objects_dir

            self.assertTrue(path_dispatch_called)
            self.assertFalse(actual_source_path.exists())
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
