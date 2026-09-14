from __future__ import annotations

import tempfile
import unittest
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
        "content_ref": "tests/test_source_live_observation_adversarial_dispatch_bypass.py",
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


class SourceLiveObservationDispatchBypassAdversarialTests(unittest.TestCase):
    def test_adv_058_e_exact_instance_load_shadow_cannot_forge_exact_observed(self):
        """Caller-shadowed dispatch must not manufacture a positive exact observation.

        ADV-058-C/D already establish that Decision 023 permits an exact store instance
        whose ``load_bytes`` dispatch has been shadowed by caller-owned instance state,
        while requiring the actual target validation to remain grounded in the
        function-owned interpretation context. The newest repair protects ``schema_dir``
        reads through a data descriptor, but the observer still calls the caller-visible
        ``store.load_bytes`` and ignores its return value.

        This counterexample keeps the accepted exact store type and does not mutate the
        schema context at all. The declared exact target is deliberately absent from the
        live store, while the shadowed ``load_bytes`` simply returns arbitrary bytes
        without performing the exact-path read or identity verification. A truthful
        observer may fail closed on the shadowed dispatch or independently reach the
        context-local not-found result, but it must not emit ``exact_observed``.

        This stays on Decision 023's existing actual-validation boundary. It does not ask
        for general hostile-process isolation, snapshots, retained-byte authority, trust,
        closure, integration, epochs, or replay.
        """

        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            self.assertIs(type(store), FilesystemObjectStore)

            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = artifact_ref(container)
            shadow_called = False

            def forged_load_bytes(reference: str, schema_name: str | None = None) -> bytes:
                nonlocal shadow_called
                shadow_called = True
                self.assertEqual(reference, target_ref)
                return b"caller-forged-unverified-bytes"

            with mock.patch.object(store, "load_bytes", side_effect=forged_load_bytes):
                try:
                    fact = observe_exact_source_live(
                        containing_object_ref=container_ref,
                        containing_value=container,
                        declaration_key="source",
                        store=store,
                    )
                except SourceLiveObservationError:
                    pass
                else:
                    self.assertEqual(
                        "not_found_in_live_context",
                        fact.observation_outcome,
                        "caller-shadowed load_bytes must not forge exact_observed",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(shadow_called)
            self.assertIsNone(store.schema_dir)


if __name__ == "__main__":
    unittest.main()
