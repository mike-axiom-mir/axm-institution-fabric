from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from axm_institution.identity import make_immutable_ref
from axm_institution.source_runtime_capability import (
    SourceRuntimeCapabilityContextError,
    SourceRuntimeCapabilityInputError,
    project_exact_source_runtime_capability,
)


BASE_REF = (
    "axmref:v1:state-revision:revision.capability-base:-:sha256:" + "c" * 64
)
SUBJECT_REF = (
    "axmref:v1:artifact:artifact.capability-subject:v=1:sha256:" + "d" * 64
)
SUPPORTED_TARGET = (
    "axmref:v1:artifact:artifact.target-not-present:v=1:sha256:" + "a" * 64
)
SUPPORTED_EVIDENCE_TARGET = (
    "axmref:v1:evidence-record:evidence.target-not-present:-:sha256:" + "b" * 64
)
UNSUPPORTED_TARGET = (
    "axmref:v1:future-source-kind.unregistered:source.future:v=1:sha256:" + "e" * 64
)


def exact_declaration(target_ref: str) -> dict:
    return {"source_class": "exact_axm_object", "object_ref": target_ref}


def typed_artifact(
    declarations: dict,
    *,
    artifact_id: str = "artifact.capability-container",
    version: str = "1",
) -> dict:
    return {
        "schema_version": "0.4",
        "id": artifact_id,
        "type": "source_runtime_capability_fixture",
        "version": version,
        "content_ref": "tests/test_source_runtime_capability.py",
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
        "id": "evidence.capability-container",
        "subject_ref": SUBJECT_REF,
        "state": "automated_tested",
        "claim": "Decision 022 bundled runtime capability fixture.",
        "method": "deterministic no-target-I/O capability projection",
        "source_declarations": declarations,
    }


def artifact_ref(value: dict) -> str:
    return make_immutable_ref("artifact.schema.json", value)


def evidence_ref(value: dict) -> str:
    return make_immutable_ref("evidence-record.schema.json", value)


class SourceRuntimeCapabilityTests(unittest.TestCase):
    def project_artifact(self, value: dict, key: str):
        return project_exact_source_runtime_capability(
            containing_object_ref=artifact_ref(value),
            containing_value=value,
            declaration_key=key,
        )

    def test_artifact_occurrence_reports_supported_bundled_kind(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        fact = self.project_artifact(artifact, "source")
        self.assertEqual(artifact_ref(artifact), fact.containing_object_ref)
        self.assertEqual("source", fact.declaration_key)
        self.assertEqual(SUPPORTED_TARGET, fact.target_object_ref)
        self.assertEqual("artifact", fact.target_kind)
        self.assertEqual("supported", fact.runtime_capability)

    def test_evidence_occurrence_reports_supported_bundled_kind(self):
        evidence = typed_evidence({"source": exact_declaration(SUPPORTED_EVIDENCE_TARGET)})
        fact = project_exact_source_runtime_capability(
            containing_object_ref=evidence_ref(evidence),
            containing_value=evidence,
            declaration_key="source",
        )
        self.assertEqual(evidence_ref(evidence), fact.containing_object_ref)
        self.assertEqual("evidence-record", fact.target_kind)
        self.assertEqual("supported", fact.runtime_capability)

    def test_canonical_unregistered_kind_reports_unsupported_kind(self):
        artifact = typed_artifact({"future-kind": exact_declaration(UNSUPPORTED_TARGET)})
        fact = self.project_artifact(artifact, "future-kind")
        self.assertEqual(UNSUPPORTED_TARGET, fact.target_object_ref)
        self.assertEqual("future-source-kind.unregistered", fact.target_kind)
        self.assertEqual("unsupported_kind", fact.runtime_capability)

    def test_same_target_under_two_keys_remains_two_occurrence_attributions(self):
        artifact = typed_artifact(
            {
                "alpha": exact_declaration(SUPPORTED_TARGET),
                "beta": exact_declaration(SUPPORTED_TARGET),
            }
        )
        alpha = self.project_artifact(artifact, "alpha")
        beta = self.project_artifact(artifact, "beta")
        self.assertEqual(alpha.target_object_ref, beta.target_object_ref)
        self.assertEqual(alpha.containing_object_ref, beta.containing_object_ref)
        self.assertEqual("alpha", alpha.declaration_key)
        self.assertEqual("beta", beta.declaration_key)
        self.assertNotEqual(alpha, beta)

    def test_same_key_in_two_exact_containers_remains_two_occurrences(self):
        first = typed_artifact(
            {"source": exact_declaration(SUPPORTED_TARGET)},
            artifact_id="artifact.capability-container-a",
        )
        second = typed_artifact(
            {"source": exact_declaration(SUPPORTED_TARGET)},
            artifact_id="artifact.capability-container-b",
        )
        first_fact = self.project_artifact(first, "source")
        second_fact = self.project_artifact(second, "source")
        self.assertEqual("source", first_fact.declaration_key)
        self.assertEqual("source", second_fact.declaration_key)
        self.assertNotEqual(first_fact.containing_object_ref, second_fact.containing_object_ref)
        self.assertNotEqual(first_fact, second_fact)

    def test_later_same_logical_id_container_cannot_rebind_earlier_occurrence(self):
        earlier = typed_artifact(
            {"source": exact_declaration(SUPPORTED_TARGET)},
            artifact_id="artifact.same-logical",
            version="1",
        )
        later = typed_artifact(
            {"source": exact_declaration(UNSUPPORTED_TARGET)},
            artifact_id="artifact.same-logical",
            version="2",
        )
        earlier_fact = self.project_artifact(earlier, "source")
        later_fact = self.project_artifact(later, "source")
        self.assertEqual(SUPPORTED_TARGET, earlier_fact.target_object_ref)
        self.assertEqual("supported", earlier_fact.runtime_capability)
        self.assertEqual(UNSUPPORTED_TARGET, later_fact.target_object_ref)
        self.assertEqual("unsupported_kind", later_fact.runtime_capability)
        self.assertNotEqual(earlier_fact.containing_object_ref, later_fact.containing_object_ref)

    def test_declaration_map_order_grants_no_capability_authority(self):
        left = typed_artifact(
            {
                "source": exact_declaration(SUPPORTED_TARGET),
                "other": exact_declaration(UNSUPPORTED_TARGET),
            }
        )
        right = typed_artifact(
            {
                "other": exact_declaration(UNSUPPORTED_TARGET),
                "source": exact_declaration(SUPPORTED_TARGET),
            }
        )
        self.assertEqual(artifact_ref(left), artifact_ref(right))
        self.assertEqual(self.project_artifact(left, "source"), self.project_artifact(right, "source"))

    def test_non_exact_source_class_is_not_promoted_by_axmref_looking_text(self):
        artifact = typed_artifact(
            {
                "source": {
                    "source_class": "opaque_label",
                    "token": SUPPORTED_TARGET,
                }
            }
        )
        with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "not an exact_axm_object"):
            self.project_artifact(artifact, "source")

    def test_projection_performs_no_source_target_store_lookup(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        with mock.patch(
            "axm_institution.store.FilesystemObjectStore.load",
            side_effect=AssertionError("source target load must not occur"),
        ), mock.patch(
            "axm_institution.store.FilesystemObjectStore.load_bytes",
            side_effect=AssertionError("source target load_bytes must not occur"),
        ):
            fact = self.project_artifact(artifact, "source")
        self.assertEqual("supported", fact.runtime_capability)

    def test_named_transport_preserves_meaning_or_fails_closed(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        fact = self.project_artifact(artifact, "source")
        expected = {
            "containing_object_ref": artifact_ref(artifact),
            "declaration_key": "source",
            "target_object_ref": SUPPORTED_TARGET,
            "target_kind": "artifact",
            "runtime_capability": "supported",
        }
        self.assertEqual(expected, fact._asdict())
        self.assertEqual(expected, json.loads(bytes(fact)))
        with self.assertRaises(TypeError):
            json.dumps(fact)

    def test_result_exposes_only_bounded_capability_facts(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        fact = self.project_artifact(artifact, "source")
        self.assertEqual(
            {
                "containing_object_ref",
                "declaration_key",
                "target_object_ref",
                "target_kind",
                "runtime_capability",
            },
            set(fact._asdict()),
        )
        for forbidden in (
            "exists",
            "available",
            "retrieved",
            "integrity",
            "trusted",
            "complete",
            "closed",
            "accepted",
            "replayable",
        ):
            self.assertFalse(hasattr(fact, forbidden), forbidden)

    def test_exact_containing_ref_mismatch_fails_closed(self):
        original = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        stale_ref = artifact_ref(original)
        mutated = copy.deepcopy(original)
        mutated["version"] = "2"
        with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "does not reproduce"):
            project_exact_source_runtime_capability(
                containing_object_ref=stale_ref,
                containing_value=mutated,
                declaration_key="source",
            )

    def test_absent_declaration_key_fails_without_fallback(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "absent"):
            self.project_artifact(artifact, "source-neighbor")

    def test_invalid_existing_bundled_schema_is_context_failure_not_unsupported(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        with tempfile.TemporaryDirectory() as tmp:
            schema_dir = Path(tmp)
            (schema_dir / "artifact.schema.json").write_text("{", encoding="utf-8")
            with mock.patch(
                "axm_institution.source_runtime_capability.BUNDLED_SCHEMA_DIR",
                schema_dir,
            ):
                with self.assertRaises(SourceRuntimeCapabilityContextError):
                    self.project_artifact(artifact, "source")
