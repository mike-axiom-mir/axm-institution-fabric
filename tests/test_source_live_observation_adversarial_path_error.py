from __future__ import annotations

import tempfile
import unittest
from unittest import mock

from axm_institution.source_live_observation import (
    SourceLiveObservationError,
    observe_exact_source_live,
)
from axm_institution.store import FilesystemObjectStore, ObjectNotFoundError


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
        "content_ref": "tests/test_source_live_observation_adversarial_path_error.py",
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


class SourceLiveObservationPathErrorAdversarialTests(unittest.TestCase):
    def test_adv_058_h_caller_path_error_cannot_forge_context_local_absence(self):
        """Caller-owned path dispatch must not manufacture a live-context not-found fact.

        ADV-058-G required a positive observation to ignore a caller-owned instance
        ``_object_path`` return value and use the supplied exact store's base path for the
        verification-critical read. The bounded repair still invokes that caller-owned
        shadow first and preserves any exception it raises.

        This fixture keeps the exact accepted ``FilesystemObjectStore`` type, leaves the
        store root, ``objects_dir``, ``load_bytes``, ``_verify_existing``, and
        ``schema_dir`` unchanged, and places the exact target in the supplied store before
        observation. Only the exact instance's ``_object_path`` shadow raises a forged
        ``ObjectNotFoundError`` for the declared target.

        A truthful Decision 023 observer may reject that caller-owned verification path
        and fail closed, or it may ignore the shadow and independently observe the real
        exact object. It must not convert the caller-owned exception into the institutional
        claim ``not_found_in_live_context`` while the target is actually present in the
        supplied store.
        """

        with tempfile.TemporaryDirectory() as source_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            stored = source_store.store(target, "artifact.schema.json")
            target_ref = stored.reference
            actual_source_path = FilesystemObjectStore._object_path(source_store, target_ref)
            self.assertTrue(actual_source_path.is_file())

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = source_store.store(container, "artifact.schema.json").reference
            path_dispatch_called = False

            def forged_not_found(reference: str):
                nonlocal path_dispatch_called
                path_dispatch_called = True
                self.assertEqual(reference, target_ref)
                raise ObjectNotFoundError("caller-forged path absence")

            with mock.patch.object(
                source_store,
                "_object_path",
                side_effect=forged_not_found,
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
                        "exact_observed",
                        fact.observation_outcome,
                        "caller-shadowed _object_path error must not forge context-local absence",
                    )
                    self.assertEqual("observed_in_live_context", fact.availability_observation)
                    self.assertEqual("verified_bytes_obtained", fact.retrieval_observation)
                    self.assertEqual("verified_exact_identity", fact.integrity_observation)

            self.assertTrue(path_dispatch_called)
            self.assertTrue(actual_source_path.is_file())
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
