from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

EXACT_LOOKING_ARTIFACT_REF = (
    "axmref:v1:artifact:artifact.source-decoy:v=9:sha256:"
    + "a" * 64
)
EXACT_BASE_REF = (
    "axmref:v1:state-revision:revision.fixture.0001:-:sha256:"
    + "b" * 64
)

REPRESENTATIVE_HISTORICAL_SOURCE_STRINGS = (
    "NEXT_BUILD.md",
    "coordination/decisions/019_SOURCE_PROVENANCE_TAXONOMY_RESEARCH_GATE.md",
    "https://example.invalid/source",
    "git:deadbeef",
    "sha256:" + "c" * 64,
    "artifact.logical-label",
    EXACT_LOOKING_ARTIFACT_REF,
)


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def artifact_instance(schema_version: str, source_ref: str) -> dict:
    provenance = {
        "producer_lane_id": "lane-02",
        "source_refs": [source_ref],
    }
    if schema_version == "0.1":
        provenance["base_state_revision"] = "revision.fixture.0001"
    else:
        provenance["base_state_revision_ref"] = EXACT_BASE_REF

    return {
        "schema_version": schema_version,
        "id": "artifact.source-compatibility",
        "type": "source_compatibility_fixture",
        "version": "0.1",
        "content_ref": "fixtures/source-compatibility",
        "provenance": provenance,
        "evidence_refs": [],
        "dependency_refs": [],
    }


def evidence_instance(source_ref: str) -> dict:
    return {
        "schema_version": "0.1",
        "id": "evidence.source-compatibility",
        "subject_ref": "artifact.source-compatibility",
        "state": "automated_tested",
        "claim": "Historical source strings remain valid under the authored v0.1 evidence contract.",
        "method": "schema compatibility regression",
        "source_refs": [source_ref],
    }


class HistoricalSourceRefCompatibilityTests(unittest.TestCase):
    """Guard authored historical syntax without assigning new source semantics."""

    @classmethod
    def setUpClass(cls):
        cls.artifact_schema = load_schema("artifact.schema.json")
        cls.evidence_schema = load_schema("evidence-record.schema.json")
        Draft202012Validator.check_schema(cls.artifact_schema)
        Draft202012Validator.check_schema(cls.evidence_schema)
        cls.artifact_validator = Draft202012Validator(cls.artifact_schema)
        cls.evidence_validator = Draft202012Validator(cls.evidence_schema)

    def test_all_historical_artifact_versions_accept_representative_opaque_source_strings(self):
        for schema_version in ("0.1", "0.2", "0.3"):
            for source_ref in REPRESENTATIVE_HISTORICAL_SOURCE_STRINGS:
                with self.subTest(schema_version=schema_version, source_ref=source_ref):
                    errors = list(
                        self.artifact_validator.iter_errors(
                            artifact_instance(schema_version, source_ref)
                        )
                    )
                    self.assertEqual([], errors)

    def test_historical_evidence_v01_accepts_representative_opaque_source_strings(self):
        for source_ref in REPRESENTATIVE_HISTORICAL_SOURCE_STRINGS:
            with self.subTest(source_ref=source_ref):
                errors = list(self.evidence_validator.iter_errors(evidence_instance(source_ref)))
                self.assertEqual([], errors)

    def test_artifact_source_refs_still_reject_empty_strings(self):
        for schema_version in ("0.1", "0.2", "0.3"):
            with self.subTest(schema_version=schema_version):
                errors = list(
                    self.artifact_validator.iter_errors(
                        artifact_instance(schema_version, "")
                    )
                )
                self.assertTrue(errors)

    def test_evidence_source_refs_still_reject_empty_strings(self):
        errors = list(self.evidence_validator.iter_errors(evidence_instance("")))
        self.assertTrue(errors)

    def test_artifact_source_refs_still_reject_duplicate_opaque_tokens(self):
        for schema_version in ("0.1", "0.2", "0.3"):
            with self.subTest(schema_version=schema_version):
                instance = artifact_instance(schema_version, "NEXT_BUILD.md")
                instance["provenance"]["source_refs"] = [
                    "NEXT_BUILD.md",
                    "NEXT_BUILD.md",
                ]
                errors = list(self.artifact_validator.iter_errors(instance))
                self.assertTrue(errors)

    def test_evidence_source_refs_still_reject_duplicate_opaque_tokens(self):
        instance = evidence_instance("NEXT_BUILD.md")
        instance["source_refs"] = ["NEXT_BUILD.md", "NEXT_BUILD.md"]
        errors = list(self.evidence_validator.iter_errors(instance))
        self.assertTrue(errors)

    def test_strong_evidence_still_requires_at_least_one_opaque_source_token(self):
        instance = evidence_instance("NEXT_BUILD.md")
        instance["source_refs"] = []
        errors = list(self.evidence_validator.iter_errors(instance))
        self.assertTrue(errors)

    def test_proposed_evidence_still_does_not_require_source_refs(self):
        instance = evidence_instance("NEXT_BUILD.md")
        instance["state"] = "proposed"
        instance.pop("method")
        instance.pop("source_refs")
        errors = list(self.evidence_validator.iter_errors(instance))
        self.assertEqual([], errors)

    def test_artifact_source_ref_schema_does_not_assign_identity_strength(self):
        source_item = self.artifact_schema["properties"]["provenance"]["properties"][
            "source_refs"
        ]["items"]
        self.assertEqual("string", source_item["type"])
        self.assertEqual(1, source_item["minLength"])
        for identity_constraint in ("pattern", "format", "enum", "const"):
            self.assertNotIn(identity_constraint, source_item)

        for version_branch in self.artifact_schema.get("allOf", []):
            provenance = (
                version_branch.get("then", {})
                .get("properties", {})
                .get("provenance", {})
            )
            version_properties = provenance.get("properties", {})
            self.assertNotIn("source_refs", version_properties)

    def test_evidence_source_ref_schema_does_not_assign_identity_strength(self):
        source_item = self.evidence_schema["properties"]["source_refs"]["items"]
        self.assertEqual("string", source_item["type"])
        self.assertEqual(1, source_item["minLength"])
        for identity_constraint in ("pattern", "format", "enum", "const"):
            self.assertNotIn(identity_constraint, source_item)


if __name__ == "__main__":
    unittest.main()
