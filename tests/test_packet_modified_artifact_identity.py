from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_artifact_provenance import (
    ArtifactProducerLaneMismatchError,
    ArtifactProvenanceBaseMismatchError,
)
from axm_institution.packet_modified_artifact_identity import (
    ModifiedArtifactContractVersionError,
    ModifiedArtifactPriorMembershipError,
    ModifiedArtifactReferenceError,
    preflight_modified_artifact_identity,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class ModifiedArtifactIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self):
        lane = self._fixture("lane.schema.json")
        result = self.store.store(lane, "lane.schema.json")
        return lane, result.reference

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
        producer_lane_id: str = "lane-02",
        content_ref: str = "artifact://modified/result",
        supersedes_ref: str | None = None,
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.2"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = "0.2"
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": producer_lane_id,
            "base_state_revision_ref": base_ref,
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        if supersedes_ref is None:
            artifact.pop("supersedes_ref", None)
        else:
            artifact["supersedes_ref"] = supersedes_ref
        return artifact

    def _store_base(
        self,
        lane_ref: str,
        artifact_refs: list[str],
        *,
        revision_id: str = "revision.modified.base",
        uncertainty: str = "Decision 011 modified-artifact base fixture.",
    ) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = list(artifact_refs)
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [uncertainty]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self):
        lane, lane_ref = self._store_lane()
        prior = self._prior_artifact()
        prior_ref = self.store.store(prior, "artifact.schema.json").reference
        base_ref = self._store_base(lane_ref, [prior_ref])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.modified"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.modified"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        result = self._result_artifact(base_ref=base_ref)
        result_ref = self.store.store(result, "artifact.schema.json").reference
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
        schema_version: str = "0.4",
        modified=None,
        packet_id: str = "packet.modified",
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
        packet["evidence_refs"] = []
        return submit_return_packet(self.store, packet).packet_ref

    def test_v04_explicit_prior_result_pair_resolves_exactly(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(context)

        resolved = preflight_modified_artifact_identity(self.store, packet_ref)

        self.assertEqual(resolved.claim_ref, context["claim_ref"])
        self.assertEqual(resolved.claim_base_ref, context["base_ref"])
        self.assertEqual(resolved.occupancy_ref, context["occupancy_ref"])
        self.assertEqual(resolved.lane_ref, context["lane_ref"])
        self.assertEqual(len(resolved.modifications), 1)
        modification = resolved.modifications[0]
        self.assertEqual(modification.prior_artifact.reference, context["prior_ref"])
        self.assertEqual(modification.result_artifact.reference, context["result_ref"])
        self.assertEqual(
            modification.result_provenance.provenance_base_ref,
            context["base_ref"],
        )
        self.assertEqual(modification.result_provenance.producer_lane_id, "lane-02")

    def test_historical_v03_opaque_modified_entry_remains_operationally_unresolved(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            schema_version="0.3",
            modified=["artifact.modified"],
        )

        with self.assertRaises(ModifiedArtifactContractVersionError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_v03_rejects_new_pair_shape_instead_of_silently_changing_history(self) -> None:
        context = self._ground_context()

        with self.assertRaises(ContractValidationError):
            self._submit_packet(
                context,
                schema_version="0.3",
                modified=[
                    {
                        "prior_artifact_ref": context["prior_ref"],
                        "result_artifact_ref": context["result_ref"],
                    }
                ],
            )

    def test_v04_rejects_legacy_opaque_string_instead_of_dual_authority(self) -> None:
        context = self._ground_context()

        with self.assertRaises(ContractValidationError):
            self._submit_packet(
                context,
                schema_version="0.4",
                modified=["artifact.modified"],
            )

    def test_same_logical_prior_decoy_not_in_exact_claim_base_cannot_substitute(self) -> None:
        context = self._ground_context()
        decoy = self._prior_artifact(
            artifact_id="artifact.modified",
            content_ref="artifact://modified/prior-decoy",
        )
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        self.assertNotEqual(decoy_ref, context["prior_ref"])
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": decoy_ref,
                    "result_artifact_ref": context["result_ref"],
                }
            ],
        )

        with self.assertRaises(ModifiedArtifactPriorMembershipError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_wrong_kind_prior_ref_fails_before_membership_or_logical_fallback(self) -> None:
        context = self._ground_context()
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": context["lane_ref"],
                    "result_artifact_ref": context["result_ref"],
                }
            ],
        )

        with self.assertRaises(ModifiedArtifactReferenceError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_missing_exact_prior_listed_in_claim_base_fails_exact_load(self) -> None:
        lane, lane_ref = self._store_lane()
        missing_prior_ref = (
            "axmref:v1:artifact:artifact.modified.missing:v=0.1:sha256:" + "a" * 64
        )
        base_ref = self._store_base(lane_ref, [missing_prior_ref])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.modified.missing"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref
        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.modified.missing"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref
        result_ref = self.store.store(
            self._result_artifact(base_ref=base_ref),
            "artifact.schema.json",
        ).reference
        context = {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": missing_prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
            "result_ref": result_ref,
        }
        packet_ref = self._submit_packet(context)

        with self.assertRaises(ModifiedArtifactReferenceError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_result_provenance_must_equal_exact_claim_base(self) -> None:
        context = self._ground_context()
        other_base_ref = self._store_base(
            context["lane_ref"],
            [context["prior_ref"]],
            revision_id="revision.modified.other",
            uncertainty="different exact base",
        )
        stale_result_ref = self.store.store(
            self._result_artifact(
                base_ref=other_base_ref,
                artifact_id="artifact.modified.stale-result",
            ),
            "artifact.schema.json",
        ).reference
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": stale_result_ref,
                }
            ],
        )

        with self.assertRaises(ArtifactProvenanceBaseMismatchError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_result_producer_lane_must_match_exact_claim_base_lane(self) -> None:
        context = self._ground_context()
        wrong_lane_result_ref = self.store.store(
            self._result_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.wrong-lane-result",
                producer_lane_id="lane-decoy",
            ),
            "artifact.schema.json",
        ).reference
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": wrong_lane_result_ref,
                }
            ],
        )

        with self.assertRaises(ArtifactProducerLaneMismatchError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_supersedes_ref_does_not_override_explicit_prior_pair(self) -> None:
        context = self._ground_context()
        decoy = self._prior_artifact(
            artifact_id="artifact.modified.decoy",
            content_ref="artifact://modified/decoy",
        )
        decoy_ref = self.store.store(decoy, "artifact.schema.json").reference
        result_ref = self.store.store(
            self._result_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.result-with-supersedes",
                supersedes_ref=decoy_ref,
            ),
            "artifact.schema.json",
        ).reference
        packet_ref = self._submit_packet(
            context,
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": result_ref,
                }
            ],
        )

        resolved = preflight_modified_artifact_identity(self.store, packet_ref)

        self.assertEqual(
            resolved.modifications[0].prior_artifact.reference,
            context["prior_ref"],
        )
        self.assertNotEqual(
            resolved.modifications[0].prior_artifact.reference,
            decoy_ref,
        )


if __name__ == "__main__":
    unittest.main()
