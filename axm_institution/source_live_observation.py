from __future__ import annotations

import hashlib
import stat
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .identity import canonical_bytes, parse_json_strict
from .source_runtime_capability import (
    BUNDLED_SCHEMA_DIR,
    ExactSourceRuntimeCapabilityFact,
    SourceRuntimeCapabilityContextError,
    _project_exact_source_runtime_capability_in_schema_context,
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


def _capture_bundled_schema_context() -> tuple[dict[str, bytes], tuple[tuple[Any, ...], ...]]:
    """Capture one bounded bundled-schema interpretation plus mutation-sensitive token."""

    try:
        paths = sorted(BUNDLED_SCHEMA_DIR.glob("*.schema.json"), key=lambda path: path.name)
    except OSError as exc:
        raise SourceLiveObservationContextError(
            f"cannot enumerate bundled schema context: {exc}"
        ) from exc
    if not paths:
        raise SourceLiveObservationContextError("bundled schema context is empty")

    snapshot: dict[str, bytes] = {}
    token: list[tuple[Any, ...]] = []
    for path in paths:
        try:
            before = path.stat()
            if not stat.S_ISREG(before.st_mode):
                raise SourceLiveObservationContextError(
                    f"bundled schema path is not a regular file: {path.name!r}"
                )
            raw = path.read_bytes()
            after = path.stat()
        except SourceLiveObservationContextError:
            raise
        except OSError as exc:
            raise SourceLiveObservationContextError(
                f"cannot capture bundled schema {path.name!r}: {exc}"
            ) from exc

        before_signature = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        after_signature = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        )
        if before_signature != after_signature or len(raw) != after.st_size:
            raise SourceLiveObservationContextError(
                f"bundled schema changed while being captured: {path.name!r}"
            )

        snapshot[path.name] = raw
        token.append(
            (
                path.name,
                *after_signature,
                hashlib.sha256(raw).hexdigest(),
            )
        )

    try:
        names_after = sorted(path.name for path in BUNDLED_SCHEMA_DIR.glob("*.schema.json"))
    except OSError as exc:
        raise SourceLiveObservationContextError(
            f"cannot re-enumerate bundled schema context: {exc}"
        ) from exc
    if names_after != list(snapshot):
        raise SourceLiveObservationContextError(
            "bundled schema membership changed while the observation context was captured"
        )

    return snapshot, tuple(token)


def _assert_bundled_schema_context_unchanged(expected_token: tuple[tuple[Any, ...], ...]) -> None:
    _, observed_token = _capture_bundled_schema_context()
    if observed_token != expected_token:
        raise SourceLiveObservationContextError(
            "bundled schema context changed during Decision 023 observation"
        )


def _write_schema_snapshot(snapshot: Mapping[str, bytes], target_dir: Path) -> None:
    try:
        for name, raw in snapshot.items():
            (target_dir / name).write_bytes(raw)
    except OSError as exc:
        raise SourceLiveObservationContextError(
            f"cannot materialize function-owned bundled schema snapshot: {exc}"
        ) from exc


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

    The bundled schema set is copied into a function-owned temporary interpretation
    context. Both capability classification and exact target validation use that same
    copy. Ambient bundled-schema mutation during the invocation fails closed before a
    normal observation fact is emitted. During the exact target load, the accepted exact
    store instance is temporarily given an invocation-local data-descriptor guard. Its
    `schema_dir` getter verifies that the instance dictionary still names the function-
    owned snapshot, so both ordinary assignment and direct `__dict__` rebinding fail
    closed when validation tries to consume the interpretation context. Its `load_bytes`
    data descriptor prevents a caller-owned instance shadow from becoming proof of either
    presence or absence: a caller-raised `ObjectNotFoundError` is not absence evidence, so
    the base exact-store read still independently decides. Other caller-raised store-layer
    failures retain the existing indeterminate store-error classification. Its
    `_verify_existing` data descriptor applies the same rule one layer deeper: any caller-
    owned instance verifier shadow may run first, but neither a successful return nor a
    caller-raised `ObjectNotFoundError` is sufficient evidence; the base exact-store
    verifier must independently read and reproduce the exact immutable identity before
    positive or negative context-local truth is emitted. Its `_object_path` data
    descriptor applies that same bounded rule to object location: a caller-owned exact-
    instance path shadow may run, but neither its return value nor any store-layer error it
    raises can establish presence or absence. The invocation-entry `objects_dir` value is
    also preserved as the only location state the subsequent base path may consume; any
    caller-side drift is failed closed and restored before returning control. Unexpected
    non-store exceptions still fail closed. The temporary copy and guards are not retained
    and therefore do not create historical snapshot, durable store-root identity,
    hostile-process isolation, or re-execution standing.
    """

    if type(store) is not FilesystemObjectStore:
        raise SourceLiveObservationContextError(
            "Decision 023 requires the exact FilesystemObjectStore implementation; "
            "subclass dispatch is outside this bounded observation contract"
        )
    if store.schema_dir is not None:
        raise SourceLiveObservationContextError(
            "Decision 023 rejects caller-supplied/custom schema_dir before target-object I/O"
        )

    bundled_snapshot, bundled_token = _capture_bundled_schema_context()

    with tempfile.TemporaryDirectory(prefix="axm-decision023-schema-") as tmp:
        snapshot_dir = Path(tmp)
        _write_schema_snapshot(bundled_snapshot, snapshot_dir)

        try:
            capability = _project_exact_source_runtime_capability_in_schema_context(
                containing_object_ref=containing_object_ref,
                containing_value=containing_value,
                declaration_key=declaration_key,
                schema_dir=snapshot_dir,
                context_label="Decision 023 invocation",
            )
        except SourceRuntimeCapabilityContextError as exc:
            raise SourceLiveObservationContextError(
                f"cannot establish Decision 023 bundled interpretation context: {exc}"
            ) from exc

        _assert_bundled_schema_context_unchanged(bundled_token)

        if capability.runtime_capability == "unsupported_kind":
            return _fact(
                capability,
                outcome="not_attempted_unsupported_kind",
                availability="not_observed",
                retrieval="not_attempted",
                integrity="not_evaluated",
            )

        invocation_objects_dir = store.objects_dir

        class _InvocationSchemaGuard(FilesystemObjectStore):
            @property
            def schema_dir(self) -> Path:
                if self.__dict__.get("schema_dir") != snapshot_dir:
                    raise SourceLiveObservationContextError(
                        "Decision 023 store interpretation context changed during exact target load"
                    )
                return snapshot_dir

            @schema_dir.setter
            def schema_dir(self, value: Path | None) -> None:
                if value != snapshot_dir:
                    raise SourceLiveObservationContextError(
                        "Decision 023 store interpretation context changed during exact target load"
                    )
                self.__dict__["schema_dir"] = snapshot_dir

            @property
            def load_bytes(self):
                caller_dispatch = self.__dict__.get("load_bytes")

                def verified_load(reference: str, schema_name: str | None = None) -> bytes:
                    if caller_dispatch is not None:
                        try:
                            caller_dispatch(reference, schema_name)
                        except ObjectNotFoundError:
                            # A caller-owned not-found classification is not evidence that
                            # the supplied store lacks the object. The base read decides.
                            pass
                    return FilesystemObjectStore.load_bytes(self, reference, schema_name)

                return verified_load

            @property
            def _verify_existing(self):
                caller_dispatch = self.__dict__.get("_verify_existing")

                def verified_existing(reference: str, schema_name: str):
                    if caller_dispatch is not None:
                        try:
                            caller_dispatch(reference, schema_name)
                        except ObjectNotFoundError:
                            # Caller-owned verifier absence is not evidence that the exact
                            # object is absent from this supplied store. The base verifier
                            # independently grounds presence/absence/identity below.
                            pass
                    return FilesystemObjectStore._verify_existing(self, reference, schema_name)

                return verified_existing

            @property
            def _object_path(self):
                caller_dispatch = self.__dict__.get("_object_path")

                def verified_object_path(reference: str) -> Path:
                    if caller_dispatch is not None:
                        try:
                            caller_dispatch(reference)
                        except ObjectStoreError:
                            # Caller-owned path dispatch is exercised for continuity with
                            # ADV-058-G/H, but its return/error classification is not
                            # evidence about the supplied store. The base path decides.
                            pass
                    if self.objects_dir != invocation_objects_dir:
                        raise SourceLiveObservationContextError(
                            "Decision 023 store location context changed during exact target load"
                        )
                    return FilesystemObjectStore._object_path(self, reference)

                return verified_object_path

        load_error: ObjectStoreError | None = None
        original_schema_dir = store.schema_dir
        original_objects_dir = store.objects_dir
        original_store_class = store.__class__
        schema_override_drifted = False
        try:
            store.schema_dir = snapshot_dir
            store.__class__ = _InvocationSchemaGuard
            try:
                store.load_bytes(capability.target_object_ref)
            except ObjectStoreError as exc:
                load_error = exc
            finally:
                schema_override_drifted = store.schema_dir != snapshot_dir
        finally:
            store.__class__ = original_store_class
            store.schema_dir = original_schema_dir
            store.objects_dir = original_objects_dir

        _assert_bundled_schema_context_unchanged(bundled_token)
        if schema_override_drifted:
            raise SourceLiveObservationContextError(
                "Decision 023 store interpretation context changed during exact target load"
            )

    if isinstance(load_error, ObjectNotFoundError):
        return _fact(
            capability,
            outcome="not_found_in_live_context",
            availability="not_found_in_live_context",
            retrieval="not_obtained",
            integrity="not_evaluated",
        )
    if isinstance(load_error, ObjectCorruptionError):
        return _fact(
            capability,
            outcome="corrupt_material_in_live_context",
            availability="indeterminate_in_live_context",
            retrieval="unverified_bytes_obtained",
            integrity="failed_exact_identity",
        )
    if load_error is not None:
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
