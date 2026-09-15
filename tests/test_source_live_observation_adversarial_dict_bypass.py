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
        "content_ref": "tests/test_source_live_observation_adversarial_dict_bypass.py",
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


def artifact_ref(value: dict) -> str:
    return make_immutable_ref("artifact.schema.json", value)


class SourceLiveObservationDictBypassAdversarialTests(unittest.TestCase):
    def test_adv_058_d_direct_instance_dict_schema_rebind_and_restore_fails_closed(self):
        """The invocation guard must not be bypassable through direct instance state.

        The Decision 023 repair temporarily changes the exact store instance's class so
        ``schema_dir`` writes pass through a function-owned ``__setattr__`` guard. But an
        ordinary Python instance still exposes ``__dict__``. A caller-owned replacement
        for that exact instance's ``load_bytes`` can therefore write ``schema_dir``
        directly into the instance dictionary, invoke the unmodified class loader under a
        caller-owned permissive schema, then restore the observer-owned directory before
        returning. That bypasses both guarded assignment and the post-call equality check.

        Decision 023 requires capability classification and actual target validation to
        use one function-owned interpretation context, or fail closed. This attack stays
        on that same bounded coherence surface and does not claim general hostile-process
        isolation, immutable snapshots, trust, closure, integration, or replay.
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
                store.__dict__["schema_dir"] = alternate_schema_dir
                try:
                    return FilesystemObjectStore.load_bytes(store, reference, schema_name)
                finally:
                    store.__dict__["schema_dir"] = observer_schema_dir

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
