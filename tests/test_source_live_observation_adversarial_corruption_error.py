from __future__ import annotations

import tempfile
import unittest
from unittest import mock

from axm_institution.source_live_observation import (
    SourceLiveObservationError,
    observe_exact_source_live,
)
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
)


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
        "content_ref": "tests/test_source_live_observation_adversarial_corruption_error.py",
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


class SourceLiveObservationCorruptionErrorAuthorityAdversarialTests(unittest.TestCase):
    def test_adv_058_o_caller_load_corruption_error_cannot_forge_material_corruption(self):
        """Caller-owned dispatch must not become authority for exact-material corruption.

        ADV-058-I already established that caller-owned ``load_bytes`` not-found errors
        cannot manufacture context-local absence before the function-owned exact-store
        read. The current guard catches that one error class, but lets a caller-raised
        ``ObjectCorruptionError`` escape to the outer observation classifier. The outer
        classifier then maps that error to ``corrupt_material_in_live_context`` even when
        the supplied exact store contains the correct canonical target bytes.

        This fixture keeps the exact target genuinely present and byte-identical in the
        supplied exact ``FilesystemObjectStore``. Only the exact instance's caller-owned
        ``load_bytes`` shadow raises a forged ``ObjectCorruptionError``; it performs no
        target I/O and mutates no store/schema/location state.

        A bounded observer may fail closed, independently establish ``exact_observed``,
        or conservatively classify caller interference as an indeterminate store error.
        It must not assert material corruption / failed exact identity solely because a
        caller-owned pre-dispatch raised the corruption exception class.
        """

        with tempfile.TemporaryDirectory() as source_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            target_ref = source_store.store(target, "artifact.schema.json").reference
            canonical_before = source_store.load_bytes(target_ref)
            target_path = FilesystemObjectStore._object_path(source_store, target_ref)
            self.assertTrue(target_path.exists())

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = source_store.store(container, "artifact.schema.json").reference
            shadow_called = False

            def forge_corruption(reference: str, schema_name: str | None = None) -> bytes:
                nonlocal shadow_called
                shadow_called = True
                self.assertEqual(target_ref, reference)
                raise ObjectCorruptionError("caller-forged corruption classification")

            with mock.patch.object(
                source_store,
                "load_bytes",
                side_effect=forge_corruption,
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
                    self.assertNotEqual(
                        "corrupt_material_in_live_context",
                        fact.observation_outcome,
                        "caller-owned load dispatch must not forge material corruption",
                    )
                    self.assertNotEqual(
                        "failed_exact_identity",
                        fact.integrity_observation,
                        "caller-owned load dispatch must not forge failed exact identity",
                    )
                    self.assertIn(
                        fact.observation_outcome,
                        {"exact_observed", "store_error_in_live_context"},
                    )
                    if fact.observation_outcome == "exact_observed":
                        self.assertEqual("observed_in_live_context", fact.availability_observation)
                        self.assertEqual("verified_bytes_obtained", fact.retrieval_observation)
                        self.assertEqual("verified_exact_identity", fact.integrity_observation)
                    else:
                        self.assertEqual("indeterminate_in_live_context", fact.availability_observation)
                        self.assertEqual("not_obtained", fact.retrieval_observation)
                        self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(shadow_called)
            self.assertEqual(canonical_before, source_store.load_bytes(target_ref))
            self.assertTrue(target_path.exists())
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
