from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable
import zipfile


EXECUTION_FABRIC_SCHEMA = "axm.monolith.execution-fabric/v0.1"
KNOWN_ADAPTER_STATUSES = frozenset(
    {
        "blocked_missing_callable_binding",
        "blocked_missing_native_contract",
        "callable_through_named_workflow",
        "executable_inspection",
        "executable_test_evidence",
        "launchable_local_surface",
    }
)

_STANDING_BY_STATUS = {
    "blocked_missing_callable_binding": "blocked_missing_callable_binding",
    "blocked_missing_native_contract": "blocked_missing_native_contract",
    "callable_through_named_workflow": "source_callable_named_workflow",
    "executable_inspection": "inspectable_not_source_execution",
    "executable_test_evidence": "test_entrypoint_evidence_not_tests_passed",
    "launchable_local_surface": "launchable_not_runtime_verified",
}


class ConnectedMonolithError(ValueError):
    """Base error for the bounded connected-monolith discovery adapter."""


class ConnectedMonolithContractError(ConnectedMonolithError):
    """Raised when the execution-fabric document is ambiguous or unsupported."""


class ConnectedMonolithIntegrityError(ConnectedMonolithError):
    """Raised when an expected package digest does not match the supplied ZIP."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConnectedMonolithContractError(f"duplicate JSON member: {key!r}")
        result[key] = value
    return result


def _parse_json_strict(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ConnectedMonolithContractError("execution fabric is not valid UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=_strict_object)
    except ConnectedMonolithContractError:
        raise
    except json.JSONDecodeError as exc:
        raise ConnectedMonolithContractError("execution fabric is not valid JSON") from exc


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConnectedMonolithContractError(f"{label} must be a non-empty string")
    return value


def _string_tuple(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ConnectedMonolithContractError(f"{label} must be an array")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(_require_string(item, f"{label}[{index}]"))
    return tuple(result)


def _normalize_expected_sha256(value: str) -> str:
    digest = value.removeprefix("sha256:")
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ConnectedMonolithIntegrityError(
            "expected ZIP SHA-256 must be lowercase 64-hex, optionally prefixed with 'sha256:'"
        )
    return digest


@dataclass(frozen=True, slots=True)
class ConnectedMonolithCapabilityFact:
    address: str
    capability: str
    module: str
    repository: str
    commit: str
    accepts: tuple[str, ...]
    provides: tuple[str, ...]
    adapter_status: str
    evidence_status: str
    institution_standing: str
    source_capability_execution: bool
    named_workflow: str | None
    workflow_stage: str | None
    institution_action_authority: str = "discovery_only_no_action_authority"

    @property
    def source_callable(self) -> bool:
        return self.institution_standing == "source_callable_named_workflow"

    def as_dict(self) -> dict[str, Any]:
        return {
            "address": self.address,
            "capability": self.capability,
            "module": self.module,
            "repository": self.repository,
            "commit": self.commit,
            "accepts": list(self.accepts),
            "provides": list(self.provides),
            "adapter_status": self.adapter_status,
            "evidence_status": self.evidence_status,
            "institution_standing": self.institution_standing,
            "source_capability_execution": self.source_capability_execution,
            "named_workflow": self.named_workflow,
            "workflow_stage": self.workflow_stage,
            "institution_action_authority": self.institution_action_authority,
        }


def _validate_workflow_registry(
    raw: bytes,
    endpoints: tuple[ConnectedMonolithCapabilityFact, ...],
) -> None:
    data = _parse_json_strict(raw)
    if not isinstance(data, dict):
        raise ConnectedMonolithContractError("workflow registry root must be an object")
    if data.get("schema") != "axm.monolith.workflow-registry/v0.1":
        raise ConnectedMonolithContractError(
            f"unsupported workflow registry schema: {data.get('schema')!r}"
        )
    workflows = data.get("workflows")
    if not isinstance(workflows, list):
        raise ConnectedMonolithContractError("workflow registry workflows must be an array")
    if data.get("workflow_count") != len(workflows):
        raise ConnectedMonolithContractError("workflow_count does not match workflows array length")

    by_id: dict[str, dict[str, Any]] = {}
    for index, workflow in enumerate(workflows):
        if not isinstance(workflow, dict):
            raise ConnectedMonolithContractError(f"workflows[{index}] must be an object")
        workflow_id = _require_string(workflow.get("id"), f"workflows[{index}].id")
        if workflow_id in by_id:
            raise ConnectedMonolithContractError(f"duplicate workflow id: {workflow_id}")
        by_id[workflow_id] = workflow

    for fact in endpoints:
        if not fact.source_callable:
            continue
        assert fact.named_workflow is not None
        workflow = by_id.get(fact.named_workflow)
        if workflow is None:
            raise ConnectedMonolithContractError(
                f"{fact.address}: named workflow {fact.named_workflow!r} is absent from WORKFLOW_REGISTRY.json"
            )
        if workflow.get("status") != "callable":
            raise ConnectedMonolithContractError(
                f"{fact.address}: named workflow {fact.named_workflow!r} is not marked callable"
            )
        stages = workflow.get("stages")
        if not isinstance(stages, list):
            raise ConnectedMonolithContractError(
                f"{fact.address}: workflow {fact.named_workflow!r} stages must be an array"
            )
        stage_capabilities = {
            stage.get("capability")
            for stage in stages
            if isinstance(stage, dict) and isinstance(stage.get("capability"), str)
        }
        if fact.address not in stage_capabilities:
            raise ConnectedMonolithContractError(
                f"{fact.address}: named workflow {fact.named_workflow!r} does not contain this capability address"
            )


@dataclass(frozen=True, slots=True)
class ConnectedMonolithCatalog:
    execution_fabric_schema: str
    execution_fabric_sha256: str
    workflow_registry_sha256: str | None
    package_sha256: str | None
    endpoint_count: int
    adapter_status_counts: tuple[tuple[str, int], ...]
    source_authority_flags: tuple[tuple[str, bool], ...]
    truth_boundary: str
    endpoints: tuple[ConnectedMonolithCapabilityFact, ...]

    @classmethod
    def from_execution_fabric_bytes(
        cls,
        raw: bytes,
        *,
        package_sha256: str | None = None,
    ) -> "ConnectedMonolithCatalog":
        data = _parse_json_strict(raw)
        if not isinstance(data, dict):
            raise ConnectedMonolithContractError("execution fabric root must be an object")
        if data.get("schema") != EXECUTION_FABRIC_SCHEMA:
            raise ConnectedMonolithContractError(
                f"unsupported execution fabric schema: {data.get('schema')!r}"
            )

        truth_boundary = _require_string(data.get("truth_boundary"), "truth_boundary")
        authority = data.get("authority")
        if not isinstance(authority, dict):
            raise ConnectedMonolithContractError("authority must be an object")
        authority_flags: list[tuple[str, bool]] = []
        for key, value in sorted(authority.items()):
            if not isinstance(key, str) or not isinstance(value, bool):
                raise ConnectedMonolithContractError("authority flags must be boolean values")
            authority_flags.append((key, value))

        endpoints_raw = data.get("endpoints")
        if not isinstance(endpoints_raw, list):
            raise ConnectedMonolithContractError("endpoints must be an array")

        seen_addresses: set[str] = set()
        facts: list[ConnectedMonolithCapabilityFact] = []
        computed_status_counts: dict[str, int] = {}
        for index, endpoint in enumerate(endpoints_raw):
            if not isinstance(endpoint, dict):
                raise ConnectedMonolithContractError(f"endpoints[{index}] must be an object")
            address = _require_string(endpoint.get("address"), f"endpoints[{index}].address")
            if address in seen_addresses:
                raise ConnectedMonolithContractError(f"duplicate endpoint address: {address}")
            seen_addresses.add(address)

            adapter = endpoint.get("adapter")
            if not isinstance(adapter, dict):
                raise ConnectedMonolithContractError(f"{address}: adapter must be an object")
            status = _require_string(adapter.get("status"), f"{address}.adapter.status")
            if status not in KNOWN_ADAPTER_STATUSES:
                raise ConnectedMonolithContractError(
                    f"{address}: unsupported adapter status {status!r}; refusing to infer semantics"
                )
            source_execution = adapter.get("source_capability_execution")
            if not isinstance(source_execution, bool):
                raise ConnectedMonolithContractError(
                    f"{address}: adapter.source_capability_execution must be boolean"
                )

            workflow: str | None = None
            stage: str | None = None
            if status == "callable_through_named_workflow":
                if not source_execution:
                    raise ConnectedMonolithContractError(
                        f"{address}: named-workflow callable status requires source_capability_execution=true"
                    )
                workflow = _require_string(adapter.get("workflow"), f"{address}.adapter.workflow")
                stage = _require_string(adapter.get("stage"), f"{address}.adapter.stage")
            elif source_execution:
                raise ConnectedMonolithContractError(
                    f"{address}: source execution is only grounded for the known named-workflow status"
                )

            computed_status_counts[status] = computed_status_counts.get(status, 0) + 1
            facts.append(
                ConnectedMonolithCapabilityFact(
                    address=address,
                    capability=_require_string(endpoint.get("capability"), f"{address}.capability"),
                    module=_require_string(endpoint.get("module"), f"{address}.module"),
                    repository=_require_string(endpoint.get("repository"), f"{address}.repository"),
                    commit=_require_string(endpoint.get("commit"), f"{address}.commit"),
                    accepts=_string_tuple(endpoint.get("accepts"), f"{address}.accepts"),
                    provides=_string_tuple(endpoint.get("provides"), f"{address}.provides"),
                    adapter_status=status,
                    evidence_status=_require_string(
                        endpoint.get("evidence_status"), f"{address}.evidence_status"
                    ),
                    institution_standing=_STANDING_BY_STATUS[status],
                    source_capability_execution=source_execution,
                    named_workflow=workflow,
                    workflow_stage=stage,
                )
            )

        summary = data.get("summary")
        if not isinstance(summary, dict):
            raise ConnectedMonolithContractError("summary must be an object")
        if summary.get("endpoint_count") != len(facts):
            raise ConnectedMonolithContractError(
                "summary.endpoint_count does not match the endpoint array length"
            )
        source_counts = summary.get("adapter_status_counts")
        if not isinstance(source_counts, dict):
            raise ConnectedMonolithContractError("summary.adapter_status_counts must be an object")
        normalized_source_counts: dict[str, int] = {}
        for key, value in source_counts.items():
            if not isinstance(key, str) or key not in KNOWN_ADAPTER_STATUSES:
                raise ConnectedMonolithContractError(
                    f"summary contains unsupported adapter status {key!r}"
                )
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ConnectedMonolithContractError(
                    f"summary adapter count for {key!r} must be a non-negative integer"
                )
            normalized_source_counts[key] = value
        if normalized_source_counts != computed_status_counts:
            raise ConnectedMonolithContractError(
                "summary.adapter_status_counts does not match endpoint adapter statuses"
            )

        package_digest = None
        if package_sha256 is not None:
            package_digest = _normalize_expected_sha256(package_sha256)

        return cls(
            execution_fabric_schema=EXECUTION_FABRIC_SCHEMA,
            execution_fabric_sha256=sha256(raw).hexdigest(),
            workflow_registry_sha256=None,
            package_sha256=package_digest,
            endpoint_count=len(facts),
            adapter_status_counts=tuple(sorted(computed_status_counts.items())),
            source_authority_flags=tuple(authority_flags),
            truth_boundary=truth_boundary,
            endpoints=tuple(sorted(facts, key=lambda fact: fact.address)),
        )

    @classmethod
    def from_zip(
        cls,
        zip_path: str | Path,
        *,
        expected_zip_sha256: str | None = None,
    ) -> "ConnectedMonolithCatalog":
        path = Path(zip_path)
        package_bytes_digest = sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                package_bytes_digest.update(chunk)
        actual_package_sha = package_bytes_digest.hexdigest()
        if expected_zip_sha256 is not None:
            expected = _normalize_expected_sha256(expected_zip_sha256)
            if actual_package_sha != expected:
                raise ConnectedMonolithIntegrityError(
                    f"ZIP SHA-256 mismatch: expected {expected}, got {actual_package_sha}"
                )

        try:
            with zipfile.ZipFile(path) as archive:
                execution_members = [
                    name
                    for name in archive.namelist()
                    if name == "EXECUTION_FABRIC.json" or name.endswith("/EXECUTION_FABRIC.json")
                ]
                workflow_members = [
                    name
                    for name in archive.namelist()
                    if name == "WORKFLOW_REGISTRY.json" or name.endswith("/WORKFLOW_REGISTRY.json")
                ]
                if len(execution_members) != 1:
                    raise ConnectedMonolithContractError(
                        f"expected exactly one EXECUTION_FABRIC.json in ZIP, found {len(execution_members)}"
                    )
                if len(workflow_members) != 1:
                    raise ConnectedMonolithContractError(
                        f"expected exactly one WORKFLOW_REGISTRY.json in ZIP, found {len(workflow_members)}"
                    )
                raw = archive.read(execution_members[0])
                workflow_raw = archive.read(workflow_members[0])
        except zipfile.BadZipFile as exc:
            raise ConnectedMonolithContractError("connected monolith input is not a valid ZIP") from exc

        catalog = cls.from_execution_fabric_bytes(raw, package_sha256=actual_package_sha)
        _validate_workflow_registry(workflow_raw, catalog.endpoints)
        return cls(
            execution_fabric_schema=catalog.execution_fabric_schema,
            execution_fabric_sha256=catalog.execution_fabric_sha256,
            workflow_registry_sha256=sha256(workflow_raw).hexdigest(),
            package_sha256=catalog.package_sha256,
            endpoint_count=catalog.endpoint_count,
            adapter_status_counts=catalog.adapter_status_counts,
            source_authority_flags=catalog.source_authority_flags,
            truth_boundary=catalog.truth_boundary,
            endpoints=catalog.endpoints,
        )

    def query(
        self,
        *,
        address: str | None = None,
        capability: str | None = None,
        module: str | None = None,
        accepts_all: Iterable[str] = (),
        provides_all: Iterable[str] = (),
        adapter_statuses: Iterable[str] = (),
    ) -> tuple[ConnectedMonolithCapabilityFact, ...]:
        accepts_required = frozenset(accepts_all)
        provides_required = frozenset(provides_all)
        allowed_statuses = frozenset(adapter_statuses)
        unknown = allowed_statuses - KNOWN_ADAPTER_STATUSES
        if unknown:
            raise ConnectedMonolithContractError(
                f"query contains unsupported adapter status(es): {sorted(unknown)!r}"
            )

        results: list[ConnectedMonolithCapabilityFact] = []
        for fact in self.endpoints:
            if address is not None and fact.address != address:
                continue
            if capability is not None and fact.capability != capability:
                continue
            if module is not None and fact.module != module:
                continue
            if not accepts_required.issubset(fact.accepts):
                continue
            if not provides_required.issubset(fact.provides):
                continue
            if allowed_statuses and fact.adapter_status not in allowed_statuses:
                continue
            results.append(fact)
        return tuple(results)

    def as_summary_dict(self) -> dict[str, Any]:
        return {
            "execution_fabric_schema": self.execution_fabric_schema,
            "execution_fabric_sha256": self.execution_fabric_sha256,
            "workflow_registry_sha256": self.workflow_registry_sha256,
            "package_sha256": self.package_sha256,
            "endpoint_count": self.endpoint_count,
            "adapter_status_counts": dict(self.adapter_status_counts),
            "source_authority_flags": dict(self.source_authority_flags),
            "truth_boundary": self.truth_boundary,
            "institution_boundary": (
                "catalog discovery grants no action, merge, canon, install, network, or source-mutation authority"
            ),
        }
