from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "fixtures" / "contracts"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


class ContractSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = load_json(FIXTURE_DIR / "valid.json")
        cls.invalid = load_json(FIXTURE_DIR / "invalid.json")

    def validator_for(self, schema_name: str):
        schema = load_json(SCHEMA_DIR / schema_name)
        Draft202012Validator.check_schema(schema)
        return Draft202012Validator(schema, format_checker=FormatChecker())

    def test_all_schemas_are_valid_draft_2020_12(self):
        schema_paths = sorted(SCHEMA_DIR.glob("*.schema.json"))
        self.assertGreaterEqual(len(schema_paths), 9)
        for path in schema_paths:
            with self.subTest(schema=path.name):
                Draft202012Validator.check_schema(load_json(path))

    def test_valid_contract_fixtures_validate(self):
        for schema_name, instance in sorted(self.valid.items()):
            with self.subTest(schema=schema_name):
                self.validator_for(schema_name).validate(instance)

    def test_invalid_contract_fixtures_are_rejected(self):
        for case in self.invalid:
            with self.subTest(case=case["case"]):
                errors = list(self.validator_for(case["schema"]).iter_errors(case["instance"]))
                self.assertTrue(errors, f"expected invalid fixture to fail: {case['case']}")

    def test_fixture_canonicalization_is_reproducible(self):
        for schema_name, instance in sorted(self.valid.items()):
            with self.subTest(schema=schema_name):
                first = canonical_bytes(instance)
                reparsed = json.loads(first.decode("utf-8"))
                second = canonical_bytes(reparsed)
                self.assertEqual(first, second)
                self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())

    def test_done_is_not_an_evidence_state(self):
        schema = load_json(SCHEMA_DIR / "evidence-record.schema.json")
        allowed = schema["properties"]["state"]["enum"]
        self.assertNotIn("done", allowed)


if __name__ == "__main__":
    unittest.main()
