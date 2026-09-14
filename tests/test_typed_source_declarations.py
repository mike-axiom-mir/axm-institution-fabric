from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from axm_institution.identity import (
    ContractValidationError,
    make_immutable_ref,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "typed_source_declarations.json"

EXACT_BASE_REF = (
    "axmref:v1:state-revision:revision.fixture.0001:-:sha256:"
    + "c" * 64
)
EXACT_ARTIFACT_REF = (
    "axmref:v1:artifact:artifact.source:v=1:sha256:"
    + "a" * 64
)
NONCANONICAL_EXACT_REF = (
    "axmref:v1:artifact:artifact%2Esource:v=1:sha256:"
    + "a" * 64
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def typed_artifact(source_declarations: dict, *, artifact_id: str = "artifact.typed-source") -> dict:
    return {
        "schema_version": "0.4",
        "id": artifact_id,
        "type": "typed_source_fixture",
        "version": "1",
        "content_ref": "fixtures/contracts/typed_source_declarations.json",
        "provenance": {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": EXACT_BASE_REF,
            "source_declarations": source_declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def typed_evidence(
    source_declarations: dict | None,
    *,
    state: str = "automated_tested",
    evidence_id: str = "evidence.typed-source",
) -> dict:
    value = {
        "schema_version": "0.2",
        "id": evidence_id,
        "subject_ref": EXACT_ARTIFACT_REF,
        "state": state,
        "claim": "Decision 020 typed source declaration contract fixture.",
    }
    if state in {
        "compiled",
        "automated_tested",
        "runtime_tested",
        "visually_inspected",
        "playtested",
        "measured",
    }:
        value["method"] = "deterministic contract regression"
    if source_declarations is not None:
        value["source_declarations"] = source_declarations
    return value


class TypedSourceDeclarationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_json(FIXTURE_PATH)
        cls.declaration_schema = load_json(SCHEMA_DIR / "source-declaration.schema.json")
        Draft202012Validator.check_schema(cls.declaration_schema)
        cls.declaration_validator = Draft202012Validator(cls.declaration_schema)

    def test_shared_contract_accepts_all_four_explicit_classes(self):
        expected = {"opaque", "exact", "content", "locator"}
        self.assertEqual(expected, set(self.fixture["valid_declarations"]))
        for name, declaration in self.fixture["valid_declarations"].items():
            with self.subTest(name=name):
                self.assertEqual([], list(self.declaration_validator.iter_errors(declaration)))

    def test_shared_contract_rejects_invalid_or_mixed_class_payloads(self):
        for case in self.fixture["invalid_declarations"]:
            with self.subTest(case=case["case"]):
                self.assertTrue(
                    list(self.declaration_validator.iter_errors(case["declaration"])),
                    case["case"],
                )

    def test_artifact_v04_validates_all_four_classes_through_shared_contract(self):
        artifact = typed_artifact(copy.deepcopy(self.fixture["valid_declarations"]))
        self.assertEqual(artifact, validate_instance(artifact, "artifact.schema.json"))

    def test_strong_evidence_v02_accepts_typed_source_presence_only(self):
        evidence = typed_evidence({"suite": copy.deepcopy(self.fixture["valid_declarations"]["locator"])})
        self.assertEqual(evidence, validate_instance(evidence, "evidence-record.schema.json"))
        self.assertNotIn("integrity", evidence)
        self.assertNotIn("trusted", evidence)
        self.assertNotIn("accepted", evidence)

    def test_strong_evidence_v02_requires_nonempty_typed_source_map(self):
        for declarations in (None, {}):
            with self.subTest(declarations=declarations):
                with self.assertRaises(ContractValidationError):
                    validate_instance(
                        typed_evidence(declarations),
                        "evidence-record.schema.json",
                    )

    def test_proposed_evidence_v02_does_not_require_sources_or_method(self):
        evidence = typed_evidence(None, state="proposed")
        self.assertNotIn("method", evidence)
        self.assertNotIn("source_declarations", evidence)
        self.assertEqual(evidence, validate_instance(evidence, "evidence-record.schema.json"))

    def test_typed_artifact_forbids_legacy_source_refs_dual_authority(self):
        artifact = typed_artifact({"source": copy.deepcopy(self.fixture["valid_declarations"]["opaque"])})
        artifact["provenance"]["source_refs"] = ["NEXT_BUILD.md"]
        with self.assertRaises(ContractValidationError):
            validate_instance(artifact, "artifact.schema.json")

    def test_typed_evidence_forbids_legacy_source_refs_dual_authority(self):
        evidence = typed_evidence({"source": copy.deepcopy(self.fixture["valid_declarations"]["opaque"])})
        evidence["source_refs"] = ["NEXT_BUILD.md"]
        with self.assertRaises(ContractValidationError):
            validate_instance(evidence, "evidence-record.schema.json")

    def test_historical_artifact_versions_reject_new_typed_field(self):
        for version in ("0.1", "0.2", "0.3"):
            with self.subTest(version=version):
                provenance = {
                    "producer_lane_id": "lane-02",
                    "source_refs": ["NEXT_BUILD.md"],
                    "source_declarations": {
                        "source": copy.deepcopy(self.fixture["valid_declarations"]["locator"])
                    },
                }
                if version == "0.1":
                    provenance["base_state_revision"] = "revision.fixture.0001"
                else:
                    provenance["base_state_revision_ref"] = EXACT_BASE_REF
                artifact = {
                    "schema_version": version,
                    "id": "artifact.historical-source",
                    "type": "historical_source_fixture",
                    "version": "1",
                    "content_ref": "NEXT_BUILD.md",
                    "provenance": provenance,
                    "evidence_refs": [],
                    "dependency_refs": [],
                }
                with self.assertRaises(ContractValidationError):
                    validate_instance(artifact, "artifact.schema.json")

    def test_historical_evidence_v01_rejects_new_typed_field(self):
        evidence = {
            "schema_version": "0.1",
            "id": "evidence.historical-source",
            "subject_ref": "artifact.historical-source",
            "state": "automated_tested",
            "claim": "Historical source strings remain historical.",
            "method": "compatibility regression",
            "source_refs": ["NEXT_BUILD.md"],
            "source_declarations": {
                "source": copy.deepcopy(self.fixture["valid_declarations"]["locator"])
            },
        }
        with self.assertRaises(ContractValidationError):
            validate_instance(evidence, "evidence-record.schema.json")

    def test_exact_looking_opaque_label_is_not_lexically_promoted(self):
        declaration = copy.deepcopy(self.fixture["valid_declarations"]["opaque"])
        self.assertTrue(declaration["token"].startswith("axmref:"))
        artifact = typed_artifact({"source": declaration})
        self.assertEqual(artifact, validate_instance(artifact, "artifact.schema.json"))

    def test_exact_axm_object_reuses_stage2_canonical_reference_parser(self):
        artifact = typed_artifact(
            {
                "source": {
                    "source_class": "exact_axm_object",
                    "object_ref": NONCANONICAL_EXACT_REF,
                }
            }
        )
        with self.assertRaisesRegex(ContractValidationError, "non-canonical"):
            validate_instance(artifact, "artifact.schema.json")

    def test_exact_axm_object_does_not_require_target_loading(self):
        declaration = {
            "source_class": "exact_axm_object",
            "object_ref": (
                "axmref:v1:artifact:artifact.not-present:v=404:sha256:" + "d" * 64
            ),
        }
        artifact = typed_artifact({"missing-but-declared": declaration})
        self.assertEqual(artifact, validate_instance(artifact, "artifact.schema.json"))

    def test_content_address_is_bounded_to_sha256_lowercase64_raw_bytes(self):
        good = copy.deepcopy(self.fixture["valid_declarations"]["content"])
        self.assertEqual([], list(self.declaration_validator.iter_errors(good)))
        mutations = (
            {**good, "algorithm": "sha512"},
            {**good, "digest": good["digest"].upper()},
            {**good, "digest": "a" * 63},
            {**good, "byte_scope": "canonical_json"},
        )
        for declaration in mutations:
            with self.subTest(declaration=declaration):
                with self.assertRaises(ContractValidationError):
                    validate_instance(
                        typed_artifact({"source": declaration}),
                        "artifact.schema.json",
                    )

    def test_locator_cannot_gain_integrity_or_content_fields(self):
        locator = copy.deepcopy(self.fixture["valid_declarations"]["locator"])
        for extra_key, extra_value in (
            ("digest", "b" * 64),
            ("algorithm", "sha256"),
            ("integrity_verified", True),
            ("resolved_ref", EXACT_ARTIFACT_REF),
        ):
            with self.subTest(extra_key=extra_key):
                declaration = {**locator, extra_key: extra_value}
                with self.assertRaises(ContractValidationError):
                    validate_instance(
                        typed_artifact({"source": declaration}),
                        "artifact.schema.json",
                    )

    def test_declaration_key_must_use_stable_id_spelling(self):
        artifact = typed_artifact(
            {"Source 1": copy.deepcopy(self.fixture["valid_declarations"]["opaque"])}
        )
        with self.assertRaises(ContractValidationError):
            validate_instance(artifact, "artifact.schema.json")

    def test_equal_target_text_under_distinct_keys_remains_two_occurrences(self):
        declaration = copy.deepcopy(self.fixture["valid_declarations"]["opaque"])
        artifact = typed_artifact(
            {"first": copy.deepcopy(declaration), "second": copy.deepcopy(declaration)}
        )
        validated = validate_instance(artifact, "artifact.schema.json")
        self.assertEqual({"first", "second"}, set(validated["provenance"]["source_declarations"]))

    def test_map_key_insertion_order_does_not_change_exact_containing_identity(self):
        first = typed_artifact(
            {
                "z-source": copy.deepcopy(self.fixture["valid_declarations"]["locator"]),
                "a-source": copy.deepcopy(self.fixture["valid_declarations"]["content"]),
            }
        )
        second = typed_artifact(
            {
                "a-source": copy.deepcopy(self.fixture["valid_declarations"]["content"]),
                "z-source": copy.deepcopy(self.fixture["valid_declarations"]["locator"]),
            }
        )
        self.assertEqual(
            make_immutable_ref("artifact.schema.json", first),
            make_immutable_ref("artifact.schema.json", second),
        )

    def test_same_declaration_key_in_distinct_containing_objects_does_not_collapse(self):
        declaration = copy.deepcopy(self.fixture["valid_declarations"]["locator"])
        first = typed_artifact({"source": copy.deepcopy(declaration)}, artifact_id="artifact.one")
        second = typed_artifact({"source": copy.deepcopy(declaration)}, artifact_id="artifact.two")
        first_ref = make_immutable_ref("artifact.schema.json", first)
        second_ref = make_immutable_ref("artifact.schema.json", second)
        self.assertNotEqual(first_ref, second_ref)
        self.assertIn("source", first["provenance"]["source_declarations"])
        self.assertIn("source", second["provenance"]["source_declarations"])

    def test_mixed_target_classes_fail_closed(self):
        mixed = {
            "source_class": "locator",
            "locator_context": "repository-relative",
            "locator": "NEXT_BUILD.md",
            "algorithm": "sha256",
            "digest": "b" * 64,
            "byte_scope": "raw_bytes",
        }
        with self.assertRaises(ContractValidationError):
            validate_instance(typed_artifact({"source": mixed}), "artifact.schema.json")

    def test_contract_exposes_no_resolution_association_trust_or_priority_fields(self):
        forbidden = {
            "resolved_ref",
            "resolved_bytes",
            "verified",
            "trusted",
            "priority",
            "associated_with",
            "accepted",
            "complete",
        }
        serialized = json.dumps(self.declaration_schema, sort_keys=True)
        for field in forbidden:
            with self.subTest(field=field):
                self.assertNotIn(f'"{field}"', serialized)


if __name__ == "__main__":
    unittest.main()
