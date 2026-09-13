from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_evidence_subject import EvidenceSubjectKindError
from axm_institution.packet_modified_artifact_identity import ModifiedArtifactContractVersionError
from axm_institution.packet_modified_result_compatibility import (
    preflight_modified_result_compatibility,
)
from axm_institution.packet_output_compatibility import (
    EvidenceRequirementAmbiguityError,
    EvidenceRequirementNotFoundError,
    OutputContractAmbiguityError,
    OutputContractNotFoundError,
    RequiredStateSemanticsUnresolvedError,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ModifiedResultCompatibilityTests(unittest.TestCase):
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
        content_ref: str = "artifact://modified/prior",
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

    def _result_artifact(
        self,
        *,
        base_ref: str,
        artifact_id: str = "artifact.modified.result",
        content_ref: str = "artifact://modified/result",
        evidence_refs=None,
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
        artifact["evidence_refs"] = list(evidence_refs or [])
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _evidence(self, *, evidence_id: str, subject_ref: str, state: str = "automated_tested"):
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = state
        evidence["claim"] = "Decision 012 modified-result compatibility regression evidence."
        return evidence

    def _store_base(self, lane_ref: str, artifact_refs: list[str]) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.modified.compatibility.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = list(artifact_refs)
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = ["Decision 012 bounded compatibility fixture."]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self, lane=None):
        lane = copy.deepcopy(lane) if lane is not None else self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self.store.store(
            self._prior_artifact(), "artifact.schema.json"
        ).reference
        base_ref = self._store_base(lane_ref, [prior_ref])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.modified.compatibility"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.modified.compatibility"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        result_ref = self.store.store(
            self._result_artifact(base_ref=base_ref), "artifact.schema.json"
        ).reference
        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
            "result_ref": result_ref,
        }

    def _submit_packet(
        self,
        context,
        *,
        evidence_refs=(),
        modified=None,
        schema_version: str = "0.4",
        packet_id: str = "packet.modified.compatibility",
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = schema_version
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = []
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

    def _store_evidence(self, *, evidence_id: str, subject_ref: str, state: str = "automated_tested") -> str:
        return self.store.store(
            self._evidence(evidence_id=evidence_id, subject_ref=subject_ref, state=state),
            "evidence-record.schema.json",
        ).reference

    def test_exact_result_subject_evidence_satisfies_narrow_contract(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.result",
            subject_ref=context["result_ref"],
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertEqual(resolved.claim_ref, context["claim_ref"])
        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(resolved.occupancy_ref, context["occupancy_ref"])
        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(len(resolved.modified_results), 1)
        result = resolved.modified_results[0]
        self.assertEqual(result.modification.result_artifact.reference, context["result_ref"])
        self.assertEqual(result.output_type, "kernel_contracts")
        self.assertEqual(result.required_state, "automated_tested")
        self.assertEqual(tuple(item.reference for item in result.subject_evidence), (evidence_ref,))
        self.assertEqual(tuple(item.reference for item in result.satisfying_evidence), (evidence_ref,))
        self.assertTrue(result.satisfied)
        self.assertEqual(resolved.unmatched_evidence, ())

    def test_exact_prior_subject_evidence_cannot_satisfy_result(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.prior",
            subject_ref=context["prior_ref"],
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())
        self.assertEqual(len(resolved.unmatched_evidence), 1)
        self.assertEqual(resolved.unmatched_evidence[0].evidence.reference, evidence_ref)
        self.assertEqual(resolved.unmatched_evidence[0].reason, "exact_artifact_not_modified_result")

    def test_same_logical_different_exact_result_subject_cannot_substitute(self) -> None:
        context = self._ground_context()
        decoy_ref = self.store.store(
            self._result_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.result",
                content_ref="artifact://modified/result-decoy",
            ),
            "artifact.schema.json",
        ).reference
        self.assertNotEqual(decoy_ref, context["result_ref"])
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.same-logical-decoy",
            subject_ref=decoy_ref,
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.unmatched_evidence[0].subject_ref, decoy_ref)

    def test_evidence_for_one_result_is_not_pooled_into_another_result(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_one_ref = self.store.store(
            self._prior_artifact(artifact_id="artifact.modified.one"),
            "artifact.schema.json",
        ).reference
        prior_two_ref = self.store.store(
            self._prior_artifact(
                artifact_id="artifact.modified.two",
                content_ref="artifact://modified/two/prior",
            ),
            "artifact.schema.json",
        ).reference
        base_ref = self._store_base(lane_ref, [prior_one_ref, prior_two_ref])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.modified.multi"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref
        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.modified.multi"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref
        result_one_ref = self.store.store(
            self._result_artifact(
                base_ref=base_ref,
                artifact_id="artifact.modified.one.result",
                content_ref="artifact://modified/one/result",
            ),
            "artifact.schema.json",
        ).reference
        result_two_ref = self.store.store(
            self._result_artifact(
                base_ref=base_ref,
                artifact_id="artifact.modified.two.result",
                content_ref="artifact://modified/two/result",
            ),
            "artifact.schema.json",
        ).reference
        context = {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_one_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
            "result_ref": result_one_ref,
        }
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.only-one",
            subject_ref=result_one_ref,
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[evidence_ref],
            modified=[
                {
                    "prior_artifact_ref": prior_one_ref,
                    "result_artifact_ref": result_one_ref,
                },
                {
                    "prior_artifact_ref": prior_two_ref,
                    "result_artifact_ref": result_two_ref,
                },
            ],
            packet_id="packet.modified.multi",
        )

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertEqual(tuple(item.satisfied for item in resolved.modified_results), (True, False))
        self.assertEqual(resolved.modified_results[1].subject_evidence, ())

    def test_non_exact_subject_remains_explicitly_unmatched(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.non-exact",
            subject_ref="artifact.modified.result",
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.unmatched_evidence[0].reason, "non_exact_subject")

    def test_wrong_kind_exact_subject_fails_closed(self) -> None:
        context = self._ground_context()
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.wrong-kind",
            subject_ref=context["lane_ref"],
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        with self.assertRaises(EvidenceSubjectKindError):
            preflight_modified_result_compatibility(self.store, packet_ref)

    def test_missing_and_duplicate_contract_entries_fail_closed(self) -> None:
        missing_output_lane = self._fixture("lane.schema.json")
        missing_output_lane["outputs"] = []
        context = self._ground_context(missing_output_lane)
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.missing-output",
            subject_ref=context["result_ref"],
        )
        with self.assertRaises(OutputContractNotFoundError):
            preflight_modified_result_compatibility(
                self.store,
                self._submit_packet(context, evidence_refs=[evidence_ref]),
            )

        duplicate_output_lane = self._fixture("lane.schema.json")
        duplicate_output_lane["outputs"].append(copy.deepcopy(duplicate_output_lane["outputs"][0]))
        context = self._ground_context(duplicate_output_lane)
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.duplicate-output",
            subject_ref=context["result_ref"],
        )
        with self.assertRaises(OutputContractAmbiguityError):
            preflight_modified_result_compatibility(
                self.store,
                self._submit_packet(context, evidence_refs=[evidence_ref]),
            )

        missing_requirement_lane = self._fixture("lane.schema.json")
        missing_requirement_lane["evidence_requirements"] = []
        context = self._ground_context(missing_requirement_lane)
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.missing-requirement",
            subject_ref=context["result_ref"],
        )
        with self.assertRaises(EvidenceRequirementNotFoundError):
            preflight_modified_result_compatibility(
                self.store,
                self._submit_packet(context, evidence_refs=[evidence_ref]),
            )

        duplicate_requirement_lane = self._fixture("lane.schema.json")
        duplicate_requirement_lane["evidence_requirements"].append(
            copy.deepcopy(duplicate_requirement_lane["evidence_requirements"][0])
        )
        context = self._ground_context(duplicate_requirement_lane)
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.duplicate-requirement",
            subject_ref=context["result_ref"],
        )
        with self.assertRaises(EvidenceRequirementAmbiguityError):
            preflight_modified_result_compatibility(
                self.store,
                self._submit_packet(context, evidence_refs=[evidence_ref]),
            )

    def test_multiple_required_states_remain_semantically_unresolved(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane["evidence_requirements"][0]["required_states"] = [
            "implemented",
            "automated_tested",
        ]
        context = self._ground_context(lane)
        evidence_ref = self._store_evidence(
            evidence_id="evidence.modified.multiple-required",
            subject_ref=context["result_ref"],
        )
        packet_ref = self._submit_packet(context, evidence_refs=[evidence_ref])

        with self.assertRaises(RequiredStateSemanticsUnresolvedError):
            preflight_modified_result_compatibility(self.store, packet_ref)

    def test_conflicting_exact_subject_evidence_remains_explicit_not_closure(self) -> None:
        context = self._ground_context()
        passing_ref = self._store_evidence(
            evidence_id="evidence.modified.passing",
            subject_ref=context["result_ref"],
            state="automated_tested",
        )
        conflicting_ref = self._store_evidence(
            evidence_id="evidence.modified.conflicting",
            subject_ref=context["result_ref"],
            state="invalidated",
        )
        packet_ref = self._submit_packet(
            context,
            evidence_refs=[passing_ref, conflicting_ref],
        )

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)
        result = resolved.modified_results[0]

        self.assertTrue(result.satisfied)
        self.assertEqual(
            tuple(item.reference for item in result.subject_evidence),
            (passing_ref, conflicting_ref),
        )
        self.assertEqual(
            tuple(item.reference for item in result.satisfying_evidence),
            (passing_ref,),
        )

    def test_artifact_local_evidence_refs_do_not_override_packet_subject_binding(self) -> None:
        context = self._ground_context()
        decoy_ref = self._store_evidence(
            evidence_id="evidence.modified.local-decoy",
            subject_ref=context["prior_ref"],
        )
        result_ref = self.store.store(
            self._result_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.result-with-local-evidence",
                content_ref="artifact://modified/result-with-local-evidence",
                evidence_refs=[decoy_ref],
            ),
            "artifact.schema.json",
        ).reference
        context["result_ref"] = result_ref
        packet_ref = self._submit_packet(context, evidence_refs=[decoy_ref])

        resolved = preflight_modified_result_compatibility(self.store, packet_ref)

        self.assertFalse(resolved.modified_results[0].satisfied)
        self.assertEqual(resolved.modified_results[0].subject_evidence, ())
        self.assertEqual(resolved.unmatched_evidence[0].evidence.reference, decoy_ref)

    def test_historical_v03_modified_entry_cannot_enter_compatibility(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            schema_version="0.3",
            modified=["artifact.modified"],
        )

        with self.assertRaises(ModifiedArtifactContractVersionError):
            preflight_modified_result_compatibility(self.store, packet_ref)


if __name__ == "__main__":
    unittest.main()
