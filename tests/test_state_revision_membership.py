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


class ExactRevisionMembershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def immutable_ref(self, schema_name: str, value=None) -> str:
        instance = self.valid[schema_name] if value is None else value
        return make_immutable_ref(schema_name, instance)

    def revision(self, *, objective_ref=None, lane_refs=None, parent_revision_ref=None):
        return {
            "schema_version": "0.2",
            "id": "revision.membership.fixture",
            "parent_revision_ref": parent_revision_ref,
            "objective_ref": objective_ref or self.immutable_ref("objective.schema.json"),
            "lane_refs": lane_refs or [self.immutable_ref("lane.schema.json")],
            "occupancy_refs": [self.immutable_ref("occupancy.schema.json")],
            "claim_refs": [self.immutable_ref("work-claim.schema.json")],
            "artifact_refs": [self.immutable_ref("artifact.schema.json")],
            "evidence_refs": [self.immutable_ref("evidence-record.schema.json")],
            "return_packet_refs": [self.immutable_ref("return-packet.schema.json")],
            "integration_receipt_refs": [self.immutable_ref("integration-receipt.schema.json")],
            "uncertainties": ["Fixture proves exact membership contract semantics, not persistence."],
            "created_at": "2026-09-12T18:00:00Z",
        }

    def test_same_logical_objective_id_different_content_has_different_ref(self):
        first = copy.deepcopy(self.valid["objective.schema.json"])
        second = copy.deepcopy(first)
        second["desired_outcome"] = "A different desired outcome under the same logical id."
        self.assertEqual(first["id"], second["id"])
        self.assertNotEqual(
            self.immutable_ref("objective.schema.json", first),
            self.immutable_ref("objective.schema.json", second),
        )

    def test_objective_ref_substitution_changes_revision_identity(self):
        first = copy.deepcopy(self.valid["objective.schema.json"])
        second = copy.deepcopy(first)
        second["desired_outcome"] = "A different desired outcome under the same logical id."
        first_revision = self.revision(
            objective_ref=self.immutable_ref("objective.schema.json", first)
        )
        second_revision = self.revision(
            objective_ref=self.immutable_ref("objective.schema.json", second)
        )
        validate_instance(first_revision, "state-revision.schema.json")
        validate_instance(second_revision, "state-revision.schema.json")
        self.assertNotEqual(
            self.immutable_ref("state-revision.schema.json", first_revision),
            self.immutable_ref("state-revision.schema.json", second_revision),
        )

    def test_same_logical_lane_id_different_content_cannot_collapse(self):
        first = copy.deepcopy(self.valid["lane.schema.json"])
        second = copy.deepcopy(first)
        second["purpose"] = "Different professional contract under the same logical lane id."
        first_ref = self.immutable_ref("lane.schema.json", first)
        second_ref = self.immutable_ref("lane.schema.json", second)
        self.assertEqual(first["id"], second["id"])
        self.assertNotEqual(first_ref, second_ref)
        first_revision = self.revision(lane_refs=[first_ref])
        second_revision = self.revision(lane_refs=[second_ref])
        self.assertNotEqual(
            self.immutable_ref("state-revision.schema.json", first_revision),
            self.immutable_ref("state-revision.schema.json", second_revision),
        )

    def test_parent_revision_requires_exact_state_revision_ref(self):
        parent = self.revision()
        parent["id"] = "revision.parent.fixture"
        parent_ref = self.immutable_ref("state-revision.schema.json", parent)
        child = self.revision(parent_revision_ref=parent_ref)
        validate_instance(child, "state-revision.schema.json")
        self.assertEqual(parse_immutable_ref(child["parent_revision_ref"]).kind, "state-revision")

        child["parent_revision_ref"] = parent["id"]
        with self.assertRaises(ContractValidationError):
            validate_instance(child, "state-revision.schema.json")

    def test_duplicate_exact_membership_refs_are_rejected(self):
        array_fields = (
            "lane_refs",
            "occupancy_refs",
            "claim_refs",
            "artifact_refs",
            "evidence_refs",
            "return_packet_refs",
            "integration_receipt_refs",
        )
        for field in array_fields:
            with self.subTest(field=field):
                candidate = self.revision()
                candidate[field] = [candidate[field][0], candidate[field][0]]
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, "state-revision.schema.json")

    def test_all_revision_membership_fields_are_typed_exact_refs(self):
        revision = self.revision()
        validate_instance(revision, "state-revision.schema.json")
        expected_kinds = {
            "objective_ref": "objective",
            "lane_refs": "lane",
            "occupancy_refs": "occupancy",
            "claim_refs": "work-claim",
            "artifact_refs": "artifact",
            "evidence_refs": "evidence-record",
            "return_packet_refs": "return-packet",
            "integration_receipt_refs": "integration-receipt",
        }
        for field, expected_kind in expected_kinds.items():
            values = revision[field] if isinstance(revision[field], list) else [revision[field]]
            for reference in values:
                with self.subTest(field=field, reference=reference):
                    parsed = parse_immutable_ref(reference)
                    self.assertEqual(parsed.kind, expected_kind)
                    self.assertEqual(str(parsed), reference)

    def test_legacy_logical_membership_shape_is_rejected(self):
        legacy = {
            "schema_version": "0.1",
            "id": "revision.legacy",
            "parent_revision_id": None,
            "objective_id": "objective.v0-proof",
            "lane_ids": ["lane-02"],
            "occupancy_ids": [],
            "claim_ids": [],
            "artifact_refs": [],
            "evidence_refs": [],
            "return_packet_ids": [],
            "integration_receipt_ids": [],
            "uncertainties": ["Legacy membership is intentionally under-bound."],
            "created_at": "2026-09-12T18:00:00Z",
        }
        with self.assertRaises(ContractValidationError):
            validate_instance(legacy, "state-revision.schema.json")


if __name__ == "__main__":
    unittest.main()
