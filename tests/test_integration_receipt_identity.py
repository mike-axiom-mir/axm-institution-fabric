from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError, validate_instance
from axm_institution.integration_receipt_identity import (
    HistoricalReceiptInsufficientError,
    validate_exact_integration_receipt_identity,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "contracts"


def exact_ref(kind: str, logical_id: str, digest_char: str) -> str:
    return (
        f"axmref:v1:{kind}:{logical_id}:-:sha256:"
        + digest_char * 64
    )


class IntegrationReceiptIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_ref = exact_ref("state-revision", "revision.fixture.0001", "2")
        self.packet_ref = exact_ref("return-packet", "packet.lane-02.activation-02", "1")

    def root_grounding(self):
        return [
            {"root": "truth", "assessment": "grounded", "reason": "Exact inputs remain explicit."},
            {"root": "agency_non_domination", "assessment": "grounded", "reason": "No actor identity grants authority."},
            {"root": "continuity", "assessment": "grounded", "reason": "The receipt preserves exact input identity."},
            {"root": "wisdom_before_speed", "assessment": "grounded", "reason": "No successor mutation is performed here."},
        ]

    def receipt(self, *, base_ref=None, packet_refs=None, decision="accepted"):
        return {
            "schema_version": "0.2",
            "id": "receipt.fixture.0002",
            "base_state_revision_ref": self.base_ref if base_ref is None else base_ref,
            "packet_refs": [self.packet_ref] if packet_refs is None else packet_refs,
            "decision": decision,
            "reasons": ["Decision 025 exact inputs are recorded without publishing a successor."],
            "root_grounding": self.root_grounding(),
            "unresolved_conflicts": [],
            "created_at": "2026-09-15T13:10:00Z",
        }

    def test_v02_accepts_exact_base_and_packet_refs_deterministically(self):
        receipt = self.receipt()
        first = validate_exact_integration_receipt_identity(receipt)
        second = validate_exact_integration_receipt_identity(copy.deepcopy(receipt))

        self.assertEqual(first, second)
        self.assertEqual(first.base_state_revision_ref.kind, "state-revision")
        self.assertEqual(first.packet_refs[0].kind, "return-packet")
        self.assertEqual(len(first.canonical_sha256), 64)
        self.assertTrue(first.immutable_ref.startswith("axmref:v1:integration-receipt:"))

    def test_historical_v01_remains_readable_but_is_not_exact_stage5_proof(self):
        fixtures = json.loads((FIXTURE_DIR / "valid.json").read_text(encoding="utf-8"))
        historical = fixtures["integration-receipt.schema.json"]

        self.assertIs(validate_instance(historical, "integration-receipt.schema.json"), historical)
        with self.assertRaises(HistoricalReceiptInsufficientError):
            validate_exact_integration_receipt_identity(historical)

    def test_logical_or_generic_base_revision_is_rejected(self):
        receipt = self.receipt(base_ref="revision.fixture.0001")
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(receipt)

    def test_logical_packet_id_is_rejected(self):
        receipt = self.receipt(packet_refs=["packet.lane-02.activation-02"])
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(receipt)

    def test_wrong_kind_references_are_rejected(self):
        wrong_base = exact_ref("return-packet", "revision.fixture.0001", "2")
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(self.receipt(base_ref=wrong_base))

        wrong_packet = exact_ref("artifact", "packet.lane-02.activation-02", "1")
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(self.receipt(packet_refs=[wrong_packet]))

    def test_noncanonical_reference_components_fail_closed_through_shared_parser(self):
        non_nfc_base = (
            "axmref:v1:state-revision:revisione%CC%81:-:sha256:" + "2" * 64
        )
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(self.receipt(base_ref=non_nfc_base))

        non_nfc_packet = (
            "axmref:v1:return-packet:packete%CC%81:-:sha256:" + "1" * 64
        )
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(self.receipt(packet_refs=[non_nfc_packet]))

    def test_same_logical_packet_id_with_different_exact_identity_stays_distinct(self):
        packet_a = exact_ref("return-packet", "packet.same-logical-id", "a")
        packet_b = exact_ref("return-packet", "packet.same-logical-id", "b")

        identity_a = validate_exact_integration_receipt_identity(self.receipt(packet_refs=[packet_a]))
        identity_b = validate_exact_integration_receipt_identity(self.receipt(packet_refs=[packet_b]))

        self.assertEqual(identity_a.packet_refs[0].logical_id, identity_b.packet_refs[0].logical_id)
        self.assertNotEqual(identity_a.packet_refs[0].sha256, identity_b.packet_refs[0].sha256)
        self.assertNotEqual(identity_a.canonical_sha256, identity_b.canonical_sha256)
        self.assertNotEqual(identity_a.immutable_ref, identity_b.immutable_ref)

    def test_duplicate_exact_packet_refs_are_rejected(self):
        receipt = self.receipt(packet_refs=[self.packet_ref, self.packet_ref])
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(receipt)

    def test_v02_carries_no_successor_state_reference(self):
        validate_exact_integration_receipt_identity(self.receipt())

        for field in ("resulting_state_revision", "resulting_state_revision_ref"):
            with self.subTest(field=field):
                widened = self.receipt()
                widened[field] = exact_ref("state-revision", "revision.successor.0002", "9")
                with self.assertRaises(ContractValidationError):
                    validate_exact_integration_receipt_identity(widened)

    def test_one_way_successor_contract_can_reference_receipt(self):
        exact_receipt = validate_exact_integration_receipt_identity(self.receipt())
        successor = {
            "schema_version": "0.2",
            "id": "revision.successor.0002",
            "parent_revision_ref": self.base_ref,
            "objective_ref": exact_ref("objective", "objective.v0-proof", "a"),
            "lane_refs": [],
            "occupancy_refs": [],
            "claim_refs": [],
            "artifact_refs": [],
            "evidence_refs": [],
            "return_packet_refs": [],
            "integration_receipt_refs": [exact_receipt.immutable_ref],
            "uncertainties": ["Contract chronology evidence only; no successor publication runtime is implemented."],
            "created_at": "2026-09-15T13:11:00Z",
        }

        validate_instance(successor, "state-revision.schema.json")
        self.assertEqual(successor["parent_revision_ref"], self.base_ref)
        self.assertEqual(successor["integration_receipt_refs"], [exact_receipt.immutable_ref])
        self.assertNotIn("resulting_state_revision_ref", self.receipt())


if __name__ == "__main__":
    unittest.main()
