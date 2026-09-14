from __future__ import annotations

import json
import unittest

from axm_institution.packet_same_packet_dependency_graph import (
    ExactPacketOutputNode,
    ExactSamePacketDependencyEdge,
    ExactStronglyConnectedComponent,
)


class SamePacketDependencyGraphTransportTests(unittest.TestCase):
    """Lane 02 transport regressions for Decision 016 named graph leaves."""

    def _assert_rejects_or_preserves_named_semantics(self, value, expected) -> None:
        try:
            encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError):
            return

        transported = json.loads(encoded)
        self.assertIsInstance(
            transported,
            dict,
            "Decision 016 graph leaf was accepted by stdlib JSON transport but lost named semantics",
        )
        self.assertEqual(transported, expected)

    def test_output_node_transport_rejects_or_preserves_named_semantics(self) -> None:
        node = ExactPacketOutputNode(
            output_ref="axmref:v1:artifact:" + ("a" * 64),
            category="created",
        )
        self._assert_rejects_or_preserves_named_semantics(
            node,
            {
                "output_ref": node.output_ref,
                "category": "created",
            },
        )

    def test_dependency_edge_transport_rejects_or_preserves_named_semantics(self) -> None:
        edge = ExactSamePacketDependencyEdge(
            required_output_ref="axmref:v1:artifact:" + ("a" * 64),
            dependent_output_ref="axmref:v1:artifact:" + ("b" * 64),
        )
        self._assert_rejects_or_preserves_named_semantics(
            edge,
            {
                "required_output_ref": edge.required_output_ref,
                "dependent_output_ref": edge.dependent_output_ref,
            },
        )

    def test_scc_transport_rejects_or_preserves_named_semantics(self) -> None:
        component = ExactStronglyConnectedComponent(
            member_refs=(
                "axmref:v1:artifact:" + ("a" * 64),
                "axmref:v1:artifact:" + ("b" * 64),
            ),
            has_cycle=True,
        )
        self._assert_rejects_or_preserves_named_semantics(
            component,
            {
                "member_refs": list(component.member_refs),
                "has_cycle": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
