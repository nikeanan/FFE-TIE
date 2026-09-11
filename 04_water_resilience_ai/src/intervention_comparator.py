from typing import List, Dict


class SUDSInterventionComparator:
    """Compares gray infrastructure (conduit upsizing) vs blue-green infrastructure (rain gardens, detention basins)."""

    @staticmethod
    def compare_options(
        baseline_surcharge_m3s: float,
        options: List[Dict],
    ) -> List[Dict]:
        results = []
        for opt in options:
            mitigated_flow = baseline_surcharge_m3s - opt["peak_flow_reduction_m3s"]
            residual_surcharge = max(0.0, mitigated_flow)
            cost_lakhs = opt["estimated_cost_inr_lakhs"]
            cost_per_m3s_mitigated = cost_lakhs / opt["peak_flow_reduction_m3s"] if opt["peak_flow_reduction_m3s"] > 0 else 999.0

            results.append({
                "intervention_name": opt["name"],
                "type": opt["type"], # 'BLUE_GREEN' | 'GRAY_INFRASTRUCTURE'
                "flow_reduction_m3s": round(opt["peak_flow_reduction_m3s"], 3),
                "residual_surcharge_m3s": round(residual_surcharge, 3),
                "estimated_cost_inr_lakhs": cost_lakhs,
                "cost_efficiency_lakhs_per_m3s": round(cost_per_m3s_mitigated, 2),
                "completely_resolves_flood": residual_surcharge == 0.0,
            })

        # Rank by cost efficiency
        results.sort(key=lambda x: x["cost_efficiency_lakhs_per_m3s"])
        return results
