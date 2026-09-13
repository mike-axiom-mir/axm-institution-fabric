from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import (
    ContractValidationError,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)
from axm_institution.store import FilesystemObjectStore, ObjectNotFoundError

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "contracts" / "valid.json"


class PostBaseAuthoritativeReferenceAdversarialTests(unittest.TestCase):
    """Lane 03 exact-head adversarial checks for Decision 007's direct refs.

    These tests intentionally stay below lifecycle mutation. They challenge whether
    immutable relationship identity survives later same-logical-id objects, older
    base members, storage order, malformed/wrong-kind input, and missing exact targets
    without inventing a newest/current fallback.
    """

    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def base_revision(self, logical_id: str):
        revision = copy.deepcopy(self.valid["state-revision.schema.json"])
        revision["id"] = logical_id
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["return_packet_refs"] = []
        revision["uncertainties"] = [
            "Lane 03 adversarial chronology fixture; later lifecycle objects are intentionally absent."
        ]
        validate_instance(revision, "state-revision.schema.json")
        return revision

    def occupancy(self, base_ref: str, *, actor_ref: str, logical_id: str = "occupancy.same"):
        occupancy = copy.deepcopy(self.valid["occupancy.schema.json"])
        occupancy["id"] = logical_id
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["actor_ref"] = actor_ref
        occupancy["claim_ids"] = []
        validate_instance(occupancy, "occupancy.schema.json")
        return occupancy

    def claim(
        self,
        base_ref: str,
        occupancy_ref: str,
        *,
        summary: str,
        logical_id: str = "claim.same",
    ):
        claim = copy.deepcopy(self.valid["work-claim.schema.json"])
        claim["id"] = logical_id
        claim["base_state_revision_ref"] = base_ref
        claim["occupancy_ref"] = occupancy_ref
        claim["summary"] = summary
        validate_instance(claim, "work-claim.schema.json")
        return claim

    def packet(
        self,
        base_ref: str,
        claim_ref: str,
        *,
        logical_id: str = "packet.same",
    ):
        packet = copy.deepcopy(self.valid["return-packet.schema.json"])
        packet["id"] = logical_id
        packet["base_state_revision_ref"] = base_ref
        packet["claim_ref"] = claim_ref
        validate_instance(packet, "return-packet.schema.json")
        return packet

    def test_later_same_id_occupancy_cannot_rebind_existing_claim(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)
            base_result = store.store(
                self.base_revision("revision.adv16.occupancy-recency"),
                "state-revision.schema.json",
            )

            occupancy_a = self.occupancy(
                base_result.reference,
                actor_ref="fixture:occupant-a",
            )
            occupancy_a_result = store.store(occupancy_a, "occupancy.schema.json")
            claim = self.claim(
                base_result.reference,
                occupancy_a_result.reference,
                summary="Bind exact occupancy A before a later same-id occupancy exists.",
            )
            claim_result = store.store(claim, "work-claim.schema.json")

            occupancy_b = self.occupancy(
                base_result.reference,
                actor_ref="fixture:occupant-b",
            )
            occupancy_b_result = store.store(occupancy_b, "occupancy.schema.json")

            self.assertEqual(
                parse_immutable_ref(occupancy_a_result.reference).logical_id,
                parse_immutable_ref(occupancy_b_result.reference).logical_id,
            )
            self.assertNotEqual(occupancy_a_result.reference, occupancy_b_result.reference)

            loaded_claim = store.load(claim_result.reference)
            self.assertEqual(loaded_claim["occupancy_ref"], occupancy_a_result.reference)
            self.assertNotEqual(loaded_claim["occupancy_ref"], occupancy_b_result.reference)
            self.assertEqual(
                store.load(loaded_claim["occupancy_ref"])["actor_ref"],
                "fixture:occupant-a",
            )

    def test_later_same_id_claim_cannot_rebind_existing_packet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)
            base_result = store.store(
                self.base_revision("revision.adv16.claim-recency"),
                "state-revision.schema.json",
            )
            occupancy_result = store.store(
                self.occupancy(base_result.reference, actor_ref="fixture:occupant"),
                "occupancy.schema.json",
            )

            claim_a_result = store.store(
                self.claim(
                    base_result.reference,
                    occupancy_result.reference,
                    summary="Claim A is the exact packet target.",
                ),
                "work-claim.schema.json",
            )
            packet_result = store.store(
                self.packet(base_result.reference, claim_a_result.reference),
                "return-packet.schema.json",
            )

            claim_b_result = store.store(
                self.claim(
                    base_result.reference,
                    occupancy_result.reference,
                    summary="Claim B is later but has the same logical id.",
                ),
                "work-claim.schema.json",
            )

            self.assertEqual(
                parse_immutable_ref(claim_a_result.reference).logical_id,
                parse_immutable_ref(claim_b_result.reference).logical_id,
            )
            self.assertNotEqual(claim_a_result.reference, claim_b_result.reference)

            loaded_packet = store.load(packet_result.reference)
            self.assertEqual(loaded_packet["claim_ref"], claim_a_result.reference)
            self.assertNotEqual(loaded_packet["claim_ref"], claim_b_result.reference)
            self.assertEqual(
                store.load(loaded_packet["claim_ref"])["summary"],
                "Claim A is the exact packet target.",
            )

    def test_same_id_occupancy_already_in_base_cannot_substitute_post_base_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)

            prior_result = store.store(
                self.base_revision("revision.adv16.prior-occupancy"),
                "state-revision.schema.json",
            )
            old_occupancy_result = store.store(
                self.occupancy(
                    prior_result.reference,
                    actor_ref="fixture:old-occupant",
                    logical_id="occupancy.same",
                ),
                "occupancy.schema.json",
            )

            work_base = self.base_revision("revision.adv16.work-occupancy")
            work_base["occupancy_refs"] = [old_occupancy_result.reference]
            work_base_result = store.store(work_base, "state-revision.schema.json")

            new_occupancy_result = store.store(
                self.occupancy(
                    work_base_result.reference,
                    actor_ref="fixture:new-post-base-occupant",
                    logical_id="occupancy.same",
                ),
                "occupancy.schema.json",
            )
            self.assertNotIn(new_occupancy_result.reference, work_base["occupancy_refs"])

            claim_result = store.store(
                self.claim(
                    work_base_result.reference,
                    new_occupancy_result.reference,
                    summary="Direct post-base target must beat same-id base history.",
                    logical_id="claim.post-base",
                ),
                "work-claim.schema.json",
            )
            loaded_claim = store.load(claim_result.reference)
            self.assertEqual(loaded_claim["occupancy_ref"], new_occupancy_result.reference)
            self.assertNotEqual(loaded_claim["occupancy_ref"], old_occupancy_result.reference)

    def test_same_id_claim_already_in_base_cannot_substitute_post_base_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)

            prior_result = store.store(
                self.base_revision("revision.adv16.prior-claim"),
                "state-revision.schema.json",
            )
            prior_occupancy_result = store.store(
                self.occupancy(
                    prior_result.reference,
                    actor_ref="fixture:prior-occupant",
                    logical_id="occupancy.prior",
                ),
                "occupancy.schema.json",
            )
            old_claim_result = store.store(
                self.claim(
                    prior_result.reference,
                    prior_occupancy_result.reference,
                    summary="Old claim instance carried into the later base.",
                    logical_id="claim.same",
                ),
                "work-claim.schema.json",
            )

            work_base = self.base_revision("revision.adv16.work-claim")
            work_base["claim_refs"] = [old_claim_result.reference]
            work_base_result = store.store(work_base, "state-revision.schema.json")

            new_occupancy_result = store.store(
                self.occupancy(
                    work_base_result.reference,
                    actor_ref="fixture:new-occupant",
                    logical_id="occupancy.new",
                ),
                "occupancy.schema.json",
            )
            new_claim_result = store.store(
                self.claim(
                    work_base_result.reference,
                    new_occupancy_result.reference,
                    summary="New post-base claim with an old logical id.",
                    logical_id="claim.same",
                ),
                "work-claim.schema.json",
            )
            self.assertNotIn(new_claim_result.reference, work_base["claim_refs"])

            packet_result = store.store(
                self.packet(
                    work_base_result.reference,
                    new_claim_result.reference,
                    logical_id="packet.post-base",
                ),
                "return-packet.schema.json",
            )
            loaded_packet = store.load(packet_result.reference)
            self.assertEqual(loaded_packet["claim_ref"], new_claim_result.reference)
            self.assertNotEqual(loaded_packet["claim_ref"], old_claim_result.reference)

    def test_wrong_kind_and_trailing_data_fail_real_store_publication(self):
        malformed_cases = (
            (
                "work-claim.schema.json",
                "occupancy_ref",
                make_immutable_ref("objective.schema.json", self.valid["objective.schema.json"]),
            ),
            (
                "return-packet.schema.json",
                "claim_ref",
                make_immutable_ref("occupancy.schema.json", self.valid["occupancy.schema.json"]),
            ),
            (
                "work-claim.schema.json",
                "occupancy_ref",
                "axmref:v1:occupancy:occupancy.same:-:sha256:" + "1" * 64 + "\n",
            ),
            (
                "return-packet.schema.json",
                "claim_ref",
                "axmref:v1:work-claim:claim.same:-:sha256:" + "2" * 64 + "x",
            ),
        )

        for schema_name, field, reference in malformed_cases:
            with self.subTest(schema=schema_name, field=field, reference=reference):
                with tempfile.TemporaryDirectory() as temp_dir:
                    store = FilesystemObjectStore(temp_dir)
                    candidate = copy.deepcopy(self.valid[schema_name])
                    candidate[field] = reference
                    with self.assertRaises(ContractValidationError):
                        store.store(candidate, schema_name)
                    self.assertEqual(list(Path(temp_dir).rglob("*.json")), [])

    def test_syntactically_exact_but_missing_target_requires_explicit_future_load(self):
        """Freeze the current truth boundary: syntax is not target existence/closure."""

        with tempfile.TemporaryDirectory() as temp_dir:
            store = FilesystemObjectStore(temp_dir)
            base_result = store.store(
                self.base_revision("revision.adv16.missing-target"),
                "state-revision.schema.json",
            )

            missing_occupancy_ref = (
                "axmref:v1:occupancy:occupancy.missing:-:sha256:" + "a" * 64
            )
            claim = self.claim(
                base_result.reference,
                missing_occupancy_ref,
                summary="Reference language is valid but target is deliberately absent.",
                logical_id="claim.missing-target",
            )
            claim_result = store.store(claim, "work-claim.schema.json")
            self.assertEqual(
                store.load(claim_result.reference)["occupancy_ref"],
                missing_occupancy_ref,
            )
            with self.assertRaises(ObjectNotFoundError):
                store.load(missing_occupancy_ref)


if __name__ == "__main__":
    unittest.main()
