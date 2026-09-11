from decimal import Decimal


def evaluate_treds_bid(
    invoice_amount: Decimal,
    days_to_maturity: int,
    treds_annual_discount_bid: Decimal,
    msme_cc_od_annual_rate: Decimal,
) -> dict:
    """Evaluates whether to accept a financier's bid on TReDS vs. using existing Cash Credit facility."""
    treds_cost = (
        invoice_amount
        * treds_annual_discount_bid
        * (Decimal(days_to_maturity) / Decimal("365"))
    )
    cc_cost = (
        invoice_amount
        * msme_cc_od_annual_rate
        * (Decimal(days_to_maturity) / Decimal("365"))
    )
    net_savings = cc_cost - treds_cost

    return {
        "recommended_action": "ACCEPT_TREDS_BID" if net_savings > 0 else "HOLD_SELF_FINANCE",
        "treds_discount_cost": round(treds_cost, 2),
        "bank_od_cost": round(cc_cost, 2),
        "net_working_capital_savings": round(net_savings, 2),
        "effective_apr_spread": float((msme_cc_od_annual_rate - treds_annual_discount_bid) * 100),
    }
