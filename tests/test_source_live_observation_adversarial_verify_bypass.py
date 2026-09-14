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
        "content_ref": "tests/test_source_live_observation_adversarial_verify_bypass.py",
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


class SourceLiveObservationVerifyBypassAdversarialTests(unittest.TestCase):
    def test_adv_058_f_exact_instance_verify_shadow_cannot_forge_exact_observed(self):
        """Base load dispatch must still perform the real exact-store verification path.

        ADV-058-E established that caller-owned ``load_bytes`` dispatch cannot by itself
        prove a positive exact observation. The bounded repair now calls
        ``FilesystemObjectStore.load_bytes(self, ...)`` directly after any caller shadow.
        That base method, however, still reaches verification through
        ``self._verify_existing(...)``. ``_verify_existing`` is an ordinary method and an
        exact store instance may therefore carry a caller-owned instance shadow for it.

        This counterexample keeps the accepted exact store type, does not mutate the
        schema context, and does not replace ``load_bytes``. The declared exact target is
        deliberately absent. Only ``_verify_existing`` is shadowed so the base
        ``load_bytes`` call returns arbitrary bytes without reading the exact object path,
        validating schema/canonical bytes, or reproducing immutable identity. A truthful
        observer may fail closed on caller-owned verifier dispatch or independently reach
        the context-local not-found result, but it must not emit ``exact_observed``.

        This remains inside Decision 023's existing actual exact-store validation
        boundary; it does not ask for general hostile-process isolation, snapshots,
        retained-byte authority, trust, closure, integration, epochs, or replay.
        """

        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            self.assertIs(type(store), FilesystemObjectStore)

            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = artifact_ref(container)
            verify_called = False

            def forged_verify_existing(reference: str, schema_name: str):
                nonlocal verify_called
                verify_called = True
                self.assertEqual(reference, target_ref)
                self.assertEqual(schema_name, "artifact.schema.json")
                return {}, b"caller-forged-unverified-bytes"

            with mock.patch.object(
                store,
                "_verify_existing",
                side_effect=forged_verify_existing,
            ):
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
                        "caller-shadowed _verify_existing must not forge exact_observed",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(verify_called)
            self.assertIsNone(store.schema_dir)


if __name__ == "__main__":
    unittest.main()
