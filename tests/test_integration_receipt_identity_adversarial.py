from __future__ import annotations

import copy
import json
import unittest
from dataclasses import asdict
from pathlib import Path

from axm_institution.identity import ContractValidationError, validate_instance
from axm_institution.integration_receipt_identity import (
    HistoricalReceiptInsufficientError,
    validate_exact_integration_receipt_identity,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "contracts"


def exact_ref(kind: str, logical_id: str, digest_char: str) -> str:
    return f"axmref:v1:{kind}:{logical_id}:-:sha256:" + digest_char * 64


class Decision025AdversarialContinuityTests(unittest.TestCase):
    """Lane 03 bounded adversarial checks for Decision 025 only."""

    def setUp(self) -> None:
        self.base_ref = exact_ref("state-revision", "revision.fixture.0001", "2")
        self.packet_a = exact_ref("return-packet", "packet.same-logical", "a")
        self.packet_b = exact_ref("return-packet", "packet.same-logical", "b")

    def root_grounding(self):
        return [
            {"root": "truth", "assessment": "grounded", "reason": "Exact inputs remain explicit."},
            {"root": "agency_non_domination", "assessment": "grounded", "reason": "No actor identity grants authority."},
            {"root": "continuity", "assessment": "grounded", "reason": "Exact receipt inputs remain reconstructable."},
            {"root": "wisdom_before_speed", "assessment": "grounded", "reason": "No successor mutation occurs here."},
        ]

    def receipt(self, *, base_ref=None, packet_refs=None):
        return {
            "schema_version": "0.2",
            "id": "receipt.lane03.adv060",
            "base_state_revision_ref": self.base_ref if base_ref is None else base_ref,
            "packet_refs": [self.packet_a] if packet_refs is None else packet_refs,
            "decision": "accepted",
            "reasons": ["Bounded Decision 025 adversarial fixture."],
            "root_grounding": self.root_grounding(),
            "unresolved_conflicts": [],
            "created_at": "2026-09-15T13:27:00Z",
        }

    def test_same_logical_different_exact_packets_survive_together_without_substitution(self):
        resolved = validate_exact_integration_receipt_identity(
            self.receipt(packet_refs=[self.packet_a, self.packet_b])
        )

        self.assertEqual(len(resolved.packet_refs), 2)
        self.assertEqual(resolved.packet_refs[0].logical_id, resolved.packet_refs[1].logical_id)
        self.assertNotEqual(resolved.packet_refs[0].sha256, resolved.packet_refs[1].sha256)
        self.assertEqual(str(resolved.packet_refs[0]), self.packet_a)
        self.assertEqual(str(resolved.packet_refs[1]), self.packet_b)

    def test_duplicate_exact_packet_membership_stays_rejected_after_json_materialization(self):
        materialized = json.loads(
            json.dumps(self.receipt(packet_refs=[self.packet_a, self.packet_a]))
        )
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(materialized)

    def test_wrong_kind_and_noncanonical_refs_do_not_gain_fallback_authority(self):
        wrong_kind_base = exact_ref("return-packet", "revision.fixture.0001", "2")
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(self.receipt(base_ref=wrong_kind_base))

        wrong_kind_packet = exact_ref("artifact", "packet.same-logical", "a")
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(
                self.receipt(packet_refs=[wrong_kind_packet])
            )

        noncanonical_packet = (
            "axmref:v1:return-packet:packete%cc%81:-:sha256:" + "a" * 64
        )
        with self.assertRaises(ContractValidationError):
            validate_exact_integration_receipt_identity(
                self.receipt(packet_refs=[noncanonical_packet])
            )

    def test_hidden_current_head_or_actor_fields_are_rejected_not_used_as_identity(self):
        for field, value in (
            ("current_state_revision_ref", self.base_ref),
            ("head", "main"),
            ("actor_id", "lane-03"),
        ):
            with self.subTest(field=field):
                widened = self.receipt()
                widened[field] = value
                with self.assertRaises(ContractValidationError):
                    validate_exact_integration_receipt_identity(widened)

    def test_successor_identity_fields_cannot_reappear_in_v02(self):
        successor_ref = exact_ref("state-revision", "revision.successor.0002", "9")
        for field, value in (
            ("resulting_state_revision", "revision.successor.0002"),
            ("resulting_state_revision_ref", successor_ref),
            ("successor_state_revision_ref", successor_ref),
        ):
            with self.subTest(field=field):
                widened = self.receipt()
                widened[field] = value
                with self.assertRaises(ContractValidationError):
                    validate_exact_integration_receipt_identity(widened)

    def test_historical_v01_remains_readable_but_cannot_cross_exact_identity_gate(self):
        fixtures = json.loads((FIXTURE_DIR / "valid.json").read_text(encoding="utf-8"))
        historical = copy.deepcopy(fixtures["integration-receipt.schema.json"])

        validate_instance(historical, "integration-receipt.schema.json")
        with self.assertRaises(HistoricalReceiptInsufficientError):
            validate_exact_integration_receipt_identity(historical)

    def test_standard_named_materialization_preserves_exact_identity_components(self):
        resolved = validate_exact_integration_receipt_identity(
            self.receipt(packet_refs=[self.packet_a, self.packet_b])
        )
        transported = json.loads(json.dumps(asdict(resolved)))

        self.assertEqual(transported["base_state_revision_ref"]["kind"], "state-revision")
        self.assertEqual(transported["base_state_revision_ref"]["sha256"], "2" * 64)
        self.assertEqual(transported["packet_refs"][0]["kind"], "return-packet")
        self.assertEqual(transported["packet_refs"][0]["sha256"], "a" * 64)
        self.assertEqual(transported["packet_refs"][1]["sha256"], "b" * 64)
        self.assertTrue(transported["immutable_ref"].startswith("axmref:v1:integration-receipt:"))


if __name__ == "__main__":
    unittest.main()
