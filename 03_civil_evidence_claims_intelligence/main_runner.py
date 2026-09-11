from datetime import date
from src.schema import ArtifactType, BOQItem, EvidenceNode
from src.evidence_graph import CivilEvidenceGraph
from src.boq_discrepancy_detector import BOQDiscrepancyDetector
from src.claim_package_generator import ClaimDossierGenerator


def main():
    print("=" * 70)
    print("03. Civil Evidence & Claims Intelligence - Pipeline Demo")
    print("=" * 70)

    # 1. Setup BOQ Items
    boq_piling = BOQItem(
        item_id="BOQ-04.1",
        item_no="04.1",
        description="Bored Cast-in-Situ Reinforced Concrete Piles 1200mm Dia in Hard Rock",
        unit="RMT",
        tender_quantity=1200.0,
        tender_rate=14500.0,
        executed_quantity=1620.0, # 35% overrun due to geological rock head strata variance
    )

    # 2. Check BOQ Variation Deviations
    detector = BOQDiscrepancyDetector()
    findings = detector.analyze_quantities([boq_piling])
    print("\n[1] BOQ Variance Analysis:")
    for f in findings:
        print(f"    Item {f['item_no']}: {f['status']} | Dev: {f['deviation_percent']:+0.1f}% (Executed: {f['executed_qty']} {boq_piling.unit})")
        print(f"    -> Action: {f['action_required']}")

    # 3. Build Evidence Graph
    graph = CivilEvidenceGraph()
    
    # Add BOQ node
    graph.add_node(EvidenceNode(
        node_id="BOQ-04.1",
        artifact_type=ArtifactType.BOQ_ITEM,
        title="Bored Piles 1200mm Dia Item 04.1",
        date_created=date(2025, 6, 1),
        reference_path="/tender/boq_civil_vol2.pdf#p44"
    ))

    # Add Drawing node
    graph.add_node(EvidenceNode(
        node_id="DWG-STR-P04-R2",
        artifact_type=ArtifactType.DRAWING_REVISION,
        title="Substructure Pier P4 Pile Layout Rev-2 (Rock Level Adjusted)",
        date_created=date(2026, 2, 14),
        reference_path="/drawings/structural/DWG-STR-P04-R2.dwg"
    ))

    # Add Measurement Sheet node
    graph.add_node(EvidenceNode(
        node_id="MB-42-P18",
        artifact_type=ArtifactType.MEASUREMENT_BOOK_ENTRY,
        title="Measurement Book #42 Page 18-24 (Pile Depth Boring Logs)",
        date_created=date(2026, 7, 20),
        reference_path="/measurements/MB_42_certified.pdf"
    ))

    # Add Site Photo node
    graph.add_node(EvidenceNode(
        node_id="PHOTO-PIER4-CORE",
        artifact_type=ArtifactType.SITE_PHOTO,
        title="Geo-tagged Rock Core Samples Pier 4 Deep Socketing",
        date_created=date(2026, 7, 21),
        reference_path="/site_media/geo_photos/IMG_20260721_1430.jpg"
    ))

    # Link artifacts
    graph.link_artifacts("DWG-STR-P04-R2", "BOQ-04.1", "REVISED_SPECIFICATION_FOR")
    graph.link_artifacts("MB-42-P18", "BOQ-04.1", "CERTIFIES_EXECUTED_QUANTITY_OF")
    graph.link_artifacts("PHOTO-PIER4-CORE", "BOQ-04.1", "VISUAL_EVIDENCE_FOR")

    # 4. Trace Evidence Audit Trail
    audit_trail = graph.trace_audit_trail("BOQ-04.1")
    print(f"\n[2] Evidence Audit Trail for {boq_piling.item_no}: {len(audit_trail)} linked source artifacts.")
    for e in audit_trail:
        print(f"    - [{e['type']}] {e['title']} ({e['relation']})")

    # 5. Generate Variation Claim Dossier
    dossier = ClaimDossierGenerator.generate_variation_claim_memo(
        project_name="Metro Elevated Viaduct Package EV-03",
        contractor_name="Apex Mega-Infra JV",
        client_name="State Metro Rail Corporation",
        item_no=boq_piling.item_no,
        description=boq_piling.description,
        tender_qty=boq_piling.tender_quantity,
        executed_qty=boq_piling.executed_quantity,
        unit=boq_piling.unit,
        rate=boq_piling.tender_rate,
        evidence_chain=audit_trail,
    )

    print("\n[3] Generated Variation Claim Dossier Excerpt:")
    print("-" * 50)
    print("\n".join(dossier.strip().split("\n")[:14]) + "\n...")
    print("=" * 70)


if __name__ == "__main__":
    main()
