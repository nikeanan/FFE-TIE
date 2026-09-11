from typing import List
from fastapi import FastAPI
from src.schema import BOQItem
from src.boq_discrepancy_detector import BOQDiscrepancyDetector

app = FastAPI(
    title="Civil Engineering Evidence & Claims Intelligence API",
    description="REST API for BOQ deviation auditing under CPWD Clause 12 / FIDIC Red Book and multi-modal claim dossier generation.",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"service": "Civil Evidence & Claims API", "status": "ONLINE"}

@app.post("/api/boq/audit-variations")
def audit_boq_variations(items: List[BOQItem]):
    detector = BOQDiscrepancyDetector()
    findings = detector.analyze_quantities(items)
    return {
        "total_items_audited": len(items),
        "variations_detected": len(findings),
        "findings": findings,
    }
