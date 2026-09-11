from typing import Dict, List
import networkx as nx
from .schema import EvidenceNode, ArtifactType


class CivilEvidenceGraph:
    """Manages multi-modal relational links across BOQ, drawings, measurement sheets, and site records."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node: EvidenceNode):
        self.graph.add_node(
            node.node_id,
            type=node.artifact_type.value,
            title=node.title,
            date=node.date_created.isoformat(),
            reference=node.reference_path,
            metadata=node.metadata,
        )

    def link_artifacts(self, source_id: str, target_id: str, relation: str):
        """Creates an edge such as: MEASUREMENT_ENTRY -> SUPPORTS -> BOQ_ITEM"""
        self.graph.add_edge(source_id, target_id, relation=relation)

    def trace_audit_trail(self, boq_item_id: str) -> List[Dict]:
        """Traces all evidence nodes backing a given BOQ item for certification/audit."""
        if boq_item_id not in self.graph:
            return []
        
        predecessors = list(self.graph.predecessors(boq_item_id))
        audit_trail = []
        for pred_id in predecessors:
            node_data = self.graph.nodes[pred_id]
            edge_data = self.graph.get_edge_data(pred_id, boq_item_id)
            audit_trail.append({
                "evidence_id": pred_id,
                "type": node_data.get("type"),
                "title": node_data.get("title"),
                "relation": edge_data.get("relation"),
                "reference": node_data.get("reference"),
            })
        return audit_trail
