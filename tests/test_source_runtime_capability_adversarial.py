from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from axm_institution.identity import make_immutable_ref
from axm_institution.source_runtime_capability import (
    SourceRuntimeCapabilityContextError,
    SourceRuntimeCapabilityInputError,
    project_exact_source_runtime_capability,
)


BASE_REF = (
    "axmref:v1:state-revision:revision.adv057-base:-:sha256:" + "1" * 64
)
SUPPORTED_TARGET = (
    "axmref:v1:artifact:artifact.adv057-target:v=1:sha256:" + "2" * 64
)
UNSUPPORTED_TARGET = (
    "axmref:v1:future-source-kind.unregistered:source.adv057-future:v=1:sha256:"
    + "3" * 64
)


def exact_declaration(target_ref: str) -> dict:
    return {"source_class": "exact_axm_object", "object_ref": target_ref}


def typed_artifact(declarations: dict, *, version: str = "1") -> dict:
    return {
        "schema_version": "0.4",
        "id": "artifact.adv057-container",
        "type": "decision022_adversarial_fixture",
        "version": version,
        "content_ref": "tests/test_source_runtime_capability_adversarial.py",
        "provenance": {
            "producer_lane_id": "lane-03",
            "base_state_revision_ref": BASE_REF,
            "source_declarations": declarations,
        },
        "evidence_refs": [],
        "dependency_refs": [],
    }


def artifact_ref(value: dict) -> str:
    return make_immutable_ref("artifact.schema.json", value)


def project(value: dict, key: str):
    return project_exact_source_runtime_capability(
        containing_object_ref=artifact_ref(value),
        containing_value=value,
        declaration_key=key,
    )


class Decision022AdversarialContinuityTests(unittest.TestCase):
    def test_adv057_a_invalid_utf8_bundled_schema_is_context_failure(self):
        """An existing undecodable bundled schema must fail through the dedicated context error."""

        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        with tempfile.TemporaryDirectory() as tmp:
            bundled_root = Path(tmp)
            (bundled_root / "artifact.schema.json").write_bytes(b"\xff")
            with mock.patch(
                "axm_institution.source_runtime_capability.BUNDLED_SCHEMA_DIR",
                bundled_root,
            ):
                with self.assertRaises(SourceRuntimeCapabilityContextError):
                    project(artifact, "source")

    def test_adv057_b_same_target_occurrences_remain_attributable_after_materialization(self):
        artifact = typed_artifact(
            {
                "alpha": exact_declaration(SUPPORTED_TARGET),
                "beta": exact_declaration(SUPPORTED_TARGET),
            }
        )
        alpha = project(artifact, "alpha")
        beta = project(artifact, "beta")
        self.assertEqual(alpha.target_object_ref, beta.target_object_ref)
        self.assertNotEqual(alpha.declaration_key, beta.declaration_key)
        self.assertNotEqual(bytes(alpha), bytes(beta))
        self.assertEqual("alpha", json.loads(bytes(alpha))["declaration_key"])
        self.assertEqual("beta", json.loads(bytes(beta))["declaration_key"])

    def test_adv057_c_copy_paths_must_reject_or_preserve_named_meaning(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        fact = project(artifact, "source")
        expected = fact._asdict()
        for copier in (copy.copy, copy.deepcopy):
            try:
                copied = copier(fact)
            except (TypeError, ValueError):
                continue
            self.assertEqual(expected, copied._asdict())
            self.assertEqual(expected, json.loads(bytes(copied)))

    def test_adv057_d_non_exact_neighbor_cannot_gain_capability_from_axmref_text(self):
        artifact = typed_artifact(
            {
                "exact": exact_declaration(UNSUPPORTED_TARGET),
                "label": {
                    "source_class": "opaque_label",
                    "token": SUPPORTED_TARGET,
                },
            }
        )
        self.assertEqual("unsupported_kind", project(artifact, "exact").runtime_capability)
        with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "not an exact_axm_object"):
            project(artifact, "label")

    def test_adv057_e_stale_container_cannot_rebind_same_key(self):
        earlier = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)}, version="1")
        later = typed_artifact({"source": exact_declaration(UNSUPPORTED_TARGET)}, version="2")
        stale_ref = artifact_ref(earlier)
        with self.assertRaisesRegex(SourceRuntimeCapabilityInputError, "does not reproduce"):
            project_exact_source_runtime_capability(
                containing_object_ref=stale_ref,
                containing_value=later,
                declaration_key="source",
            )

    def test_adv057_f_capability_fact_does_not_grow_lifecycle_authority(self):
        artifact = typed_artifact({"source": exact_declaration(SUPPORTED_TARGET)})
        fact = project(artifact, "source")
        self.assertEqual("supported", fact.runtime_capability)
        self.assertEqual(
            {
                "containing_object_ref",
                "declaration_key",
                "target_object_ref",
                "target_kind",
                "runtime_capability",
            },
            set(fact._asdict()),
        )
        for forbidden in (
            "exists",
            "available",
            "retrieved",
            "integrity",
            "provenance",
            "trusted",
            "complete",
            "closed",
            "accepted",
            "integrated",
            "epoch_complete",
            "replayable",
        ):
            self.assertFalse(hasattr(fact, forbidden), forbidden)


if __name__ == "__main__":
    unittest.main()
