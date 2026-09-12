from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from axm_institution.identity import (
    ContractValidationError,
    ImmutableReferenceError,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "valid.json"
ADVERSARIAL_PATH = ROOT / "adversarial" / "fixtures" / "STAGE3_EXACT_LIFECYCLE_BASE_GAPS.json"
ANCHOR_ADVERSARIAL_PATH = ROOT / "adversarial" / "fixtures" / "STAGE3_REGEX_ANCHOR_CONTINUITY_GAPS.json"
SCHEMA_DIR = ROOT / "schemas"

LIFECYCLE_SCHEMAS = (
    "occupancy.schema.json",
    "work-claim.schema.json",
    "return-packet.schema.json",
)

TRUE_END = r"(?![\s\S])"
STATE_REVISION_ID_PATTERN = r"^[a-z0-9][a-z0-9._-]*(?![\s\S])"
STATE_REVISION_REF_PATTERN = (
    r"^axmref:v1:state-revision:[a-z0-9][a-z0-9._-]*:-:sha256:[0-9a-f]{64}(?![\s\S])"
)
UNRESERVED_ASCII = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
LOGICAL_ID_FIRST = "abcdefghijklmnopqrstuvwxyz0123456789"
LOGICAL_ID_REST = LOGICAL_ID_FIRST + "._-"


class ExactLifecycleBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.adversarial = json.loads(ADVERSARIAL_PATH.read_text(encoding="utf-8"))
        cls.anchor_adversarial = json.loads(ANCHOR_ADVERSARIAL_PATH.read_text(encoding="utf-8"))

    def immutable_ref(self, schema_name: str, value=None) -> str:
        instance = self.valid[schema_name] if value is None else value
        return make_immutable_ref(schema_name, instance)

    def same_logical_revision_refs(self) -> tuple[str, str]:
        first = copy.deepcopy(self.valid["state-revision.schema.json"])
        second = copy.deepcopy(first)
        first["id"] = "revision.same-logical-id"
        second["id"] = "revision.same-logical-id"
        first["uncertainties"] = ["Witness A for exact lifecycle-base semantics."]
        second["uncertainties"] = ["Witness B differs while retaining the same logical revision id."]
        validate_instance(first, "state-revision.schema.json")
        validate_instance(second, "state-revision.schema.json")
        first_ref = self.immutable_ref("state-revision.schema.json", first)
        second_ref = self.immutable_ref("state-revision.schema.json", second)
        self.assertEqual(parse_immutable_ref(first_ref).logical_id, "revision.same-logical-id")
        self.assertEqual(parse_immutable_ref(second_ref).logical_id, "revision.same-logical-id")
        self.assertNotEqual(first_ref, second_ref)
        return first_ref, second_ref

    def assert_lifecycle_contracts_reject(self, reference: str) -> None:
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name, reference=reference):
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["base_state_revision_ref"] = reference
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)

    def assert_lifecycle_contracts_accept(self, reference: str) -> None:
        parsed = parse_immutable_ref(reference)
        self.assertEqual(parsed.kind, "state-revision")
        self.assertIsNone(parsed.version)
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name, reference=reference):
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["base_state_revision_ref"] = reference
                validate_instance(candidate, schema_name)

    def test_same_logical_revision_id_can_name_distinct_exact_instances(self):
        first_ref, second_ref = self.same_logical_revision_refs()
        self.assertEqual(parse_immutable_ref(first_ref).kind, "state-revision")
        self.assertEqual(parse_immutable_ref(second_ref).kind, "state-revision")

    def test_exact_base_substitution_changes_each_lifecycle_object_identity(self):
        first_ref, second_ref = self.same_logical_revision_refs()
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                first = copy.deepcopy(self.valid[schema_name])
                second = copy.deepcopy(first)
                first["base_state_revision_ref"] = first_ref
                second["base_state_revision_ref"] = second_ref
                validate_instance(first, schema_name)
                validate_instance(second, schema_name)
                self.assertNotEqual(
                    self.immutable_ref(schema_name, first),
                    self.immutable_ref(schema_name, second),
                )

    def test_bare_logical_revision_ids_are_rejected(self):
        self.assert_lifecycle_contracts_reject("revision.same-logical-id")

    def test_wrong_kind_immutable_refs_are_rejected(self):
        wrong_kind_ref = self.immutable_ref("objective.schema.json")
        self.assertEqual(parse_immutable_ref(wrong_kind_ref).kind, "objective")
        self.assert_lifecycle_contracts_reject(wrong_kind_ref)

    def test_contract_upgrade_is_narrow_and_visible(self):
        legacy_property_sets = {
            "occupancy.schema.json": {
                "schema_version", "id", "lane_id", "actor_ref", "base_state_revision",
                "capability_ref", "started_at", "ended_at", "status", "claim_ids",
            },
            "work-claim.schema.json": {
                "schema_version", "id", "lane_id", "base_state_revision", "occupancy_id",
                "summary", "created_at", "status", "scope_refs", "overlap_with_claim_ids", "notes",
            },
            "return-packet.schema.json": {
                "schema_version", "id", "claim_id", "lane_id", "base_state_revision", "changes",
                "artifacts_created", "artifacts_modified", "evidence_refs", "uncertainties",
                "failures_or_blockers", "downstream_effects", "requested_followup",
            },
        }
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
                expected = set(legacy_property_sets[schema_name])
                expected.remove("base_state_revision")
                expected.add("base_state_revision_ref")
                self.assertEqual(schema["properties"]["schema_version"]["const"], "0.2")
                self.assertEqual(set(schema["properties"]), expected)
                self.assertIn("base_state_revision_ref", schema["required"])
                self.assertNotIn("base_state_revision", schema["properties"])
                validate_instance(self.valid[schema_name], schema_name)

        packet = self.valid["return-packet.schema.json"]
        for preserved in (
            "evidence_refs", "uncertainties", "failures_or_blockers",
            "downstream_effects", "requested_followup",
        ):
            self.assertIn(preserved, packet)

    def test_legacy_v01_base_field_is_rejected_without_compatibility_fallback(self):
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["schema_version"] = "0.1"
                candidate["base_state_revision"] = candidate.pop("base_state_revision_ref")
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)

    def test_adv_026_a_counterexample_is_rejected_at_contract_boundary(self):
        oracle = self.adversarial["exact_ref_contract_oracles"][0]
        self.assertEqual(oracle["oracle_id"], "ADV-026-A")
        reference = oracle["counterexample_ref"]
        with self.assertRaises(ImmutableReferenceError):
            parse_immutable_ref(reference)
        self.assert_lifecycle_contracts_reject(reference)

    def test_all_percent_encoded_unreserved_ascii_is_rejected(self):
        digest = "2" * 64
        for char in UNRESERVED_ASCII:
            encoded = f"%{ord(char):02X}"
            reference = (
                "axmref:v1:state-revision:revision"
                + encoded
                + "fixture:-:sha256:"
                + digest
            )
            with self.subTest(char=char, reference=reference):
                with self.assertRaises(ImmutableReferenceError):
                    parse_immutable_ref(reference)
                self.assert_lifecycle_contracts_reject(reference)

    def test_adv_028_a_trailing_lf_state_revision_id_is_rejected(self):
        oracle = self.anchor_adversarial["oracles"][0]
        self.assertEqual(oracle["oracle_id"], "ADV-028-A")
        candidate = copy.deepcopy(self.valid["state-revision.schema.json"])
        candidate["id"] = oracle["counterexample_state_revision_id_json"]
        with self.assertRaises(ContractValidationError):
            validate_instance(candidate, "state-revision.schema.json")

        schema = json.loads((SCHEMA_DIR / "state-revision.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["id"]["pattern"], STATE_REVISION_ID_PATTERN)
        self.assertNotIn("$", STATE_REVISION_ID_PATTERN)
        self.assertTrue(STATE_REVISION_ID_PATTERN.endswith(TRUE_END))

    def test_adv_028_b_trailing_lf_lifecycle_ref_is_rejected(self):
        oracle = self.anchor_adversarial["oracles"][1]
        self.assertEqual(oracle["oracle_id"], "ADV-028-B")
        reference = oracle["counterexample_ref_json"]
        with self.assertRaises(ImmutableReferenceError):
            parse_immutable_ref(reference)
        self.assert_lifecycle_contracts_reject(reference)

    def test_true_end_assertion_rejects_extra_line_terminators_and_suffix_data(self):
        reference = self.immutable_ref("state-revision.schema.json")
        for suffix in ("\n", "\r", "\u2028", "\u2029", "x", "0"):
            with self.subTest(suffix=repr(suffix)):
                self.assert_lifecycle_contracts_reject(reference + suffix)

    def test_current_state_revision_id_alphabet_crosses_lifecycle_boundary(self):
        base = copy.deepcopy(self.valid["state-revision.schema.json"])

        for char in LOGICAL_ID_FIRST:
            with self.subTest(position="first", char=char):
                revision = copy.deepcopy(base)
                revision["id"] = char + "revision"
                validate_instance(revision, "state-revision.schema.json")
                self.assert_lifecycle_contracts_accept(
                    self.immutable_ref("state-revision.schema.json", revision)
                )

        for char in LOGICAL_ID_REST:
            with self.subTest(position="rest", char=char):
                revision = copy.deepcopy(base)
                revision["id"] = "revision.a" + char + "z"
                validate_instance(revision, "state-revision.schema.json")
                self.assert_lifecycle_contracts_accept(
                    self.immutable_ref("state-revision.schema.json", revision)
                )

    def test_lifecycle_pattern_matches_refs_produced_by_valid_state_revisions(self):
        revision = copy.deepcopy(self.valid["state-revision.schema.json"])
        revision["id"] = "revision.a_b-c0"
        validate_instance(revision, "state-revision.schema.json")
        reference = self.immutable_ref("state-revision.schema.json", revision)
        self.assertEqual(parse_immutable_ref(reference).kind, "state-revision")
        self.assertNotIn("%", reference)
        self.assertIn(":-:sha256:", reference)

        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
                self.assertEqual(
                    schema["properties"]["base_state_revision_ref"]["pattern"],
                    STATE_REVISION_REF_PATTERN,
                )
                self.assertNotIn("$", STATE_REVISION_REF_PATTERN)
                self.assertTrue(STATE_REVISION_REF_PATTERN.endswith(TRUE_END))
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["base_state_revision_ref"] = reference
                validate_instance(candidate, schema_name)


if __name__ == "__main__":
    unittest.main()
