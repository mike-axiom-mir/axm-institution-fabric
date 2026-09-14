from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from axm_institution.lifecycle import admit_occupancy, open_work_claim, submit_return_packet
from axm_institution.packet_same_packet_dependency_graph import (
    ExactSamePacketDependencyEdge,
    SamePacketDependencyGraphConsistencyError,
    _strongly_connected_components,
    _topological_witness,
    preflight_same_packet_dependency_graph,
)
from axm_institution.store import FilesystemObjectStore


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = json.loads(
    (ROOT / "fixtures/contracts/valid.json").read_text(encoding="utf-8")
)


class SamePacketDependencyGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.store = FilesystemObjectStore(Path(self.tempdir.name))

    def _fixture(self, schema_name: str):
        return copy.deepcopy(VALID_FIXTURES[schema_name])

    def _historical_artifact(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        version: str = "0.1",
    ):
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.1"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision": "historical:before-decision-016",
            "source_refs": [],
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = []
        artifact.pop("supersedes_ref", None)
        return artifact

    def _store_historical(
        self,
        *,
        artifact_id: str,
        content_ref: str,
        version: str = "0.1",
    ) -> str:
        return self.store.store(
            self._historical_artifact(
                artifact_id=artifact_id,
                content_ref=content_ref,
                version=version,
            ),
            "artifact.schema.json",
        ).reference

    def _store_base(self, lane_ref: str, artifact_refs) -> str:
        revision = self._fixture("state-revision.schema.json")
        revision["id"] = "revision.dependency.graph.base"
        revision["lane_refs"] = [lane_ref]
        revision["occupancy_refs"] = []
        revision["claim_refs"] = []
        revision["artifact_refs"] = list(artifact_refs)
        revision["evidence_refs"] = []
        revision["return_packet_refs"] = []
        revision["integration_receipt_refs"] = []
        revision["uncertainties"] = [
            "Decision 016 exposes packet-local topology without chronology or validity policy."
        ]
        return self.store.store(revision, "state-revision.schema.json").reference

    def _ground_context(self, *, extra_base_artifact_refs=()):
        lane = self._fixture("lane.schema.json")
        lane_ref = self.store.store(lane, "lane.schema.json").reference
        prior_ref = self._store_historical(
            artifact_id="artifact.modified",
            content_ref="artifact://decision016/prior",
        )
        base_ref = self._store_base(
            lane_ref,
            [prior_ref, *extra_base_artifact_refs],
        )

        occupancy = self._fixture("occupancy.schema.json")
        occupancy["id"] = "occupancy.dependency.graph"
        occupancy["base_state_revision_ref"] = base_ref
        occupancy["lane_id"] = lane["id"]
        occupancy["claim_ids"] = []
        occupancy_ref = admit_occupancy(self.store, occupancy).occupancy_ref

        claim = self._fixture("work-claim.schema.json")
        claim["id"] = "claim.dependency.graph"
        claim["base_state_revision_ref"] = base_ref
        claim["lane_id"] = lane["id"]
        claim["occupancy_ref"] = occupancy_ref
        claim["overlap_with_claim_ids"] = []
        claim_ref = open_work_claim(self.store, claim).claim_ref

        return {
            "lane": lane,
            "lane_ref": lane_ref,
            "prior_ref": prior_ref,
            "base_ref": base_ref,
            "occupancy_ref": occupancy_ref,
            "claim_ref": claim_ref,
        }

    def _store_output(
        self,
        context,
        *,
        artifact_id: str,
        content_ref: str,
        dependency_refs=(),
        version: str = "0.3",
        supersedes_ref: str | None = None,
        source_refs=(),
    ) -> str:
        artifact = self._fixture("artifact.schema.json")
        artifact["schema_version"] = "0.3"
        artifact["id"] = artifact_id
        artifact["type"] = "kernel_contracts"
        artifact["version"] = version
        artifact["content_ref"] = content_ref
        artifact["provenance"] = {
            "producer_lane_id": "lane-02",
            "base_state_revision_ref": context["base_ref"],
            "source_refs": list(source_refs),
        }
        artifact["evidence_refs"] = []
        artifact["dependency_refs"] = list(dependency_refs)
        if supersedes_ref is None:
            artifact.pop("supersedes_ref", None)
        else:
            artifact["supersedes_ref"] = supersedes_ref
        return self.store.store(artifact, "artifact.schema.json").reference

    def _store_evidence(self, *, evidence_id: str, subject_ref: str) -> str:
        evidence = self._fixture("evidence-record.schema.json")
        evidence["id"] = evidence_id
        evidence["subject_ref"] = subject_ref
        evidence["state"] = "automated_tested"
        evidence["claim"] = "Decision 016 graph fixture evidence."
        return self.store.store(evidence, "evidence-record.schema.json").reference

    def _submit_packet(
        self,
        context,
        *,
        created_refs=(),
        modified_result_ref: str | None = None,
        evidence_refs=(),
        packet_id: str,
    ) -> str:
        packet = self._fixture("return-packet.schema.json")
        packet["schema_version"] = "0.4"
        packet["id"] = packet_id
        packet["base_state_revision_ref"] = context["base_ref"]
        packet["lane_id"] = context["lane"]["id"]
        packet["claim_ref"] = context["claim_ref"]
        packet["artifacts_created"] = list(created_refs)
        packet["artifacts_modified"] = (
            []
            if modified_result_ref is None
            else [
                {
                    "prior_artifact_ref": context["prior_ref"],
                    "result_artifact_ref": modified_result_ref,
                }
            ]
        )
        packet["evidence_refs"] = list(evidence_refs)
        return submit_return_packet(self.store, packet).packet_ref

    def _evidence_for(self, refs, prefix: str):
        return [
            self._store_evidence(
                evidence_id=f"evidence.decision016.{prefix}.{index}",
                subject_ref=reference,
            )
            for index, reference in enumerate(refs)
        ]

    def test_created_dependency_forms_required_to_dependent_edge(self) -> None:
        context = self._ground_context()
        required_ref = self._store_output(
            context,
            artifact_id="artifact.graph.required",
            content_ref="artifact://decision016/required",
        )
        dependent_ref = self._store_output(
            context,
            artifact_id="artifact.graph.dependent",
            content_ref="artifact://decision016/dependent",
            dependency_refs=[required_ref],
        )
        evidence_refs = self._evidence_for(
            [required_ref, dependent_ref], "created-edge"
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[dependent_ref, required_ref],
            evidence_refs=list(reversed(evidence_refs)),
            packet_id="packet.decision016.created-edge",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)

        self.assertEqual(
            graph.edges,
            (
                ExactSamePacketDependencyEdge(
                    required_output_ref=required_ref,
                    dependent_output_ref=dependent_ref,
                ),
            ),
        )
        self.assertFalse(graph.has_cycle)
        self.assertIsNotNone(graph.topological_witness)
        witness = graph.topological_witness
        assert witness is not None
        self.assertLess(witness.index(required_ref), witness.index(dependent_ref))

    def test_modified_result_target_forms_edge_without_family_precedence(self) -> None:
        context = self._ground_context()
        modified_ref = self._store_output(
            context,
            artifact_id="artifact.graph.modified-required",
            content_ref="artifact://decision016/modified-required",
        )
        created_dependent_ref = self._store_output(
            context,
            artifact_id="artifact.graph.created-dependent",
            content_ref="artifact://decision016/created-dependent",
            dependency_refs=[modified_ref],
        )
        evidence_refs = self._evidence_for(
            [modified_ref, created_dependent_ref], "mixed-family"
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[created_dependent_ref],
            modified_result_ref=modified_ref,
            evidence_refs=evidence_refs,
            packet_id="packet.decision016.mixed-family",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        by_ref = {node.output_ref: node.category for node in graph.nodes}

        self.assertEqual(by_ref[modified_ref], "modified_result")
        self.assertEqual(by_ref[created_dependent_ref], "created")
        self.assertEqual(
            graph.edges,
            (
                ExactSamePacketDependencyEdge(
                    required_output_ref=modified_ref,
                    dependent_output_ref=created_dependent_ref,
                ),
            ),
        )
        witness = graph.topological_witness
        assert witness is not None
        self.assertLess(witness.index(modified_ref), witness.index(created_dependent_ref))

    def test_base_only_and_external_dependencies_create_no_packet_local_edges(self) -> None:
        base_dependency_ref = self._store_historical(
            artifact_id="artifact.graph.base-only",
            content_ref="artifact://decision016/base-only",
        )
        context = self._ground_context(
            extra_base_artifact_refs=[base_dependency_ref]
        )
        external_ref = self._store_historical(
            artifact_id="artifact.graph.external",
            content_ref="artifact://decision016/external",
        )
        output_ref = self._store_output(
            context,
            artifact_id="artifact.graph.consumer-nonlocal",
            content_ref="artifact://decision016/consumer-nonlocal",
            dependency_refs=[external_ref, base_dependency_ref],
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision016.nonlocal",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision016.nonlocal",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        facts = graph.dependency_context.created_outputs[0].dependencies
        by_ref = {fact.dependency.reference: fact for fact in facts}

        self.assertEqual(graph.edges, ())
        self.assertTrue(by_ref[base_dependency_ref].in_claim_base)
        self.assertFalse(by_ref[base_dependency_ref].in_packet_created)
        self.assertFalse(by_ref[external_ref].in_claim_base)
        self.assertFalse(by_ref[external_ref].in_packet_created)
        self.assertEqual(graph.topological_witness, (output_ref,))

    def test_same_logical_decoy_does_not_become_packet_edge(self) -> None:
        context = self._ground_context()
        packet_target_ref = self._store_output(
            context,
            artifact_id="artifact.graph.same-logical",
            content_ref="artifact://decision016/packet-target",
            version="0.3",
        )
        decoy_ref = self._store_output(
            context,
            artifact_id="artifact.graph.same-logical",
            content_ref="artifact://decision016/decoy",
            version="9.9",
            supersedes_ref=packet_target_ref,
        )
        consumer_ref = self._store_output(
            context,
            artifact_id="artifact.graph.decoy-consumer",
            content_ref="artifact://decision016/decoy-consumer",
            dependency_refs=[decoy_ref],
            supersedes_ref=packet_target_ref,
        )
        evidence_refs = self._evidence_for(
            [packet_target_ref, consumer_ref], "decoy"
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[packet_target_ref, consumer_ref],
            evidence_refs=evidence_refs,
            packet_id="packet.decision016.decoy",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        dependency_fact = next(
            output
            for output in graph.dependency_context.created_outputs
            if output.artifact.reference == consumer_ref
        ).dependencies[0]

        self.assertEqual(dependency_fact.dependency.reference, decoy_ref)
        self.assertFalse(dependency_fact.in_packet_created)
        self.assertEqual(graph.edges, ())

    def test_packet_output_array_order_cannot_choose_graph_or_witness(self) -> None:
        context = self._ground_context()
        first_ref = self._store_output(
            context,
            artifact_id="artifact.graph.order-first",
            content_ref="artifact://decision016/order-first",
        )
        second_ref = self._store_output(
            context,
            artifact_id="artifact.graph.order-second",
            content_ref="artifact://decision016/order-second",
        )
        evidence_refs = self._evidence_for([first_ref, second_ref], "order")

        packet_a = self._submit_packet(
            context,
            created_refs=[first_ref, second_ref],
            evidence_refs=evidence_refs,
            packet_id="packet.decision016.order-a",
        )
        packet_b = self._submit_packet(
            context,
            created_refs=[second_ref, first_ref],
            evidence_refs=list(reversed(evidence_refs)),
            packet_id="packet.decision016.order-b",
        )

        graph_a = preflight_same_packet_dependency_graph(self.store, packet_a)
        graph_b = preflight_same_packet_dependency_graph(self.store, packet_b)

        self.assertEqual(graph_a.nodes, graph_b.nodes)
        self.assertEqual(graph_a.edges, graph_b.edges)
        self.assertEqual(
            graph_a.strongly_connected_components,
            graph_b.strongly_connected_components,
        )
        self.assertEqual(graph_a.topological_witness, graph_b.topological_witness)
        self.assertEqual(graph_a.topological_witness, tuple(sorted([first_ref, second_ref])))

    def test_acyclic_witness_uses_lexical_tiebreaker_and_respects_every_edge(self) -> None:
        context = self._ground_context()
        root_ref = self._store_output(
            context,
            artifact_id="artifact.graph.root",
            content_ref="artifact://decision016/root",
        )
        left_ref = self._store_output(
            context,
            artifact_id="artifact.graph.left",
            content_ref="artifact://decision016/left",
            dependency_refs=[root_ref],
        )
        right_ref = self._store_output(
            context,
            artifact_id="artifact.graph.right",
            content_ref="artifact://decision016/right",
            dependency_refs=[root_ref],
        )
        refs = [right_ref, root_ref, left_ref]
        packet_ref = self._submit_packet(
            context,
            created_refs=refs,
            evidence_refs=self._evidence_for(refs, "witness"),
            packet_id="packet.decision016.witness",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        witness = graph.topological_witness
        assert witness is not None
        positions = {reference: index for index, reference in enumerate(witness)}

        for edge in graph.edges:
            self.assertLess(
                positions[edge.required_output_ref],
                positions[edge.dependent_output_ref],
            )
        self.assertEqual(witness[0], root_ref)
        self.assertEqual(witness[1:], tuple(sorted([left_ref, right_ref])))

    def test_graph_exposes_no_validity_chronology_or_acceptance_authority(self) -> None:
        context = self._ground_context()
        output_ref = self._store_output(
            context,
            artifact_id="artifact.graph.boundary",
            content_ref="artifact://decision016/boundary",
        )
        evidence_ref = self._store_evidence(
            evidence_id="evidence.decision016.boundary",
            subject_ref=output_ref,
        )
        packet_ref = self._submit_packet(
            context,
            created_refs=[output_ref],
            evidence_refs=[evidence_ref],
            packet_id="packet.decision016.boundary",
        )

        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)

        self.assertEqual(graph.dependency_context.packet_ref, packet_ref)
        for forbidden in (
            "dependencies_valid",
            "dependencies_closed",
            "accepted",
            "rejected",
            "complete",
            "closed",
            "satisfied",
            "execution_order",
            "execution_chronology",
            "required_production_order",
            "integration_ready",
        ):
            self.assertFalse(hasattr(graph, forbidden))

    def test_self_edge_is_preserved_as_cycle_fact_by_deterministic_graph_kernel(self) -> None:
        node = "axmref:v1:artifact:" + ("a" * 64)
        edge = ExactSamePacketDependencyEdge(
            required_output_ref=node,
            dependent_output_ref=node,
        )

        components = _strongly_connected_components((node,), (edge,))

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0].member_refs, (node,))
        self.assertTrue(components[0].has_cycle)
        with self.assertRaises(SamePacketDependencyGraphConsistencyError):
            _topological_witness((node,), (edge,))

    def test_two_node_cycle_is_one_deterministic_scc_and_has_no_topological_witness(self) -> None:
        node_a = "axmref:v1:artifact:" + ("a" * 64)
        node_b = "axmref:v1:artifact:" + ("b" * 64)
        edges = (
            ExactSamePacketDependencyEdge(node_b, node_a),
            ExactSamePacketDependencyEdge(node_a, node_b),
        )

        components = _strongly_connected_components((node_b, node_a), edges)

        self.assertEqual(len(components), 1)
        self.assertEqual(components[0].member_refs, tuple(sorted([node_a, node_b])))
        self.assertTrue(components[0].has_cycle)
        with self.assertRaises(SamePacketDependencyGraphConsistencyError):
            _topological_witness((node_a, node_b), edges)

    def test_scc_presentation_is_deterministic_under_node_and_edge_order(self) -> None:
        node_a = "axmref:v1:artifact:" + ("a" * 64)
        node_b = "axmref:v1:artifact:" + ("b" * 64)
        node_c = "axmref:v1:artifact:" + ("c" * 64)
        edges_a = (
            ExactSamePacketDependencyEdge(node_a, node_b),
            ExactSamePacketDependencyEdge(node_b, node_a),
            ExactSamePacketDependencyEdge(node_b, node_c),
        )
        edges_b = tuple(reversed(edges_a))

        components_a = _strongly_connected_components(
            (node_c, node_a, node_b), edges_a
        )
        components_b = _strongly_connected_components(
            (node_b, node_c, node_a), edges_b
        )

        self.assertEqual(components_a, components_b)
        self.assertEqual(
            components_a,
            (
                type(components_a[0])((node_a, node_b), True),
                type(components_a[0])((node_c,), False),
            ),
        )


if __name__ == "__main__":
    unittest.main()
