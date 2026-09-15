from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from axm_institution.connected_monolith import (
    ConnectedMonolithCatalog,
    ConnectedMonolithContractError,
    ConnectedMonolithIntegrityError,
)


TRUTH_BOUNDARY = (
    "aggregate labels and exact declared leaf IDs are counted separately; addressable is not callable. "
    "Only grounded adapters or named workflows invoke source behavior, and every unbound declaration remains blocked."
)


def endpoint(address: str, status: str, *, source_execution: bool = False, provides=(), accepts=(), **adapter_extra):
    adapter = {
        "kind": "test-adapter",
        "source_capability_execution": source_execution,
        "status": status,
        **adapter_extra,
    }
    return {
        "accepts": list(accepts),
        "adapter": adapter,
        "address": address,
        "capability": address.split("::")[-1],
        "commit": "a" * 40,
        "evidence_status": "detected_not_executed",
        "module": address.split("::")[0],
        "provides": list(provides),
        "repository": "mike-axiom-mir/example",
    }


def fabric(endpoints):
    counts = {}
    for item in endpoints:
        status = item["adapter"]["status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "authority": {
            "automatic_canon": False,
            "automatic_install": False,
            "automatic_merge": False,
            "automatic_network": False,
            "automatic_source_mutation": False,
        },
        "endpoints": endpoints,
        "schema": "axm.monolith.execution-fabric/v0.1",
        "summary": {"adapter_status_counts": counts, "endpoint_count": len(endpoints)},
        "truth_boundary": TRUTH_BOUNDARY,
    }


def raw_fabric(endpoints):
    return json.dumps(fabric(endpoints), sort_keys=True, separators=(",", ":")).encode("utf-8")


def workflow_registry(*capability_addresses: str):
    return {
        "schema": "axm.monolith.workflow-registry/v0.1",
        "workflow_count": 1,
        "workflows": [
            {
                "id": "ghost-studio.blackline-3d.v0.4",
                "status": "callable",
                "stages": [
                    {"order": index + 1, "capability": address, "contract": "test"}
                    for index, address in enumerate(capability_addresses)
                ],
            }
        ],
    }


def raw_workflow_registry(*capability_addresses: str):
    return json.dumps(
        workflow_registry(*capability_addresses), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


class ConnectedMonolithCatalogTests(unittest.TestCase):
    def test_creation_machine_named_workflow_is_discoverable_but_grants_no_action_authority(self):
        raw = raw_fabric(
            [
                endpoint(
                    "axm-universal-creation::creation.universal",
                    "callable_through_named_workflow",
                    source_execution=True,
                    accepts=("capability.request", "objective", "specification"),
                    provides=("artifact", "artifact.software", "capability.generated"),
                    workflow="ghost-studio.blackline-3d.v0.4",
                    stage="brief-to-visual-recipe",
                )
            ]
        )
        catalog = ConnectedMonolithCatalog.from_execution_fabric_bytes(raw)
        (fact,) = catalog.query(module="axm-universal-creation", provides_all=("capability.generated",))
        self.assertEqual(fact.address, "axm-universal-creation::creation.universal")
        self.assertEqual(fact.institution_standing, "source_callable_named_workflow")
        self.assertEqual(fact.named_workflow, "ghost-studio.blackline-3d.v0.4")
        self.assertEqual(fact.workflow_stage, "brief-to-visual-recipe")
        self.assertTrue(fact.source_callable)
        self.assertEqual(fact.institution_action_authority, "discovery_only_no_action_authority")

    def test_non_callable_statuses_are_not_promoted(self):
        endpoints = [
            endpoint("uc::inspection", "executable_inspection"),
            endpoint("uc::tests", "executable_test_evidence"),
            endpoint("uc::launch", "launchable_local_surface"),
            endpoint("uc::contract", "blocked_missing_native_contract"),
            endpoint("uc::leaf", "blocked_missing_callable_binding"),
        ]
        catalog = ConnectedMonolithCatalog.from_execution_fabric_bytes(raw_fabric(endpoints))
        by_status = {fact.adapter_status: fact for fact in catalog.endpoints}
        self.assertEqual(by_status["executable_inspection"].institution_standing, "inspectable_not_source_execution")
        self.assertEqual(
            by_status["executable_test_evidence"].institution_standing,
            "test_entrypoint_evidence_not_tests_passed",
        )
        self.assertEqual(by_status["launchable_local_surface"].institution_standing, "launchable_not_runtime_verified")
        self.assertFalse(any(fact.source_callable for fact in catalog.endpoints))

    def test_query_is_exact_and_deterministic_not_confidence_ranked(self):
        endpoints = [
            endpoint("z::cap", "executable_inspection", provides=("artifact",)),
            endpoint("a::cap", "executable_inspection", provides=("artifact",)),
            endpoint("m::other", "executable_inspection", provides=("other",)),
        ]
        catalog = ConnectedMonolithCatalog.from_execution_fabric_bytes(raw_fabric(endpoints))
        results = catalog.query(provides_all=("artifact",))
        self.assertEqual([fact.address for fact in results], ["a::cap", "z::cap"])

    def test_unknown_status_fails_closed(self):
        with self.assertRaises(ConnectedMonolithContractError):
            ConnectedMonolithCatalog.from_execution_fabric_bytes(
                raw_fabric([endpoint("uc::future", "future_magic_status")])
            )

    def test_summary_mismatch_is_rejected(self):
        data = fabric([endpoint("uc::inspection", "executable_inspection")])
        data["summary"]["endpoint_count"] = 2
        with self.assertRaises(ConnectedMonolithContractError):
            ConnectedMonolithCatalog.from_execution_fabric_bytes(json.dumps(data).encode())

    def test_duplicate_addresses_are_rejected(self):
        one = endpoint("uc::dup", "executable_inspection")
        with self.assertRaises(ConnectedMonolithContractError):
            ConnectedMonolithCatalog.from_execution_fabric_bytes(raw_fabric([one, copy.deepcopy(one)]))

    def test_source_execution_true_outside_named_workflow_fails_closed(self):
        with self.assertRaises(ConnectedMonolithContractError):
            ConnectedMonolithCatalog.from_execution_fabric_bytes(
                raw_fabric([endpoint("uc::bad", "executable_inspection", source_execution=True)])
            )

    def test_zip_loader_verifies_package_hash_and_reads_without_extraction(self):
        raw = raw_fabric([endpoint("uc::inspection", "executable_inspection")])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "monolith.zip"
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("snapshot/EXECUTION_FABRIC.json", raw)
                workflow_raw = raw_workflow_registry()
                archive.writestr("snapshot/WORKFLOW_REGISTRY.json", workflow_raw)
            expected = sha256(path.read_bytes()).hexdigest()
            catalog = ConnectedMonolithCatalog.from_zip(path, expected_zip_sha256=f"sha256:{expected}")
            self.assertEqual(catalog.package_sha256, expected)
            self.assertEqual(catalog.execution_fabric_sha256, sha256(raw).hexdigest())
            self.assertEqual(catalog.workflow_registry_sha256, sha256(workflow_raw).hexdigest())

    def test_zip_hash_mismatch_is_rejected(self):
        raw = raw_fabric([endpoint("uc::inspection", "executable_inspection")])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "monolith.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("EXECUTION_FABRIC.json", raw)
                archive.writestr("WORKFLOW_REGISTRY.json", raw_workflow_registry())
            with self.assertRaises(ConnectedMonolithIntegrityError):
                ConnectedMonolithCatalog.from_zip(path, expected_zip_sha256="0" * 64)

    def test_zip_loader_cross_checks_named_workflow_membership(self):
        raw = raw_fabric(
            [
                endpoint(
                    "axm-universal-creation::creation.universal",
                    "callable_through_named_workflow",
                    source_execution=True,
                    workflow="ghost-studio.blackline-3d.v0.4",
                    stage="brief-to-visual-recipe",
                )
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "monolith.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("EXECUTION_FABRIC.json", raw)
                archive.writestr(
                    "WORKFLOW_REGISTRY.json",
                    raw_workflow_registry("some-other-module::other.capability"),
                )
            with self.assertRaises(ConnectedMonolithContractError):
                ConnectedMonolithCatalog.from_zip(path)

    def test_duplicate_json_members_fail_closed(self):
        raw = b'{"schema":"axm.monolith.execution-fabric/v0.1","schema":"x"}'
        with self.assertRaises(ConnectedMonolithContractError):
            ConnectedMonolithCatalog.from_execution_fabric_bytes(raw)


if __name__ == "__main__":
    unittest.main()
