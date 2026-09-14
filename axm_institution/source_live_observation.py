from __future__ import annotations

from typing import Any, Mapping

from .identity import canonical_bytes, parse_json_strict
from .source_runtime_capability import (
    ExactSourceRuntimeCapabilityFact,
    project_exact_source_runtime_capability,
)
from .store import (
    FilesystemObjectStore,
    ObjectCorruptionError,
    ObjectNotFoundError,
    ObjectStoreError,
)


_OBSERVATION_METHOD = "filesystem_exact_load_v1"
_CONTEXT_STANDING = "live_mutable_store"
_REEXECUTION_STANDING = "not_established"
_OBSERVATION_OUTCOMES = frozenset(
    {
        "exact_observed",
        "not_found_in_live_context",
        "corrupt_material_in_live_context",
        "store_error_in_live_context",
        "not_attempted_unsupported_kind",
    }
)
_AVAILABILITY_OBSERVATIONS = frozenset(
    {
        "observed_in_live_context",
        "not_found_in_live_context",
        "indeterminate_in_live_context",
        "not_observed",
    }
)
_RETRIEVAL_OBSERVATIONS = frozenset(
    {
        "verified_bytes_obtained",
        "unverified_bytes_obtained",
        "not_obtained",
        "not_attempted",
    }
)
_INTEGRITY_OBSERVATIONS = frozenset(
    {
        "verified_exact_identity",
        "failed_exact_identity",
        "not_evaluated",
    }
)


class SourceLiveObservationError(RuntimeError):
    """Base error for Decision 023 exact live source observation facts."""


class SourceLiveObservationContextError(SourceLiveObservationError):
    """The requested live observation context is outside Decision 023."""


class ExactSourceLiveObservationFact(bytes):
    """Canonical-byte-backed named Decision 023 live observation fact.

    The authoritative representation is immutable canonical JSON bytes. The fact records
    only exact occurrence identity, Decision 022 runtime capability, fixed live-context
    standing, and one classified observation result. It deliberately contains no path,
    host, process, timestamp, actor, CI, branch, Git, trust, closure, or replay authority.
    """

    __slots__ = ()
    _fields = (
        "containing_object_ref",
        "declaration_key",
        "target_object_ref",
        "target_kind",
        "runtime_capability",
        "observation_method",
        "context_standing",
        "reexecution_standing",
        "observation_outcome",
        "availability_observation",
        "retrieval_observation",
        "integrity_observation",
    )

    def __new__(
        cls,
        *,
        capability: ExactSourceRuntimeCapabilityFact,
        observation_outcome: str,
        availability_observation: str,
        retrieval_observation: str,
        integrity_observation: str,
    ):
        if observation_outcome not in _OBSERVATION_OUTCOMES:
            raise ValueError(f"unsupported observation outcome: {observation_outcome!r}")
        if availability_observation not in _AVAILABILITY_OBSERVATIONS:
            raise ValueError(
                f"unsupported availability observation: {availability_observation!r}"
            )
        if retrieval_observation not in _RETRIEVAL_OBSERVATIONS:
            raise ValueError(f"unsupported retrieval observation: {retrieval_observation!r}")
        if integrity_observation not in _INTEGRITY_OBSERVATIONS:
            raise ValueError(f"unsupported integrity observation: {integrity_observation!r}")

        return bytes.__new__(
            cls,
            canonical_bytes(
                {
                    "containing_object_ref": capability.containing_object_ref,
                    "declaration_key": capability.declaration_key,
                    "target_object_ref": capability.target_object_ref,
                    "target_kind": capability.target_kind,
                    "runtime_capability": capability.runtime_capability,
                    "observation_method": _OBSERVATION_METHOD,
                    "context_standing": _CONTEXT_STANDING,
                    "reexecution_standing": _REEXECUTION_STANDING,
                    "observation_outcome": observation_outcome,
                    "availability_observation": availability_observation,
                    "retrieval_observation": retrieval_observation,
                    "integrity_observation": integrity_observation,
                }
            ),
        )

    def _plain(self) -> dict[str, Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, dict):
            raise TypeError("frozen Decision 023 observation fact did not decode as a mapping")
        return value

    def _asdict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self._fields}

    def __repr__(self) -> str:
        values = ", ".join(f"{field}={getattr(self, field)!r}" for field in self._fields)
        return f"{type(self).__name__}({values})"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return bytes.__eq__(self, other)

    __hash__ = bytes.__hash__

    def _string(self, field: str) -> str:
        value = self._plain()[field]
        if not isinstance(value, str):
            raise TypeError(f"Decision 023 {field} is not a string")
        return value

    @property
    def containing_object_ref(self) -> str:
        return self._string("containing_object_ref")

    @property
    def declaration_key(self) -> str:
        return self._string("declaration_key")

    @property
    def target_object_ref(self) -> str:
        return self._string("target_object_ref")

    @property
    def target_kind(self) -> str:
        return self._string("target_kind")

    @property
    def runtime_capability(self) -> str:
        return self._string("runtime_capability")

    @property
    def observation_method(self) -> str:
        return self._string("observation_method")

    @property
    def context_standing(self) -> str:
        return self._string("context_standing")

    @property
    def reexecution_standing(self) -> str:
        return self._string("reexecution_standing")

    @property
    def observation_outcome(self) -> str:
        return self._string("observation_outcome")

    @property
    def availability_observation(self) -> str:
        return self._string("availability_observation")

    @property
    def retrieval_observation(self) -> str:
        return self._string("retrieval_observation")

    @property
    def integrity_observation(self) -> str:
        return self._string("integrity_observation")


def _fact(
    capability: ExactSourceRuntimeCapabilityFact,
    *,
    outcome: str,
    availability: str,
    retrieval: str,
    integrity: str,
) -> ExactSourceLiveObservationFact:
    return ExactSourceLiveObservationFact(
        capability=capability,
        observation_outcome=outcome,
        availability_observation=availability,
        retrieval_observation=retrieval,
        integrity_observation=integrity,
    )


def observe_exact_source_live(
    *,
    containing_object_ref: str,
    containing_value: Mapping[str, Any],
    declaration_key: str,
    store: FilesystemObjectStore,
) -> ExactSourceLiveObservationFact:
    """Observe one exact Decision 020 source occurrence in a live mutable local store.

    Decision 023 deliberately records only the bounded result of this invocation. It does
    not identify the mutable store root, retain source bytes, establish literal
    re-execution, or grant provenance, trust, closure, acceptance, integration, epoch, or
    replay authority.
    """

    capability = project_exact_source_runtime_capability(
        containing_object_ref=containing_object_ref,
        containing_value=containing_value,
        declaration_key=declaration_key,
    )

    if not isinstance(store, FilesystemObjectStore):
        raise SourceLiveObservationContextError(
            "Decision 023 supports only FilesystemObjectStore live observation"
        )
    if store.schema_dir is not None:
        raise SourceLiveObservationContextError(
            "Decision 023 rejects caller-supplied/custom schema_dir before target-object I/O"
        )

    if capability.runtime_capability == "unsupported_kind":
        return _fact(
            capability,
            outcome="not_attempted_unsupported_kind",
            availability="not_observed",
            retrieval="not_attempted",
            integrity="not_evaluated",
        )

    try:
        store.load_bytes(capability.target_object_ref)
    except ObjectNotFoundError:
        return _fact(
            capability,
            outcome="not_found_in_live_context",
            availability="not_found_in_live_context",
            retrieval="not_obtained",
            integrity="not_evaluated",
        )
    except ObjectCorruptionError:
        return _fact(
            capability,
            outcome="corrupt_material_in_live_context",
            availability="indeterminate_in_live_context",
            retrieval="unverified_bytes_obtained",
            integrity="failed_exact_identity",
        )
    except ObjectStoreError:
        return _fact(
            capability,
            outcome="store_error_in_live_context",
            availability="indeterminate_in_live_context",
            retrieval="not_obtained",
            integrity="not_evaluated",
        )

    return _fact(
        capability,
        outcome="exact_observed",
        availability="observed_in_live_context",
        retrieval="verified_bytes_obtained",
        integrity="verified_exact_identity",
    )
