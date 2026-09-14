from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from axm_institution.packet_dependency_context_membership import (
    ExactDependencyContextMembership,
    ResolvedOutputDependencyContext,
    ResolvedPacketDependencyContextMembership,
)
from axm_institution.packet_local_dependency_reachability import (
    ExactPacketOutputReachability,
    ResolvedPacketLocalDependencyReachability,
)
from axm_institution.packet_output_identity import ExactPacketRelation
from axm_institution.packet_reachable_dependency_frontier import (
    ExactPacketOutputDependencyFrontier,
    ExactReachableDependencyFrontierRelation,
    ReachableDependencyFrontierConsistencyError,
    _derive_frontiers,
    preflight_reachable_dependency_frontier,
)
from axm_institution.packet_same_packet_dependency_graph import (
    ExactPacketOutputNode,
    ExactStronglyConnectedComponent,
    ResolvedPacketSamePacketDependencyGraph,
)


def ref(letter: str) -> str:
    return "axmref:v1:artifact:" + (letter * 64)


PACKET_REF = "axmref:v1:return-packet:" + ("1" * 64)
CLAIM_REF = "axmref:v1:work-claim:" + ("2" * 64)
BASE_REF = "axmref:v1:state-revision:" + ("3" * 64)
OCCUPANCY_REF = "axmref:v1:occupancy:" + ("4" * 64)
LANE_REF = "axmref:v1:lane:" + ("5" * 64)


class PacketReachableDependencyFrontierTests(unittest.TestCase):
    def _relation(self, reference: str, value=None) -> ExactPacketRelation:
        return ExactPacketRelation(reference=reference, value={} if value is None else value)

    def _dependency(
        self,
        reference: str,
        *,
        in_claim_base: bool = False,
        in_packet_created: bool = False,
        in_packet_modified_result: bool = False,
        value=None,
    ) -> ExactDependencyContextMembership:
        return ExactDependencyContextMembership(
            dependency=self._relation(reference, value=value),
            in_claim_base=in_claim_base,
            in_packet_created=in_packet_created,
            in_packet_modified_result=in_packet_modified_result,
        )

    def _output(self, reference: str, dependencies=(), category="created"):
        return ResolvedOutputDependencyContext(
            category=category,
            artifact=self._relation(reference),
            dependencies=tuple(dependencies),
        )

    def _reachability(
        self,
        outputs,
        *,
        strict_by_ref=None,
        direct_by_ref=None,
        reachability_order=None,
    ) -> ResolvedPacketLocalDependencyReachability:
        strict_by_ref = strict_by_ref or {}
        direct_by_ref = direct_by_ref or {}
        created = tuple(output for output in outputs if output.category == "created")
        modified = tuple(output for output in outputs if output.category == "modified_result")
        dependency_context = ResolvedPacketDependencyContextMembership(
            packet_ref=PACKET_REF,
            claim_ref=CLAIM_REF,
            claim_base_ref=BASE_REF,
            occupancy_ref=OCCUPANCY_REF,
            lane_ref=LANE_REF,
            dependency_identity=None,
            claim_base=self._relation(BASE_REF),
            created_outputs=created,
            modified_results=modified,
        )
        output_refs = tuple(output.artifact.reference for output in outputs)
        graph = ResolvedPacketSamePacketDependencyGraph(
            packet_ref=PACKET_REF,
            claim_ref=CLAIM_REF,
            claim_base_ref=BASE_REF,
            occupancy_ref=OCCUPANCY_REF,
            lane_ref=LANE_REF,
            dependency_context=dependency_context,
            nodes=tuple(
                ExactPacketOutputNode(output_ref=output.artifact.reference, category=output.category)
                for output in sorted(outputs, key=lambda item: item.artifact.reference)
            ),
            edges=(),
            strongly_connected_components=tuple(
                ExactStronglyConnectedComponent((reference,), False)
                for reference in sorted(output_refs)
            ),
            self_edge_refs=(),
            has_cycle=False,
            topological_witness=tuple(sorted(output_refs)),
        )
        order = reachability_order or output_refs
        reachability_outputs = tuple(
            ExactPacketOutputReachability(
                output_ref=reference,
                direct_prerequisite_refs=tuple(sorted(direct_by_ref.get(reference, ()))),
                strict_transitive_prerequisite_refs=tuple(
                    sorted(strict_by_ref.get(reference, ()))
                ),
            )
            for reference in order
        )
        return ResolvedPacketLocalDependencyReachability(
            packet_ref=PACKET_REF,
            claim_ref=CLAIM_REF,
            claim_base_ref=BASE_REF,
            occupancy_ref=OCCUPANCY_REF,
            lane_ref=LANE_REF,
            graph=graph,
            outputs=reachability_outputs,
        )

    def _by_ref(self, result):
        return {output.output_ref: output for output in result}

    def _triples(self, output):
        return tuple(
            (
                relation.declaring_output_ref,
                relation.dependency_ref,
                relation.in_claim_base,
            )
            for relation in output.frontier_relations
        )

    def test_direct_claim_base_dependency_produces_named_frontier_relation(self) -> None:
        output_ref, base_dep = ref("a"), ref("b")
        reachability = self._reachability(
            (self._output(output_ref, (self._dependency(base_dep, in_claim_base=True),)),)
        )

        result = _derive_frontiers(reachability)

        self.assertEqual(
            self._triples(result[0]),
            ((output_ref, base_dep, True),),
        )

    def test_outside_dependency_remains_explicit_false_without_validity_meaning(self) -> None:
        output_ref, outside_dep = ref("a"), ref("f")
        result = _derive_frontiers(
            self._reachability(
                (self._output(output_ref, (self._dependency(outside_dep),)),)
            )
        )
        relation = result[0].frontier_relations[0]

        self.assertEqual(relation.dependency_ref, outside_dep)
        self.assertFalse(relation.in_claim_base)
        for name in ("valid", "invalid", "allowed", "rejected", "satisfied"):
            self.assertFalse(hasattr(relation, name), name)

    def test_final_output_inherits_frontier_from_direct_packet_prerequisite(self) -> None:
        prerequisite, final, base_dep = ref("a"), ref("b"), ref("c")
        outputs = (
            self._output(prerequisite, (self._dependency(base_dep, in_claim_base=True),)),
            self._output(
                final,
                (self._dependency(prerequisite, in_packet_created=True),),
            ),
        )
        reachability = self._reachability(
            outputs,
            strict_by_ref={final: (prerequisite,)},
            direct_by_ref={final: (prerequisite,)},
        )

        result = self._by_ref(_derive_frontiers(reachability))

        self.assertEqual(
            self._triples(result[final]),
            ((prerequisite, base_dep, True),),
        )

    def test_three_node_chain_carries_root_frontier_to_final(self) -> None:
        root, middle, final, outside_dep = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = (
            self._output(root, (self._dependency(outside_dep),)),
            self._output(middle, (self._dependency(root, in_packet_created=True),)),
            self._output(final, (self._dependency(middle, in_packet_created=True),)),
        )
        reachability = self._reachability(
            outputs,
            strict_by_ref={middle: (root,), final: (root, middle)},
        )

        result = self._by_ref(_derive_frontiers(reachability))

        self.assertEqual(self._triples(result[final]), ((root, outside_dep, False),))

    def test_diamond_preserves_both_reachable_branch_frontiers(self) -> None:
        root, left, right, final = ref("a"), ref("b"), ref("c"), ref("d")
        left_dep, right_dep = ref("e"), ref("f")
        outputs = (
            self._output(root),
            self._output(
                left,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(left_dep, in_claim_base=True),
                ),
            ),
            self._output(
                right,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(right_dep),
                ),
            ),
            self._output(
                final,
                (
                    self._dependency(left, in_packet_created=True),
                    self._dependency(right, in_packet_created=True),
                ),
            ),
        )
        reachability = self._reachability(
            outputs,
            strict_by_ref={left: (root,), right: (root,), final: (root, left, right)},
        )

        result = self._by_ref(_derive_frontiers(reachability))

        self.assertEqual(
            self._triples(result[final]),
            tuple(sorted(((left, left_dep, True), (right, right_dep, False)))),
        )

    def test_sibling_outside_prerequisite_subgraph_contributes_nothing(self) -> None:
        root, final, sibling = ref("a"), ref("b"), ref("c")
        root_dep, sibling_dep = ref("d"), ref("e")
        outputs = (
            self._output(root, (self._dependency(root_dep),)),
            self._output(final, (self._dependency(root, in_packet_created=True),)),
            self._output(sibling, (self._dependency(sibling_dep),)),
        )
        reachability = self._reachability(outputs, strict_by_ref={final: (root,)})

        result = self._by_ref(_derive_frontiers(reachability))

        self.assertEqual(self._triples(result[final]), ((root, root_dep, False),))
        self.assertNotIn(sibling_dep, tuple(item[1] for item in self._triples(result[final])))

    def test_same_packet_target_is_not_frontier_relation(self) -> None:
        required, dependent = ref("a"), ref("b")
        outputs = (
            self._output(required),
            self._output(
                dependent,
                (self._dependency(required, in_packet_created=True),),
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(outputs, strict_by_ref={dependent: (required,)})
            )
        )

        self.assertEqual(result[dependent].frontier_relations, ())

    def test_packet_target_also_in_claim_base_stays_packet_local_not_frontier(self) -> None:
        required, dependent = ref("a"), ref("b")
        outputs = (
            self._output(required, category="modified_result"),
            self._output(
                dependent,
                (
                    self._dependency(
                        required,
                        in_claim_base=True,
                        in_packet_modified_result=True,
                    ),
                ),
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(outputs, strict_by_ref={dependent: (required,)})
            )
        )

        self.assertEqual(result[dependent].frontier_relations, ())

    def test_same_dependency_declared_by_two_reachable_outputs_keeps_both_declarers(self) -> None:
        root, middle, final, shared_dep = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = (
            self._output(root, (self._dependency(shared_dep, in_claim_base=True),)),
            self._output(
                middle,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(shared_dep, in_claim_base=True),
                ),
            ),
            self._output(final, (self._dependency(middle, in_packet_created=True),)),
        )
        reachability = self._reachability(
            outputs,
            strict_by_ref={middle: (root,), final: (root, middle)},
        )

        result = self._by_ref(_derive_frontiers(reachability))

        self.assertEqual(
            self._triples(result[final]),
            ((root, shared_dep, True), (middle, shared_dep, True)),
        )

    def test_output_and_dependency_order_do_not_change_frontier_facts(self) -> None:
        a, b, c, dep1, dep2 = ref("a"), ref("b"), ref("c"), ref("d"), ref("e")
        a_one = self._output(
            a,
            (self._dependency(dep2), self._dependency(dep1, in_claim_base=True)),
        )
        a_two = self._output(
            a,
            tuple(reversed(a_one.dependencies)),
        )
        b_output = self._output(b, (self._dependency(a, in_packet_created=True),))
        c_output = self._output(c)
        first = self._reachability(
            (a_one, b_output, c_output),
            strict_by_ref={b: (a,)},
            reachability_order=(c, b, a),
        )
        second = self._reachability(
            (c_output, b_output, a_two),
            strict_by_ref={b: (a,)},
            reachability_order=(a, b, c),
        )

        self.assertEqual(_derive_frontiers(first), _derive_frontiers(second))

    def test_logical_version_supersedes_metadata_cannot_substitute_exact_dependency(self) -> None:
        output_ref, exact_dep, decoy = ref("a"), ref("b"), ref("c")
        metadata = {
            "id": "artifact-shared-logical-id",
            "version": "999",
            "supersedes_ref": decoy,
        }
        output = self._output(
            output_ref,
            (
                self._dependency(
                    exact_dep,
                    in_claim_base=True,
                    value=metadata,
                ),
            ),
        )

        result = _derive_frontiers(self._reachability((output,)))

        self.assertEqual(result[0].frontier_relations[0].dependency_ref, exact_dep)
        self.assertNotEqual(result[0].frontier_relations[0].dependency_ref, decoy)

    def test_unknown_decision017_prerequisite_ref_fails_closed(self) -> None:
        output_ref, unknown = ref("a"), ref("f")
        reachability = self._reachability(
            (self._output(output_ref),),
            strict_by_ref={output_ref: (unknown,)},
        )

        with self.assertRaises(ReachableDependencyFrontierConsistencyError):
            _derive_frontiers(reachability)

    def test_preflight_consumes_decision017_once_and_preserves_nested_projection(self) -> None:
        output_ref, dep = ref("a"), ref("b")
        reachability = self._reachability(
            (self._output(output_ref, (self._dependency(dep),)),)
        )
        with patch(
            "axm_institution.packet_reachable_dependency_frontier."
            "preflight_packet_local_dependency_reachability",
            return_value=reachability,
        ) as resolver:
            result = preflight_reachable_dependency_frontier(object(), PACKET_REF)

        resolver.assert_called_once_with(unittest.mock.ANY, PACKET_REF)
        self.assertIs(result.reachability, reachability)
        self.assertEqual(self._triples(result.outputs[0]), ((output_ref, dep, False),))

    def test_named_frontier_leaves_fail_closed_or_preserve_named_transport(self) -> None:
        declaring, dep = ref("a"), ref("b")
        relation = ExactReachableDependencyFrontierRelation(declaring, dep, True)
        output = ExactPacketOutputDependencyFrontier(declaring, (relation,))

        with self.assertRaises(TypeError):
            json.dumps(relation)
        transported_relation = json.loads(json.dumps(relation._asdict()))
        self.assertEqual(
            transported_relation,
            {
                "declaring_output_ref": declaring,
                "dependency_ref": dep,
                "in_claim_base": True,
            },
        )
        with self.assertRaises(TypeError):
            json.dumps(output)
        physical = json.loads(memoryview(output).tobytes().decode("utf-8"))
        self.assertEqual(physical["output_ref"], declaring)
        self.assertEqual(
            physical["frontier_relations"],
            [
                {
                    "declaring_output_ref": declaring,
                    "dependency_ref": dep,
                    "in_claim_base": True,
                }
            ],
        )

    def test_projection_exposes_no_policy_chronology_or_lifecycle_authority(self) -> None:
        output_ref, dep = ref("a"), ref("b")
        reachability = self._reachability(
            (self._output(output_ref, (self._dependency(dep),)),)
        )
        with patch(
            "axm_institution.packet_reachable_dependency_frontier."
            "preflight_packet_local_dependency_reachability",
            return_value=reachability,
        ):
            result = preflight_reachable_dependency_frontier(object(), PACKET_REF)

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
        for target in (result, result.outputs[0], result.outputs[0].frontier_relations[0]):
            for name in forbidden:
                self.assertFalse(hasattr(target, name), name)


if __name__ == "__main__":
    unittest.main()
