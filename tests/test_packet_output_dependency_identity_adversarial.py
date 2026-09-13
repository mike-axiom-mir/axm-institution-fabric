from __future__ import annotations

import json
import unittest

from axm_institution.packet_output_dependency_identity import (
    HistoricalDependencySemanticsUnresolvedError,
    OutputDependencyReferenceError,
    preflight_output_dependency_identity,
)
import test_packet_output_dependency_identity as base_tests


class OutputDependencyIdentityAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-047 continuity attacks for Decision 014 only."""

    def setUp(self) -> None:
        self.fixture = base_tests.OutputDependencyIdentityTests(
            methodName="test_created_only_v03_exact_dependency_round_trips_as_ref_value_pair"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store

    def _created_packet_with_dependency(self, *, packet_id: str):
        context = self.fixture._ground_context()
        dependency_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.dependency",
            content_ref="artifact://adv047/dependency",
        )
        created_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv047.created",
            content_ref="artifact://adv047/created",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv047.created",
            subject_ref=created_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id=packet_id,
        )
        return context, dependency_ref, created_ref, packet_ref

    def test_adv047_a_corrupt_exact_dependency_target_fails_closed(self) -> None:
        _, dependency_ref, _, packet_ref = self._created_packet_with_dependency(
            packet_id="packet.adv047.corrupt-target"
        )
        dependency_path = self.store._object_path(dependency_ref)
        dependency_path.write_text("{}", encoding="utf-8")

        with self.assertRaises(OutputDependencyReferenceError):
            preflight_output_dependency_identity(self.store, packet_ref)

    def test_adv047_b_high_version_superseding_same_logical_decoy_cannot_rebind_dependency(self) -> None:
        context = self.fixture._ground_context()
        selected_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.same-logical",
            content_ref="artifact://adv047/selected",
        )
        decoy = self.fixture._historical_artifact(
            artifact_id="artifact.adv047.same-logical",
            content_ref="artifact://adv047/decoy",
        )
        decoy["version"] = "999.0"
        decoy["supersedes_ref"] = selected_ref
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(selected_ref, decoy_ref)

        created_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv047.selected-output",
            content_ref="artifact://adv047/selected-output",
            dependency_refs=[selected_ref],
        )
        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv047.selected-output",
            subject_ref=created_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.adv047.version-supersedes-decoy",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        relation = resolved.created_outputs[0].dependencies[0]
        self.assertEqual(relation.reference, selected_ref)
        self.assertNotEqual(relation.reference, decoy_ref)
        self.assertEqual(relation.value.get("content_ref"), "artifact://adv047/selected")

    def test_adv047_c_modified_result_historical_exact_looking_dependency_stays_unresolved(self) -> None:
        context = self.fixture._ground_context()
        dependency_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.modified-historical-dependency",
            content_ref="artifact://adv047/modified-historical-dependency",
        )
        result_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv047.modified-historical-result",
            content_ref="artifact://adv047/modified-historical-result",
            schema_version="0.2",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv047.modified-historical-result",
            subject_ref=result_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            modified_result_ref=result_ref,
            evidence_refs=[evidence_ref],
            packet_id="packet.adv047.modified-historical-result",
        )

        with self.assertRaises(HistoricalDependencySemanticsUnresolvedError):
            preflight_output_dependency_identity(self.store, packet_ref)

    def test_adv047_d_modified_result_source_and_artifact_evidence_refs_gain_no_dependency_authority(self) -> None:
        context = self.fixture._ground_context()
        metadata_decoy_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.metadata-decoy",
            content_ref="artifact://adv047/metadata-decoy",
        )
        result_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv047.modified-metadata-result",
            content_ref="artifact://adv047/modified-metadata-result",
            dependency_refs=[],
            source_refs=[metadata_decoy_ref],
            evidence_refs=[metadata_decoy_ref],
        )
        packet_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv047.modified-metadata-result",
            subject_ref=result_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            modified_result_ref=result_ref,
            evidence_refs=[packet_evidence_ref],
            packet_id="packet.adv047.modified-metadata-result",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(resolved.modified_results[0].dependencies, ())
        self.assertEqual(
            resolved.modified_results[0].artifact.reference,
            result_ref,
        )

    def test_adv047_e_same_logical_different_exact_dependencies_remain_two_explicit_relations(self) -> None:
        context = self.fixture._ground_context()
        first_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.parallel",
            content_ref="artifact://adv047/parallel-a",
        )
        second_ref = self.fixture._store_dependency(
            artifact_id="artifact.adv047.parallel",
            content_ref="artifact://adv047/parallel-b",
        )
        self.assertNotEqual(first_ref, second_ref)
        created_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv047.parallel-output",
            content_ref="artifact://adv047/parallel-output",
            dependency_refs=[first_ref, second_ref],
        )
        evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv047.parallel-output",
            subject_ref=created_ref,
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.adv047.parallel-output",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(
            tuple(item.reference for item in resolved.created_outputs[0].dependencies),
            (first_ref, second_ref),
        )
        self.assertEqual(
            tuple(item.value.get("content_ref") for item in resolved.created_outputs[0].dependencies),
            ("artifact://adv047/parallel-a", "artifact://adv047/parallel-b"),
        )

    def test_adv047_f_materialized_dependency_copies_cannot_mutate_exact_operational_facts(self) -> None:
        context, dependency_ref, created_ref, packet_ref = self._created_packet_with_dependency(
            packet_id="packet.adv047.materialize"
        )
        resolved = preflight_output_dependency_identity(self.store, packet_ref)
        outer_copy = resolved._asdict()
        output_copy = resolved.created_outputs[0]._asdict()
        dependency_value_copy = dict(resolved.created_outputs[0].dependencies[0].value)

        outer_copy["lane_ref"] = "lane.decoy"
        output_copy["category"] = "modified_result"
        dependency_value_copy["content_ref"] = "artifact://adv047/decoy-mutated"

        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(resolved.created_outputs[0].category, "created")
        self.assertEqual(resolved.created_outputs[0].artifact.reference, created_ref)
        self.assertEqual(resolved.created_outputs[0].dependencies[0].reference, dependency_ref)
        self.assertEqual(
            resolved.created_outputs[0].dependencies[0].value.get("content_ref"),
            "artifact://adv047/dependency",
        )

    def test_adv047_g_ordinary_json_transport_fails_closed_and_identity_does_not_become_acceptance(self) -> None:
        _, _, _, packet_ref = self._created_packet_with_dependency(
            packet_id="packet.adv047.transport-and-boundary"
        )
        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        with self.assertRaises(TypeError):
            json.dumps(resolved)
        with self.assertRaises(TypeError):
            json.dumps(resolved._asdict())

        for forbidden in (
            "dependencies_closed",
            "accepted",
            "rejected",
            "complete",
            "closed",
            "satisfied",
        ):
            self.assertFalse(hasattr(resolved, forbidden))


if __name__ == "__main__":
    unittest.main()
