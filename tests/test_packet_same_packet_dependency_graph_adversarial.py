from __future__ import annotations

import json
import unittest

from axm_institution.packet_same_packet_dependency_graph import (
    ExactSamePacketDependencyEdge,
    SamePacketDependencyGraphConsistencyError,
    _strongly_connected_components,
    _topological_witness,
    preflight_same_packet_dependency_graph,
)
import test_packet_same_packet_dependency_graph as base_tests


class SamePacketDependencyGraphAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-049 continuity attacks for Decision 016 only."""

    def setUp(self) -> None:
        self.fixture = base_tests.SamePacketDependencyGraphTests(
            methodName="test_created_dependency_forms_required_to_dependent_edge"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.store = self.fixture.store

    def _two_output_graph(self, *, prefix: str):
        context = self.fixture._ground_context()
        required_ref = self.fixture._store_output(
            context,
            artifact_id=f"artifact.adv049.{prefix}.required",
            content_ref=f"artifact://adv049/{prefix}/required",
        )
        dependent_ref = self.fixture._store_output(
            context,
            artifact_id=f"artifact.adv049.{prefix}.dependent",
            content_ref=f"artifact://adv049/{prefix}/dependent",
            dependency_refs=[required_ref],
        )
        evidence_refs = self.fixture._evidence_for(
            [required_ref, dependent_ref], f"adv049-{prefix}"
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[dependent_ref, required_ref],
            evidence_refs=list(reversed(evidence_refs)),
            packet_id=f"packet.adv049.{prefix}",
        )
        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        return context, required_ref, dependent_ref, packet_ref, graph

    def test_adv049_a_later_same_logical_superseding_output_cannot_rebind_earlier_graph(self) -> None:
        context, required_ref, dependent_ref, packet_ref, first = self._two_output_graph(
            prefix="later-decoy"
        )
        decoy_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.later-decoy.required",
            content_ref="artifact://adv049/later-decoy/replacement",
            version="999.0",
            supersedes_ref=required_ref,
        )
        self.assertNotEqual(decoy_ref, required_ref)

        second = preflight_same_packet_dependency_graph(self.store, packet_ref)

        self.assertEqual(first.nodes, second.nodes)
        self.assertEqual(first.edges, second.edges)
        self.assertEqual(first.topological_witness, second.topological_witness)
        self.assertEqual(
            second.edges,
            (
                ExactSamePacketDependencyEdge(
                    required_output_ref=required_ref,
                    dependent_output_ref=dependent_ref,
                ),
            ),
        )
        self.assertNotIn(decoy_ref, {node.output_ref for node in second.nodes})

    def test_adv049_b_external_dependency_cannot_be_promoted_by_source_metadata(self) -> None:
        context = self.fixture._ground_context()
        packet_target_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.metadata.packet-target",
            content_ref="artifact://adv049/metadata/packet-target",
        )
        external_ref = self.fixture._store_historical(
            artifact_id="artifact.adv049.metadata.external",
            content_ref="artifact://adv049/metadata/external",
        )
        consumer_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.metadata.consumer",
            content_ref="artifact://adv049/metadata/consumer",
            dependency_refs=[external_ref],
            source_refs=[packet_target_ref, external_ref],
        )
        refs = [packet_target_ref, consumer_ref]
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=refs,
            evidence_refs=self.fixture._evidence_for(refs, "adv049-metadata"),
            packet_id="packet.adv049.metadata",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        consumer = next(
            output
            for output in graph.dependency_context.created_outputs
            if output.artifact.reference == consumer_ref
        )
        fact = consumer.dependencies[0]

        self.assertEqual(fact.dependency.reference, external_ref)
        self.assertFalse(fact.in_packet_created)
        self.assertFalse(fact.in_packet_modified_result)
        self.assertEqual(graph.edges, ())

    def test_adv049_c_created_dependency_of_modified_result_has_no_family_precedence(self) -> None:
        context = self.fixture._ground_context()
        created_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.family.created-required",
            content_ref="artifact://adv049/family/created-required",
        )
        modified_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.family.modified-dependent",
            content_ref="artifact://adv049/family/modified-dependent",
            dependency_refs=[created_ref],
        )
        evidence_refs = self.fixture._evidence_for(
            [created_ref, modified_ref], "adv049-family"
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[created_ref],
            modified_result_ref=modified_ref,
            evidence_refs=list(reversed(evidence_refs)),
            packet_id="packet.adv049.family",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        categories = {node.output_ref: node.category for node in graph.nodes}

        self.assertEqual(categories[created_ref], "created")
        self.assertEqual(categories[modified_ref], "modified_result")
        self.assertEqual(
            graph.edges,
            (
                ExactSamePacketDependencyEdge(
                    required_output_ref=created_ref,
                    dependent_output_ref=modified_ref,
                ),
            ),
        )
        witness = graph.topological_witness
        assert witness is not None
        self.assertLess(witness.index(created_ref), witness.index(modified_ref))

    def test_adv049_d_later_parallel_packet_cannot_rebind_first_packet_external_target(self) -> None:
        context = self.fixture._ground_context()
        later_output_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.parallel.later-output",
            content_ref="artifact://adv049/parallel/later-output",
        )
        first_consumer_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.parallel.first-consumer",
            content_ref="artifact://adv049/parallel/first-consumer",
            dependency_refs=[later_output_ref],
        )
        first_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv049.parallel.first-consumer",
            subject_ref=first_consumer_ref,
        )
        first_packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[first_consumer_ref],
            evidence_refs=[first_evidence_ref],
            packet_id="packet.adv049.parallel.first",
        )

        later_evidence_ref = self.fixture._store_evidence(
            evidence_id="evidence.adv049.parallel.later-output",
            subject_ref=later_output_ref,
        )
        later_packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[later_output_ref],
            evidence_refs=[later_evidence_ref],
            packet_id="packet.adv049.parallel.later",
        )

        first = preflight_same_packet_dependency_graph(self.store, first_packet_ref)
        later = preflight_same_packet_dependency_graph(self.store, later_packet_ref)

        self.assertEqual(first.packet_ref, first_packet_ref)
        self.assertEqual(later.packet_ref, later_packet_ref)
        self.assertEqual(first.edges, ())
        first_fact = first.dependency_context.created_outputs[0].dependencies[0]
        self.assertEqual(first_fact.dependency.reference, later_output_ref)
        self.assertFalse(first_fact.in_packet_created)
        self.assertEqual({node.output_ref for node in later.nodes}, {later_output_ref})

    def test_adv049_e_self_edge_remains_cycle_and_cannot_receive_fake_witness(self) -> None:
        node = "artifact:adv049-self"
        edges = (
            ExactSamePacketDependencyEdge(
                required_output_ref=node,
                dependent_output_ref=node,
            ),
        )

        components = _strongly_connected_components((node,), edges)

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0].member_refs, (node,))
        self.assertTrue(components[0].has_cycle)
        with self.assertRaises(SamePacketDependencyGraphConsistencyError):
            _topological_witness((node,), edges)

    def test_adv049_f_two_node_cycle_remains_one_cycle_and_cannot_receive_fake_witness(self) -> None:
        first = "artifact:adv049-cycle-a"
        second = "artifact:adv049-cycle-b"
        edges = (
            ExactSamePacketDependencyEdge(first, second),
            ExactSamePacketDependencyEdge(second, first),
        )

        components = _strongly_connected_components((second, first), tuple(reversed(edges)))

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0].member_refs, tuple(sorted((first, second))))
        self.assertTrue(components[0].has_cycle)
        with self.assertRaises(SamePacketDependencyGraphConsistencyError):
            _topological_witness((first, second), edges)

    def test_adv049_g_acyclic_witness_respects_edges_with_independent_ready_node(self) -> None:
        context = self.fixture._ground_context()
        required_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.witness.required",
            content_ref="artifact://adv049/witness/required",
        )
        dependent_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.witness.dependent",
            content_ref="artifact://adv049/witness/dependent",
            dependency_refs=[required_ref],
        )
        independent_ref = self.fixture._store_output(
            context,
            artifact_id="artifact.adv049.witness.independent",
            content_ref="artifact://adv049/witness/independent",
        )
        refs = [dependent_ref, independent_ref, required_ref]
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=refs,
            evidence_refs=list(reversed(self.fixture._evidence_for(refs, "adv049-witness"))),
            packet_id="packet.adv049.witness",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        witness = graph.topological_witness
        assert witness is not None
        positions = {reference: index for index, reference in enumerate(witness)}

        self.assertEqual(set(witness), set(refs))
        for edge in graph.edges:
            self.assertLess(
                positions[edge.required_output_ref],
                positions[edge.dependent_output_ref],
            )

    def test_adv049_h_detached_materialization_cannot_rewrite_authoritative_graph(self) -> None:
        _, required_ref, dependent_ref, _, graph = self._two_output_graph(
            prefix="materialization"
        )
        outer_copy = graph._asdict()
        node_copy = graph.nodes[0]._asdict()
        edge_copy = graph.edges[0]._asdict()
        component_copy = graph.strongly_connected_components[0]._asdict()

        outer_copy["has_cycle"] = True
        outer_copy["topological_witness"] = ()
        node_copy["category"] = "decoy"
        edge_copy["required_output_ref"] = dependent_ref
        edge_copy["dependent_output_ref"] = required_ref
        component_copy["has_cycle"] = True

        self.assertFalse(graph.has_cycle)
        self.assertIsNotNone(graph.topological_witness)
        self.assertNotEqual(graph.nodes[0].category, "decoy")
        self.assertEqual(
            graph.edges[0],
            ExactSamePacketDependencyEdge(required_ref, dependent_ref),
        )
        self.assertTrue(all(not component.has_cycle for component in graph.strongly_connected_components))

    def test_adv049_i_graph_facts_expose_no_validity_chronology_closure_or_acceptance_authority(self) -> None:
        _, _, _, _, graph = self._two_output_graph(prefix="authority")
        targets = [
            graph,
            *graph.nodes,
            *graph.edges,
            *graph.strongly_connected_components,
        ]
        forbidden = (
            "dependencies_valid",
            "dependencies_closed",
            "accepted",
            "rejected",
            "complete",
            "closed",
            "satisfied",
            "execution_order",
            "production_order",
            "integration_ready",
            "epoch_complete",
            "replay_valid",
        )

        for target in targets:
            for field in forbidden:
                self.assertFalse(hasattr(target, field), (type(target).__name__, field))

    def test_adv049_j_exact_edge_transport_must_fail_closed_instead_of_becoming_positional_array(self) -> None:
        _, _, _, _, graph = self._two_output_graph(prefix="transport")
        edge = graph.edges[0]

        # ADV-037 already established that unsupported ordinary JSON transport must fail
        # closed rather than silently change an authoritative record's representation.
        # Decision 016's graph leaves must preserve that proof-to-use boundary too.
        with self.assertRaises(TypeError):
            json.dumps(edge)


if __name__ == "__main__":
    unittest.main()
