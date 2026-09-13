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


class _FrozenDict(dict[str, Any]):
    """Recursively immutable JSON object that remains identity-canonicalizable.

    The Stage 2 canonicalizer intentionally accepts only JSON-native ``dict``/``list``
    containers. Subclassing those containers preserves that exact identity language while
    rejecting mutation after exact verification. The class is private because it is an
    operational return-value guard, not a new kernel contract type.
    """

    @staticmethod
    def _immutable(*_args: Any, **_kwargs: Any) -> None:
        raise TypeError("resolved exact JSON value is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable
    __ior__ = _immutable


class _FrozenList(list[Any]):
    """Recursively immutable JSON array compatible with Stage 2 canonicalization."""

    @staticmethod
    def _immutable(*_args: Any, **_kwargs: Any) -> None:
        raise TypeError("resolved exact JSON value is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    append = _immutable
    clear = _immutable
    extend = _immutable
    insert = _immutable
    pop = _immutable
    remove = _immutable
    reverse = _immutable
    sort = _immutable
    __iadd__ = _immutable
    __imul__ = _immutable


def _freeze_json(value: Any) -> Any:
    """Return a detached recursively immutable JSON-native snapshot.

    Exact identity is proved against durable bytes by ``FilesystemObjectStore.load()``.
    This second boundary prevents the returned operational value from drifting away from
    the immutable reference after that proof. Scalars are already immutable; objects and
    arrays are copied recursively into mutation-rejecting ``dict``/``list`` subclasses so
    existing canonical identity functions can still reproduce the paired exact ref.
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
    object-store loading. Returned JSON values are recursively immutable snapshots so
    their content cannot drift away from the paired exact refs after resolution. It does
    not prove artifact provenance closure, evidence subject/quality closure, lane
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
