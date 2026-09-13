from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_evidence_subject import EvidenceSubjectKindError
from axm_institution.packet_mixed_compatibility import (
    MixedOutputCategoryCollisionError,
    preflight_mixed_packet_compatibility,
)
from axm_institution.packet_modified_artifact_identity import ModifiedArtifactContractVersionError
from axm_institution.packet_modified_result_compatibility import (
    preflight_modified_result_compatibility,
)
from axm_institution.packet_output_compatibility import (
    RequiredStateSemanticsUnresolvedError,
    preflight_created_output_compatibility,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class MixedPacketCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _prior_artifact(
        self,
        *,
        artifact_id: str = "artifact.modified",
        content_ref: str = "artifact://mixed/prior",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.1"
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-claim",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _output_artifact(
        self,
        *,
        base_ref: str,
        artifact_id: str,
        content_ref: str,
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.2"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.2"
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": base_ref,
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str = "automated_tested",
    ):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = "Decision 013 mixed compatibility regression evidence."
        return evidence

    def _store_base(self, lane_ref: str, prior_ref: str) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.mixed.compatibility.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = [prior_ref]
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = ["Decision 013 bounded mixed compatibility fixture."]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self, lane=None):
        lane = copy.deepcopy(lane) if lane is not None else self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self.store.store(
            self._prior_artifact(), "artifact.schema.json"
        ).reference
        base_ref = self._store_base(lane_ref, prior_ref)

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.mixed.compatibility"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.mixed.compatibility"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        created_ref = self.store.store(
            self._output_artifact(
                base_ref=base_ref,
                artifact_id="artifact.created",
                content_ref="artifact://mixed/created",
            ),
            "artifact.schema.json",
        ).reference
        result_ref = self.store.store(
            self._output_artifact(
                base_ref=base_ref,
                artifact_id="artifact.modified.result",
                content_ref="artifact://mixed/modified-result",
            ),
            "artifact.schema.json",
        ).reference
        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
            "created_ref": created_ref,
            "result_ref": result_ref,
        }

    def _store_evidence(
        self,
        *,
        evidence_id: str,
        subject_ref: str,
        state: str = "automated_tested",
    ) -> str:
        return self.store.store(
            self._evidence(
                evidence_id=evidence_id,
                subject_ref=subject_ref,
                state=state,
            ),
            "evidence-record.schema.json",
        ).reference

    def _submit_packet(
        self,
        context,
        *,
        created=None,
        modified=None,
        evidence_refs=(),
        schema_version: str = "0.4",
        packet_id: str = "packet.mixed.compatibility",
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = schema_version
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = (
            [context["created_ref"]] if created is None else list(created)
        )
        packet["artifacts_modified"] = (
            [
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": context["result_ref"],
                }
            ]
            if modified is None
            else modified
        )
        packet["evidence_refs"] = list(evidence_refs)
        return submit_return_packet(self.store, packet).packet_ref

    def test_mixed_packet_projects_both_output_families_from_one_exact_context(self) -> None:
        context = self._ground_context()
        created_evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.created",
            subject_ref=context["created_ref"],
        )
        result_evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.result",
            subject_ref=context["result_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[created_evidence_ref, result_evidence_ref],
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(resolved.packet_ref, packet_ref)
        self.assertEqual(resolved.claim_ref, context["claim_ref"])
        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(resolved.occupancy_ref, context["occupancy_ref"])
        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(
            tuple(item.artifact.reference for item in resolved.created_bindings),
            (context["created_ref"],),
        )
        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertEqual(
            resolved.modified_results[0].modification.result_artifact.reference,
            context["result_ref"],
        )
        self.assertTrue(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.unmatched_evidence, ())
        for forbidden in ("accepted", "complete", "closed", "satisfied"):
            self.assertFalse(hasattr(resolved, forbidden))

    def test_created_only_projection_preserves_canonical_created_behavior(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.created-only",
            subject_ref=context["created_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            modified=[],
            evidence_refs=[evidence_ref],
            packet_id="packet.mixed.created-only",
        )

        canonical = preflight_created_output_compatibility(self.store, packet_ref)
        mixed = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(mixed.created_outputs, canonical.created_outputs)
        self.assertEqual(
            tuple(
                (
                    binding.artifact.reference,
                    tuple(item.reference for item in binding.evidence_records),
                )
                for binding in mixed.created_bindings
            ),
            tuple(
                (
                    binding.artifact.reference,
                    tuple(item.reference for item in binding.evidence_records),
                )
                for binding in canonical.subject_resolution.created_artifact_bindings
            ),
        )
        self.assertEqual(mixed.modified_results, ())
        self.assertEqual(mixed.unmatched_evidence, ())

    def test_modified_only_projection_consumes_decision_012_unchanged(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.modified-only",
            subject_ref=context["result_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            created=[],
            evidence_refs=[evidence_ref],
            packet_id="packet.mixed.modified-only",
        )

        canonical = preflight_modified_result_compatibility(self.store, packet_ref)
        mixed = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(mixed.created_outputs, ())
        self.assertEqual(mixed.created_bindings, ())
        self.assertEqual(mixed.modified_results, canonical.modified_results)
        self.assertEqual(
            (mixed.claim_ref, mixed.claim_base_ref, mixed.occupancy_ref, mixed.lane_ref),
            (
                canonical.claim_ref,
                canonical.claim_base_ref,
                canonical.occupancy_ref,
                canonical.lane_ref,
            ),
        )
        self.assertEqual(mixed.unmatched_evidence, ())

    def test_cross_family_evidence_is_not_pooled(self) -> None:
        context = self._ground_context()
        created_evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.created-not-result",
            subject_ref=context["created_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[created_evidence_ref],
            packet_id="packet.mixed.no-cross-pool",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())
        self.assertEqual(resolved.unmatched_evidence, ())

    def test_exact_created_modified_result_collision_fails_closed(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            created=[context["result_ref"]],
            packet_id="packet.mixed.category-collision",
        )

        with self.assertRaises(MixedOutputCategoryCollisionError):
            preflight_mixed_packet_compatibility(self.store, packet_ref)

    def test_same_logical_different_exact_outputs_remain_separate(self) -> None:
        context = self._ground_context()
        same_logical_created_ref = self.store.store(
            self._output_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.result",
                content_ref="artifact://mixed/same-logical-created",
            ),
            "artifact.schema.json",
        ).reference
        self.assertNotEqual(same_logical_created_ref, context["result_ref"])
        evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.same-logical-created",
            subject_ref=same_logical_created_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created=[same_logical_created_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.mixed.same-logical",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(
            resolved.created_outputs[0].artifact.reference,
            same_logical_created_ref,
        )
        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertEqual(
            resolved.modified_results[0].modification.result_artifact.reference,
            context["result_ref"],
        )
        self.assertFalse(resolved.modified_results[0].satisfied)

    def test_conflicting_exact_evidence_remains_explicit_in_both_families(self) -> None:
        context = self._ground_context()
        refs = [
            self._store_evidence(
                evidence_id="evidence.mixed.created.pass",
                subject_ref=context["created_ref"],
            ),
            self._store_evidence(
                evidence_id="evidence.mixed.created.invalidated",
                subject_ref=context["created_ref"],
                state="invalidated",
            ),
            self._store_evidence(
                evidence_id="evidence.mixed.result.pass",
                subject_ref=context["result_ref"],
            ),
            self._store_evidence(
                evidence_id="evidence.mixed.result.invalidated",
                subject_ref=context["result_ref"],
                state="invalidated",
            ),
        ]
        packet_ref = self._submit_packet(
            context,
            evidence_refs=refs,
            packet_id="packet.mixed.conflicting-evidence",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertTrue(resolved.created_outputs[0].satisfied)
        self.assertEqual(
            tuple(
                item.value.get("state")
                for item in resolved.created_bindings[0].evidence_records
            ),
            ("automated_tested", "invalidated"),
        )
        self.assertTrue(resolved.modified_results[0].satisfied)
        self.assertEqual(
            tuple(
                item.value.get("state")
                for item in resolved.modified_results[0].subject_evidence
            ),
            ("automated_tested", "invalidated"),
        )

    def test_non_exact_and_unrelated_exact_evidence_remain_unmatched(self) -> None:
        context = self._ground_context()
        non_exact_ref = self._store_evidence(
            evidence_id="evidence.mixed.non-exact",
            subject_ref="artifact.created",
        )
        prior_ref = self._store_evidence(
            evidence_id="evidence.mixed.prior",
            subject_ref=context["prior_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[non_exact_ref, prior_ref],
            packet_id="packet.mixed.unmatched",
        )

        resolved = preflight_mixed_packet_compatibility(self.store, packet_ref)

        self.assertEqual(
            tuple(item.reason for item in resolved.unmatched_evidence),
            ("non_exact_subject", "exact_artifact_not_packet_output"),
        )
        self.assertFalse(resolved.created_outputs[0].satisfied)
        self.assertFalse(resolved.modified_results[0].satisfied)

    def test_wrong_kind_exact_subject_fails_closed(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.wrong-kind",
            subject_ref=context["lane_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            packet_id="packet.mixed.wrong-kind",
        )

        with self.assertRaises(EvidenceSubjectKindError):
            preflight_mixed_packet_compatibility(self.store, packet_ref)

    def test_historical_v03_modified_entries_do_not_enter_mixed_projection(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            schema_version="0.3",
            modified=[context["prior_ref"]],
            packet_id="packet.mixed.historical-v03",
        )

        with self.assertRaises(ModifiedArtifactContractVersionError):
            preflight_mixed_packet_compatibility(self.store, packet_ref)

    def test_multiple_required_states_gain_no_semantics_through_wrapper(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["evidence_requirements"][0]["required_states"] = [
            "automated_tested",
            "runtime_tested",
        ]
        context = self._ground_context(lane)
        created_evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.multistate-created",
            subject_ref=context["created_ref"],
        )
        result_evidence_ref = self._store_evidence(
            evidence_id="evidence.mixed.multistate-result",
            subject_ref=context["result_ref"],
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[created_evidence_ref, result_evidence_ref],
            packet_id="packet.mixed.multistate",
        )

        with self.assertRaises(RequiredStateSemanticsUnresolvedError):
            preflight_mixed_packet_compatibility(self.store, packet_ref)


if __name__ == "__main__":
    unittest.main()
