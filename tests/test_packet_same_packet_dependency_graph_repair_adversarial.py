from __future__ import annotations

import copy
import json
import unittest

from axm_institution.identity import parse_json_strict
from axm_institution.packet_same_packet_dependency_graph import (
    ExactSamePacketDependencyEdge,
    preflight_same_packet_dependency_graph,
)
import test_packet_same_packet_dependency_graph as base_tests


class SamePacketDependencyGraphRepairAdversarialTests(unittest.TestCase):
    """Lane 03 ADV-050 attacks on the Decision 016 transport repair only."""

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
            artifact_id=f"artifact.adv050.{prefix}.required",
            content_ref=f"artifact://adv050/{prefix}/required",
        )
        dependent_ref = self.fixture._store_output(
            context,
            artifact_id=f"artifact.adv050.{prefix}.dependent",
            content_ref=f"artifact://adv050/{prefix}/dependent",
            dependency_refs=[required_ref],
        )
        evidence_refs = self.fixture._evidence_for(
            [required_ref, dependent_ref], f"adv050-{prefix}"
        )
        packet_ref = self.fixture._submit_packet(
            context,
            created_refs=[dependent_ref, required_ref],
            evidence_refs=list(reversed(evidence_refs)),
            packet_id=f"packet.adv050.{prefix}",
        )
        graph = preflight_same_packet_dependency_graph(self.store, packet_ref)
        return required_ref, dependent_ref, graph

    def test_adv050_a_physical_edge_payload_preserves_named_direction(self) -> None:
        required_ref, dependent_ref, graph = self._two_output_graph(prefix="payload")
        edge = graph.edges[0]

        transported = parse_json_strict(memoryview(edge).tobytes().decode("utf-8"))

        self.assertEqual(
            transported,
            {
                "dependent_output_ref": dependent_ref,
                "required_output_ref": required_ref,
            },
        )
        self.assertEqual(edge.required_output_ref, required_ref)
        self.assertEqual(edge.dependent_output_ref, dependent_ref)

    def test_adv050_b_nested_json_transport_rejects_or_preserves_named_leaf_semantics(self) -> None:
        required_ref, dependent_ref, graph = self._two_output_graph(prefix="nested-json")
        payload = {
            "node": graph.nodes[0],
            "edge": graph.edges[0],
            "component": graph.strongly_connected_components[0],
        }

        try:
            encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return

        transported = json.loads(encoded)
        self.assertIsInstance(transported, dict)
        self.assertIsInstance(transported["node"], dict)
        self.assertIsInstance(transported["edge"], dict)
        self.assertIsInstance(transported["component"], dict)
        self.assertEqual(
            transported["edge"],
            {
                "required_output_ref": required_ref,
                "dependent_output_ref": dependent_ref,
            },
        )

    def test_adv050_c_asdict_json_transport_is_named_and_detached(self) -> None:
        required_ref, dependent_ref, graph = self._two_output_graph(prefix="asdict")
        edge = graph.edges[0]
        materialized = edge._asdict()

        transported = json.loads(
            json.dumps(materialized, ensure_ascii=False, separators=(",", ":"))
        )
        self.assertEqual(
            transported,
            {
                "required_output_ref": required_ref,
                "dependent_output_ref": dependent_ref,
            },
        )

        transported["required_output_ref"] = dependent_ref
        transported["dependent_output_ref"] = required_ref
        self.assertEqual(
            edge,
            ExactSamePacketDependencyEdge(
                required_output_ref=required_ref,
                dependent_output_ref=dependent_ref,
            ),
        )

    def test_adv050_d_copy_paths_reject_or_preserve_exact_named_leaf(self) -> None:
        _, _, graph = self._two_output_graph(prefix="copy")

        for leaf in (
            graph.nodes[0],
            graph.edges[0],
            graph.strongly_connected_components[0],
        ):
            for copier in (copy.copy, copy.deepcopy):
                try:
                    copied = copier(leaf)
                except (TypeError, ValueError):
                    continue
                self.assertIs(type(copied), type(leaf))
                self.assertEqual(copied._asdict(), leaf._asdict())
                self.assertEqual(bytes(copied), bytes(leaf))

    def test_adv050_e_full_graph_transport_rejects_or_preserves_named_top_level_semantics(self) -> None:
        required_ref, dependent_ref, graph = self._two_output_graph(prefix="full-graph")

        try:
            encoded = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return

        transported = json.loads(encoded)
        self.assertIsInstance(
            transported,
            dict,
            "Decision 016 aggregate transport was accepted but lost named top-level semantics",
        )
        self.assertEqual(transported["packet_ref"], graph.packet_ref)
        self.assertEqual(transported["claim_ref"], graph.claim_ref)
        self.assertIsInstance(transported["edges"], list)
        self.assertEqual(
            transported["edges"],
            [
                {
                    "required_output_ref": required_ref,
                    "dependent_output_ref": dependent_ref,
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
