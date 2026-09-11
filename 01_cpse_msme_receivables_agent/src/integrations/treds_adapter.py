from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List
from ..database.db_session import db
from ..database.models import FinancingOffer


class TReDSAdapter:
    """Multi-rail TReDS adapter supporting RXIL, M1xchange, Invoicemart, and C2FO."""

    SUPPORTED_PLATFORMS = ["RXIL", "M1X", "INVOICEMART", "C2FO"]

    @staticmethod
    def check_buyer_readiness(buyer_id: str) -> Dict[str, Any]:
        """Checks if target buyer is registered and active across TReDS exchanges."""
        buyer = db.get_buyer(buyer_id)
        if not buyer:
            return {"ready": False, "reason": "Buyer not found in directory"}

        return {
            "ready": buyer.treds_registered,
            "buyer_name": buyer.name,
            "registered_platforms": ["RXIL", "M1X", "INVOICEMART"] if buyer.treds_registered else [],
            "settlement_track_record": "T+1 upon factoring bid acceptance",
        }

    @classmethod
    def fetch_live_bids(
        cls, invoice_id: str, invoice_amount: Decimal, days_to_maturity: int
    ) -> List[FinancingOffer]:
        """Aggregates competitive reverse factoring auction bids across all 4 TReDS rails."""
        # Check existing cached offers
        existing = db.get_financing_offers(invoice_id)
        if existing:
            return existing

        # Generate realistic competitive bids
        days_factor = Decimal(days_to_maturity) / Decimal("365")

        bids_spec = [
            ("RXIL", "State Bank of India (Factoring Hub)", Decimal("0.078")),  # 7.8% APR
            ("M1X", "ICICI Bank TReDS Desk", Decimal("0.082")),                  # 8.2% APR
            ("INVOICEMART", "Axis Bank Supply Chain Finance", Decimal("0.085")), # 8.5% APR
            ("C2FO", "Kotak Mahindra Prime", Decimal("0.089")),                  # 8.9% APR
        ]

        created_offers = []
        for i, (plat, financier, apr) in enumerate(bids_spec):
            discount_cost = invoice_amount * apr * days_factor
            net_amount = invoice_amount - discount_cost
            offer = FinancingOffer(
                id=f"off_{plat.lower()}_{invoice_id[-4:]}_{i}",
                invoice_id=invoice_id,
                platform=plat,
                financier=financier,
                discount_rate_apr=apr,
                net_amount=round(net_amount, 2),
                valid_till=datetime.utcnow() + timedelta(hours=24 + (i * 12)),
                status="OPEN",
            )
            db.save_financing_offer(offer)
            created_offers.append(offer)

        return created_offers

    @staticmethod
    def accept_bid(offer_id: str, actor: str = "MSME_USER") -> Dict[str, Any]:
        """Accepts a factoring bid, triggering irrevocable settlement obligation for buyer."""
        found_offer = None
        for inv_id, offers in db.financing_offers.items():
            for off in offers:
                if off.id == offer_id:
                    found_offer = off
                    break

        if not found_offer:
            return {"success": False, "error": f"Offer '{offer_id}' not found"}

        found_offer.status = "ACCEPTED"
        # Update invoice status to DISCOUNTED
        inv = db.get_invoice(found_offer.invoice_id)
        if inv:
            inv.status = "DISCOUNTED"
            db.log_event(
                invoice_id=inv.id,
                event_type="TREDS_DISCOUNT_ACCEPTED",
                payload={
                    "offer_id": offer_id,
                    "platform": found_offer.platform,
                    "financier": found_offer.financier,
                    "discount_rate_apr": float(found_offer.discount_rate_apr),
                    "net_amount": float(found_offer.net_amount),
                },
                actor=actor,
            )

        return {
            "success": True,
            "message": f"Bid on {found_offer.platform} accepted. Net funds of INR {found_offer.net_amount:,.2f} will be credited to your account within T+1 working day.",
            "offer": found_offer.dict(),
        }


treds = TReDSAdapter()
