from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch

from axm_institution.identity import parse_json_strict
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


class PacketReachableDependencyFrontierAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-052 attacks on Decision 018 frontier facts only."""

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
        packet_ref=PACKET_REF,
        topological_witness=None,
    ) -> ResolvedPacketLocalDependencyReachability:
        strict_by_ref = strict_by_ref or {}
        direct_by_ref = direct_by_ref or {}
        created = tuple(output for output in outputs if output.category == "created")
        modified = tuple(output for output in outputs if output.category == "modified_result")
        dependency_context = ResolvedPacketDependencyContextMembership(
            packet_ref=packet_ref,
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
        witness = (
            tuple(sorted(output_refs))
            if topological_witness is None
            else tuple(topological_witness)
        )
        graph = ResolvedPacketSamePacketDependencyGraph(
            packet_ref=packet_ref,
            claim_ref=CLAIM_REF,
            claim_base_ref=BASE_REF,
            occupancy_ref=OCCUPANCY_REF,
            lane_ref=LANE_REF,
            dependency_context=dependency_context,
            nodes=tuple(
                ExactPacketOutputNode(
                    output_ref=output.artifact.reference,
                    category=output.category,
                )
                for output in sorted(outputs, key=lambda item: item.artifact.reference)
            ),
            edges=(),
            strongly_connected_components=tuple(
                ExactStronglyConnectedComponent((reference,), False)
                for reference in sorted(output_refs)
            ),
            self_edge_refs=(),
            has_cycle=False,
            topological_witness=witness,
        )
        order = reachability_order or output_refs
        return ResolvedPacketLocalDependencyReachability(
            packet_ref=packet_ref,
            claim_ref=CLAIM_REF,
            claim_base_ref=BASE_REF,
            occupancy_ref=OCCUPANCY_REF,
            lane_ref=LANE_REF,
            graph=graph,
            outputs=tuple(
                ExactPacketOutputReachability(
                    output_ref=reference,
                    direct_prerequisite_refs=tuple(sorted(direct_by_ref.get(reference, ()))),
                    strict_transitive_prerequisite_refs=tuple(
                        sorted(strict_by_ref.get(reference, ()))
                    ),
                )
                for reference in order
            ),
        )

    def _by_ref(self, outputs):
        return {output.output_ref: output for output in outputs}

    def _triples(self, output):
        return tuple(
            (
                relation.declaring_output_ref,
                relation.dependency_ref,
                relation.in_claim_base,
            )
            for relation in output.frontier_relations
        )

    def test_adv052_a_reverse_dependent_traversal_cannot_pull_downstream_frontier(self) -> None:
        root, middle, final = ref("a"), ref("b"), ref("c")
        middle_dep, final_dep = ref("d"), ref("e")
        outputs = (
            self._output(root),
            self._output(
                middle,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(middle_dep, in_claim_base=True),
                ),
            ),
            self._output(
                final,
                (
                    self._dependency(middle, in_packet_created=True),
                    self._dependency(final_dep),
                ),
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(
                    outputs,
                    strict_by_ref={middle: (root,), final: (root, middle)},
                )
            )
        )
        self.assertEqual(self._triples(result[root]), ())
        self.assertEqual(self._triples(result[middle]), ((middle, middle_dep, True),))
        self.assertEqual(
            self._triples(result[final]),
            tuple(sorted(((middle, middle_dep, True), (final, final_dep, False)))),
        )

    def test_adv052_b_multi_hop_scope_keeps_every_reachable_declarer(self) -> None:
        root, middle, final = ref("a"), ref("b"), ref("c")
        root_dep, middle_dep, final_dep = ref("d"), ref("e"), ref("f")
        outputs = (
            self._output(root, (self._dependency(root_dep, in_claim_base=True),)),
            self._output(
                middle,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(middle_dep),
                ),
            ),
            self._output(
                final,
                (
                    self._dependency(middle, in_packet_created=True),
                    self._dependency(final_dep, in_claim_base=True),
                ),
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(
                    outputs,
                    strict_by_ref={middle: (root,), final: (root, middle)},
                )
            )
        )
        self.assertEqual(
            self._triples(result[final]),
            tuple(
                sorted(
                    (
                        (root, root_dep, True),
                        (middle, middle_dep, False),
                        (final, final_dep, True),
                    )
                )
            ),
        )

    def test_adv052_c_sibling_and_unrelated_branch_frontiers_do_not_leak(self) -> None:
        root, left, sibling, final = ref("a"), ref("b"), ref("c"), ref("d")
        root_dep, left_dep, sibling_dep = ref("e"), ref("f"), ref("0")
        outputs = (
            self._output(root, (self._dependency(root_dep),)),
            self._output(
                left,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(left_dep, in_claim_base=True),
                ),
            ),
            self._output(
                sibling,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(sibling_dep),
                ),
            ),
            self._output(final, (self._dependency(left, in_packet_created=True),)),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(
                    outputs,
                    strict_by_ref={
                        left: (root,),
                        sibling: (root,),
                        final: (root, left),
                    },
                )
            )
        )
        final_refs = tuple(item[1] for item in self._triples(result[final]))
        self.assertIn(root_dep, final_refs)
        self.assertIn(left_dep, final_refs)
        self.assertNotIn(sibling_dep, final_refs)

    def test_adv052_d_same_packet_targets_stay_outside_frontier_without_family_precedence(self) -> None:
        created, modified = ref("a"), ref("b")
        consumer_created, consumer_modified = ref("c"), ref("d")
        outputs = (
            self._output(created, category="created"),
            self._output(modified, category="modified_result"),
            self._output(
                consumer_created,
                (self._dependency(modified, in_packet_modified_result=True),),
                category="created",
            ),
            self._output(
                consumer_modified,
                (self._dependency(created, in_packet_created=True),),
                category="modified_result",
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(
                    outputs,
                    strict_by_ref={
                        consumer_created: (modified,),
                        consumer_modified: (created,),
                    },
                )
            )
        )
        self.assertEqual(result[consumer_created].frontier_relations, ())
        self.assertEqual(result[consumer_modified].frontier_relations, ())

    def test_adv052_e_shared_target_keeps_each_declaring_output_identity(self) -> None:
        root, middle, final, shared = ref("a"), ref("b"), ref("c"), ref("d")
        outputs = (
            self._output(root, (self._dependency(shared, in_claim_base=True),)),
            self._output(
                middle,
                (
                    self._dependency(root, in_packet_created=True),
                    self._dependency(shared, in_claim_base=True),
                ),
            ),
            self._output(
                final,
                (
                    self._dependency(middle, in_packet_created=True),
                    self._dependency(shared, in_claim_base=True),
                ),
            ),
        )
        result = self._by_ref(
            _derive_frontiers(
                self._reachability(
                    outputs,
                    strict_by_ref={middle: (root,), final: (root, middle)},
                )
            )
        )
        self.assertEqual(
            self._triples(result[final]),
            ((root, shared, True), (middle, shared, True), (final, shared, True)),
        )

    def test_adv052_f_claim_base_membership_is_fact_not_precedence_or_validity(self) -> None:
        output, base_dep, outside_dep = ref("a"), ref("b"), ref("c")
        result = _derive_frontiers(
            self._reachability(
                (
                    self._output(
                        output,
                        (
                            self._dependency(outside_dep),
                            self._dependency(base_dep, in_claim_base=True),
                        ),
                    ),
                )
            )
        )[0]
        self.assertEqual(
            self._triples(result),
            ((output, base_dep, True), (output, outside_dep, False)),
        )
        forbidden = (
            "valid",
            "invalid",
            "allowed",
            "satisfied",
            "accepted",
            "rejected",
            "preferred",
            "priority",
        )
        for relation in result.frontier_relations:
            for name in forbidden:
                self.assertFalse(hasattr(relation, name), name)

    def test_adv052_g_same_logical_high_version_superseding_decoy_gets_no_substitution_authority(self) -> None:
        output, exact_dep, decoy = ref("a"), ref("b"), ref("f")
        dependency_value = {
            "id": "shared-logical-artifact",
            "version": "999999",
            "supersedes_ref": exact_dep,
            "source_refs": [decoy],
            "recency_hint": "newest",
        }
        result = _derive_frontiers(
            self._reachability(
                (
                    self._output(
                        output,
                        (
                            self._dependency(
                                exact_dep,
                                in_claim_base=True,
                                value=dependency_value,
                            ),
                        ),
                    ),
                )
            )
        )[0]
        self.assertEqual(result.frontier_relations[0].dependency_ref, exact_dep)
        self.assertNotEqual(result.frontier_relations[0].dependency_ref, decoy)

    def test_adv052_h_array_lexical_and_topological_witness_order_cannot_choose_frontier(self) -> None:
        required, final, dep_low, dep_high = ref("f"), ref("0"), ref("1"), ref("e")
        required_one = self._output(
            required,
            (
                self._dependency(dep_high),
                self._dependency(dep_low, in_claim_base=True),
            ),
        )
        required_two = self._output(required, tuple(reversed(required_one.dependencies)))
        final_output = self._output(
            final,
            (self._dependency(required, in_packet_created=True),),
        )
        first = self._reachability(
            (required_one, final_output),
            strict_by_ref={final: (required,)},
            reachability_order=(final, required),
            topological_witness=(final, required),
        )
        second = self._reachability(
            (final_output, required_two),
            strict_by_ref={final: (required,)},
            reachability_order=(required, final),
            topological_witness=(required, final),
        )
        self.assertEqual(_derive_frontiers(first), _derive_frontiers(second))

    def test_adv052_i_later_parallel_packet_projection_cannot_rebind_first_frontier(self) -> None:
        first_output, first_dep = ref("a"), ref("b")
        second_output, second_dep = ref("c"), ref("d")
        first_reachability = self._reachability(
            (self._output(first_output, (self._dependency(first_dep),)),),
            packet_ref="axmref:v1:return-packet:" + ("6" * 64),
        )
        second_reachability = self._reachability(
            (self._output(second_output, (self._dependency(second_dep),)),),
            packet_ref="axmref:v1:return-packet:" + ("7" * 64),
        )
        with patch(
            "axm_institution.packet_reachable_dependency_frontier."
            "preflight_packet_local_dependency_reachability",
            side_effect=(first_reachability, second_reachability),
        ):
            first = preflight_reachable_dependency_frontier(
                object(), first_reachability.packet_ref
            )
            second = preflight_reachable_dependency_frontier(
                object(), second_reachability.packet_ref
            )
        self.assertEqual(first.packet_ref, first_reachability.packet_ref)
        self.assertEqual(second.packet_ref, second_reachability.packet_ref)
        self.assertEqual(self._triples(first.outputs[0]), ((first_output, first_dep, False),))
        self.assertEqual(self._triples(second.outputs[0]), ((second_output, second_dep, False),))
        self.assertNotEqual(first.outputs[0], second.outputs[0])

    def test_adv052_j_named_relation_materialization_copy_and_transport_preserve_meaning(self) -> None:
        declaring, dependency, decoy = ref("a"), ref("b"), ref("c")
        relation = ExactReachableDependencyFrontierRelation(declaring, dependency, True)
        output = ExactPacketOutputDependencyFrontier(declaring, (relation,))
        physical = parse_json_strict(memoryview(relation).tobytes().decode("utf-8"))
        self.assertEqual(
            physical,
            {
                "declaring_output_ref": declaring,
                "dependency_ref": dependency,
                "in_claim_base": True,
            },
        )
        transported = json.loads(json.dumps(relation._asdict()))
        transported["dependency_ref"] = decoy
        transported["in_claim_base"] = False
        self.assertEqual(relation.dependency_ref, dependency)
        self.assertTrue(relation.in_claim_base)
        for copier in (copy.copy, copy.deepcopy):
            try:
                copied = copier(relation)
            except (TypeError, ValueError):
                continue
            self.assertIs(type(copied), type(relation))
            self.assertEqual(bytes(copied), bytes(relation))
            self.assertEqual(copied._asdict(), relation._asdict())
        with self.assertRaises(TypeError):
            json.dumps(relation)
        with self.assertRaises(TypeError):
            json.dumps(output)

    def test_adv052_k_projection_exposes_no_dependency_policy_or_lifecycle_authority(self) -> None:
        output, dep = ref("a"), ref("b")
        reachability = self._reachability(
            (self._output(output, (self._dependency(dep),)),)
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
        targets = (result, result.outputs[0], result.outputs[0].frontier_relations[0])
        for target in targets:
            for name in forbidden:
                self.assertFalse(hasattr(target, name), name)
        try:
            encoded = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return
        transported = json.loads(encoded)
        self.assertIsInstance(
            transported,
            dict,
            "Decision 018 aggregate transport was accepted but lost named top-level semantics",
        )
        self.assertEqual(transported["packet_ref"], PACKET_REF)
        self.assertIn("outputs", transported)

    def test_adv052_l_duplicate_exact_output_across_families_fails_closed(self) -> None:
        duplicate = ref("a")
        reachability = self._reachability(
            (
                self._output(duplicate, category="created"),
                self._output(duplicate, category="modified_result"),
            ),
            reachability_order=(duplicate,),
        )
        with self.assertRaises(ReachableDependencyFrontierConsistencyError):
            _derive_frontiers(reachability)


if __name__ == "__main__":
    unittest.main()
