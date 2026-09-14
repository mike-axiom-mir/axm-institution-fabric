from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from axm_institution.identity import make_immutable_ref
from axm_institution.source_live_observation import (
    SourceLiveObservationContextError,
    observe_exact_source_live,
)
from axm_institution.source_runtime_capability import SourceRuntimeCapabilityInputError
from axm_institution.store import FilesystemObjectStore, ObjectStoreError


BASE_REF = (
    "axmref:v1:state-revision:revision.observation-base:-:sha256:" + "c" * 64
)
SUBJECT_REF = (
    "axmref:v1:artifact:artifact.observation-subject:v=1:sha256:" + "d" * 64
)
UNSUPPORTED_TARGET = (
    "axmref:v1:future-source-kind.unregistered:source.future:v=1:sha256:" + "e" * 64
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
        "type": "source_live_observation_fixture",
        "version": version,
        "content_ref": "tests/test_source_live_observation.py",
        "provenance": {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": BASE_REF,
            "source_declarations": declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def typed_evidence(declarations: dict) -> dict:
    return {
        "schema_version": "0.2",
        "id": "evidence.observation-container",
        "subject_ref": SUBJECT_REF,
        "state": "automated_tested",
        "claim": "Decision 023 exact source live observation fixture.",
        "method": "deterministic live exact source observation",
        "source_declarations": declarations,
    }


def target_artifact(*, version: str = "1") -> dict:
    return typed_artifact(
        {},
        artifact_id="artifact.observed-target",
        version=version,
    )


def artifact_ref(value: dict) -> str:
    return make_immutable_ref("artifact.schema.json", value)


def evidence_ref(value: dict) -> str:
    return make_immutable_ref("evidence-record.schema.json", value)


class SourceLiveObservationTests(unittest.TestCase):
    def observe_artifact(self, container: dict, key: str, store: FilesystemObjectStore):
        return observe_exact_source_live(
            containing_object_ref=artifact_ref(container),
            containing_value=container,
            declaration_key=key,
            store=store,
        )

    def test_exact_success_records_bounded_live_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = store.store(target, "artifact.schema.json").reference
            container = typed_artifact({"source": exact_declaration(target_ref)})

            fact = self.observe_artifact(container, "source", store)

        self.assertEqual(artifact_ref(container), fact.containing_object_ref)
        self.assertEqual("source", fact.declaration_key)
        self.assertEqual(target_ref, fact.target_object_ref)
        self.assertEqual("artifact", fact.target_kind)
        self.assertEqual("supported", fact.runtime_capability)
        self.assertEqual("filesystem_exact_load_v1", fact.observation_method)
        self.assertEqual("live_mutable_store", fact.context_standing)
        self.assertEqual("not_established", fact.reexecution_standing)
        self.assertEqual("exact_observed", fact.observation_outcome)
        self.assertEqual("observed_in_live_context", fact.availability_observation)
        self.assertEqual("verified_bytes_obtained", fact.retrieval_observation)
        self.assertEqual("verified_exact_identity", fact.integrity_observation)

    def test_exact_evidence_container_occurrence_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = store.store(target, "artifact.schema.json").reference
            evidence = typed_evidence({"source": exact_declaration(target_ref)})
            fact = observe_exact_source_live(
                containing_object_ref=evidence_ref(evidence),
                containing_value=evidence,
                declaration_key="source",
                store=store,
            )
        self.assertEqual(evidence_ref(evidence), fact.containing_object_ref)
        self.assertEqual(target_ref, fact.target_object_ref)
        self.assertEqual("exact_observed", fact.observation_outcome)

    def test_not_found_is_context_bound_not_global_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            fact = self.observe_artifact(container, "source", store)
        self.assertEqual("not_found_in_live_context", fact.observation_outcome)
        self.assertEqual("not_found_in_live_context", fact.availability_observation)
        self.assertEqual("not_obtained", fact.retrieval_observation)
        self.assertEqual("not_evaluated", fact.integrity_observation)
        for forbidden in ("absent", "nonexistent", "globally_missing"):
            self.assertFalse(hasattr(fact, forbidden), forbidden)

    def test_corrupt_exact_path_material_preserves_corruption_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            target_path = store._object_path(target_ref)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(b"{")
            container = typed_artifact({"source": exact_declaration(target_ref)})
            fact = self.observe_artifact(container, "source", store)
        self.assertEqual("corrupt_material_in_live_context", fact.observation_outcome)
        self.assertEqual("indeterminate_in_live_context", fact.availability_observation)
        self.assertEqual("unverified_bytes_obtained", fact.retrieval_observation)
        self.assertEqual("failed_exact_identity", fact.integrity_observation)

    def test_generic_store_failure_remains_indeterminate_not_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=ObjectStoreError("synthetic read failure"),
            ):
                fact = self.observe_artifact(container, "source", store)
        self.assertEqual("store_error_in_live_context", fact.observation_outcome)
        self.assertEqual("indeterminate_in_live_context", fact.availability_observation)
        self.assertEqual("not_obtained", fact.retrieval_observation)
        self.assertEqual("not_evaluated", fact.integrity_observation)

    def test_unsupported_kind_performs_no_target_object_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            container = typed_artifact({"future": exact_declaration(UNSUPPORTED_TARGET)})
            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=AssertionError("unsupported target must not be read"),
            ):
                fact = self.observe_artifact(container, "future", store)
        self.assertEqual("unsupported_kind", fact.runtime_capability)
        self.assertEqual("not_attempted_unsupported_kind", fact.observation_outcome)
        self.assertEqual("not_observed", fact.availability_observation)
        self.assertEqual("not_attempted", fact.retrieval_observation)
        self.assertEqual("not_evaluated", fact.integrity_observation)

    def test_equal_target_refs_preserve_distinct_declaration_occurrences(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = store.store(target, "artifact.schema.json").reference
            container = typed_artifact(
                {
                    "alpha": exact_declaration(target_ref),
                    "beta": exact_declaration(target_ref),
                }
            )
            alpha = self.observe_artifact(container, "alpha", store)
            beta = self.observe_artifact(container, "beta", store)
        self.assertEqual(alpha.target_object_ref, beta.target_object_ref)
        self.assertEqual("alpha", alpha.declaration_key)
        self.assertEqual("beta", beta.declaration_key)
        self.assertNotEqual(alpha, beta)

    def test_stale_container_identity_fails_before_target_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            original = typed_artifact({"source": exact_declaration(target_ref)})
            stale_ref = artifact_ref(original)
            mutated = copy.deepcopy(original)
            mutated["version"] = "2"
            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=AssertionError("stale container must fail before target I/O"),
            ):
                with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "does not reproduce"):
                    observe_exact_source_live(
                        containing_object_ref=stale_ref,
                        containing_value=mutated,
                        declaration_key="source",
                        store=store,
                    )

    def test_exact_lookup_does_not_fallback_to_newer_same_logical_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            requested = target_artifact(version="1")
            requested_ref = artifact_ref(requested)
            later = target_artifact(version="2")
            later_ref = store.store(later, "artifact.schema.json").reference
            self.assertNotEqual(requested_ref, later_ref)
            container = typed_artifact({"source": exact_declaration(requested_ref)})
            fact = self.observe_artifact(container, "source", store)
        self.assertEqual(requested_ref, fact.target_object_ref)
        self.assertEqual("not_found_in_live_context", fact.observation_outcome)

    def test_canonical_transport_contains_only_bounded_named_facts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            fact = self.observe_artifact(container, "source", store)

        expected_keys = {
            "containing_object_ref",
            "declaration_key",
            "target_object_ref",
            "target_kind",
            "runtime_capability",
            "observation_method",
            "context_standing",
            "reexecution_standing",
            "observation_outcome",
            "availability_observation",
            "retrieval_observation",
            "integrity_observation",
        }
        self.assertEqual(expected_keys, set(fact._asdict()))
        self.assertEqual(fact._asdict(), json.loads(bytes(fact)))
        with self.assertRaises(TypeError):
            json.dumps(fact)
        for forbidden in (
            "store_root",
            "path",
            "host",
            "process",
            "timestamp",
            "actor",
            "ci",
            "branch",
            "git",
            "trusted",
            "complete",
            "closed",
            "accepted",
            "replayable",
        ):
            self.assertFalse(hasattr(fact, forbidden), forbidden)

    def test_repeated_identical_classified_inputs_produce_identical_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            first = self.observe_artifact(container, "source", store)
            second = self.observe_artifact(container, "source", store)
        self.assertEqual(first, second)
        self.assertEqual(bytes(first), bytes(second))

    def test_same_live_store_root_may_truthfully_change_later_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FilesystemObjectStore(tmp)
            target = target_artifact()
            target_ref = artifact_ref(target)
            container = typed_artifact({"source": exact_declaration(target_ref)})

            before = self.observe_artifact(container, "source", store)
            stored = store.store(target, "artifact.schema.json")
            self.assertEqual(target_ref, stored.reference)
            after = self.observe_artifact(container, "source", store)

        self.assertEqual("not_found_in_live_context", before.observation_outcome)
        self.assertEqual("exact_observed", after.observation_outcome)
        self.assertEqual("live_mutable_store", before.context_standing)
        self.assertEqual("live_mutable_store", after.context_standing)
        self.assertEqual("not_established", before.reexecution_standing)
        self.assertEqual("not_established", after.reexecution_standing)

    def test_custom_schema_dir_rejected_before_target_object_io(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as schemas:
            store = FilesystemObjectStore(tmp, schema_dir=Path(schemas))
            target_ref = artifact_ref(target_artifact())
            container = typed_artifact({"source": exact_declaration(target_ref)})
            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=AssertionError("custom schema context must fail before target I/O"),
            ):
                with self.assertRaisesRegex(SourceLiveObservationContextError, "custom schema_dir"):
                    self.observe_artifact(container, "source", store)

    def test_custom_schema_dir_rejected_before_unsupported_outcome_mapping(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as schemas:
            store = FilesystemObjectStore(tmp, schema_dir=Path(schemas))
            container = typed_artifact({"future": exact_declaration(UNSUPPORTED_TARGET)})
            with mock.patch.object(
                store,
                "load_bytes",
                side_effect=AssertionError("custom schema context must fail before target I/O"),
            ):
                with self.assertRaisesRegex(SourceLiveObservationContextError, "custom schema_dir"):
                    self.observe_artifact(container, "future", store)


if __name__ == "__main__":
    unittest.main()
