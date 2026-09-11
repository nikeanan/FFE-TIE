from dataclasses import dataclass
from typing import List
from .schema import BatchTicket


@dataclass
class QCAlert:
    severity: str  # 'CRITICAL' | 'WARNING' | 'INFO'
    parameter: str
    target_value: float
    actual_value: float
    deviation_percent: float
    explanation: str
    recommended_engineer_action: str


class BatchQCAnomalyEngine:
    """Detects batch plant scale drift, moisture spikes, and mix design deviations per IS 4926."""

    TOLERANCE_CEMENT = 0.02  # +/- 2% per IS 4926 Table 2
    TOLERANCE_WATER = 0.03   # +/- 3%
    TOLERANCE_AGGREGATE = 0.03 # +/- 3%

    def inspect_batch(self, batch: BatchTicket) -> List[QCAlert]:
        alerts: List[QCAlert] = []
        target = batch.target_proportions

        # 1. Cement Variance Check
        cement_dev = (batch.actual_cement_kg - target.cement_opc_kg) / target.cement_opc_kg
        if abs(cement_dev) > self.TOLERANCE_CEMENT:
            sev = "CRITICAL" if cement_dev < -self.TOLERANCE_CEMENT else "WARNING"
            alerts.append(
                QCAlert(
                    severity=sev,
                    parameter="Cement Weight (Batch Scale)",
                    target_value=target.cement_opc_kg,
                    actual_value=batch.actual_cement_kg,
                    deviation_percent=round(cement_dev * 100, 2),
                    explanation="Under-dosing risks structural strength deficit; over-dosing increases batch cost unnecessarily.",
                    recommended_engineer_action="Inspect cement weighing hopper pneumatic discharge valve & tare zero calibration.",
                )
            )

        # 2. Water / Sand Moisture Check
        free_water = batch.free_water_from_sand_liters
        total_effective_water = batch.actual_water_liters + free_water
        water_dev = (total_effective_water - target.water_liters) / target.water_liters

        if abs(water_dev) > self.TOLERANCE_WATER:
            alerts.append(
                QCAlert(
                    severity="CRITICAL" if water_dev > 0.05 else "WARNING",
                    parameter="Effective Water (Incl. Moisture)",
                    target_value=target.water_liters,
                    actual_value=round(total_effective_water, 2),
                    deviation_percent=round(water_dev * 100, 2),
                    explanation=f"Aggregate moisture ({batch.sand_moisture_percent}%) added {free_water:.1f}L unmetered water, shifting effective W/C ratio.",
                    recommended_engineer_action=f"Trim batching water by {free_water:.1f} Liters on the PLC console for next batch.",
                )
            )

        return alerts
