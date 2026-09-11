from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from ..database.db_session import db
from ..database.models import FinancingOffer, Invoice
from ..integrations.treds_adapter import treds
from ..integrations.whatsapp_adapter import whatsapp


class FinancingAnalysis(BaseModel):
    invoice_id: str
    invoice_number: str
    buyer_name: str
    invoice_amount: Decimal
    days_to_maturity: int
    treds_ready: bool
    msme_cc_od_apr: Decimal
    best_offer: Optional[FinancingOffer] = None
    all_offers: List[FinancingOffer] = []
    treds_discount_cost: Decimal
    bank_od_cost: Decimal
    net_working_capital_savings: Decimal
    effective_apr_spread: float
    recommended_action: str  # ACCEPT_TREDS_BID | HOLD_SELF_FINANCE
    whatsapp_alert: Optional[str] = None


class FinancierAgent:
    """Financing Rail Service & Optimizer: Automated rate-shopping, TReDS bidding, and liquidity maximization."""

    @classmethod
    def evaluate_financing(cls, invoice_id: str) -> FinancingAnalysis:
        inv = db.get_invoice(invoice_id)
        if not inv:
            raise ValueError(f"Invoice {invoice_id} not found")

        msme = db.get_msme(inv.msme_id)
        buyer = db.get_buyer(inv.buyer_id)
        buyer_name = buyer.name if buyer else "CPSE Buyer"

        # Days to maturity
        due_date = inv.due_date or (inv.invoice_date + timedelta(days=45))
        days_to_maturity = max(1, (due_date - date.today()).days)

        # MSME Bank OD / CC facility rate (e.g. 12.5% APR)
        cc_apr = msme.cash_credit_apr if msme else Decimal("0.125")

        # TReDS readiness check
        treds_status = treds.check_buyer_readiness(inv.buyer_id)
        is_ready = treds_status.get("ready", False)

        offers: List[FinancingOffer] = []
        if is_ready:
            offers = treds.fetch_live_bids(
                invoice_id=inv.id,
                invoice_amount=inv.amount,
                days_to_maturity=days_to_maturity,
            )

        best_offer = None
        if offers:
            # Sort by lowest APR
            sorted_offers = sorted(offers, key=lambda x: x.discount_rate_apr)
            best_offer = sorted_offers[0]

        best_apr = best_offer.discount_rate_apr if best_offer else Decimal("0.082")

        # Financial Comparison
        days_factor = Decimal(days_to_maturity) / Decimal("365")
        treds_cost = round(inv.amount * best_apr * days_factor, 2)
        bank_od_cost = round(inv.amount * cc_apr * days_factor, 2)
        net_savings = round(bank_od_cost - treds_cost, 2)
        apr_spread = float((cc_apr - best_apr) * 100)

        action = "ACCEPT_TREDS_BID" if net_savings > 0 and is_ready else "HOLD_SELF_FINANCE"

        wa_alert = None
        if best_offer and action == "ACCEPT_TREDS_BID":
            wa_alert = whatsapp.format_treds_offer_alert(
                invoice_no=inv.invoice_number,
                buyer_name=buyer_name,
                platform=best_offer.platform,
                apr=float(best_offer.discount_rate_apr * 100),
                net_amount=float(best_offer.net_amount),
                savings_vs_od=float(net_savings),
                lang="en",
            )

        return FinancingAnalysis(
            invoice_id=inv.id,
            invoice_number=inv.invoice_number,
            buyer_name=buyer_name,
            invoice_amount=inv.amount,
            days_to_maturity=days_to_maturity,
            treds_ready=is_ready,
            msme_cc_od_apr=cc_apr,
            best_offer=best_offer,
            all_offers=offers,
            treds_discount_cost=treds_cost,
            bank_od_cost=bank_od_cost,
            net_working_capital_savings=net_savings,
            effective_apr_spread=apr_spread,
            recommended_action=action,
            whatsapp_alert=wa_alert,
        )

    @classmethod
    def execute_bid_acceptance(cls, offer_id: str, actor: str = "MSME_USER") -> Dict[str, Any]:
        """Accepts the chosen factoring bid through the TReDS adapter."""
        return treds.accept_bid(offer_id=offer_id, actor=actor)


financier_agent = FinancierAgent()
