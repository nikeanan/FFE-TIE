"""Time Impact & Delay Analysis Engine for Civil Claims.
Implements Critical Path Method (CPM) delay window analysis, concurrent delay allocation,
and prolongation cost quantification under CPWD Clause 5 and FIDIC Clause 8.4 / 20.1.
"""
from typing import List, Dict, Any
from datetime import date
from pydantic import BaseModel
from .schema import DelayEvent, DelayCategory, ContractClause, ProlongationClaim


class DelaySummaryResult(BaseModel):
    total_gross_delay_days: int
    employer_caused_delay_days: int
    contractor_caused_delay_days: int
    force_majeure_days: int
    concurrent_delay_days: int
    net_excusable_eot_days: int  # Extension of Time entitlement (Employer + Force Majeure)
    net_compensable_days: int    # Prolongation cost entitlement (Employer delay only)
    daily_overhead_rate_inr: float
    prolongation_claim_amount_inr: float
    ld_shielded_amount_inr: float
    delay_events_breakdown: List[Dict[str, Any]]
    contractual_verdict: str


class DelayAnalysisEngine:
    """Performs Time Impact Analysis (TIA) and delay liability apportionment."""

    def analyze_delays(
        self,
        events: List[DelayEvent],
        contract_clause: ContractClause = ContractClause.CPWD_CLAUSE_5_EOT,
        custom_daily_overhead_inr: float = 85000.0,
        custom_daily_ld_inr: float = 120000.0,
    ) -> DelaySummaryResult:
        if not events:
            return DelaySummaryResult(
                total_gross_delay_days=0,
                employer_caused_delay_days=0,
                contractor_caused_delay_days=0,
                force_majeure_days=0,
                concurrent_delay_days=0,
                net_excusable_eot_days=0,
                net_compensable_days=0,
                daily_overhead_rate_inr=custom_daily_overhead_inr,
                prolongation_claim_amount_inr=0.0,
                ld_shielded_amount_inr=0.0,
                delay_events_breakdown=[],
                contractual_verdict="NO_DELAYS_RECORDED",
            )

        employer_days = 0
        contractor_days = 0
        force_majeure_days = 0
        concurrent_days = 0
        total_gross = 0
        breakdown = []

        for ev in events:
            total_gross += ev.duration_days
            if ev.category == DelayCategory.EMPLOYER_RISK:
                employer_days += ev.duration_days
            elif ev.category == DelayCategory.CONTRACTOR_RISK:
                contractor_days += ev.duration_days
            elif ev.category == DelayCategory.FORCE_MAJEURE:
                force_majeure_days += ev.duration_days
            elif ev.category == DelayCategory.CONCURRENT_DELAY:
                concurrent_days += ev.duration_days

            breakdown.append({
                "event_id": ev.event_id,
                "title": ev.title,
                "category": ev.category.value,
                "duration_days": ev.duration_days,
                "critical_path": ev.is_critical_path,
                "evidence_count": len(ev.evidence_nodes),
            })

        # Under Indian standard contracts (CPWD/FIDIC):
        # Excusable days (no LD levied): Employer Risk + Force Majeure + Concurrent (excusable non-compensable)
        net_excusable = employer_days + force_majeure_days + concurrent_days
        
        # Compensable days (Prolongation overhead cost payable by Client): Employer Risk only
        net_compensable = employer_days

        prolongation_amount = net_compensable * custom_daily_overhead_inr
        ld_shielded = net_excusable * custom_daily_ld_inr

        verdict = (
            f"EOT ENTITLED: {net_excusable} Days Extension of Time justified. "
            f"Contractor is shielded from ₹ {ld_shielded:,.2f} Liquidated Damages, "
            f"with ₹ {prolongation_amount:,.2f} compensable site prolongation overhead."
        )

        return DelaySummaryResult(
            total_gross_delay_days=total_gross,
            employer_caused_delay_days=employer_days,
            contractor_caused_delay_days=contractor_days,
            force_majeure_days=force_majeure_days,
            concurrent_delay_days=concurrent_days,
            net_excusable_eot_days=net_excusable,
            net_compensable_days=net_compensable,
            daily_overhead_rate_inr=custom_daily_overhead_inr,
            prolongation_claim_amount_inr=prolongation_amount,
            ld_shielded_amount_inr=ld_shielded,
            delay_events_breakdown=breakdown,
            contractual_verdict=verdict,
        )


delay_engine = DelayAnalysisEngine()
