from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .identity import IdentityError, parse_immutable_ref
from .store import FilesystemObjectStore, ObjectStoreError


class ReturnPacketOutputIdentityError(ObjectStoreError):
    """Base error for exact return-packet output/evidence identity resolution."""


class ReturnPacketRelationKindError(ReturnPacketOutputIdentityError):
    """A packet relationship does not use the required immutable object kind."""


class ModifiedArtifactIdentityUnresolvedError(ReturnPacketOutputIdentityError):
    """The current packet contract cannot ground modified-artifact identity safely."""


class _FrozenList(tuple[Any, ...]):
    """Tuple-backed immutable JSON array accepted by the existing Stage 2 boundary.

    The object is *not* a ``list`` or a ``list`` subclass, so callers cannot bypass
    immutability with ``list.__setitem__`` or another builtin list mutator.  The
    ``__class__`` compatibility view is intentionally narrow: Stage 2 already uses
    ``isinstance(value, list)`` to recognize its JSON-native array language.  Reporting
    that compatibility view lets the existing canonicalizer and schema validator read
    this immutable operational snapshot without changing or broadening Stage 2 itself.

    Storage is entirely tuple-backed and instances have no writable attributes.
    """

    __slots__ = ()

    def __new__(cls, values: Any = ()) -> _FrozenList:
        return tuple.__new__(cls, values)

    @property
    def __class__(self) -> type[list[Any]]:
        return list

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (list, tuple)):
            return False
        return len(self) == len(other) and all(
            left == right for left, right in zip(tuple.__iter__(self), other)
        )

    __hash__ = None


class _FrozenDict(tuple[tuple[str, Any], ...]):
    """Tuple-backed immutable JSON object accepted by the existing Stage 2 boundary.

    This is deliberately not a ``dict`` subclass.  Its content is an immutable tuple of
    key/value pairs whose values are recursively frozen.  Builtin base-class mutators
    such as ``dict.__setitem__`` therefore reject the object at the Python type boundary.

    As with ``_FrozenList``, ``__class__`` only preserves compatibility with Stage 2's
    existing ``isinstance(value, dict)`` JSON-object checks; no identity/canonicalization
    rule is changed and no new general Mapping/Sequence language is introduced.
    """

    __slots__ = ()

    def __new__(cls, mapping: Mapping[str, Any]) -> _FrozenDict:
        return tuple.__new__(cls, tuple(mapping.items()))

    @property
    def __class__(self) -> type[dict[str, Any]]:
        return dict

    def __iter__(self):
        return (key for key, _value in tuple.__iter__(self))

    def __getitem__(self, key: str) -> Any:
        for candidate, value in tuple.__iter__(self):
            if candidate == key:
                return value
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        return any(candidate == key for candidate, _value in tuple.__iter__(self))

    def keys(self) -> tuple[str, ...]:
        return tuple(key for key, _value in tuple.__iter__(self))

    def items(self) -> tuple[tuple[str, Any], ...]:
        return tuple(tuple.__iter__(self))

    def values(self) -> tuple[Any, ...]:
        return tuple(value for _key, value in tuple.__iter__(self))

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, dict):
            return False
        try:
            return len(self) == len(other) and all(
                key in other and value == other[key] for key, value in self.items()
            )
        except (KeyError, TypeError):
            return False

    __hash__ = None


def _freeze_json(value: Any) -> Any:
    """Return a detached recursively immutable tuple-backed operational snapshot.

    Exact identity is first proved against durable bytes by
    ``FilesystemObjectStore.load()``.  This second boundary prevents the authoritative
    operational value from drifting away from that exact reference after verification.

    Objects and arrays are recursively copied into tuple-backed non-builtin containers.
    They remain readable by the *existing* Stage 2 canonicalizer/schema validator through
    their bounded ``__class__`` compatibility view, but builtin ``dict`` / ``list`` base
    mutators cannot operate on them because their real runtime type is tuple-backed.
    Scalars are already immutable.
    """

    if isinstance(value, dict):
        return _FrozenDict({key: _freeze_json(item) for key, item in value.items()})
    if isinstance(value, list):
        return _FrozenList(_freeze_json(item) for item in value)
    return value


@dataclass(frozen=True)
class ExactPacketRelation:
    """One exact immutable object selected directly by a packet relationship."""

    reference: str
    value: Mapping[str, Any]


@dataclass(frozen=True)
class ResolvedReturnPacketOutputIdentity:
    """Identity-only result for packet-created artifacts and packet evidence records.

    This result proves only exact-instance selection through immutable refs and exact
    object-store loading. Returned JSON values are recursively immutable tuple-backed
    snapshots so their content cannot drift away from the paired exact refs through
    ordinary mutation or builtin ``dict`` / ``list`` base-class mutators. It does not
    prove artifact provenance closure, evidence subject/quality closure, lane
    compatibility, packet acceptance, claim closure, successor-state publication,
    integration, epochs, or replay.
    """

    packet_ref: str
    packet: Mapping[str, Any]
    created_artifacts: tuple[ExactPacketRelation, ...]
    evidence_records: tuple[ExactPacketRelation, ...]


def _load_exact_relation(
    store: FilesystemObjectStore,
    reference: str,
    *,
    expected_kind: str,
    field: str,
) -> ExactPacketRelation:
    """Parse and exact-load one authoritative packet relationship.

    The shared Stage 2 parser remains the sole reference-language authority. No
    logical-id lookup, newest object, storage order, array order, current/HEAD state,
    actor identity, or hidden execution history participates.
    """

    try:
        parsed = parse_immutable_ref(reference)
    except IdentityError as exc:
        # parse_immutable_ref intentionally surfaces both malformed reference errors
        # and canonicalization errors (for example non-NFC decoded components). They
        # are one fail-closed Stage 2 reference-language boundary here.
        raise ReturnPacketOutputIdentityError(
            f"return-packet output identity failed at {field}: {exc}"
        ) from exc

    if parsed.kind != expected_kind:
        raise ReturnPacketRelationKindError(
            f"return-packet output identity failed at {field}: expected kind "
            f"{expected_kind!r}, got {parsed.kind!r}"
        )

    value = store.load(reference, f"{expected_kind}.schema.json")
    logical_id = value.get("id")
    if logical_id != parsed.logical_id:
        # The current filesystem store already makes this impossible after exact
        # identity verification. Keep the invariant explicit for alternate future
        # store implementations rather than trusting call-path history.
        raise ReturnPacketOutputIdentityError(
            f"verified {expected_kind!r} at {field} exposes logical id "
            f"{logical_id!r}, not reference id {parsed.logical_id!r}"
        )
    return ExactPacketRelation(reference=reference, value=_freeze_json(value))


def resolve_return_packet_output_identity(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedReturnPacketOutputIdentity:
    """Ground the smallest safe exact-instance precondition before compatibility.

    Chronology is intentionally asymmetric:

    * ``artifacts_created`` names result objects created by the work, so each result
      can bind directly to one exact immutable ``artifact`` ref.
    * ``evidence_refs`` names evidence records available to the handoff, so each can
      bind directly to one exact immutable ``evidence-record`` ref.
    * ``artifacts_modified`` currently carries only one opaque string per entry. A
      truthful modification relationship needs both the exact prior artifact instance
      observed by the work and the exact produced result instance. The present packet
      and artifact contracts cannot express that pair without guessing. Any non-empty
      modified-artifact list therefore fails closed at this identity precondition.

    The function is read-only. It deliberately does not evaluate lane output types,
    required evidence states, artifact provenance closure, evidence subject binding,
    stale/current compatibility, or any integration decision.
    """

    try:
        parsed_packet = parse_immutable_ref(packet_ref)
    except IdentityError as exc:
        raise ReturnPacketOutputIdentityError(
            f"invalid exact return-packet reference: {exc}"
        ) from exc
    if parsed_packet.kind != "return-packet":
        raise ReturnPacketRelationKindError(
            f"packet_ref must have kind 'return-packet', got {parsed_packet.kind!r}"
        )

    packet = store.load(packet_ref, "return-packet.schema.json")

    modified = packet.get("artifacts_modified", ())
    if modified:
        raise ModifiedArtifactIdentityUnresolvedError(
            "return-packet artifacts_modified cannot yet be used operationally: "
            "the current contract records one opaque value but modification identity "
            "requires both the exact prior artifact observed and the exact produced "
            "artifact result; artifact provenance.base_state_revision and "
            "supersedes_ref also remain insufficient for exact stale-target/provenance "
            "claims"
        )

    created_artifacts = tuple(
        _load_exact_relation(
            store,
            reference,
            expected_kind="artifact",
            field=f"$.artifacts_created[{index}]",
        )
        for index, reference in enumerate(packet.get("artifacts_created", ()))
    )
    evidence_records = tuple(
        _load_exact_relation(
            store,
            reference,
            expected_kind="evidence-record",
            field=f"$.evidence_refs[{index}]",
        )
        for index, reference in enumerate(packet.get("evidence_refs", ()))
    )

    return ResolvedReturnPacketOutputIdentity(
        packet_ref=packet_ref,
        packet=_freeze_json(packet),
        created_artifacts=created_artifacts,
        evidence_records=evidence_records,
    )
