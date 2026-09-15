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
        "content_ref": "tests/test_source_live_observation_adversarial_verifier_corruption_error.py",
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


class SourceLiveObservationVerifierCorruptionErrorAuthorityAdversarialTests(unittest.TestCase):
    def test_adv_058_p_caller_verify_corruption_error_cannot_forge_material_corruption(self):
        """Caller-owned verifier dispatch must not become corruption authority.

        ADV-058-O established the rule at the outer ``load_bytes`` dispatch layer: a
        caller-owned ``ObjectCorruptionError`` is not source-truth evidence when the
        function-owned exact-store read has not independently observed corruption.
        Lane 02's bounded O repair applies that rule to caller-owned ``load_bytes``.

        The adjacent verifier layer remains caller-visible. The current invocation guard
        catches caller-owned ``ObjectNotFoundError`` from ``_verify_existing`` so J cannot
        forge absence, but a caller-owned ``ObjectCorruptionError`` still escapes to the
        outer observation classifier before the base verifier can read the real target.

        This fixture keeps the exact target genuinely present and byte-identical in the
        supplied exact ``FilesystemObjectStore``. Only the exact instance's caller-owned
        ``_verify_existing`` shadow raises a forged ``ObjectCorruptionError``; it performs
        no target I/O and mutates no schema or store-location state.

        A bounded observer may fail closed, independently establish ``exact_observed``,
        or conservatively classify caller interference as an indeterminate store error.
        It must not assert material corruption / failed exact identity solely because a
        caller-owned verifier pre-dispatch raised the corruption exception class.
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
            verify_dispatch_called = False

            def forge_corruption(reference: str, schema_name: str):
                nonlocal verify_dispatch_called
                verify_dispatch_called = True
                self.assertEqual(target_ref, reference)
                self.assertEqual("artifact.schema.json", schema_name)
                raise ObjectCorruptionError("caller-forged verifier corruption classification")

            with mock.patch.object(
                source_store,
                "_verify_existing",
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
                        "caller-owned verifier dispatch must not forge material corruption",
                    )
                    self.assertNotEqual(
                        "failed_exact_identity",
                        fact.integrity_observation,
                        "caller-owned verifier dispatch must not forge failed exact identity",
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

            self.assertTrue(verify_dispatch_called)
            self.assertEqual(canonical_before, source_store.load_bytes(target_ref))
            self.assertTrue(target_path.exists())
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
