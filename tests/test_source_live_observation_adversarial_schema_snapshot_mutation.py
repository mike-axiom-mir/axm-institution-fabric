from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
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
        "content_ref": "tests/test_source_live_observation_adversarial_schema_snapshot_mutation.py",
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


class SourceLiveObservationSchemaSnapshotMutationAdversarialTests(unittest.TestCase):
    def test_adv_058_q_caller_dispatch_cannot_mutate_function_owned_schema_snapshot_into_corruption(self):
        """Caller-visible dispatch must not rewrite the observer's fixed schema context.

        Decision 023 promises one function-owned bundled-schema interpretation for both
        capability classification and exact target validation. The repaired invocation
        guard exposes that temporary snapshot through ``store.schema_dir`` while executing
        caller-owned exact-instance dispatch. A caller hook can therefore obtain the
        function-owned snapshot path and mutate ``artifact.schema.json`` in place after
        capability classification but before the base verifier consumes it.

        This fixture keeps the exact target genuinely present and canonical in the
        supplied exact ``FilesystemObjectStore``. Only the exact instance's caller-owned
        ``_verify_existing`` shadow rewrites the invocation-local snapshot to a valid JSON
        Schema that rejects the target, then returns normally. It does not change the
        ambient bundled schemas, store root, target bytes, target path, or schema_dir
        binding.

        A bounded observer may fail closed, independently establish ``exact_observed``,
        or conservatively report an indeterminate store error. It must not issue a durable
        material-corruption / failed-identity fact when the only contradictory evidence
        came from caller mutation of the observer's own temporary interpretation copy.
        """

        rejecting_schema = (
            b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
            b'"type":"object","required":["adv_058_q_missing_field"]}'
        )

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
            snapshot_mutated = False

            def mutate_snapshot(reference: str, schema_name: str):
                nonlocal snapshot_mutated
                self.assertEqual(target_ref, reference)
                self.assertEqual("artifact.schema.json", schema_name)
                observer_schema_dir = source_store.schema_dir
                self.assertIsInstance(observer_schema_dir, Path)
                snapshot_schema = observer_schema_dir / "artifact.schema.json"
                self.assertTrue(snapshot_schema.exists())
                snapshot_schema.write_bytes(rejecting_schema)
                snapshot_mutated = True
                return {}, b"caller return is deliberately non-authoritative"

            with mock.patch.object(
                source_store,
                "_verify_existing",
                side_effect=mutate_snapshot,
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
                        "caller mutation of the observer-owned schema snapshot must not forge material corruption",
                    )
                    self.assertNotEqual(
                        "failed_exact_identity",
                        fact.integrity_observation,
                        "caller mutation of the observer-owned schema snapshot must not forge failed exact identity",
                    )
                    self.assertIn(
                        fact.observation_outcome,
                        {"exact_observed", "store_error_in_live_context"},
                    )

            self.assertTrue(snapshot_mutated)
            self.assertEqual(canonical_before, source_store.load_bytes(target_ref))
            self.assertTrue(target_path.exists())
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
