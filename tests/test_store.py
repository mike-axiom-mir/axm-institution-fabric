from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.identity import ContractValidationError, make_immutable_ref
from axm_institution.store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
    ObjectReferenceMismatchError,
)


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads((ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8"))


class FilesystemObjectStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))
        self.objective = copy.deepcopy(VALID_FIXTURES["objective.schema.json"])

    def test_store_and_exact_load_round_trip(self) -> None:
        result = self.store.store(self.objective, "objective.schema.json")
        self.assertTrue(result.created)
        self.assertIsNone(result.referenced_members_verified)
        self.assertEqual(self.store.load(result.reference), self.objective)
        self.assertEqual(
            self.store.load_bytes(result.reference),
            self.store._object_path(result.reference).read_bytes(),
        )

    def test_repeated_store_of_same_object_is_idempotent(self) -> None:
        first = self.store.store(self.objective, "objective.schema.json")
        second = self.store.store(self.objective, "objective.schema.json")
        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.reference, second.reference)

    def test_expected_reference_mismatch_fails_before_publication(self) -> None:
        changed = copy.deepcopy(self.objective)
        changed["desired_outcome"] = "A different immutable objective instance."
        wrong_reference = make_immutable_ref("objective.schema.json", changed)

        with self.assertRaises(ObjectReferenceMismatchError):
            self.store.store(
                self.objective,
                "objective.schema.json",
                expected_reference=wrong_reference,
            )

        expected = make_immutable_ref("objective.schema.json", self.objective)
        self.assertFalse(self.store._object_path(expected).exists())

    def test_corruption_after_write_is_rejected_loudly(self) -> None:
        result = self.store.store(self.objective, "objective.schema.json")
        path = self.store._object_path(result.reference)
        path.write_bytes(b" " + path.read_bytes())

        with self.assertRaises(ObjectCorruptionError):
            self.store.load(result.reference)

    def test_existing_corrupt_target_is_never_silently_overwritten(self) -> None:
        result = self.store.store(self.objective, "objective.schema.json")
        path = self.store._object_path(result.reference)
        path.write_bytes(b"{}")

        with self.assertRaises(ObjectCorruptionError):
            self.store.store(self.objective, "objective.schema.json")
        self.assertEqual(path.read_bytes(), b"{}")

    def test_invalid_object_is_rejected_before_storage(self) -> None:
        invalid = copy.deepcopy(self.objective)
        invalid.pop("id")

        with self.assertRaises(ContractValidationError):
            self.store.store(invalid, "objective.schema.json")

        stored_json = list((Path(self.tempdir.name) / "objects").rglob("*.json"))
        self.assertEqual(stored_json, [])

    def test_missing_exact_reference_fails(self) -> None:
        reference = make_immutable_ref("objective.schema.json", self.objective)
        with self.assertRaises(ObjectNotFoundError):
            self.store.load(reference)

    def test_interrupted_temp_write_is_not_visible_as_canonical_object(self) -> None:
        reference = make_immutable_ref("objective.schema.json", self.objective)
        target = self.store._object_path(reference)
        target.parent.mkdir(parents=True, exist_ok=True)
        interrupted = target.parent / ".axm-tmp-interrupted"
        interrupted.write_text('{"partial":', encoding="utf-8")

        with self.assertRaises(ObjectNotFoundError):
            self.store.load(reference)
        self.assertFalse(target.exists())
        self.assertTrue(interrupted.exists())

    def test_same_logical_id_different_instances_coexist(self) -> None:
        changed = copy.deepcopy(self.objective)
        changed["desired_outcome"] = "Second immutable instance under the same logical id."

        first = self.store.store(self.objective, "objective.schema.json")
        second = self.store.store(changed, "objective.schema.json")

        self.assertNotEqual(first.reference, second.reference)
        self.assertEqual(self.store.load(first.reference), self.objective)
        self.assertEqual(self.store.load(second.reference), changed)

    def test_state_revision_storage_does_not_claim_member_closure(self) -> None:
        revision = copy.deepcopy(VALID_FIXTURES["state-revision.schema.json"])
        result = self.store.store(revision, "state-revision.schema.json")

        self.assertTrue(result.created)
        self.assertFalse(result.referenced_members_verified)
        self.assertEqual(self.store.load(result.reference), revision)

    def test_explicit_wrong_schema_cannot_reinterpret_reference(self) -> None:
        result = self.store.store(self.objective, "objective.schema.json")
        with self.assertRaises(ObjectReferenceMismatchError):
            self.store.load(result.reference, "artifact.schema.json")


if __name__ == "__main__":
    unittest.main()
