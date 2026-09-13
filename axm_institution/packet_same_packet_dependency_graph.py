from __future__ import annotations

import heapq
from typing import NamedTuple

from .packet_dependency_context_membership import (
    ExactDependencyContextMembership,
    ResolvedOutputDependencyContext,
    ResolvedPacketDependencyContextMembership,
    preflight_dependency_context_membership,
)
from .store import FilesystemObjectStore, ObjectStoreError


class SamePacketDependencyGraphError(ObjectStoreError):
    """Base error for Decision 016 exact same-packet dependency graph facts."""


class SamePacketDependencyGraphConsistencyError(SamePacketDependencyGraphError):
    """Decision 015 packet-output membership facts cannot form one exact graph."""


class ExactPacketOutputNode(NamedTuple):
    """One exact packet output node with its non-authoritative output-family fact."""

    output_ref: str
    category: str


class ExactSamePacketDependencyEdge(NamedTuple):
    """One exact declared packet-local dependency edge.

    The direction is ``required_output_ref -> dependent_output_ref``. The edge is a
    declaration fact only; it is not an execution timestamp, scheduler decision, or
    acceptance result.
    """

    required_output_ref: str
    dependent_output_ref: str


class ExactStronglyConnectedComponent(NamedTuple):
    """One deterministic SCC over exact packet-output refs.

    ``has_cycle`` is a topology fact only. A singleton has a cycle exactly when its node
    has an explicit self-edge.
    """

    member_refs: tuple[str, ...]
    has_cycle: bool


class ResolvedPacketSamePacketDependencyGraph(NamedTuple):
    """Read-only Decision 016 topology projection for one exact return packet.

    ``dependency_context`` remains the authority for exact packet context, output
    selection, dependency identity, and packet-output membership. This wrapper adds only
    deterministic graph facts over those already-grounded exact relations.

    ``topological_witness`` is present only for an acyclic graph. It is one deterministic
    exact-ref-lexically-tiebroken witness that satisfies the declared edge relation; it is
    not historical chronology, scheduler authority, required production order, or packet
    acceptance authority.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    dependency_context: ResolvedPacketDependencyContextMembership
    nodes: tuple[ExactPacketOutputNode, ...]
    edges: tuple[ExactSamePacketDependencyEdge, ...]
    strongly_connected_components: tuple[ExactStronglyConnectedComponent, ...]
    self_edge_refs: tuple[str, ...]
    has_cycle: bool
    topological_witness: tuple[str, ...] | None


def _node_map(
    dependency_context: ResolvedPacketDependencyContextMembership,
) -> dict[str, str]:
    nodes: dict[str, str] = {}

    def register(output: ResolvedOutputDependencyContext, expected_category: str) -> None:
        if output.category != expected_category:
            raise SamePacketDependencyGraphConsistencyError(
                "Decision 016 received a Decision 015 output with category "
                f"{output.category!r} in the {expected_category!r} family"
            )
        reference = output.artifact.reference
        if reference in nodes:
            raise SamePacketDependencyGraphConsistencyError(
                "Decision 016 requires one exact node per packet output ref; duplicate or "
                f"cross-family output ref encountered: {reference!r}"
            )
        nodes[reference] = expected_category

    for output in dependency_context.created_outputs:
        register(output, "created")
    for output in dependency_context.modified_results:
        register(output, "modified_result")
    return nodes


def _same_packet_target_category(
    dependency: ExactDependencyContextMembership,
    *,
    nodes: dict[str, str],
) -> str | None:
    reference = dependency.dependency.reference

    if dependency.in_packet_created and dependency.in_packet_modified_result:
        raise SamePacketDependencyGraphConsistencyError(
            "Decision 016 cannot collapse a Decision 015 dependency that is simultaneously "
            f"classified as created and modified-result output: {reference!r}"
        )

    observed_category: str | None
    if dependency.in_packet_created:
        observed_category = "created"
    elif dependency.in_packet_modified_result:
        observed_category = "modified_result"
    else:
        observed_category = None

    exact_node_category = nodes.get(reference)
    if observed_category != exact_node_category:
        raise SamePacketDependencyGraphConsistencyError(
            "Decision 016 found an internal mismatch between Decision 015 packet-output "
            f"membership and its exact packet-output node set for {reference!r}: "
            f"membership={observed_category!r}, node={exact_node_category!r}"
        )
    return observed_category


def _collect_edges(
    dependency_context: ResolvedPacketDependencyContextMembership,
    *,
    nodes: dict[str, str],
) -> tuple[ExactSamePacketDependencyEdge, ...]:
    edge_pairs: set[tuple[str, str]] = set()

    for output in (*dependency_context.created_outputs, *dependency_context.modified_results):
        dependent_ref = output.artifact.reference
        if dependent_ref not in nodes:
            raise SamePacketDependencyGraphConsistencyError(
                "Decision 016 received a Decision 015 output absent from its exact node set: "
                f"{dependent_ref!r}"
            )
        for dependency in output.dependencies:
            category = _same_packet_target_category(dependency, nodes=nodes)
            if category is None:
                # Base-only and external/unclassified exact dependencies remain preserved in
                # dependency_context but do not become packet-local edges.
                continue
            required_ref = dependency.dependency.reference
            edge_pairs.add((required_ref, dependent_ref))

    return tuple(
        ExactSamePacketDependencyEdge(required_output_ref=required, dependent_output_ref=dependent)
        for required, dependent in sorted(edge_pairs)
    )


def _strongly_connected_components(
    node_refs: tuple[str, ...],
    edges: tuple[ExactSamePacketDependencyEdge, ...],
) -> tuple[ExactStronglyConnectedComponent, ...]:
    adjacency: dict[str, list[str]] = {reference: [] for reference in node_refs}
    reverse: dict[str, list[str]] = {reference: [] for reference in node_refs}
    self_edges: set[str] = set()

    for edge in edges:
        required = edge.required_output_ref
        dependent = edge.dependent_output_ref
        if required not in adjacency or dependent not in adjacency:
            raise SamePacketDependencyGraphConsistencyError(
                "Decision 016 graph edge names a ref outside the exact packet-output node set"
            )
        adjacency[required].append(dependent)
        reverse[dependent].append(required)
        if required == dependent:
            self_edges.add(required)

    for reference in node_refs:
        adjacency[reference].sort()
        reverse[reference].sort()

    visited: set[str] = set()
    finish_order: list[str] = []

    def visit_forward(reference: str) -> None:
        visited.add(reference)
        for neighbour in adjacency[reference]:
            if neighbour not in visited:
                visit_forward(neighbour)
        finish_order.append(reference)

    for reference in node_refs:
        if reference not in visited:
            visit_forward(reference)

    visited.clear()
    raw_components: list[tuple[str, ...]] = []

    def visit_reverse(reference: str, component: list[str]) -> None:
        visited.add(reference)
        component.append(reference)
        for neighbour in reverse[reference]:
            if neighbour not in visited:
                visit_reverse(neighbour, component)

    for reference in reversed(finish_order):
        if reference in visited:
            continue
        component: list[str] = []
        visit_reverse(reference, component)
        raw_components.append(tuple(sorted(component)))

    components = tuple(
        ExactStronglyConnectedComponent(
            member_refs=members,
            has_cycle=(len(members) > 1 or members[0] in self_edges),
        )
        for members in sorted(raw_components)
    )
    return components


def _topological_witness(
    node_refs: tuple[str, ...],
    edges: tuple[ExactSamePacketDependencyEdge, ...],
) -> tuple[str, ...]:
    adjacency: dict[str, set[str]] = {reference: set() for reference in node_refs}
    indegree: dict[str, int] = {reference: 0 for reference in node_refs}

    for edge in edges:
        required = edge.required_output_ref
        dependent = edge.dependent_output_ref
        if dependent not in adjacency[required]:
            adjacency[required].add(dependent)
            indegree[dependent] += 1

    ready = [reference for reference in node_refs if indegree[reference] == 0]
    heapq.heapify(ready)
    witness: list[str] = []

    while ready:
        reference = heapq.heappop(ready)
        witness.append(reference)
        for dependent in sorted(adjacency[reference]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(witness) != len(node_refs):
        raise SamePacketDependencyGraphConsistencyError(
            "Decision 016 could not produce an acyclic topological witness for all exact nodes"
        )
    return tuple(witness)


def preflight_same_packet_dependency_graph(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketSamePacketDependencyGraph:
    """Reconstruct exact packet-local dependency topology from Decision 015 facts only.

    Graph nodes are exact created and modified-result output refs already selected by
    Decision 015. An edge exists only when Decision 015 classifies one output's exact
    dependency target as another exact output of the same packet, and its direction is
    ``required_output_ref -> dependent_output_ref``.

    Node/edge/SCC presentation is deterministic and independent of packet/output/dependency
    array order, store insertion order, logical ids, artifact version, ``supersedes_ref``,
    source/evidence metadata, actor identity, scheduler position, or Git authority.

    Exact self-edges and strongly connected components are preserved as topology facts.
    Cyclic graphs expose no topological witness. Acyclic graphs expose one exact-ref-
    lexically-tiebroken witness only; that witness is not execution history or policy.

    Base-only and external/unclassified dependencies remain available through the nested
    Decision 015 ``dependency_context`` and create no packet-local edge.

    A successful result does not establish dependency admissibility, dependency
    satisfaction, actual chronology, closure/completeness, source/evidence closure,
    lineage policy, packet acceptance/rejection, claim closure, successor publication,
    Stage 5 integration, epochs/barriers, or replay correctness.
    """

    dependency_context = preflight_dependency_context_membership(store, packet_ref)
    nodes_by_ref = _node_map(dependency_context)
    node_refs = tuple(sorted(nodes_by_ref))
    nodes = tuple(
        ExactPacketOutputNode(output_ref=reference, category=nodes_by_ref[reference])
        for reference in node_refs
    )
    edges = _collect_edges(dependency_context, nodes=nodes_by_ref)
    components = _strongly_connected_components(node_refs, edges)
    self_edge_refs = tuple(
        sorted(
            edge.required_output_ref
            for edge in edges
            if edge.required_output_ref == edge.dependent_output_ref
        )
    )
    has_cycle = any(component.has_cycle for component in components)
    witness = None if has_cycle else _topological_witness(node_refs, edges)

    return ResolvedPacketSamePacketDependencyGraph(
        packet_ref=dependency_context.packet_ref,
        claim_ref=dependency_context.claim_ref,
        claim_base_ref=dependency_context.claim_base_ref,
        occupancy_ref=dependency_context.occupancy_ref,
        lane_ref=dependency_context.lane_ref,
        dependency_context=dependency_context,
        nodes=nodes,
        edges=edges,
        strongly_connected_components=components,
        self_edge_refs=self_edge_refs,
        has_cycle=has_cycle,
        topological_witness=witness,
    )
