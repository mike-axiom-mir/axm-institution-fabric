from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
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


class ModifiedArtifactIdentityAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-044 attacks for Decision 011's exact prior/result pair."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self):
        lane = self._fixture("lane.schema.json")
        stored = self.store.store(lane, "lane.schema.json")
        return lane, stored.reference

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

    def _store_base(self, lane_ref: str, artifact_refs: list[str]) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.adv044.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = list(artifact_refs)
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = ["ADV-044 exact modification identity fixture."]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self):
        lane, lane_ref = self._store_lane()
        prior_ref = self.store.store(
            self._prior_artifact(), "artifact.schema.json"
        ).reference
        base_ref = self._store_base(lane_ref, [prior_ref])

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.adv044"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.adv044"
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
            "claim_ref": claim_ref,
            "result_ref": result_ref,
        }

    def _submit(self, context, *, packet_id: str, modified, schema_version: str = "0.4"):
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = schema_version
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = []
        packet["artifacts_modified"] = modified
        packet["evidence_refs"] = []
        return submit_return_packet(self.store, packet).packet_ref

    def test_adv044_a_v03_exact_looking_single_ref_remains_unresolved(self) -> None:
        """Legacy one-string packets must not gain exact-pair meaning from string shape."""
        context = self._ground_context()
        packet_ref = self._submit(
            context,
            packet_id="packet.adv044.a",
            schema_version="0.3",
            modified=[context["prior_ref"]],
        )

        with self.assertRaises(ModifiedArtifactContractVersionError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_adv044_b_wrong_kind_and_missing_result_refs_fail_closed(self) -> None:
        """The result side gets the same exact kind/existence treatment as the prior side."""
        context = self._ground_context()
        wrong_kind_packet = self._submit(
            context,
            packet_id="packet.adv044.b.wrong-kind",
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": context["lane_ref"],
                }
            ],
        )
        with self.assertRaises(ModifiedArtifactReferenceError):
            preflight_modified_artifact_identity(self.store, wrong_kind_packet)

        missing_ref = (
            "axmref:v1:artifact:artifact.modified.result:v=0.2:sha256:" + "b" * 64
        )
        missing_packet = self._submit(
            context,
            packet_id="packet.adv044.b.missing",
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": missing_ref,
                }
            ],
        )
        with self.assertRaises(ModifiedArtifactReferenceError):
            preflight_modified_artifact_identity(self.store, missing_packet)

    def test_adv044_c_corrupt_exact_result_cannot_survive_identity_verification(self) -> None:
        """An exact-looking durable target must still reproduce its claimed immutable identity."""
        context = self._ground_context()
        self.store._object_path(context["result_ref"]).write_bytes(b"{}")
        packet_ref = self._submit(
            context,
            packet_id="packet.adv044.c",
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": context["result_ref"],
                }
            ],
        )

        with self.assertRaises(ModifiedArtifactReferenceError):
            preflight_modified_artifact_identity(self.store, packet_ref)

    def test_adv044_d_later_same_logical_result_decoy_gets_no_recency_authority(self) -> None:
        """A later stored same-id result cannot replace the exact result named by the packet."""
        context = self._ground_context()
        decoy_ref = self.store.store(
            self._result_artifact(
                base_ref=context["base_ref"],
                artifact_id="artifact.modified.result",
                content_ref="artifact://modified/result-later-decoy",
            ),
            "artifact.schema.json",
        ).reference
        self.assertNotEqual(decoy_ref, context["result_ref"])

        packet_ref = self._submit(
            context,
            packet_id="packet.adv044.d",
            modified=[
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": context["result_ref"],
                }
            ],
        )
        resolved = preflight_modified_artifact_identity(self.store, packet_ref)

        self.assertEqual(
            resolved.modifications[0].result_artifact.reference,
            context["result_ref"],
        )
        self.assertNotEqual(
            resolved.modifications[0].result_artifact.reference,
            decoy_ref,
        )

    def test_adv044_e_array_order_cannot_hide_invalid_prior_relation(self) -> None:
        """A valid relation cannot make an invalid relation disappear by appearing first or last."""
        context = self._ground_context()
        decoy_prior_ref = self.store.store(
            self._prior_artifact(
                artifact_id="artifact.modified",
                content_ref="artifact://modified/prior-outside-base",
            ),
            "artifact.schema.json",
        ).reference
        valid = {
            "prior_artifact_ref": context["prior_ref"],
            "result_artifact_ref": context["result_ref"],
        }
        invalid = {
            "prior_artifact_ref": decoy_prior_ref,
            "result_artifact_ref": context["result_ref"],
        }

        for packet_id, relations in (
            ("packet.adv044.e.valid-first", [valid, invalid]),
            ("packet.adv044.e.invalid-first", [invalid, valid]),
        ):
            packet_ref = self._submit(
                context,
                packet_id=packet_id,
                modified=relations,
            )
            with self.assertRaises(ModifiedArtifactPriorMembershipError):
                preflight_modified_artifact_identity(self.store, packet_ref)


if __name__ == "__main__":
    unittest.main()
