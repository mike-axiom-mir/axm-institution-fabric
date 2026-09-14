from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch

from axm_institution.identity import parse_json_strict
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


class PacketLocalDependencyReachabilityAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-051 attacks on Decision 017 reachability facts only."""

    def _by_ref(self, outputs):
        return {output.output_ref: output for output in outputs}

    def _fake_graph(
        self,
        nodes,
        edges,
        *,
        categories=None,
        packet_hex="1",
        topological_witness=None,
    ):
        categories = categories or {}
        node_records = tuple(
            ExactPacketOutputNode(
                output_ref=node,
                category=categories.get(node, "created"),
            )
            for node in sorted(nodes)
        )
        witness = (
            tuple(sorted(nodes))
            if topological_witness is None
            else tuple(topological_witness)
        )
        return ResolvedPacketSamePacketDependencyGraph(
            packet_ref="axmref:v1:return-packet:" + (packet_hex * 64),
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
            topological_witness=witness,
        )

    def test_adv051_a_diamond_keeps_direction_and_all_multi_hop_prerequisites(self) -> None:
        root, left, right, final = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = _derive_reachability(
            (final, right, root, left),
            (
                ExactSamePacketDependencyEdge(root, left),
                ExactSamePacketDependencyEdge(root, right),
                ExactSamePacketDependencyEdge(left, final),
                ExactSamePacketDependencyEdge(right, final),
            ),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(by_ref[root].strict_transitive_prerequisite_refs, ())
        self.assertEqual(
            by_ref[final].direct_prerequisite_refs,
            tuple(sorted((left, right))),
        )
        self.assertEqual(
            by_ref[final].strict_transitive_prerequisite_refs,
            tuple(sorted((root, left, right))),
        )

    def test_adv051_b_lexical_position_cannot_reverse_required_dependent_meaning(self) -> None:
        required, dependent = ref("f"), ref("a")
        outputs = _derive_reachability(
            (required, dependent),
            (ExactSamePacketDependencyEdge(required, dependent),),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(tuple(item.output_ref for item in outputs), (dependent, required))
        self.assertEqual(by_ref[dependent].direct_prerequisite_refs, (required,))
        self.assertEqual(by_ref[required].direct_prerequisite_refs, ())

    def test_adv051_c_cycle_with_upstream_root_preserves_self_and_mutual_reachability(self) -> None:
        root, a, b, c = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = _derive_reachability(
            (c, root, b, a),
            (
                ExactSamePacketDependencyEdge(root, a),
                ExactSamePacketDependencyEdge(a, b),
                ExactSamePacketDependencyEdge(b, c),
                ExactSamePacketDependencyEdge(c, a),
            ),
        )
        by_ref = self._by_ref(outputs)
        expected_cycle_prereqs = tuple(sorted((root, a, b, c)))

        self.assertEqual(by_ref[root].strict_transitive_prerequisite_refs, ())
        for member in (a, b, c):
            self.assertEqual(
                by_ref[member].strict_transitive_prerequisite_refs,
                expected_cycle_prereqs,
            )
            self.assertIn(member, by_ref[member].strict_transitive_prerequisite_refs)

    def test_adv051_d_shared_root_does_not_make_sibling_branch_a_prerequisite(self) -> None:
        root, left, sibling, final = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = _derive_reachability(
            (sibling, final, left, root),
            (
                ExactSamePacketDependencyEdge(root, left),
                ExactSamePacketDependencyEdge(root, sibling),
                ExactSamePacketDependencyEdge(left, final),
            ),
        )
        by_ref = self._by_ref(outputs)

        self.assertEqual(
            by_ref[final].strict_transitive_prerequisite_refs,
            tuple(sorted((root, left))),
        )
        self.assertNotIn(sibling, by_ref[final].strict_transitive_prerequisite_refs)

    def test_adv051_e_parallel_projection_calls_do_not_rebind_earlier_exact_facts(self) -> None:
        a, b, c, d = ref("a"), ref("b"), ref("c"), ref("d")
        first_graph = self._fake_graph(
            (a, b),
            (ExactSamePacketDependencyEdge(a, b),),
            packet_hex="1",
        )
        second_graph = self._fake_graph(
            (c, d),
            (ExactSamePacketDependencyEdge(c, d),),
            packet_hex="6",
        )

        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            side_effect=(first_graph, second_graph),
        ):
            first = preflight_packet_local_dependency_reachability(
                object(), first_graph.packet_ref
            )
            second = preflight_packet_local_dependency_reachability(
                object(), second_graph.packet_ref
            )

        self.assertEqual(first.packet_ref, first_graph.packet_ref)
        self.assertEqual(second.packet_ref, second_graph.packet_ref)
        self.assertEqual(
            self._by_ref(first.outputs)[b].strict_transitive_prerequisite_refs,
            (a,),
        )
        self.assertEqual(
            self._by_ref(second.outputs)[d].strict_transitive_prerequisite_refs,
            (c,),
        )
        self.assertNotIn(c, self._by_ref(first.outputs))
        self.assertNotIn(a, self._by_ref(second.outputs))

    def test_adv051_f_contradictory_topological_witness_cannot_rebind_reachability(self) -> None:
        required, dependent = ref("a"), ref("b")
        graph = self._fake_graph(
            (required, dependent),
            (ExactSamePacketDependencyEdge(required, dependent),),
            topological_witness=(dependent, required),
        )

        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(
                object(), graph.packet_ref
            )

        by_ref = self._by_ref(result.outputs)
        self.assertEqual(by_ref[dependent].direct_prerequisite_refs, (required,))
        self.assertEqual(by_ref[required].direct_prerequisite_refs, ())
        self.assertEqual(result.graph.topological_witness, (dependent, required))

    def test_adv051_g_duplicate_exact_node_reference_fails_closed(self) -> None:
        node = ref("a")
        with self.assertRaises(PacketLocalDependencyReachabilityConsistencyError):
            _derive_reachability((node, node), ())

    def test_adv051_h_named_leaf_materialization_copy_and_transport_preserve_meaning(self) -> None:
        required, dependent = ref("a"), ref("b")
        leaf = ExactPacketOutputReachability(
            output_ref=dependent,
            direct_prerequisite_refs=(required,),
            strict_transitive_prerequisite_refs=(required,),
        )

        physical = parse_json_strict(memoryview(leaf).tobytes().decode("utf-8"))
        self.assertEqual(
            physical,
            {
                "direct_prerequisite_refs": [required],
                "output_ref": dependent,
                "strict_transitive_prerequisite_refs": [required],
            },
        )

        materialized = leaf._asdict()
        transported = json.loads(json.dumps(materialized))
        self.assertEqual(transported["output_ref"], dependent)
        self.assertEqual(transported["direct_prerequisite_refs"], [required])
        transported["output_ref"] = required
        transported["direct_prerequisite_refs"] = []
        self.assertEqual(leaf.output_ref, dependent)
        self.assertEqual(leaf.direct_prerequisite_refs, (required,))

        for copier in (copy.copy, copy.deepcopy):
            copied = copier(leaf)
            self.assertIs(type(copied), type(leaf))
            self.assertEqual(bytes(copied), bytes(leaf))
            self.assertEqual(copied._asdict(), leaf._asdict())

        with self.assertRaises(TypeError):
            json.dumps(leaf)

    def test_adv051_i_full_projection_transport_rejects_or_preserves_named_top_level_semantics(self) -> None:
        node = ref("a")
        graph = self._fake_graph((node,), ())
        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(
                object(), graph.packet_ref
            )

        try:
            encoded = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return

        transported = json.loads(encoded)
        self.assertIsInstance(
            transported,
            dict,
            "Decision 017 aggregate transport was accepted but lost named top-level semantics",
        )
        self.assertEqual(transported["packet_ref"], graph.packet_ref)
        self.assertIn("outputs", transported)
        self.assertIsInstance(transported["outputs"], list)
        self.assertEqual(transported["outputs"][0]["output_ref"], node)

    def test_adv051_j_reachability_projection_exposes_no_policy_or_lifecycle_authority(self) -> None:
        node = ref("a")
        graph = self._fake_graph((node,), ())
        with patch(
            "axm_institution.packet_local_dependency_reachability."
            "preflight_same_packet_dependency_graph",
            return_value=graph,
        ):
            result = preflight_packet_local_dependency_reachability(
                object(), graph.packet_ref
            )

        forbidden = (
            "valid",
            "allowed",
            "satisfied",
            "complete",
            "closed",
            "accepted",
            "rejected",
            "integrated",
            "dependency_policy",
            "execution_order",
            "execution_chronology",
            "scheduler_order",
            "lexical_priority",
            "epoch_complete",
            "replayed",
        )
        for target in (result, result.outputs[0]):
            for name in forbidden:
                self.assertFalse(hasattr(target, name), name)


if __name__ == "__main__":
    unittest.main()
