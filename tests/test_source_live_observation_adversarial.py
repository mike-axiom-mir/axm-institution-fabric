from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
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

    def test_adv_058_b_store_schema_context_rebind_and_restore_fails_closed(self):
        """A caller-owned store must not swap validation context and restore it invisibly.

        Decision 023 explicitly rejects caller-selected schema contexts and requires one
        fixed bundled interpretation for capability and exact target validation. This
        accepted ``FilesystemObjectStore`` subclass starts with ``schema_dir is None``,
        so it passes the public context check, but rebinds ``schema_dir`` only during
        ``load_bytes`` and restores the observer-owned snapshot directory before return.

        If the observer checks only the attribute before/after the call, the swap-and-
        restore is invisible even though target integrity was evaluated under a caller-
        supplied permissive schema. The bounded contract must fail closed rather than
        emit a normal observation fact from that split interpretation.
        """

        class RebindingStore(FilesystemObjectStore):
            def __init__(self, root: str, alternate_schema_dir: Path) -> None:
                super().__init__(root)
                self.alternate_schema_dir = alternate_schema_dir

            def load_bytes(self, reference: str, schema_name: str | None = None) -> bytes:
                observer_schema_dir = self.schema_dir
                self.schema_dir = self.alternate_schema_dir
                try:
                    return super().load_bytes(reference, schema_name)
                finally:
                    self.schema_dir = observer_schema_dir

        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as schema_tmp:
            plain_store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = plain_store.store(target, "artifact.schema.json").reference
            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = artifact_ref(container)

            alternate_schema_dir = Path(schema_tmp)
            (alternate_schema_dir / "artifact.schema.json").write_bytes(
                b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                b'"type":"object"}'
            )
            store = RebindingStore(tmp, alternate_schema_dir)
            self.assertIsNone(store.schema_dir)

            with self.assertRaises(SourceLiveObservationError):
                observe_exact_source_live(
                    containing_object_ref=container_ref,
                    containing_value=container,
                    declaration_key="source",
                    store=store,
                )

            self.assertIsNone(store.schema_dir)

    def test_adv_058_c_exact_store_instance_method_rebind_and_restore_fails_closed(self):
        """Exact class identity must not hide caller replacement of the validation call.

        ADV-058-B is closed by rejecting subclasses, but ``FilesystemObjectStore`` has
        ordinary per-instance attributes. A caller can therefore replace ``load_bytes``
        on an exact-type store instance, temporarily rebind ``schema_dir`` only while the
        class implementation validates the target, then restore the observer-owned
        snapshot directory before return. The public exact-type check and the after-call
        attribute check both still succeed.

        Decision 023 requires the actual target-validation operation to consume the same
        function-owned interpretation context as capability classification, or fail
        closed. This test stays on that same-invocation boundary and opens no wider
        hostile-process, trust, snapshot, closure, or replay semantics.
        """

        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as schema_tmp:
            store = FilesystemObjectStore(tmp)
            self.assertIs(type(store), FilesystemObjectStore)
            target = target_artifact()
            target_ref = store.store(target, "artifact.schema.json").reference
            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = artifact_ref(container)

            alternate_schema_dir = Path(schema_tmp)
            (alternate_schema_dir / "artifact.schema.json").write_bytes(
                b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                b'"type":"object"}'
            )
            substitution_happened = False

            def rebound_load_bytes(reference: str, schema_name: str | None = None) -> bytes:
                nonlocal substitution_happened
                substitution_happened = True
                observer_schema_dir = store.schema_dir
                store.schema_dir = alternate_schema_dir
                try:
                    return FilesystemObjectStore.load_bytes(store, reference, schema_name)
                finally:
                    store.schema_dir = observer_schema_dir

            with mock.patch.object(store, "load_bytes", side_effect=rebound_load_bytes):
                with self.assertRaises(SourceLiveObservationError):
                    observe_exact_source_live(
                        containing_object_ref=container_ref,
                        containing_value=container,
                        declaration_key="source",
                        store=store,
                    )

            self.assertTrue(substitution_happened)
            self.assertIsNone(store.schema_dir)


if __name__ == "__main__":
    unittest.main()
