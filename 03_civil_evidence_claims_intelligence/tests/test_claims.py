import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
import pytest
from src.schema import ArtifactType, BOQItem, EvidenceNode
from src.evidence_graph import CivilEvidenceGraph
from src.boq_discrepancy_detector import BOQDiscrepancyDetector
from src.claim_package_generator import ClaimDossierGenerator


def test_boq_variation_detection():
    item_normal = BOQItem(item_id="01", item_no="01", description="Excavation", unit="CUM", tender_quantity=100.0, tender_rate=500.0, executed_quantity=105.0)
    item_warning = BOQItem(item_id="02", item_no="02", description="PCC", unit="CUM", tender_quantity=100.0, tender_rate=4000.0, executed_quantity=115.0)
    item_critical = BOQItem(item_id="03", item_no="03", description="Piling", unit="RMT", tender_quantity=100.0, tender_rate=15000.0, executed_quantity=135.0)

    detector = BOQDiscrepancyDetector()
    findings = detector.analyze_quantities([item_normal, item_warning, item_critical])

    assert len(findings) == 2
    assert findings[0]["status"] == "VARIATION_WARNING"
    assert findings[1]["status"] == "CRITICAL_VARIATION_EXCEEDED"


def test_evidence_graph_linking():
    graph = CivilEvidenceGraph()
    graph.add_node(EvidenceNode(node_id="BOQ-1", artifact_type=ArtifactType.BOQ_ITEM, title="BOQ Item 1", date_created=date(2026, 1, 1), reference_path="/boq.pdf"))
    graph.add_node(EvidenceNode(node_id="DWG-1", artifact_type=ArtifactType.DRAWING_REVISION, title="Drawing 1", date_created=date(2026, 2, 1), reference_path="/dwg.dwg"))
    graph.link_artifacts("DWG-1", "BOQ-1", "SUPPORTS")

    audit = graph.trace_audit_trail("BOQ-1")
    assert len(audit) == 1
    assert audit[0]["evidence_id"] == "DWG-1"
    assert audit[0]["relation"] == "SUPPORTS"
