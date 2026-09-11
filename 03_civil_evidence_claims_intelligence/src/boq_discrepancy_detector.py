from typing import List, Dict
from .schema import BOQItem


class BOQDiscrepancyDetector:
    """Monitors tender quantities against executed quantities and flags deviation/variation limits."""

    VARIATION_THRESHOLD_WARNING = 0.10  # 10% deviation
    VARIATION_THRESHOLD_CRITICAL = 0.25 # 25% deviation (standard CPWD/FIDIC limit triggering rate revision)

    def analyze_quantities(self, items: List[BOQItem]) -> List[Dict]:
        findings = []

        for item in items:
            if item.tender_quantity == 0:
                continue

            deviation_ratio = (item.executed_quantity - item.tender_quantity) / item.tender_quantity
            deviation_percent = deviation_ratio * 100

            if deviation_ratio > self.VARIATION_THRESHOLD_CRITICAL:
                findings.append({
                    "item_no": item.item_no,
                    "description": item.description,
                    "status": "CRITICAL_VARIATION_EXCEEDED",
                    "tender_qty": item.tender_quantity,
                    "executed_qty": item.executed_quantity,
                    "deviation_percent": round(deviation_percent, 2),
                    "action_required": "Initiate formal Extra/Substituted Item Rate Analysis under Clause 12.",
                })
            elif deviation_ratio > self.VARIATION_THRESHOLD_WARNING:
                findings.append({
                    "item_no": item.item_no,
                    "description": item.description,
                    "status": "VARIATION_WARNING",
                    "tender_qty": item.tender_quantity,
                    "executed_qty": item.executed_quantity,
                    "deviation_percent": round(deviation_percent, 2),
                    "action_required": "Notify Engineer-in-Charge before exceeding 25% deviation limit.",
                })

        return findings
