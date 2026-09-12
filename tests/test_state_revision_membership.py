from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from axm_institution.identity import (
    ContractValidationError,
    ImmutableRef,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "valid.json"

FIELD_KINDS = {
    "parent_revision_ref": "state-revision",
    "objective_ref": "objective",
    "lane_refs": "lane",
    "occupancy_refs": "occupancy",
    "claim_refs": "work-claim",
    "artifact_refs": "artifact",
    "evidence_refs": "evidence-record",
    "return_packet_refs": "return-packet",
    "integration_receipt_refs": "integration-receipt",
}
ARRAY_REF_FIELDS = frozenset(FIELD_KINDS) - {"parent_revision_ref", "objective_ref"}
UNRESERVED_TEXT = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
DIGEST = "a" * 64


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

    def set_member_ref(self, revision, field: str, reference: str) -> None:
        if field in ARRAY_REF_FIELDS:
            revision[field] = [reference]
        else:
            revision[field] = reference

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

    def test_member_fields_accept_parser_canonical_percent_encoded_components(self):
        for field, kind in FIELD_KINDS.items():
            with self.subTest(field=field):
                reference = str(
                    ImmutableRef(
                        kind=kind,
                        logical_id="member café:/?",
                        version="v 1/β",
                        sha256=DIGEST,
                    )
                )
                parsed = parse_immutable_ref(reference)
                self.assertEqual(str(parsed), reference)
                self.assertEqual(parsed.kind, kind)
                candidate = self.revision()
                self.set_member_ref(candidate, field, reference)
                validate_instance(candidate, "state-revision.schema.json")

    def test_adv029a_percent_encoded_unreserved_bytes_are_rejected_everywhere(self):
        for field, kind in FIELD_KINDS.items():
            canonical = f"axmref:v1:{kind}:{UNRESERVED_TEXT}:-:sha256:{DIGEST}"
            self.assertEqual(str(parse_immutable_ref(canonical)), canonical)
            accepted = self.revision()
            self.set_member_ref(accepted, field, canonical)
            validate_instance(accepted, "state-revision.schema.json")

            for index, character in enumerate(UNRESERVED_TEXT):
                encoded = f"%{ord(character):02X}"
                bad_component = UNRESERVED_TEXT[:index] + encoded + UNRESERVED_TEXT[index + 1 :]
                noncanonical = f"axmref:v1:{kind}:{bad_component}:-:sha256:{DIGEST}"
                with self.subTest(field=field, character=character, reference=noncanonical):
                    with self.assertRaises(Exception):
                        parse_immutable_ref(noncanonical)
                    candidate = self.revision()
                    self.set_member_ref(candidate, field, noncanonical)
                    with self.assertRaises(ContractValidationError):
                        validate_instance(candidate, "state-revision.schema.json")

    def test_adv029b_final_lf_and_trailing_data_are_rejected_everywhere(self):
        suffixes = ("\n", "\r", "x", "\u2028", "\u2029")
        for field, kind in FIELD_KINDS.items():
            canonical = f"axmref:v1:{kind}:member.v0:-:sha256:{DIGEST}"
            for suffix in suffixes:
                with self.subTest(field=field, suffix=repr(suffix)):
                    candidate = self.revision()
                    self.set_member_ref(candidate, field, canonical + suffix)
                    with self.assertRaises(ContractValidationError):
                        validate_instance(candidate, "state-revision.schema.json")

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
