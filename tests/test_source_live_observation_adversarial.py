from __future__ import annotations

import tempfile
import unittest
from unittest import mock

from axm_institution.identity import make_immutable_ref
from axm_institution.source_live_observation import (
    SourceLiveObservationError,
    observe_exact_source_live,
)
from axm_institution.source_runtime_capability import BUNDLED_SCHEMA_DIR
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
        "content_ref": "tests/test_source_live_observation_adversarial.py",
        "provenance": {
            "producer_lane_id": "lane-03",
            "base_state_revision_ref": BASE_REF,
            "source_declarations": declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def target_artifact() -> dict:
    return typed_artifact(
        {},
        artifact_id="artifact.observed-target",
    )


def artifact_ref(value: dict) -> str:
    return make_immutable_ref("artifact.schema.json", value)


class SourceLiveObservationAdversarialTests(unittest.TestCase):
    def test_adv_058_a_bundled_schema_substitution_mid_observation_fails_closed(self):
        """Decision 023 must not classify under one schema then observe under another.

        The bundled schema directory is live runtime material, so another actor/process
        can change it between Decision 022 capability projection and the target load.
        This test swaps the target-kind schema for a different *valid* JSON Schema only
        after capability classification. The exact target bytes still validate and
        reproduce their immutable reference under the substituted schema, which means a
        naive implementation can incorrectly emit ``exact_observed`` even though the
        interpretation context changed inside one observation invocation.

        A bounded observer must fail closed rather than issuing a successful target fact
        whose capability and integrity dimensions came from different interpretations.
        The test accepts any observer-level Decision 023 error; it does not prescribe a
        repair mechanism or open immutable snapshot/replay semantics.
        """

        schema_path = BUNDLED_SCHEMA_DIR / "artifact.schema.json"
        original_schema = schema_path.read_bytes()
        substituted_schema = (
            b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
            b'"type":"object"}'
        )

        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = store.store(target, "artifact.schema.json").reference
            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = artifact_ref(container)
            original_load_bytes = store.load_bytes
            substitution_happened = False

            def substitute_schema_then_load(reference: str, schema_name: str | None = None) -> bytes:
                nonlocal substitution_happened
                substitution_happened = True
                schema_path.write_bytes(substituted_schema)
                try:
                    return original_load_bytes(reference, schema_name)
                finally:
                    schema_path.write_bytes(original_schema)

            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=substitute_schema_then_load,
            ):
                with self.assertRaises(SourceLiveObservationError):
                    observe_exact_source_live(
                        containing_object_ref=container_ref,
                        containing_value=container,
                        declaration_key="source",
                        store=store,
                    )

            self.assertTrue(substitution_happened)
            self.assertEqual(original_schema, schema_path.read_bytes())


if __name__ == "__main__":
    unittest.main()
