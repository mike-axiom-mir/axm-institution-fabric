from __future__ import annotations

import copy
import json
import unittest

from axm_institution.identity import (
    CanonicalizationError,
    ContractValidationError,
    make_immutable_ref,
    parse_json_strict,
    validate_instance,
)


EXACT_BASE_REF = (
    "axmref:v1:state-revision:revision.fixture.0001:-:sha256:" + "c" * 64
)
EXACT_ARTIFACT_REF = (
    "axmref:v1:artifact:artifact.source:v=1:sha256:" + "a" * 64
)


def opaque(token: str) -> dict:
    return {"source_class": "opaque_label", "token": token}


def locator(value: str = "NEXT_BUILD.md") -> dict:
    return {
        "source_class": "locator",
        "locator_context": "repository-relative",
        "locator": value,
    }


def content(digest: str = "b" * 64) -> dict:
    return {
        "source_class": "content_address",
        "algorithm": "sha256",
        "digest": digest,
        "byte_scope": "raw_bytes",
    }


def typed_artifact(
    declarations: dict,
    *,
    artifact_id: str = "artifact.adv054",
    content_ref: str = "fixtures/contracts/typed_source_declarations.json",
) -> dict:
    return {
        "schema_version": "0.4",
        "id": artifact_id,
        "type": "typed_source_adversarial_fixture",
        "version": "1",
        "content_ref": content_ref,
        "provenance": {
            "producer_lane_id": "lane-03",
            "base_state_revision_ref": EXACT_BASE_REF,
            "source_declarations": declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def typed_evidence(declarations: dict) -> dict:
    return {
        "schema_version": "0.2",
        "id": "evidence.adv054",
        "subject_ref": EXACT_ARTIFACT_REF,
        "state": "automated_tested",
        "claim": "ADV-054 Decision 020 typed source declaration adversarial fixture.",
        "method": "deterministic adversarial contract regression",
        "source_declarations": declarations,
    }


class TypedSourceDeclarationAdversarialTests(unittest.TestCase):
    def test_adv054_a_trailing_lf_declaration_key_must_fail_true_end_spelling(self):
        """Known ADV-028 `$` anchoring ambiguity must not re-enter declaration ids."""

        bad_key = "source\n"
        for schema_name, candidate in (
            ("artifact.schema.json", typed_artifact({bad_key: opaque("source-token")})),
            ("evidence-record.schema.json", typed_evidence({bad_key: opaque("source-token")})),
        ):
            with self.subTest(schema=schema_name):
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)

    def test_adv054_b_duplicate_raw_declaration_members_fail_before_contract_use(self):
        """Two authored occurrences cannot collapse through ordinary JSON duplicate keys."""

        raw = (
            '{"source_declarations":{'
            '"source":{"source_class":"opaque_label","token":"first"},'
            '"source":{"source_class":"opaque_label","token":"second"}'
            '}}'
        )
        with self.assertRaises(CanonicalizationError):
            parse_json_strict(raw)

    def test_adv054_c_transport_and_detached_copy_preserve_key_to_target_meaning(self):
        original = typed_artifact(
            {
                "source.locator": locator("NEXT_BUILD.md"),
                "source.content": content(),
            }
        )
        original_ref = make_immutable_ref("artifact.schema.json", original)

        transported = json.loads(json.dumps(original, sort_keys=True))
        self.assertEqual(original_ref, make_immutable_ref("artifact.schema.json", transported))
        self.assertEqual(
            "NEXT_BUILD.md",
            transported["provenance"]["source_declarations"]["source.locator"]["locator"],
        )

        detached = copy.deepcopy(transported)
        detached["provenance"]["source_declarations"]["source.locator"]["locator"] = "FOUNDATION.md"
        self.assertEqual(
            "NEXT_BUILD.md",
            original["provenance"]["source_declarations"]["source.locator"]["locator"],
        )
        self.assertNotEqual(
            original_ref,
            make_immutable_ref("artifact.schema.json", detached),
        )

    def test_adv054_d_same_key_across_exact_containers_cannot_rebind_target(self):
        first = typed_artifact(
            {"source": locator("NEXT_BUILD.md")},
            artifact_id="artifact.adv054.first",
        )
        second = typed_artifact(
            {"source": locator("FOUNDATION.md")},
            artifact_id="artifact.adv054.second",
        )

        first_ref = make_immutable_ref("artifact.schema.json", first)
        second_ref = make_immutable_ref("artifact.schema.json", second)
        self.assertNotEqual(first_ref, second_ref)
        self.assertEqual(
            "NEXT_BUILD.md",
            first["provenance"]["source_declarations"]["source"]["locator"],
        )
        self.assertEqual(
            "FOUNDATION.md",
            second["provenance"]["source_declarations"]["source"]["locator"],
        )

    def test_adv054_e_cross_field_lookalikes_gain_no_source_occurrence(self):
        exact_looking = EXACT_ARTIFACT_REF
        candidate = typed_artifact(
            {"declared": opaque("historical-looking-token")},
            content_ref=exact_looking,
        )
        validated = validate_instance(candidate, "artifact.schema.json")
        declarations = validated["provenance"]["source_declarations"]

        self.assertEqual({"declared"}, set(declarations))
        self.assertEqual("opaque_label", declarations["declared"]["source_class"])
        self.assertEqual(exact_looking, validated["content_ref"])
        self.assertNotIn("resolved_ref", declarations["declared"])
        self.assertNotIn("trusted", declarations["declared"])
        self.assertNotIn("accepted", declarations["declared"])

    def test_adv055_a_trailing_lf_content_digest_must_fail_exact_64_hex_spelling(self):
        """A content address is exactly 64 lowercase hex chars, not 64 hex plus final LF."""

        bad_digest = "b" * 64 + "\n"
        for schema_name, candidate in (
            ("artifact.schema.json", typed_artifact({"source": content(bad_digest)})),
            ("evidence-record.schema.json", typed_evidence({"source": content(bad_digest)})),
        ):
            with self.subTest(schema=schema_name):
                with self.assertRaises(ContractValidationError):
                    validate_instance(candidate, schema_name)


if __name__ == "__main__":
    unittest.main()
