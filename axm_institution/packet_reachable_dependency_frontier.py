from __future__ import annotations

from typing import Any, NamedTuple

from .identity import canonical_bytes, parse_json_strict
from .packet_dependency_context_membership import ResolvedOutputDependencyContext
from .packet_local_dependency_reachability import (
    ResolvedPacketLocalDependencyReachability,
    preflight_packet_local_dependency_reachability,
)
from .store import FilesystemObjectStore, ObjectStoreError


class ReachableDependencyFrontierError(ObjectStoreError):
    """Base error for Decision 018 exact reachable dependency frontier facts."""


class ReachableDependencyFrontierConsistencyError(ReachableDependencyFrontierError):
    """Canonical Decision 015-017 facts cannot form one exact frontier projection."""


class _FrozenFrontierLeaf(bytes):
    """Canonical-byte-backed named Decision 018 leaf.

    Frontier records carry named institutional meaning. Keeping the authoritative leaf as
    canonical bytes preserves physical immutability and makes unsupported ordinary JSON
    transport fail closed instead of silently converting named relations into positional
    arrays.
    """

    __slots__ = ()
    _fields: tuple[str, ...] = ()

    @classmethod
    def _from_mapping(cls, mapping: dict[str, Any]):
        return bytes.__new__(cls, canonical_bytes(mapping))

    def _plain(self) -> dict[str, Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, dict):
            raise TypeError("frozen Decision 018 frontier leaf did not decode as a mapping")
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


class ExactReachableDependencyFrontierRelation(_FrozenFrontierLeaf):
    """One exact non-packet dependency declaration reachable from one packet output.

    ``in_claim_base`` is copied unchanged from Decision 015. It is a membership fact only;
    it does not mean valid, allowed, satisfied, usable, historically prior, or accepted.
    """

    _fields = ("declaring_output_ref", "dependency_ref", "in_claim_base")

    def __new__(
        cls,
        declaring_output_ref: str,
        dependency_ref: str,
        in_claim_base: bool,
    ):
        return cls._from_mapping(
            {
                "declaring_output_ref": declaring_output_ref,
                "dependency_ref": dependency_ref,
                "in_claim_base": in_claim_base,
            }
        )

    @property
    def declaring_output_ref(self) -> str:
        value = self._plain()["declaring_output_ref"]
        if not isinstance(value, str):
            raise TypeError("frozen Decision 018 declaring_output_ref is not a string")
        return value

    @property
    def dependency_ref(self) -> str:
        value = self._plain()["dependency_ref"]
        if not isinstance(value, str):
            raise TypeError("frozen Decision 018 dependency_ref is not a string")
        return value

    @property
    def in_claim_base(self) -> bool:
        value = self._plain()["in_claim_base"]
        if not isinstance(value, bool):
            raise TypeError("frozen Decision 018 in_claim_base is not boolean")
        return value


class ExactPacketOutputDependencyFrontier(_FrozenFrontierLeaf):
    """Exact reachable non-packet dependency frontier for one exact packet output."""

    _fields = ("output_ref", "frontier_relations")

    def __new__(
        cls,
        output_ref: str,
        frontier_relations: tuple[ExactReachableDependencyFrontierRelation, ...],
    ):
        return cls._from_mapping(
            {
                "output_ref": output_ref,
                "frontier_relations": [relation._plain() for relation in frontier_relations],
            }
        )

    @property
    def output_ref(self) -> str:
        value = self._plain()["output_ref"]
        if not isinstance(value, str):
            raise TypeError("frozen Decision 018 output_ref is not a string")
        return value

    @property
    def frontier_relations(self) -> tuple[ExactReachableDependencyFrontierRelation, ...]:
        value = self._plain()["frontier_relations"]
        if not isinstance(value, list):
            raise TypeError("frozen Decision 018 frontier_relations is not an array")

        relations: list[ExactReachableDependencyFrontierRelation] = []
        for relation in value:
            if not isinstance(relation, dict):
                raise TypeError("frozen Decision 018 frontier relation is not a mapping")
            declaring_output_ref = relation.get("declaring_output_ref")
            dependency_ref = relation.get("dependency_ref")
            in_claim_base = relation.get("in_claim_base")
            if not isinstance(declaring_output_ref, str):
                raise TypeError("frozen Decision 018 declaring_output_ref is not a string")
            if not isinstance(dependency_ref, str):
                raise TypeError("frozen Decision 018 dependency_ref is not a string")
            if not isinstance(in_claim_base, bool):
                raise TypeError("frozen Decision 018 in_claim_base is not boolean")
            relations.append(
                ExactReachableDependencyFrontierRelation(
                    declaring_output_ref=declaring_output_ref,
                    dependency_ref=dependency_ref,
                    in_claim_base=in_claim_base,
                )
            )
        return tuple(relations)


class ResolvedPacketReachableDependencyFrontier(NamedTuple):
    """Read-only Decision 018 projection over canonical Decision 017 reachability.

    ``reachability`` remains the sole packet-local reachability authority and preserves the
    nested canonical Decision 015 dependency context. This wrapper adds only the exact
    non-packet dependency declarations reachable from each packet output's prerequisite
    subgraph.

    The result carries no dependency admissibility, satisfaction, completeness, closure,
    chronology, scheduler, packet acceptance, claim closure, integration, epoch, or replay
    authority.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    reachability: ResolvedPacketLocalDependencyReachability
    outputs: tuple[ExactPacketOutputDependencyFrontier, ...]


def _output_context_by_ref(
    reachability: ResolvedPacketLocalDependencyReachability,
) -> dict[str, ResolvedOutputDependencyContext]:
    dependency_context = reachability.graph.dependency_context
    if dependency_context is None:
        raise ReachableDependencyFrontierConsistencyError(
            "Decision 018 requires the nested canonical Decision 015 dependency context"
        )

    for field in ("packet_ref", "claim_ref", "claim_base_ref", "occupancy_ref", "lane_ref"):
        if getattr(reachability, field) != getattr(dependency_context, field):
            raise ReachableDependencyFrontierConsistencyError(
                f"Decision 018 found inconsistent nested {field} facts"
            )

    output_contexts: dict[str, ResolvedOutputDependencyContext] = {}

    def register(output: ResolvedOutputDependencyContext, expected_category: str) -> None:
        if output.category != expected_category:
            raise ReachableDependencyFrontierConsistencyError(
                "Decision 018 received a Decision 015 output with category "
                f"{output.category!r} in the {expected_category!r} family"
            )
        reference = output.artifact.reference
        if reference in output_contexts:
            raise ReachableDependencyFrontierConsistencyError(
                "Decision 018 requires one exact Decision 015 context per packet output: "
                f"{reference!r}"
            )
        output_contexts[reference] = output

    for output in dependency_context.created_outputs:
        register(output, "created")
    for output in dependency_context.modified_results:
        register(output, "modified_result")

    reachability_refs = tuple(output.output_ref for output in reachability.outputs)
    if len(set(reachability_refs)) != len(reachability_refs):
        raise ReachableDependencyFrontierConsistencyError(
            "Decision 018 requires one exact Decision 017 reachability record per output"
        )
    if set(reachability_refs) != set(output_contexts):
        raise ReachableDependencyFrontierConsistencyError(
            "Decision 018 Decision 017 output refs do not match the nested Decision 015 "
            "packet-output refs"
        )

    return output_contexts


def _derive_frontiers(
    reachability: ResolvedPacketLocalDependencyReachability,
) -> tuple[ExactPacketOutputDependencyFrontier, ...]:
    """Derive exact reachable non-packet declaration facts from Decisions 015-017.

    This helper does not reload objects or reclassify dependencies. Packet-local
    reachability comes only from Decision 017, while dependency target context comes only
    from the nested Decision 015 membership records.
    """

    output_contexts = _output_context_by_ref(reachability)
    packet_output_refs = frozenset(output_contexts)
    resolved: list[ExactPacketOutputDependencyFrontier] = []

    for output_reachability in sorted(reachability.outputs, key=lambda item: item.output_ref):
        output_ref = output_reachability.output_ref
        scope = {output_ref, *output_reachability.strict_transitive_prerequisite_refs}
        if not scope.issubset(packet_output_refs):
            unknown = tuple(sorted(scope.difference(packet_output_refs)))
            raise ReachableDependencyFrontierConsistencyError(
                "Decision 018 received Decision 017 prerequisite refs outside the exact "
                f"packet-output set: {unknown!r}"
            )

        relations: list[ExactReachableDependencyFrontierRelation] = []
        for declaring_output_ref in sorted(scope):
            declaring_output = output_contexts[declaring_output_ref]
            for dependency in declaring_output.dependencies:
                if dependency.in_packet_created or dependency.in_packet_modified_result:
                    # Exact same-packet targets remain represented by Decisions 016-017.
                    # ``in_claim_base`` is independent and cannot promote them into the
                    # frontier.
                    continue
                relations.append(
                    ExactReachableDependencyFrontierRelation(
                        declaring_output_ref=declaring_output_ref,
                        dependency_ref=dependency.dependency.reference,
                        in_claim_base=dependency.in_claim_base,
                    )
                )

        relations.sort(
            key=lambda relation: (
                relation.declaring_output_ref,
                relation.dependency_ref,
                relation.in_claim_base,
            )
        )
        resolved.append(
            ExactPacketOutputDependencyFrontier(
                output_ref=output_ref,
                frontier_relations=tuple(relations),
            )
        )

    return tuple(resolved)


def preflight_reachable_dependency_frontier(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketReachableDependencyFrontier:
    """Reconstruct the exact reachable non-packet dependency boundary for one packet.

    Decision 017 is called once and remains the sole packet-local reachability authority.
    Decision 018 then consumes its nested canonical Decision 015 dependency membership
    records unchanged. For each exact output, the scope is that output plus every exact
    strict-transitive packet-local prerequisite. Only declarations whose Decision 015
    packet-output membership flags are both false become frontier relations.

    ``in_claim_base`` remains an exact membership fact. ``False`` means only outside the
    exact claim-base artifact membership on this projection; it is not validity or
    rejection. Exact-ref lexical sorting is presentation only. Logical id, version,
    ``supersedes_ref``, source/evidence metadata, recency, family, topological witness,
    actor identity, scheduler state, and Git permission do not participate.

    Success establishes reachable declaration facts only. It does not establish
    admissibility, satisfaction, declaration completeness, dependency closure, actual
    chronology, scheduler order, packet acceptance, claim closure, successor publication,
    Stage 5 integration, epochs/barriers, or replay correctness.
    """

    reachability = preflight_packet_local_dependency_reachability(store, packet_ref)
    outputs = _derive_frontiers(reachability)

    return ResolvedPacketReachableDependencyFrontier(
        packet_ref=reachability.packet_ref,
        claim_ref=reachability.claim_ref,
        claim_base_ref=reachability.claim_base_ref,
        occupancy_ref=reachability.occupancy_ref,
        lane_ref=reachability.lane_ref,
        reachability=reachability,
        outputs=outputs,
    )
