import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from ..database.db_session import db
from ..database.models import BuyerLearnedRule, FlagSeverity


class InboundDisputeMiner:
    """NLP-assisted parser that reads buyer email objections, categorizes the rejection pattern,
    updates the Buyer Moat Knowledge Graph, and auto-drafts the exact rebuttal memo."""

    DISPUTE_PATTERNS = [
        {
            "category": "GRN_QUANTITY_DISCREPANCY",
            "keywords": ["grn", "short delivery", "received count", "quantity mismatch", "shortage", "excess"],
            "rule_code": "BUYER_GRN_STRICT_MATCH",
            "rule_name": "Strict Store GRN Quantity Alignment",
            "severity": FlagSeverity.BLOCKER,
            "human_reason": "Buyer accounts strictly holds payments if billed quantity exceeds stores physical receipt slip.",
            "rebuttal_template": "We have attached the certified Gate Entry & Store Weighbridge slip confirming receipt of full quantity.",
        },
        {
            "category": "INSPECTION_ANNEXURE_MISSING",
            "keywords": ["tpi", "inspection", "qa certificate", "test report", "stamp missing", "mdcc"],
            "rule_code": "BUYER_INSPECTION_SIGN_MANDATORY",
            "rule_name": "Signed TPI & Inspection Clearance Annexure",
            "severity": FlagSeverity.BLOCKER,
            "human_reason": "Buyer requires Material Dispatch Clearance Certificate (MDCC) and signed TPI report before invoice processing.",
            "rebuttal_template": "Enclosed is the third-party inspection (TPI) release certificate duly signed and stamped by your QA wing.",
        },
        {
            "category": "VENDOR_CODE_MISSING",
            "keywords": ["vendor code", "sap vendor", "vendor master", "internal code", "supplier id"],
            "rule_code": "BUYER_VENDOR_CODE_HEADER",
            "rule_name": "SAP Vendor Master Code Stamping",
            "severity": FlagSeverity.WARN,
            "human_reason": "Buyer's SAP ERP requires the 6-digit vendor master code in the invoice header note.",
            "rebuttal_template": "Our vendor registration code has been stamped and verified against your SAP vendor directory.",
        },
        {
            "category": "PRICE_VARIATION_DISPUTE",
            "keywords": ["pvc", "escalation index", "base price", "rate difference", "price variation"],
            "rule_code": "BUYER_PVC_CERTIFICATION_REQUIRED",
            "rule_name": "IEEMA / RBI Index Calculation Dossier",
            "severity": FlagSeverity.BLOCKER,
            "human_reason": "Buyer requires RBI / IEEMA wholesale price index calculation sheet for price variation claims.",
            "rebuttal_template": "Attached is the IEEMA price variation calculation with supporting RBI index bulletins.",
        },
    ]

    @classmethod
    def analyze_inbound_email(
        cls,
        buyer_id: str,
        subject: str,
        body: str,
        sender_email: str,
    ) -> Dict[str, Any]:
        combined_text = f"{subject} {body}".lower()
        matched_category = "GENERAL_DELAY_INQUIRY"
        matched_rule = None
        rebuttal_draft = "We request your prompt review and clearance of the attached documentation."

        for pattern in cls.DISPUTE_PATTERNS:
            if any(k in combined_text for k in pattern["keywords"]):
                matched_category = pattern["category"]
                matched_rule = pattern
                rebuttal_draft = pattern["rebuttal_template"]
                break

        # If a specific objection rule was mined, update the Buyer Knowledge Graph
        if matched_rule:
            existing_rules = db.get_buyer_rules(buyer_id)
            if not any(r.rule_code == matched_rule["rule_code"] for r in existing_rules):
                new_rule = BuyerLearnedRule(
                    id=f"rule_{buyer_id}_{matched_rule['rule_code'].lower()}",
                    buyer_id=buyer_id,
                    rule_code=matched_rule["rule_code"],
                    rule_name=matched_rule["rule_name"],
                    human_reason=matched_rule["human_reason"],
                    check_type=matched_category,
                    severity=matched_rule["severity"],
                    rejection_count=1,
                )
                db.save_buyer_rule(new_rule)

        return {
            "buyer_id": buyer_id,
            "sender": sender_email,
            "subject": subject,
            "detected_category": matched_category,
            "is_dispute_flagged": matched_rule is not None,
            "learned_rule_code": matched_rule["rule_code"] if matched_rule else None,
            "human_explanation": matched_rule["human_reason"] if matched_rule else "Routine follow-up communication.",
            "auto_drafted_rebuttal": rebuttal_draft,
        }


dispute_miner = InboundDisputeMiner()
