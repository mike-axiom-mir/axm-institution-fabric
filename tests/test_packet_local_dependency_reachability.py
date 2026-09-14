from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from axm_institution.packet_local_dependency_reachability import (
    ExactPacketOutputReachability,
    PacketLocalDependencyReachabilityConsistencyError,
    _derive_reachability,
    preflight_packet_local_dependency_reachability,
)
from axm_institution.packet_same_packet_dependency_graph import (
    ExactPacketOutputNode,
    ExactSamePacketDependencyEdge,
    ExactStronglyConnectedComponent,
    ResolvedPacketSamePacketDependencyGraph,
)


def ref(letter: str) -> str:
    return "axmref:v1:artifact:" + (letter * 64)


class PacketLocalDependencyReachabilityTests(unittest.TestCase):
    def _by_ref(self, outputs):
        return {output.output_ref: output for output in outputs}

    def _fake_graph(self, nodes, edges, categories=None):
        categories = categories or {}
        node_records = tuple(
            ExactPacketOutputNode(
                output_ref=node,
                category=categories.get(node, "created"),
            )
            for node in sorted(nodes)
        )
        return ResolvedPacketSamePacketDependencyGraph(
            packet_ref="axmref:v1:return-packet:" + ("1" * 64),
            claim_ref="axmref:v1:work-claim:" + ("2" * 64),
            claim_base_ref="axmref:v1:state-revision:" + ("3" * 64),
            occupancy_ref="axmref:v1:occupancy:" + ("4" * 64),
            lane_ref="axmref:v1:lane:" + ("5" * 64),
            dependency_context=None,
            nodes=node_records,
            edges=tuple(edges),
            strongly_connected_components=tuple(
                ExactStronglyConnectedComponent((node,), False)
                for node in sorted(nodes)
            ),
            self_edge_refs=(),
            has_cycle=False,
            topological_witness=tuple(sorted(nodes)),
        )

    def test_direct_edge_is_direct_and_strict_transitive_prerequisite(self) -> None:
        required, dependent = ref("a"), ref("b")
        outputs = _derive_reachability(
            (dependent, required),
            (ExactSamePacketDependencyEdge(required, dependent),),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(by_ref[required].direct_prerequisite_refs, ())
        self.assertEqual(by_ref[required].strict_transitive_prerequisite_refs, ())
        self.assertEqual(by_ref[dependent].direct_prerequisite_refs, (required,))
        self.assertEqual(
            by_ref[dependent].strict_transitive_prerequisite_refs,
            (required,),
        )

    def test_three_node_chain_includes_multi_hop_prerequisite(self) -> None:
        root, middle, final = ref("a"), ref("b"), ref("c")
        outputs = _derive_reachability(
            (final, root, middle),
            (
                ExactSamePacketDependencyEdge(root, middle),
                ExactSamePacketDependencyEdge(middle, final),
            ),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(by_ref[final].direct_prerequisite_refs, (middle,))
        self.assertEqual(
            by_ref[final].strict_transitive_prerequisite_refs,
            tuple(sorted((root, middle))),
        )

    def test_independent_lexical_neighbour_gains_no_prerequisite(self) -> None:
        root, dependent, independent = ref("a"), ref("c"), ref("b")
        outputs = _derive_reachability(
            (dependent, independent, root),
            (ExactSamePacketDependencyEdge(root, dependent),),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(by_ref[independent].direct_prerequisite_refs, ())
        self.assertEqual(by_ref[independent].strict_transitive_prerequisite_refs, ())

    def test_edge_outside_decision016_node_set_fails_closed(self) -> None:
        packet_output, external = ref("a"), ref("f")
        with self.assertRaises(PacketLocalDependencyReachabilityConsistencyError):
            _derive_reachability(
                (packet_output,),
                (ExactSamePacketDependencyEdge(external, packet_output),),
            )

    def test_created_and_modified_result_categories_do_not_change_reachability(self) -> None:
        required, dependent = ref("a"), ref("b")
        edge = ExactSamePacketDependencyEdge(required, dependent)
        graph = self._fake_graph(
            (required, dependent),
            (edge,),
            {required: "modified_result", dependent: "created"},
        )

        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(object(), graph.packet_ref)

        by_ref = self._by_ref(result.outputs)
        self.assertIs(result.graph, graph)
        self.assertEqual(by_ref[dependent].direct_prerequisite_refs, (required,))

    def test_node_and_edge_order_cannot_change_reachability_facts(self) -> None:
        a, b, c, d = ref("a"), ref("b"), ref("c"), ref("d")
        edges = (
            ExactSamePacketDependencyEdge(a, c),
            ExactSamePacketDependencyEdge(b, c),
            ExactSamePacketDependencyEdge(c, d),
        )

        first = _derive_reachability((d, b, a, c), edges)
        second = _derive_reachability((c, a, d, b), tuple(reversed(edges)))

        self.assertEqual(first, second)
        self.assertEqual(tuple(item.output_ref for item in first), tuple(sorted((a, b, c, d))))

    def test_same_logical_or_higher_version_has_no_substitution_path(self) -> None:
        exact_packet_ref, decoy_ref, dependent = ref("a"), ref("b"), ref("c")
        outputs = _derive_reachability(
            (exact_packet_ref, dependent),
            (),
        )
        by_ref = self._by_ref(outputs)

        self.assertNotIn(decoy_ref, by_ref)
        self.assertEqual(by_ref[dependent].strict_transitive_prerequisite_refs, ())

    def test_self_edge_makes_output_strictly_reachable_from_itself(self) -> None:
        node = ref("a")
        outputs = _derive_reachability(
            (node,),
            (ExactSamePacketDependencyEdge(node, node),),
        )
        reachability = outputs[0]

        self.assertEqual(reachability.direct_prerequisite_refs, (node,))
        self.assertEqual(reachability.strict_transitive_prerequisite_refs, (node,))

    def test_two_node_cycle_preserves_mutual_and_self_strict_reachability(self) -> None:
        a, b = ref("a"), ref("b")
        outputs = _derive_reachability(
            (b, a),
            (
                ExactSamePacketDependencyEdge(a, b),
                ExactSamePacketDependencyEdge(b, a),
            ),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(by_ref[a].direct_prerequisite_refs, (b,))
        self.assertEqual(by_ref[b].direct_prerequisite_refs, (a,))
        self.assertEqual(by_ref[a].strict_transitive_prerequisite_refs, (a, b))
        self.assertEqual(by_ref[b].strict_transitive_prerequisite_refs, (a, b))

    def test_acyclic_output_is_not_spuriously_self_reachable(self) -> None:
        a, b = ref("a"), ref("b")
        by_ref = self._by_ref(
            _derive_reachability(
                (a, b),
                (ExactSamePacketDependencyEdge(a, b),),
            )
        )

        self.assertNotIn(a, by_ref[a].strict_transitive_prerequisite_refs)
        self.assertNotIn(b, by_ref[b].strict_transitive_prerequisite_refs)

    def test_topological_witness_is_not_used_as_reachability_authority(self) -> None:
        a, b = ref("a"), ref("b")
        graph = self._fake_graph((a, b), (), {a: "created", b: "modified_result"})
        graph = graph._replace(topological_witness=(b, a))

        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(object(), graph.packet_ref)

        for output in result.outputs:
            self.assertEqual(output.direct_prerequisite_refs, ())
            self.assertEqual(output.strict_transitive_prerequisite_refs, ())

    def test_projection_exposes_no_policy_chronology_or_lifecycle_authority(self) -> None:
        node = ref("a")
        graph = self._fake_graph((node,), ())
        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(object(), graph.packet_ref)

        forbidden = (
            "valid",
            "allowed",
            "satisfied",
            "closed",
            "complete",
            "accepted",
            "rejected",
            "integrated",
            "execution_order",
            "execution_chronology",
            "scheduler_order",
            "epoch_complete",
            "replayed",
        )
        for target in (result, result.outputs[0]):
            for name in forbidden:
                self.assertFalse(hasattr(target, name), name)

    def test_named_reachability_leaf_fails_closed_under_ordinary_json_transport(self) -> None:
        a, b = ref("a"), ref("b")
        leaf = ExactPacketOutputReachability(
            output_ref=b,
            direct_prerequisite_refs=(a,),
            strict_transitive_prerequisite_refs=(a,),
        )

        with self.assertRaises(TypeError):
            json.dumps(leaf)
        materialized = leaf._asdict()
        transported = json.loads(json.dumps(materialized))
        self.assertEqual(transported["output_ref"], b)
        self.assertEqual(transported["direct_prerequisite_refs"], [a])
        self.assertEqual(transported["strict_transitive_prerequisite_refs"], [a])


if __name__ == "__main__":
    unittest.main()
