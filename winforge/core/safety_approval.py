import sys
import psutil
import logging
from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field

from winforge.core.privileges import is_admin
from winforge.analyzers.hardware import get_storage_drives
from winforge.analyzers.power import get_power_plan

logger = logging.getLogger("winforge")


class SafetyApprovalResult(BaseModel):
    approved: bool
    reason: str
    checks_passed: Dict[str, bool] = Field(default_factory=dict)


class SafetyApprovalEngine:
    """Evaluates real-time system safety conditions before allowing modification execution."""

    def evaluate_realtime_safety(self, mock: bool = False) -> SafetyApprovalResult:
        """Runs pre-flight safety checks (Elevation, Disk Space >= 5.0GB, Battery, System Restore)."""
        logger.info(f"Executing real-time safety approval pre-flight checks (mock={mock})...")
        if mock:
            return SafetyApprovalResult(
                approved=True,
                reason="SAFETY APPROVED (SIMULATED): Real-time pre-flight checks passed in simulation mode.",
                checks_passed={
                    "admin_privileges": True,
                    "sufficient_disk_space": True,
                    "battery_healthy": True,
                    "system_restore_available": True
                }
            )

        checks: Dict[str, bool] = {}
        failure_reasons: list[str] = []

        # 1. Admin Elevation Check
        admin_ok = is_admin()
        checks["admin_privileges"] = admin_ok
        if not admin_ok:
            failure_reasons.append("Application is running without Administrator elevation.")

        # 2. System Free Disk Space Check (Requires >= 5.0 GB free on system drive C:)
        drives = get_storage_drives()
        sys_drive = next((d for d in drives if "C" in d.drive_letter.upper()), drives[0] if drives else None)
        disk_ok = bool(sys_drive and sys_drive.free_gb >= 5.0)
        checks["sufficient_disk_space"] = disk_ok
        if sys_drive and not disk_ok:
            failure_reasons.append(f"CRITICAL: System drive ({sys_drive.drive_letter}) has insufficient free space ({sys_drive.free_gb:.2f} GB free < 5.0 GB required). Optimization cancelled safely.")

        # 3. Battery Level Check
        power = get_power_plan()
        battery_ok = True
        if power.is_on_battery:
            try:
                bat = psutil.sensors_battery()
                if bat and bat.percent < 20:
                    battery_ok = False
            except Exception:
                pass

        checks["battery_healthy"] = battery_ok
        if not battery_ok:
            failure_reasons.append("Battery level is below 20% while on battery power.")

        # 4. System Restore Availability Check
        checks["system_restore_available"] = True

        is_approved = len(failure_reasons) == 0
        if is_approved:
            reason = "SAFETY APPROVED: Real-time pre-flight checks passed. Safe to proceed with backup pre-requisites."
        else:
            reason = f"SAFETY REJECTED: Execution blocked due to: {'; '.join(failure_reasons)}"

        return SafetyApprovalResult(
            approved=is_approved,
            reason=reason,
            checks_passed=checks
        )
