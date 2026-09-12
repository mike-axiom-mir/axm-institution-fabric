from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from axm_institution.identity import (
    ContractValidationError,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "valid.json"
SCHEMA_DIR = ROOT / "schemas"

LIFECYCLE_SCHEMAS = (
    "occupancy.schema.json",
    "work-claim.schema.json",
    "return-packet.schema.json",
)


class ExactLifecycleBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

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
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["base_state_revision_ref"] = "revision.same-logical-id"
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)

    def test_wrong_kind_immutable_refs_are_rejected(self):
        wrong_kind_ref = self.immutable_ref("objective.schema.json")
        self.assertEqual(parse_immutable_ref(wrong_kind_ref).kind, "objective")
        for schema_name in LIFECYCLE_SCHEMAS:
            with self.subTest(schema=schema_name):
                candidate = copy.deepcopy(self.valid[schema_name])
                candidate["base_state_revision_ref"] = wrong_kind_ref
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)

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


if __name__ == "__main__":
    unittest.main()
