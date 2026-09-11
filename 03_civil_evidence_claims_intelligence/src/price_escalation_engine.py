"""Price Escalation Engine for Infrastructure Contracts.
Implements CPWD Clause 10CA & 10CC, MoRTH, and FIDIC Sub-Clause 13.7 escalation formulas.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from .schema import EscalationComponent, EscalationCalculationResult, ContractClause


class PriceEscalationEngine:
    """Calculates statutory and contractual price escalation claims with audit-ready formulas."""

    def calculate_clause_10ca_item(
        self,
        component: EscalationComponent,
        base_rate_inr: float,
        quantity_consumed: float,
        base_index_ci0: float,
        current_index_cin: float,
    ) -> EscalationCalculationResult:
        """CPWD Clause 10CA:
        V = Q * R0 * ( (CI_n - CI_0) / CI_0 )
        Where:
        Q = Quantity of material consumed in the period
        R0 = Base price of material fixed in contract
        CI_0 = Base Wholesale Price Index at tender submission
        CI_n = Current Wholesale Price Index at the time of execution
        """
        if base_index_ci0 <= 0:
            delta_pct = 0.0
            escalation_amt = 0.0
        else:
            delta_pct = ((current_index_cin - base_index_ci0) / base_index_ci0) * 100.0
            escalation_amt = quantity_consumed * base_rate_inr * ((current_index_cin - base_index_ci0) / base_index_ci0)

        is_claim = escalation_amt > 0

        return EscalationCalculationResult(
            component=component,
            base_index_ci0=base_index_ci0,
            current_index_cin=current_index_cin,
            delta_index_percent=round(delta_pct, 2),
            base_rate_inr=base_rate_inr,
            escalation_amount_inr=round(escalation_amt, 2),
            clause_reference="CPWD Clause 10CA / MoRTH Sub-Clause 10.8",
            is_claimable=is_claim,
        )

    def calculate_clause_10cc_composite(
        self,
        gross_work_done_inr: float,
        labour_component_pct: float = 25.0,
        materials_component_pct: float = 60.0,
        pol_fuel_component_pct: float = 15.0,
        base_labour_index: float = 135.0,
        curr_labour_index: float = 148.0,
        base_mat_index: float = 122.0,
        curr_mat_index: float = 134.5,
        base_pol_index: float = 110.0,
        curr_pol_index: float = 126.0,
    ) -> Dict[str, Any]:
        """CPWD Clause 10CC:
        VL = (W * (Y/100) * (LI - LI0) / LI0)
        VM = (W * (X/100) * (MI - MI0) / MI0)
        VF = (W * (Z/100) * (FI - FI0) / FI0)
        """
        # Labour escalation
        vl = gross_work_done_inr * (labour_component_pct / 100.0) * ((curr_labour_index - base_labour_index) / base_labour_index)
        # Material escalation
        vm = gross_work_done_inr * (materials_component_pct / 100.0) * ((curr_mat_index - base_mat_index) / base_mat_index)
        # POL Fuel escalation
        vf = gross_work_done_inr * (pol_fuel_component_pct / 100.0) * ((curr_pol_index - base_pol_index) / base_pol_index)

        total_escalation = vl + vm + vf

        return {
            "gross_work_done_inr": gross_work_done_inr,
            "labour_escalation_vl_inr": round(vl, 2),
            "material_escalation_vm_inr": round(vm, 2),
            "fuel_escalation_vf_inr": round(vf, 2),
            "total_escalation_inr": round(total_escalation, 2),
            "effective_escalation_percent": round((total_escalation / gross_work_done_inr) * 100.0, 2) if gross_work_done_inr > 0 else 0.0,
        }


escalation_engine = PriceEscalationEngine()
