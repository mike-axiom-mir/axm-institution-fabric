from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    preflight_packet_integration_eligibility,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class PacketIntegrationEligibilityV04ContinuityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def test_typed_source_artifact_preserves_exact_work_base_without_source_authority(self) -> None:
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference

        base = self._fixture("state-revision.schema.json")
        base["id"] = "revision.eligibility.v04.base"
        base["lane_refs"] = [lane_ref]
        base["occupancy_refs"] = []
        base["claim_refs"] = []
        base["artifact_refs"] = []
        base["evidence_refs"] = []
        base["return_packet_refs"] = []
        base["integration_receipt_refs"] = []
        base["uncertainties"] = ["Decision 024 v0.4 provenance continuity fixture."]
        base_ref = self.store.store(base, "state-revision.schema.json").reference

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.eligibility.v04"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.eligibility.v04"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.4"
        artifact["id"] = "artifact.eligibility.v04"
        artifact["version"] = "0.4"
        artifact["type"] = "kernel_contracts"
        artifact["content_ref"] = "artifact://eligibility/v04"
        artifact["provenance"] = {
            "producer_lane_id": lane["id"],
            "base_state_revision_ref": base_ref,
            "source_declarations": {
                "decl-a": {
                    "source_class": "opaque_label",
                    "token": "authored-source-fact-only",
                }
            },
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        artifact_ref = self.store.store(artifact, "artifact.schema.json").reference

        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = "evidence.eligibility.v04"
        evidence["subject_ref"] = artifact_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 024 v0.4 exact subject-bound evidence."
        evidence_ref = self.store.store(
            evidence, "evidence-record.schema.json"
        ).reference

        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = "packet.eligibility.v04"
        packet["base_state_revision_ref"] = base_ref
        packet["lane_id"] = lane["id"]
        packet["claim_ref"] = claim_ref
        packet["artifacts_created"] = [artifact_ref]
        packet["artifacts_modified"] = []
        packet["evidence_refs"] = [evidence_ref]
        packet_ref = submit_return_packet(self.store, packet).packet_ref

        before = self.store.load(artifact_ref, "artifact.schema.json")
        resolved = preflight_packet_integration_eligibility(self.store, packet_ref)
        after = self.store.load(artifact_ref, "artifact.schema.json")

        self.assertEqual(
            resolved.eligibility_outcome,
            ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        )
        self.assertEqual(resolved.created_output_refs, (artifact_ref,))
        self.assertEqual(before, after)
        self.assertEqual(
            after["provenance"]["source_declarations"]["decl-a"]["token"],
            "authored-source-fact-only",
        )


if __name__ == "__main__":
    unittest.main()
