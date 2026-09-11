from datetime import date, timedelta
from decimal import Decimal


class MSMEDInterestCalculator:
    """Calculates compound interest with monthly rests at 3x RBI Bank Rate for delayed payments."""

    def __init__(self, rbi_bank_rate_annual: Decimal = Decimal("0.065")):
        self.statutory_annual_rate = rbi_bank_rate_annual * Decimal("3.0")
        self.monthly_rate = self.statutory_annual_rate / Decimal("12.0")

    def calculate_dues(
        self,
        principal: Decimal,
        invoice_date: date,
        payment_due_days: int = 45,
        as_of_date: date = date.today(),
    ) -> dict:
        due_date = invoice_date + timedelta(days=min(payment_due_days, 45))

        if as_of_date <= due_date:
            return {
                "is_overdue": False,
                "days_overdue": 0,
                "principal": principal,
                "statutory_interest": Decimal("0.00"),
                "total_claimable": principal,
            }

        days_overdue = (as_of_date - due_date).days
        months = Decimal(days_overdue) / Decimal("30.416")

        compounded_total = principal * ((Decimal("1.0") + self.monthly_rate) ** months)
        interest_accumulated = compounded_total - principal

        return {
            "is_overdue": True,
            "days_overdue": days_overdue,
            "principal": round(principal, 2),
            "statutory_interest": round(interest_accumulated, 2),
            "total_claimable": round(compounded_total, 2),
            "applicable_annual_rate_percent": float(self.statutory_annual_rate * 100),
        }
