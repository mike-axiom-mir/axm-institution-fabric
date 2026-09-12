from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import (
    CanonicalizationError,
    ContractValidationError,
    EvidenceBindingError,
    ImmutableRef,
    ImmutableReferenceError,
    canonical_bytes,
    canonical_validated_sha256,
    load_and_validate,
    make_immutable_ref,
    parse_immutable_ref,
    parse_json_strict,
    reference_matches,
    resolve_reference,
    validate_evidence_subject_binding,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "fixtures" / "identity"


def load_fixture():
    return json.loads((FIXTURE_DIR / "artifact_versions.json").read_text(encoding="utf-8"))


class IdentityTests(unittest.TestCase):
    def test_same_value_has_same_canonical_bytes_and_hash_independent_of_key_order(self):
        first = {"z": [3, 2, 1], "a": {"b": True, "a": None}}
        second = {"a": {"a": None, "b": True}, "z": [3, 2, 1]}
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        self.assertEqual(canonical_bytes(first), b'{"a":{"a":null,"b":true},"z":[3,2,1]}')

    def test_adv_017_a_duplicate_json_members_fail_before_identity(self):
        with self.assertRaises(CanonicalizationError):
            parse_json_strict('{"schema_version":"0.1","id":"artifact.alpha","id":"artifact.beta"}')

    def test_adv_018_a_unicode_policy_is_explicit_nfc_only(self):
        nfc = parse_json_strict('{"name":"\\u00e9"}')
        self.assertEqual(nfc["name"], "é")
        with self.assertRaises(CanonicalizationError):
            parse_json_strict('{"name":"e\\u0301"}')

    def test_adv_019_a_schema_defaults_are_not_silently_materialized(self):
        contracts = parse_json_strict((ROOT / "fixtures" / "contracts" / "valid.json").read_text(encoding="utf-8"))
        omitted = dict(contracts["lane.schema.json"])
        omitted.pop("notes", None)
        explicit = dict(omitted)
        explicit["notes"] = []
        omitted_hash = canonical_validated_sha256(omitted, "lane.schema.json", SCHEMA_DIR)
        explicit_hash = canonical_validated_sha256(explicit, "lane.schema.json", SCHEMA_DIR)
        self.assertNotIn("notes", omitted)
        self.assertNotEqual(omitted_hash, explicit_hash)

    def test_adv_020_a_bare_digest_is_not_an_immutable_reference(self):
        with self.assertRaises(ImmutableReferenceError):
            parse_immutable_ref("0" * 64)

    def test_adv_021_a_unicode_scalar_key_order_is_explicit(self):
        value = {"\U00010000": 2, "\ue000": 1}
        self.assertEqual(canonical_bytes(value), '{"\ue000":1,"\U00010000":2}'.encode("utf-8"))

    def test_adv_022_a_reference_component_encoding_is_utf8_byte_canonical(self):
        logical_id = "a!b*a'b(c)"
        reference = str(ImmutableRef("artifact", logical_id, None, "0" * 64))
        self.assertEqual(
            reference,
            "axmref:v1:artifact:a%21b%2Aa%27b%28c%29:-:sha256:" + "0" * 64,
        )
        self.assertEqual(parse_immutable_ref(reference).logical_id, logical_id)
        utf8_reference = str(ImmutableRef("artifact", "é %~", None, "1" * 64))
        self.assertIn(":%C3%A9%20%25~:-:sha256:", utf8_reference)
        self.assertEqual(parse_immutable_ref(utf8_reference).logical_id, "é %~")
        with self.assertRaises(ImmutableReferenceError):
            parse_immutable_ref("axmref:v1:artifact:a!b:-:sha256:" + "0" * 64)
        with self.assertRaises(ImmutableReferenceError):
            parse_immutable_ref("axmref:v1:artifact:a%2ab:-:sha256:" + "0" * 64)

    def test_strict_parser_rejects_ambiguous_json(self):
        cases = (
            '{"a":1,"a":2}',
            '{"value":1.0}',
            '{"value":-0}',
            '{"value":9007199254740992}',
            '{"value":NaN}',
            '{"value":"e\\u0301"}',
        )
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(CanonicalizationError):
                    parse_json_strict(text)

    def test_all_integrated_stage1_objects_validate_and_round_trip_without_drift(self):
        contracts = parse_json_strict((ROOT / "fixtures" / "contracts" / "valid.json").read_text(encoding="utf-8"))
        self.assertEqual(len(contracts), 10)
        for schema_name, instance in sorted(contracts.items()):
            with self.subTest(schema=schema_name):
                first = canonical_bytes(instance)
                validated_hash = canonical_validated_sha256(instance, schema_name, SCHEMA_DIR)
                reparsed = parse_json_strict(first.decode("utf-8"))
                second = canonical_bytes(reparsed)
                self.assertEqual(first, second)
                self.assertEqual(validated_hash, canonical_validated_sha256(reparsed, schema_name, SCHEMA_DIR))

    def test_validated_artifact_ref_round_trips_and_matches_exact_instance(self):
        fixtures = load_fixture()
        v1 = fixtures["v1"]
        v2 = fixtures["v2"]
        ref_v1 = make_immutable_ref("artifact.schema.json", v1, SCHEMA_DIR)
        parsed = parse_immutable_ref(ref_v1)
        self.assertEqual(parsed.kind, "artifact")
        self.assertEqual(parsed.logical_id, "artifact.rules")
        self.assertEqual(parsed.version, "1")
        self.assertTrue(reference_matches(ref_v1, "artifact.schema.json", v1, SCHEMA_DIR))
        self.assertFalse(reference_matches(ref_v1, "artifact.schema.json", v2, SCHEMA_DIR))
        self.assertIs(resolve_reference(ref_v1, "artifact.schema.json", [v1, v2], SCHEMA_DIR), v1)

    def test_version_sentinel_cannot_collide_with_real_version(self):
        fixture = dict(load_fixture()["v1"])
        fixture["version"] = "-"
        reference = make_immutable_ref("artifact.schema.json", fixture, SCHEMA_DIR)
        parsed = parse_immutable_ref(reference)
        self.assertEqual(parsed.version, "-")
        self.assertIn(":v=-:sha256:", reference)

    def test_same_logical_id_different_instance_gets_different_identity(self):
        fixtures = load_fixture()
        v1 = fixtures["v1"]
        v2 = fixtures["v2"]
        ref_v1 = make_immutable_ref("artifact.schema.json", v1, SCHEMA_DIR)
        ref_v2 = make_immutable_ref("artifact.schema.json", v2, SCHEMA_DIR)
        self.assertNotEqual(ref_v1, ref_v2)
        self.assertNotEqual(
            canonical_validated_sha256(v1, "artifact.schema.json", SCHEMA_DIR),
            canonical_validated_sha256(v2, "artifact.schema.json", SCHEMA_DIR),
        )

    def test_adv_015_b_strong_evidence_cannot_follow_stable_name_to_v2(self):
        fixtures = load_fixture()
        v1 = fixtures["v1"]
        v2 = fixtures["v2"]
        ref_v1 = make_immutable_ref("artifact.schema.json", v1, SCHEMA_DIR)
        evidence = {
            "schema_version": "0.1",
            "id": "evidence.rules.v1.tests",
            "subject_ref": ref_v1,
            "state": "automated_tested",
            "claim": "Artifact rules version 1 passed deterministic tests.",
            "method": "python -m unittest tests.test_identity -v",
            "source_refs": ["tests/test_identity.py"],
        }
        validate_evidence_subject_binding(evidence, "artifact.schema.json", v1, SCHEMA_DIR)
        with self.assertRaises(EvidenceBindingError):
            validate_evidence_subject_binding(evidence, "artifact.schema.json", v2, SCHEMA_DIR)

    def test_load_and_validate_uses_strict_parser_and_schema(self):
        fixture = load_fixture()["v1"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.json"
            path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
            loaded = load_and_validate(path, "artifact.schema.json", SCHEMA_DIR)
            self.assertEqual(loaded, fixture)

            path.write_text('{"schema_version":"0.1","id":"artifact.bad"}', encoding="utf-8")
            with self.assertRaises(ContractValidationError):
                load_and_validate(path, "artifact.schema.json", SCHEMA_DIR)

            path.write_text('{"schema_version":"0.1","id":"artifact.bad","id":"artifact.dup"}', encoding="utf-8")
            with self.assertRaises(CanonicalizationError):
                load_and_validate(path, "artifact.schema.json", SCHEMA_DIR)

    def test_reference_parser_rejects_noncanonical_or_malformed_forms(self):
        bad = (
            "artifact.rules",
            "axmref:v1:artifact:%61rtifact.rules:1:sha256:" + "0" * 64,
            "axmref:v1:artifact:artifact.rules:1:sha256:not-a-hash",
        )
        for reference in bad:
            with self.subTest(reference=reference):
                with self.assertRaises(ImmutableReferenceError):
                    parse_immutable_ref(reference)

    def test_round_trip_canonical_bytes_do_not_drift(self):
        fixture = load_fixture()["v1"]
        first = canonical_bytes(fixture)
        reparsed = parse_json_strict(first.decode("utf-8"))
        second = canonical_bytes(reparsed)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
