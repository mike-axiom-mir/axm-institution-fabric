from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_output_dependency_identity import (
    HistoricalDependencySemanticsUnresolvedError,
    OutputDependencyReferenceError,
    preflight_output_dependency_identity,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class OutputDependencyIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _historical_artifact(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        dependency_refs=(),
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.1"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.1"
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-decision-014",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = list(dependency_refs)
        artifact.pop("supersedes_ref", None)
        return artifact

    def _output_artifact(
        self,
        *,
        base_ref: str,
        artifact_id: str,
        content_ref: str,
        schema_version: str = "0.3",
        dependency_refs=(),
        source_refs=(),
        evidence_refs=(),
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = schema_version
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = schema_version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": base_ref,
            "source_refs": list(source_refs),
        }
        artifact["evidence_refs"] = list(evidence_refs)
        artifact["dependency_refs"] = list(dependency_refs)
        artifact.pop("supersedes_ref", None)
        return artifact

    def _store_base(self, lane_ref: str, prior_ref: str) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.dependency.identity.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = [prior_ref]
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [
            "Decision 014 proves dependency target identity only."
        ]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self.store.store(
            self._historical_artifact(
                artifact_id="artifact.modified",
                content_ref="artifact://dependency/prior",
            ),
            "artifact.schema.json",
        ).reference
        base_ref = self._store_base(lane_ref, prior_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.dependency.identity"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.dependency.identity"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
        }

    def _store_dependency(
        self,
        *,
        artifact_id: str,
        content_ref: str,
    ) -> str:
        return self.store.store(
            self._historical_artifact(
                artifact_id=artifact_id,
                content_ref=content_ref,
            ),
            "artifact.schema.json",
        ).reference

    def _store_output(
        self,
        context,
        *,
        artifact_id: str,
        content_ref: str,
        schema_version: str = "0.3",
        dependency_refs=(),
        source_refs=(),
        evidence_refs=(),
    ) -> str:
        artifact = self._output_artifact(
            base_ref=context["base_ref"],
            artifact_id=artifact_id,
            content_ref=content_ref,
            schema_version=schema_version,
            dependency_refs=dependency_refs,
            source_refs=source_refs,
            evidence_refs=evidence_refs,
        )
        return self.store.store(artifact, "artifact.schema.json").reference

    def _store_evidence(self, *, evidence_id: str, subject_ref: str) -> str:
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 014 output compatibility fixture evidence."
        return self.store.store(evidence, "evidence-record.schema.json").reference

    def _submit_packet(
        self,
        context,
        *,
        created_refs=(),
        modified_result_ref: str | None = None,
        evidence_refs=(),
        packet_id: str = "packet.dependency.identity",
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = list(created_refs)
        packet["artifacts_modified"] = (
            []
            if modified_result_ref is None
            else [
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": modified_result_ref,
                }
            ]
        )
        packet["evidence_refs"] = list(evidence_refs)
        return submit_return_packet(self.store, packet).packet_ref

    def test_created_only_v03_exact_dependency_round_trips_as_ref_value_pair(self) -> None:
        context = self._ground_context()
        dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.created",
            content_ref="artifact://dependency/created",
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.created",
            content_ref="artifact://output/created",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.created",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.created-only",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs[0].category, "created")
        self.assertEqual(resolved.created_outputs[0].artifact.reference, created_ref)
        self.assertEqual(
            tuple(item.reference for item in resolved.created_outputs[0].dependencies),
            (dependency_ref,),
        )
        self.assertEqual(
            resolved.created_outputs[0].dependencies[0].value.get("id"),
            "artifact.dependency.created",
        )
        self.assertEqual(resolved.modified_results, ())
        self.assertTrue(resolved.mixed_compatibility.created_outputs[0].satisfied)

    def test_modified_only_v03_dependency_preserves_decision_013_context(self) -> None:
        context = self._ground_context()
        dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.modified",
            content_ref="artifact://dependency/modified",
        )
        result_ref = self._store_output(
            context,
            artifact_id="artifact.modified.result",
            content_ref="artifact://output/modified",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.modified",
            subject_ref=result_ref,
        )
        packet_ref = self._submit_packet(
            context,
            modified_result_ref=result_ref,
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.modified-only",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs, ())
        self.assertEqual(resolved.modified_results[0].category, "modified_result")
        self.assertEqual(resolved.modified_results[0].artifact.reference, result_ref)
        self.assertEqual(
            tuple(item.reference for item in resolved.modified_results[0].dependencies),
            (dependency_ref,),
        )
        self.assertEqual(resolved.packet_ref, packet_ref)
        self.assertEqual(resolved.claim_ref, context["claim_ref"])
        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(resolved.occupancy_ref, context["occupancy_ref"])
        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertTrue(resolved.mixed_compatibility.modified_results[0].satisfied)

    def test_mixed_v03_outputs_keep_dependency_families_separate(self) -> None:
        context = self._ground_context()
        created_dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.mixed.created",
            content_ref="artifact://dependency/mixed-created",
        )
        modified_dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.mixed.modified",
            content_ref="artifact://dependency/mixed-modified",
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.created.mixed",
            content_ref="artifact://output/mixed-created",
            dependency_refs=[created_dependency_ref],
        )
        result_ref = self._store_output(
            context,
            artifact_id="artifact.modified.mixed",
            content_ref="artifact://output/mixed-modified",
            dependency_refs=[modified_dependency_ref],
        )
        created_evidence = self._store_evidence(
            evidence_id="evidence.dependency.mixed.created",
            subject_ref=created_ref,
        )
        result_evidence = self._store_evidence(
            evidence_id="evidence.dependency.mixed.modified",
            subject_ref=result_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            modified_result_ref=result_ref,
            evidence_refs=[created_evidence, result_evidence],
            packet_id="packet.dependency.mixed",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(
            tuple(item.reference for item in resolved.created_outputs[0].dependencies),
            (created_dependency_ref,),
        )
        self.assertEqual(
            tuple(item.reference for item in resolved.modified_results[0].dependencies),
            (modified_dependency_ref,),
        )
        self.assertTrue(resolved.mixed_compatibility.created_outputs[0].satisfied)
        self.assertTrue(resolved.mixed_compatibility.modified_results[0].satisfied)

    def test_historical_v01_exact_looking_dependency_is_not_reinterpreted(self) -> None:
        context = self._ground_context()
        dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.historical-v01",
            content_ref="artifact://dependency/historical-v01",
        )
        artifact = self._historical_artifact(
            artifact_id="artifact.historical.v01.output",
            content_ref="artifact://output/historical-v01",
            dependency_refs=[dependency_ref],
        )
        created_ref = self.store.store(artifact, "artifact.schema.json").reference
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.historical-v01",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.historical-v01",
        )

        with self.assertRaises(HistoricalDependencySemanticsUnresolvedError):
            preflight_output_dependency_identity(self.store, packet_ref)

    def test_historical_v02_exact_looking_dependency_is_not_reinterpreted(self) -> None:
        context = self._ground_context()
        dependency_ref = self._store_dependency(
            artifact_id="artifact.dependency.historical-v02",
            content_ref="artifact://dependency/historical-v02",
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.historical.v02.output",
            content_ref="artifact://output/historical-v02",
            schema_version="0.2",
            dependency_refs=[dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.historical-v02",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.historical-v02",
        )

        with self.assertRaises(HistoricalDependencySemanticsUnresolvedError):
            preflight_output_dependency_identity(self.store, packet_ref)

    def test_empty_historical_dependency_array_continues_without_closure_claim(self) -> None:
        context = self._ground_context()
        created_ref = self._store_output(
            context,
            artifact_id="artifact.historical.v02.empty",
            content_ref="artifact://output/historical-v02-empty",
            schema_version="0.2",
            dependency_refs=[],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.historical-empty",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.historical-empty",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs[0].dependencies, ())
        for forbidden in (
            "dependencies_closed",
            "accepted",
            "rejected",
            "complete",
            "closed",
            "satisfied",
        ):
            self.assertFalse(hasattr(resolved, forbidden))

    def test_v03_path_or_logical_dependency_is_rejected_by_contract(self) -> None:
        context = self._ground_context()
        for dependency in ("schemas/lane.schema.json", "artifact.logical-only"):
            with self.subTest(dependency=dependency):
                artifact = self._output_artifact(
                    base_ref=context["base_ref"],
                    artifact_id="artifact.invalid.path-dependency",
                    content_ref="artifact://output/invalid-path",
                    dependency_refs=[dependency],
                )
                with self.assertRaises(ContractValidationError):
                    self.store.store(artifact, "artifact.schema.json")

    def test_v03_wrong_kind_exact_dependency_is_rejected_by_contract(self) -> None:
        context = self._ground_context()
        wrong_kind_ref = (
            "axmref:v1:lane:lane-02:-:sha256:" + "b" * 64
        )
        artifact = self._output_artifact(
            base_ref=context["base_ref"],
            artifact_id="artifact.invalid.wrong-kind-dependency",
            content_ref="artifact://output/invalid-kind",
            dependency_refs=[wrong_kind_ref],
        )

        with self.assertRaises(ContractValidationError):
            self.store.store(artifact, "artifact.schema.json")

    def test_missing_exact_v03_dependency_target_fails_closed(self) -> None:
        context = self._ground_context()
        missing_ref = (
            "axmref:v1:artifact:artifact.missing:v=0.1:sha256:" + "a" * 64
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.output.missing-dependency",
            content_ref="artifact://output/missing-dependency",
            dependency_refs=[missing_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.missing",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.missing",
        )

        with self.assertRaises(OutputDependencyReferenceError):
            preflight_output_dependency_identity(self.store, packet_ref)

    def test_same_logical_different_exact_dependency_cannot_substitute(self) -> None:
        context = self._ground_context()
        selected_ref = self._store_dependency(
            artifact_id="artifact.dependency.same-logical",
            content_ref="artifact://dependency/selected",
        )
        decoy_ref = self._store_dependency(
            artifact_id="artifact.dependency.same-logical",
            content_ref="artifact://dependency/decoy",
        )
        self.assertNotEqual(selected_ref, decoy_ref)
        created_ref = self._store_output(
            context,
            artifact_id="artifact.output.same-logical-dependency",
            content_ref="artifact://output/same-logical-dependency",
            dependency_refs=[selected_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.same-logical",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.same-logical",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(
            resolved.created_outputs[0].dependencies[0].reference,
            selected_ref,
        )
        self.assertNotEqual(
            resolved.created_outputs[0].dependencies[0].reference,
            decoy_ref,
        )

    def test_source_and_evidence_refs_do_not_gain_dependency_authority(self) -> None:
        context = self._ground_context()
        unrelated_ref = self._store_dependency(
            artifact_id="artifact.dependency.unrelated-metadata",
            content_ref="artifact://dependency/unrelated-metadata",
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.output.metadata-no-authority",
            content_ref="artifact://output/metadata-no-authority",
            dependency_refs=[],
            source_refs=[unrelated_ref],
            evidence_refs=[unrelated_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.metadata-no-authority",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.metadata-no-authority",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(resolved.created_outputs[0].dependencies, ())

    def test_dependency_presentation_order_is_preserved_without_selection_fallback(self) -> None:
        context = self._ground_context()
        first_ref = self._store_dependency(
            artifact_id="artifact.dependency.order.first",
            content_ref="artifact://dependency/order-first",
        )
        second_ref = self._store_dependency(
            artifact_id="artifact.dependency.order.second",
            content_ref="artifact://dependency/order-second",
        )
        created_ref = self._store_output(
            context,
            artifact_id="artifact.output.order",
            content_ref="artifact://output/order",
            dependency_refs=[second_ref, first_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.dependency.order",
            subject_ref=created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.dependency.order",
        )

        resolved = preflight_output_dependency_identity(self.store, packet_ref)

        self.assertEqual(
            tuple(item.reference for item in resolved.created_outputs[0].dependencies),
            (second_ref, first_ref),
        )


if __name__ == "__main__":
    unittest.main()
