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
        "content_ref": "tests/test_source_live_observation_adversarial_path_location_equality.py",
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


class _EqualRedirectingObjectsDir:
    """Path-like drift that compares equal to one directory but routes joins elsewhere."""

    def __init__(self, expected, redirect):
        self.expected = expected
        self.redirect = redirect

    def __eq__(self, other: object) -> bool:
        return other == self.expected

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __truediv__(self, component):
        return self.redirect / component


class SourceLiveObservationPathLocationEqualityAdversarialTests(unittest.TestCase):
    def test_adv_058_n_equal_comparing_objects_dir_drift_cannot_redirect_base_path(self):
        """Location continuity must not rely on attacker-defined equality before path use.

        ADV-058-K established that caller-owned ``_object_path`` side effects must not
        mutate ``objects_dir`` before the subsequent base path consumes it. The K repair
        captures invocation-entry ``objects_dir`` and checks ``self.objects_dir !=`` that
        value before calling ``FilesystemObjectStore._object_path``.

        This adjacent fixture keeps the target absent from the supplied exact store and
        present only in a separate decoy store. Caller-owned ``_object_path`` dispatch
        replaces ``objects_dir`` with a path-like proxy that deliberately compares equal
        to the invocation-entry directory but routes path joins into the decoy root. The
        caller hook's own returned path is not relied on. If the guard accepts equality as
        proof of unchanged location, the subsequent base path can consume the proxy and
        import exact presence from the decoy store.

        A bounded truthful observer may fail closed on location drift or independently
        report context-local absence from the supplied store. It must not emit
        ``exact_observed`` through an equality-spoofed location object.
        """

        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as decoy_tmp:
            source_store = FilesystemObjectStore(source_tmp)
            decoy_store = FilesystemObjectStore(decoy_tmp)
            self.assertIs(type(source_store), FilesystemObjectStore)

            target = target_artifact()
            target_ref = decoy_store.store(target, "artifact.schema.json").reference
            source_objects_dir = source_store.objects_dir
            decoy_objects_dir = decoy_store.objects_dir
            source_path = FilesystemObjectStore._object_path(source_store, target_ref)
            decoy_path = FilesystemObjectStore._object_path(decoy_store, target_ref)
            self.assertFalse(source_path.exists())
            self.assertTrue(decoy_path.exists())

            container = typed_artifact({"source": exact_declaration(target_ref)})
            container_ref = decoy_store.store(container, "artifact.schema.json").reference
            path_shadow_called = False

            def spoof_equal_location(reference: str):
                nonlocal path_shadow_called
                path_shadow_called = True
                self.assertEqual(reference, target_ref)
                source_store.objects_dir = _EqualRedirectingObjectsDir(
                    source_objects_dir,
                    decoy_objects_dir,
                )
                return source_path

            with mock.patch.object(
                source_store,
                "_object_path",
                side_effect=spoof_equal_location,
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
                        "caller-owned path dispatch must not pass location continuity by custom equality and redirect the base path",
                    )
                    self.assertEqual("not_found_in_live_context", fact.availability_observation)
                    self.assertEqual("not_obtained", fact.retrieval_observation)
                    self.assertEqual("not_evaluated", fact.integrity_observation)

            self.assertTrue(path_shadow_called)
            self.assertFalse(source_path.exists())
            self.assertTrue(decoy_path.exists())
            self.assertEqual(source_objects_dir, source_store.objects_dir)
            self.assertIs(type(source_store), FilesystemObjectStore)
            self.assertIsNone(source_store.schema_dir)


if __name__ == "__main__":
    unittest.main()
