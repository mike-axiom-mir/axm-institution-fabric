from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import parse_immutable_ref
from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_artifact_provenance import (
    ArtifactProvenanceBaseMismatchError,
    ArtifactProvenanceReferenceError,
    preflight_created_artifact_provenance,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class CreatedArtifactProvenanceAdversarialTests(unittest.TestCase):
    """ADV-043: re-attack Decision 010 without opening later lifecycle stages."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _store_lane(self):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        return lane, lane_ref

    def _store_base(
        self,
        lane_ref: str,
        *,
        revision_id: str = "revision.provenance.adversarial",
        uncertainty: str,
        parent_revision_ref: str | None = None,
    ) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = revision_id
        revision["parent_revision_ref"] = parent_revision_ref
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = []
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [uncertainty]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _artifact_v02(
        self,
        *,
        base_ref: str,
        artifact_id: str,
        producer_lane_id: str = "lane-02",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.2"
        artifact["id"] = artifact_id
        artifact["version"] = "0.2"
        artifact["type"] = "kernel_contracts"
        artifact["content_ref"] = f"artifact://{artifact_id}"
        artifact["provenance"] = {
            "producer_lane_id": producer_lane_id,
            "base_state_revision_ref": base_ref,
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        return artifact

    def _ground_packet(
        self,
        *,
        lane,
        base_ref: str,
        artifacts: list[dict],
        packet_id: str,
        reverse_packet_order: bool = False,
    ) -> dict[str, object]:
        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.provenance.adversarial"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.provenance.adversarial"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        artifact_refs: list[str] = []
        evidence_refs: list[str] = []
        for index, artifact in enumerate(artifacts):
            artifact_ref = self.store.store(artifact, "artifact.schema.json").reference
            artifact_refs.append(artifact_ref)

            evidence = self._fixture("evidence-record.schema.json")
            evidence["id"] = f"evidence.provenance.adversarial.{index}.{artifact['id']}"
            evidence["subject_ref"] = artifact_ref
            evidence["state"] = "automated_tested"
            evidence["claim"] = "ADV-043 exact created-artifact provenance witness."
            evidence_ref = self.store.store(
                evidence, "evidence-record.schema.json"
            ).reference
            evidence_refs.append(evidence_ref)

        if reverse_packet_order:
            artifact_refs.reverse()
            evidence_refs.reverse()

        packet = self._fixture("return-packet.schema.json")
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = artifact_refs
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = evidence_refs
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        return {
            "claim_ref": claim_ref,
            "packet_ref": packet_ref,
            "artifact_refs": tuple(artifact_refs),
            "evidence_refs": tuple(evidence_refs),
        }

    def test_adv043_a_structural_exact_lookalike_cannot_bypass_stage2_parser(self) -> None:
        lane, lane_ref = self._store_lane()
        base_ref = self._store_base(lane_ref, uncertainty="authoritative exact base")
        malformed_ref = base_ref.replace(
            "state-revision:revision.provenance.adversarial:",
            "state-revision:%72evision.provenance.adversarial:",
            1,
        )
        self.assertNotEqual(malformed_ref, base_ref)
        self.assertIn("%72", malformed_ref)

        # The v0.2 JSON Schema intentionally provides only a structural spelling filter.
        # This exact-looking but non-canonical ref therefore reaches the operational
        # Stage 2 parser, which must reject percent-encoding of an unreserved character.
        artifact = self._artifact_v02(
            base_ref=malformed_ref,
            artifact_id="artifact.adv043.parser-boundary",
        )
        context = self._ground_packet(
            lane=lane,
            base_ref=base_ref,
            artifacts=[artifact],
            packet_id="packet.adv043.parser-boundary",
        )

        with self.assertRaises(ArtifactProvenanceReferenceError):
            preflight_created_artifact_provenance(
                self.store, context["packet_ref"]  # type: ignore[arg-type]
            )

    def test_adv043_b_corrupt_exact_provenance_target_fails_closed(self) -> None:
        lane, lane_ref = self._store_lane()
        claim_base_ref = self._store_base(lane_ref, uncertainty="claim base")
        provenance_base_ref = self._store_base(
            lane_ref,
            revision_id="revision.provenance.corrupt",
            uncertainty="will be corrupted after exact publication",
        )
        artifact = self._artifact_v02(
            base_ref=provenance_base_ref,
            artifact_id="artifact.adv043.corrupt-target",
        )
        context = self._ground_packet(
            lane=lane,
            base_ref=claim_base_ref,
            artifacts=[artifact],
            packet_id="packet.adv043.corrupt-target",
        )

        parsed = parse_immutable_ref(provenance_base_ref)
        target = (
            self.store.objects_dir
            / parsed.kind
            / parsed.sha256[:2]
            / f"{parsed.sha256}.json"
        )
        target.write_text("{}", encoding="utf-8")

        with self.assertRaises(ArtifactProvenanceReferenceError):
            preflight_created_artifact_provenance(
                self.store, context["packet_ref"]  # type: ignore[arg-type]
            )

    def test_adv043_c_exact_ancestor_base_is_still_stale_for_created_output(self) -> None:
        lane, lane_ref = self._store_lane()
        old_ref = self._store_base(
            lane_ref,
            revision_id="revision.provenance.old",
            uncertainty="older exact work base",
        )
        current_ref = self._store_base(
            lane_ref,
            revision_id="revision.provenance.current",
            uncertainty="claim base with exact parent",
            parent_revision_ref=old_ref,
        )
        artifact = self._artifact_v02(
            base_ref=old_ref,
            artifact_id="artifact.adv043.stale-ancestor",
        )
        context = self._ground_packet(
            lane=lane,
            base_ref=current_ref,
            artifacts=[artifact],
            packet_id="packet.adv043.stale-ancestor",
        )

        with self.assertRaises(ArtifactProvenanceBaseMismatchError):
            preflight_created_artifact_provenance(
                self.store, context["packet_ref"]  # type: ignore[arg-type]
            )

    def test_adv043_d_packet_array_order_cannot_hide_one_stale_created_artifact(self) -> None:
        lane, lane_ref = self._store_lane()
        claim_base_ref = self._store_base(lane_ref, uncertainty="authoritative claim base")
        stale_ref = self._store_base(
            lane_ref,
            revision_id="revision.provenance.stale",
            uncertainty="valid exact but stale artifact base",
        )
        correct = self._artifact_v02(
            base_ref=claim_base_ref,
            artifact_id="artifact.adv043.correct",
        )
        stale = self._artifact_v02(
            base_ref=stale_ref,
            artifact_id="artifact.adv043.stale",
        )

        for reverse in (False, True):
            with self.subTest(reverse_packet_order=reverse):
                context = self._ground_packet(
                    lane=lane,
                    base_ref=claim_base_ref,
                    artifacts=[correct, stale],
                    packet_id=f"packet.adv043.order.{int(reverse)}",
                    reverse_packet_order=reverse,
                )
                with self.assertRaises(ArtifactProvenanceBaseMismatchError):
                    preflight_created_artifact_provenance(
                        self.store, context["packet_ref"]  # type: ignore[arg-type]
                    )

    def test_adv043_e_before_and_after_same_id_decoys_cannot_rebind_exact_base(self) -> None:
        lane, lane_ref = self._store_lane()
        decoy_before = self._store_base(
            lane_ref,
            uncertainty="same-logical-id decoy stored before authoritative base",
        )
        authoritative = self._store_base(
            lane_ref,
            uncertainty="authoritative exact claim and artifact base",
        )
        decoy_after = self._store_base(
            lane_ref,
            uncertainty="same-logical-id decoy stored after authoritative base",
        )
        self.assertEqual(
            parse_immutable_ref(decoy_before).logical_id,
            parse_immutable_ref(authoritative).logical_id,
        )
        self.assertEqual(
            parse_immutable_ref(decoy_after).logical_id,
            parse_immutable_ref(authoritative).logical_id,
        )
        self.assertEqual(len({decoy_before, authoritative, decoy_after}), 3)

        artifact = self._artifact_v02(
            base_ref=authoritative,
            artifact_id="artifact.adv043.storage-order",
        )
        context = self._ground_packet(
            lane=lane,
            base_ref=authoritative,
            artifacts=[artifact],
            packet_id="packet.adv043.storage-order",
        )

        result = preflight_created_artifact_provenance(
            self.store, context["packet_ref"]  # type: ignore[arg-type]
        )
        self.assertEqual(result.claim_base_ref, authoritative)
        self.assertEqual(result.created_artifacts[0].provenance_base_ref, authoritative)
        self.assertNotEqual(result.claim_base_ref, decoy_before)
        self.assertNotEqual(result.claim_base_ref, decoy_after)


if __name__ == "__main__":
    unittest.main()
