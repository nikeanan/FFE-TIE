from datetime import date, timedelta
from typing import Any, Dict, Optional


class GeMAdapter:
    """Adapter for Government e-Marketplace (GeM) order milestones, PRC, and CRC status."""

    @staticmethod
    def get_order_milestones(po_reference: str) -> Dict[str, Any]:
        """Fetches GeM delivery milestones: PRC (Provisional Receipt) and CRC (Consignee Receipt)."""
        return {
            "gem_contract_no": f"GEMC-{po_reference.replace('/', '-')}",
            "prc_status": "GENERATED",
            "prc_date": (date.today() - timedelta(days=20)).isoformat(),
            "crc_status": "COMPLETED",
            "crc_date": (date.today() - timedelta(days=12)).isoformat(),
            "crc_days_elapsed": 12,
            "deemed_acceptance_triggered": True,
            "statutory_mandate": "Under GeM Rule 149 & MSMED Act, payment must be processed within 10 days of CRC generation.",
        }


gem = GeMAdapter()
