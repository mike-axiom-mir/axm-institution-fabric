from __future__ import annotations

from typing import Any, NamedTuple

from .identity import canonical_bytes, parse_json_strict
from .packet_same_packet_dependency_graph import (
    ExactSamePacketDependencyEdge,
    ResolvedPacketSamePacketDependencyGraph,
    preflight_same_packet_dependency_graph,
)
from .store import FilesystemObjectStore, ObjectStoreError


class PacketLocalDependencyReachabilityError(ObjectStoreError):
    """Base error for Decision 017 exact packet-local reachability facts."""


class PacketLocalDependencyReachabilityConsistencyError(
    PacketLocalDependencyReachabilityError
):
    """Decision 016 graph facts cannot form one exact reachability projection."""


class _FrozenReachabilityLeaf(bytes):
    """Canonical-byte-backed named Decision 017 leaf.

    Decision 017 prerequisite records carry named institutional meaning. Keeping the
    authoritative leaf as canonical bytes preserves physical immutability and makes
    unsupported ordinary JSON transport fail closed instead of silently converting a
    named record into a positional array.
    """

    __slots__ = ()
    _fields: tuple[str, ...] = ()

    @classmethod
    def _from_mapping(cls, mapping: dict[str, Any]):
        return bytes.__new__(cls, canonical_bytes(mapping))

    def _plain(self) -> dict[str, Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, dict):
            raise TypeError("frozen Decision 017 reachability leaf did not decode as a mapping")
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


class ExactPacketOutputReachability(_FrozenReachabilityLeaf):
    """Exact packet-local prerequisite facts for one exact packet output.

    ``direct_prerequisite_refs`` contains only incoming Decision 016 edge sources.
    ``strict_transitive_prerequisite_refs`` contains refs reachable by one or more
    prerequisite hops. The output may therefore occur in its own strict set only when a
    non-empty self/cycle path returns to it.
    """

    _fields = (
        "output_ref",
        "direct_prerequisite_refs",
        "strict_transitive_prerequisite_refs",
    )

    def __new__(
        cls,
        output_ref: str,
        direct_prerequisite_refs: tuple[str, ...],
        strict_transitive_prerequisite_refs: tuple[str, ...],
    ):
        return cls._from_mapping(
            {
                "output_ref": output_ref,
                "direct_prerequisite_refs": list(direct_prerequisite_refs),
                "strict_transitive_prerequisite_refs": list(
                    strict_transitive_prerequisite_refs
                ),
            }
        )

    @property
    def output_ref(self) -> str:
        value = self._plain()["output_ref"]
        if not isinstance(value, str):
            raise TypeError("frozen Decision 017 output_ref is not a string")
        return value

    def _string_tuple(self, field: str) -> tuple[str, ...]:
        value = self._plain()[field]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise TypeError(f"frozen Decision 017 {field} is not a string array")
        return tuple(value)

    @property
    def direct_prerequisite_refs(self) -> tuple[str, ...]:
        return self._string_tuple("direct_prerequisite_refs")

    @property
    def strict_transitive_prerequisite_refs(self) -> tuple[str, ...]:
        return self._string_tuple("strict_transitive_prerequisite_refs")


class ResolvedPacketLocalDependencyReachability(NamedTuple):
    """Read-only Decision 017 projection over one canonical Decision 016 graph.

    ``graph`` remains the sole authority for packet-local nodes and directed edges. This
    wrapper adds only deterministic direct and strict-transitive prerequisite facts. It
    carries no validity, admissibility, satisfaction, chronology, closure, acceptance,
    integration, epoch, or replay meaning.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    graph: ResolvedPacketSamePacketDependencyGraph
    outputs: tuple[ExactPacketOutputReachability, ...]


def _derive_reachability(
    node_refs: tuple[str, ...],
    edges: tuple[ExactSamePacketDependencyEdge, ...],
) -> tuple[ExactPacketOutputReachability, ...]:
    """Derive strict prerequisite reachability from exact Decision 016 graph facts.

    This helper deliberately knows nothing about artifact ids, versions, families,
    provenance, evidence, packet ordering, scheduler state, or mutable currentness.
    """

    ordered_nodes = tuple(sorted(node_refs))
    if len(set(ordered_nodes)) != len(ordered_nodes):
        raise PacketLocalDependencyReachabilityConsistencyError(
            "Decision 017 requires one exact packet-output node per reference"
        )

    node_set = set(ordered_nodes)
    incoming: dict[str, set[str]] = {reference: set() for reference in ordered_nodes}

    for edge in edges:
        required = edge.required_output_ref
        dependent = edge.dependent_output_ref
        if required not in node_set or dependent not in node_set:
            raise PacketLocalDependencyReachabilityConsistencyError(
                "Decision 017 received a Decision 016 edge outside its exact node set"
            )
        incoming[dependent].add(required)

    resolved: list[ExactPacketOutputReachability] = []
    for output_ref in ordered_nodes:
        direct = tuple(sorted(incoming[output_ref]))
        seen: set[str] = set()
        pending = list(reversed(direct))

        while pending:
            prerequisite = pending.pop()
            if prerequisite in seen:
                continue
            seen.add(prerequisite)
            # Do not pre-seed ``seen`` with output_ref. A self/cycle path therefore adds
            # the starting ref only when a non-empty path actually returns to it.
            for transitive in sorted(incoming[prerequisite], reverse=True):
                if transitive not in seen:
                    pending.append(transitive)

        resolved.append(
            ExactPacketOutputReachability(
                output_ref=output_ref,
                direct_prerequisite_refs=direct,
                strict_transitive_prerequisite_refs=tuple(sorted(seen)),
            )
        )

    return tuple(resolved)


def preflight_packet_local_dependency_reachability(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketLocalDependencyReachability:
    """Reconstruct exact packet-local prerequisite reachability from Decision 016 only.

    Decision 016 remains the sole authority for exact packet-output nodes and exact
    ``required_output_ref -> dependent_output_ref`` edges. Decision 017 follows those
    edges backward from each dependent output to report direct and strict-transitive
    packet-local prerequisites.

    Claim-base-only and external/unclassified dependencies never become nodes or
    prerequisite refs here. Exact-ref lexical sorting is presentation only, not semantic
    priority. The Decision 016 topological witness is preserved only inside ``graph`` and
    is never used to derive reachability or historical chronology.

    A successful result is graph fact before dependency policy. It does not establish
    dependency validity/admissibility/satisfaction, declaration completeness, execution
    chronology, scheduler order, source/evidence closure, cycle permission, packet
    acceptance, claim closure, successor publication, Stage 5 integration, epochs, or
    replay correctness.
    """

    graph = preflight_same_packet_dependency_graph(store, packet_ref)
    node_refs = tuple(node.output_ref for node in graph.nodes)
    outputs = _derive_reachability(node_refs, graph.edges)

    return ResolvedPacketLocalDependencyReachability(
        packet_ref=graph.packet_ref,
        claim_ref=graph.claim_ref,
        claim_base_ref=graph.claim_base_ref,
        occupancy_ref=graph.occupancy_ref,
        lane_ref=graph.lane_ref,
        graph=graph,
        outputs=outputs,
    )
