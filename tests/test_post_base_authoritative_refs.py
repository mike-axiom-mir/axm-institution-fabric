from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import (
    ContractValidationError,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)
from axm_institution.store import FilesystemObjectStore

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "valid.json"
SCHEMA_DIR = ROOT / "schemas"


class PostBaseAuthoritativeReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def exact_ref(self, schema_name: str, value) -> str:
        return make_immutable_ref(schema_name, value)

    def base_revision(self):
        revision = copy.deepcopy(self.valid["state-revision.schema.json"])
        revision["id"] = "revision.post-base.0001"
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["return_packet_refs"] = []
        revision["uncertainties"] = [
            "Post-base chronology fixture intentionally excludes the later occupancy, claim, and packet."
        ]
        validate_instance(revision, "state-revision.schema.json")
        return revision

    def occupancy(self, base_ref: str, *, actor_ref: str, logical_id: str = "occupancy.same"):
        occupancy = copy.deepcopy(self.valid["occupancy.schema.json"])
        occupancy["id"] = logical_id
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["actor_ref"] = actor_ref
        occupancy["claim_ids"] = []
        validate_instance(occupancy, "occupancy.schema.json")
        return occupancy

    def claim(
        self,
        base_ref: str,
        occupancy_ref: str,
        *,
        summary: str,
        logical_id: str = "claim.same",
    ):
        claim = copy.deepcopy(self.valid["work-claim.schema.json"])
        claim["id"] = logical_id
        claim["base_state_revision_ref"] = base_ref
        claim["occupancy_ref"] = occupancy_ref
        claim["summary"] = summary
        validate_instance(claim, "work-claim.schema.json")
        return claim

    def packet(
        self,
        base_ref: str,
        claim_ref: str,
        *,
        logical_id: str = "packet.same",
    ):
        packet = copy.deepcopy(self.valid["return-packet.schema.json"])
        packet["id"] = logical_id
        packet["base_state_revision_ref"] = base_ref
        packet["claim_ref"] = claim_ref
        validate_instance(packet, "return-packet.schema.json")
        return packet

    def test_schema_upgrade_is_narrow_and_explicit(self):
        work_schema = json.loads((SCHEMA_DIR / "work-claim.schema.json").read_text(encoding="utf-8"))
        packet_schema = json.loads((SCHEMA_DIR / "return-packet.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(work_schema["properties"]["schema_version"]["const"], "0.3")
        self.assertIn("occupancy_ref", work_schema["required"])
        self.assertNotIn("occupancy_id", work_schema["properties"])
        self.assertEqual(work_schema["properties"]["occupancy_ref"], {"type": "string", "minLength": 1})
        self.assertIn("lane_id", work_schema["properties"])
        self.assertIn("overlap_with_claim_ids", work_schema["properties"])

        self.assertEqual(
            tuple(packet_schema["properties"]["schema_version"]["enum"]),
            ("0.3", "0.4"),
        )
        self.assertIn("claim_ref", packet_schema["required"])
        self.assertNotIn("claim_id", packet_schema["properties"])
        self.assertEqual(packet_schema["properties"]["claim_ref"], {"type": "string", "minLength": 1})
        self.assertIn("lane_id", packet_schema["properties"])
        for preserved in (
            "evidence_refs",
            "uncertainties",
            "failures_or_blockers",
            "downstream_effects",
            "requested_followup",
        ):
            self.assertIn(preserved, packet_schema["properties"])

    def test_legacy_logical_relationship_fields_are_rejected(self):
        work = copy.deepcopy(self.valid["work-claim.schema.json"])
        work["schema_version"] = "0.2"
        work["occupancy_id"] = "occupancy.lane-02.activation-02"
        work.pop("occupancy_ref")
        with self.assertRaises(ContractValidationError):
            validate_instance(work, "work-claim.schema.json")

        packet = copy.deepcopy(self.valid["return-packet.schema.json"])
        packet["schema_version"] = "0.2"
        packet["claim_id"] = "claim.lane-02.stage1-repair"
        packet.pop("claim_ref")
        with self.assertRaises(ContractValidationError):
            validate_instance(packet, "return-packet.schema.json")

    def test_bare_logical_ids_fail_shared_semantic_reference_validation(self):
        work = copy.deepcopy(self.valid["work-claim.schema.json"])
        work["occupancy_ref"] = "occupancy.logical-only"
        with self.assertRaisesRegex(ContractValidationError, "semantic reference validation"):
            validate_instance(work, "work-claim.schema.json")

        packet = copy.deepcopy(self.valid["return-packet.schema.json"])
        packet["claim_ref"] = "claim.logical-only"
        with self.assertRaisesRegex(ContractValidationError, "semantic reference validation"):
            validate_instance(packet, "return-packet.schema.json")

    def test_wrong_kind_refs_fail_shared_semantic_reference_validation(self):
        objective_ref = self.exact_ref(
            "objective.schema.json", self.valid["objective.schema.json"]
        )
        work = copy.deepcopy(self.valid["work-claim.schema.json"])
        work["occupancy_ref"] = objective_ref
        with self.assertRaisesRegex(ContractValidationError, "expected kind 'occupancy'"):
            validate_instance(work, "work-claim.schema.json")

        base_ref = self.exact_ref("state-revision.schema.json", self.base_revision())
        occupancy = self.occupancy(base_ref, actor_ref="fixture:wrong-kind")
        occupancy_ref = self.exact_ref("occupancy.schema.json", occupancy)
        packet = copy.deepcopy(self.valid["return-packet.schema.json"])
        packet["claim_ref"] = occupancy_ref
        with self.assertRaisesRegex(ContractValidationError, "expected kind 'work-claim'"):
            validate_instance(packet, "return-packet.schema.json")

    def test_noncanonical_reference_forms_fail_shared_semantic_parser(self):
        digest = "1" * 64
        cases = (
            "thing%2Eencoded",
            "%FF",
            "e%CC%81",
        )
        for field, schema_name, kind in (
            ("occupancy_ref", "work-claim.schema.json", "occupancy"),
            ("claim_ref", "return-packet.schema.json", "work-claim"),
        ):
            for encoded_id in cases:
                reference = f"axmref:v1:{kind}:{encoded_id}:-:sha256:{digest}"
                with self.subTest(field=field, encoded_id=encoded_id):
                    candidate = copy.deepcopy(self.valid[schema_name])
                    candidate[field] = reference
                    with self.assertRaisesRegex(
                        ContractValidationError, "semantic reference validation"
                    ):
                        validate_instance(candidate, schema_name)

            canonical = f"axmref:v1:{kind}:thing:-:sha256:{digest}"
            for suffix in ("\n", "\r", "x"):
                with self.subTest(field=field, suffix=repr(suffix)):
                    candidate = copy.deepcopy(self.valid[schema_name])
                    candidate[field] = canonical + suffix
                    with self.assertRaisesRegex(
                        ContractValidationError, "semantic reference validation"
                    ):
                        validate_instance(candidate, schema_name)

    def test_same_logical_occupancy_instances_change_work_claim_identity(self):
        base = self.base_revision()
        base_ref = self.exact_ref("state-revision.schema.json", base)
        occupancy_a = self.occupancy(base_ref, actor_ref="fixture:occupant-a")
        occupancy_b = self.occupancy(base_ref, actor_ref="fixture:occupant-b")
        ref_a = self.exact_ref("occupancy.schema.json", occupancy_a)
        ref_b = self.exact_ref("occupancy.schema.json", occupancy_b)
        self.assertEqual(parse_immutable_ref(ref_a).logical_id, "occupancy.same")
        self.assertEqual(parse_immutable_ref(ref_b).logical_id, "occupancy.same")
        self.assertNotEqual(ref_a, ref_b)

        claim_a = self.claim(base_ref, ref_a, summary="Same claim, occupancy instance A")
        claim_b = self.claim(base_ref, ref_b, summary="Same claim, occupancy instance A")
        self.assertNotEqual(
            self.exact_ref("work-claim.schema.json", claim_a),
            self.exact_ref("work-claim.schema.json", claim_b),
        )

    def test_same_logical_claim_instances_change_return_packet_identity(self):
        base_ref = self.exact_ref("state-revision.schema.json", self.base_revision())
        occupancy = self.occupancy(base_ref, actor_ref="fixture:occupant-a")
        occupancy_ref = self.exact_ref("occupancy.schema.json", occupancy)

        claim_a = self.claim(base_ref, occupancy_ref, summary="Claim instance A")
        claim_b = self.claim(base_ref, occupancy_ref, summary="Claim instance B")
        ref_a = self.exact_ref("work-claim.schema.json", claim_a)
        ref_b = self.exact_ref("work-claim.schema.json", claim_b)
        self.assertEqual(parse_immutable_ref(ref_a).logical_id, "claim.same")
        self.assertEqual(parse_immutable_ref(ref_b).logical_id, "claim.same")
        self.assertNotEqual(ref_a, ref_b)

        packet_a = self.packet(base_ref, ref_a)
        packet_b = self.packet(base_ref, ref_b)
        self.assertNotEqual(
            self.exact_ref("return-packet.schema.json", packet_a),
            self.exact_ref("return-packet.schema.json", packet_b),
        )

    def test_post_base_objects_bind_directly_without_false_base_membership(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)
            base = self.base_revision()
            base_result = store.store(base, "state-revision.schema.json")

            occupancy = self.occupancy(
                base_result.reference,
                actor_ref="fixture:post-base-occupant",
                logical_id="occupancy.post-base",
            )
            occupancy_result = store.store(occupancy, "occupancy.schema.json")
            self.assertNotIn(occupancy_result.reference, base["occupancy_refs"])

            claim = self.claim(
                base_result.reference,
                occupancy_result.reference,
                summary="Created after the common work base.",
                logical_id="claim.post-base",
            )
            claim_result = store.store(claim, "work-claim.schema.json")
            self.assertNotIn(claim_result.reference, base["claim_refs"])
            self.assertEqual(
                store.load(claim_result.reference)["occupancy_ref"],
                occupancy_result.reference,
            )

            packet = self.packet(
                base_result.reference,
                claim_result.reference,
                logical_id="packet.post-base",
            )
            packet_result = store.store(packet, "return-packet.schema.json")
            self.assertNotIn(packet_result.reference, base["return_packet_refs"])
            self.assertEqual(
                store.load(packet_result.reference)["claim_ref"],
                claim_result.reference,
            )

    def test_store_rejects_malformed_authoritative_refs_before_publication(self):
        malformed_cases = (
            (
                "work-claim.schema.json",
                "occupancy_ref",
                "axmref:v1:occupancy:%FF:-:sha256:" + "1" * 64,
            ),
            (
                "return-packet.schema.json",
                "claim_ref",
                "axmref:v1:work-claim:e%CC%81:-:sha256:" + "2" * 64,
            ),
        )
        for schema_name, field, reference in malformed_cases:
            with self.subTest(schema=schema_name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    store = FilesystemObjectStore(temp_dir)
                    candidate = copy.deepcopy(self.valid[schema_name])
                    candidate[field] = reference
                    with self.assertRaises(ContractValidationError):
                        store.store(candidate, schema_name)
                    self.assertEqual(list(Path(temp_dir).rglob("*.json")), [])


if __name__ == "__main__":
    unittest.main()
