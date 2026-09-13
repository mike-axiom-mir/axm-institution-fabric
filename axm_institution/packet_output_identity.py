from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from .identity import IdentityError, canonical_bytes, parse_immutable_ref, parse_json_strict
from .store import FilesystemObjectStore, ObjectStoreError


class ReturnPacketOutputIdentityError(ObjectStoreError):
    """Base error for exact return-packet output/evidence identity resolution."""


class ReturnPacketRelationKindError(ReturnPacketOutputIdentityError):
    """A packet relationship does not use the required immutable object kind."""


class ModifiedArtifactIdentityUnresolvedError(ReturnPacketOutputIdentityError):
    """The current packet contract cannot ground modified-artifact identity safely."""


class _FrozenList(bytes):
    """Immutable JSON-array view whose ordinary stdlib JSON transport fails closed.

    The exact value is stored only as Stage 2 canonical UTF-8 bytes. The object is not a
    ``list`` or ``tuple`` subclass, so builtin sequence mutators cannot operate on it and
    Python's stdlib JSON encoder cannot silently reinterpret the storage container as an
    array. The narrow ``__class__`` compatibility view preserves the repository's existing
    Stage 2 ``isinstance(value, list)`` boundary for validation/canonical identity.

    Nested objects/arrays are reconstructed from the canonical bytes only as equally
    immutable views, so callers never receive a mutable alias of the authoritative value.
    """

    __slots__ = ()

    def __new__(cls, values: Any = ()) -> _FrozenList:
        return bytes.__new__(cls, canonical_bytes(values))

    @property
    def __class__(self) -> type[list[Any]]:
        return list

    def _plain(self) -> list[Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, list):
            raise TypeError("frozen JSON array payload did not decode as a list")
        return value

    def __iter__(self):
        return (_freeze_json(item) for item in self._plain())

    def __getitem__(self, index):
        return _freeze_json(self._plain()[index])

    def __len__(self) -> int:
        return len(self._plain())

    def __contains__(self, item: object) -> bool:
        return item in self._plain()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _FrozenList):
            other = other._plain()
        if not isinstance(other, (list, tuple)):
            return False
        return self._plain() == list(other)

    __hash__ = None


class _FrozenDict(bytes):
    """Immutable JSON-object view with explicit fail-closed ordinary JSON transport.

    The object's only physical payload is the already-validated Stage 2 canonical byte
    representation. It is not a ``dict``/``list``/``tuple`` subclass, so neither builtin
    base-class mutators nor stdlib JSON's container dispatch can silently reinterpret or
    rewrite the authoritative value. The existing Stage 2 JSON-object checks continue to
    work through the bounded ``__class__ -> dict`` compatibility view.

    Mapping reads parse the canonical bytes and recursively return immutable views. No
    mutable store-loaded mapping, nested list, or nested mapping is exposed to callers.
    """

    __slots__ = ()

    def __new__(cls, mapping: Mapping[str, Any]) -> _FrozenDict:
        return bytes.__new__(cls, canonical_bytes(mapping))

    @property
    def __class__(self) -> type[dict[str, Any]]:
        return dict

    def _plain(self) -> dict[str, Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, dict):
            raise TypeError("frozen JSON object payload did not decode as a mapping")
        return value

    def __iter__(self):
        return iter(self._plain())

    def __getitem__(self, key: str) -> Any:
        return _freeze_json(self._plain()[key])

    def __contains__(self, key: object) -> bool:
        return key in self._plain()

    def __len__(self) -> int:
        return len(self._plain())

    def keys(self) -> tuple[str, ...]:
        return tuple(self._plain().keys())

    def items(self) -> tuple[tuple[str, Any], ...]:
        return tuple((key, _freeze_json(value)) for key, value in self._plain().items())

    def values(self) -> tuple[Any, ...]:
        return tuple(_freeze_json(value) for value in self._plain().values())

    def get(self, key: str, default: Any = None) -> Any:
        plain = self._plain()
        if key not in plain:
            return default
        return _freeze_json(plain[key])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _FrozenDict):
            other = other._plain()
        if not isinstance(other, dict):
            return False
        return self._plain() == other

    __hash__ = None


def _freeze_json(value: Any) -> Any:
    """Return a detached recursively immutable canonical-byte operational snapshot.

    Exact identity is first proved against durable bytes by
    ``FilesystemObjectStore.load()``. This second boundary converts each exposed JSON
    object/array into a bytes-backed immutable view whose physical storage cannot be
    changed through ordinary mutation or builtin dict/list mutators.

    The view remains readable by the existing Stage 2 canonicalizer/schema validator via
    its narrow ``__class__`` compatibility surface. Ordinary Python stdlib JSON transport
    rejects the non-container runtime type instead of silently serializing a different
    semantic shape. A future explicit transport adapter may be added separately only when
    it can prove an exact round-trip.
    """

    if isinstance(value, dict):
        return _FrozenDict(value)
    if isinstance(value, list):
        return _FrozenList(value)
    return value


class ExactPacketRelation(NamedTuple):
    """One exact immutable object selected directly by a packet relationship.

    The tuple-backed relation keeps the exact ref/value pair physically non-reassignable
    through the demonstrated ``object.__setattr__`` path (ADV-040-A/B). The JSON value
    remains the existing canonical-byte-backed immutable operational view.
    """

    reference: str
    value: Mapping[str, Any]


class ResolvedReturnPacketOutputIdentity(NamedTuple):
    """Identity-only result for packet-created artifacts and packet evidence records.

    This result proves only exact-instance selection through immutable refs and exact
    object-store loading. Returned JSON values are recursively immutable canonical-byte
    snapshots so their content cannot drift away from the paired exact refs through
    ordinary mutation or builtin ``dict`` / ``list`` base-class mutators, and ordinary
    stdlib JSON transport fails closed instead of silently changing their semantic shape.
    The tuple-backed result also prevents the demonstrated ``object.__setattr__`` path
    from replacing or dropping exact operational relations after verification (ADV-040-C).
    It does not prove artifact provenance closure, evidence subject/quality closure, lane
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