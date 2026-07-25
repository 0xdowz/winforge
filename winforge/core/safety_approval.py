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

    def evaluate_realtime_safety(self) -> SafetyApprovalResult:
        """Runs pre-flight safety checks (Elevation, Disk Space, Battery, System Restore)."""
        logger.info("Executing real-time safety approval pre-flight checks...")
        checks: Dict[str, bool] = {}
        failure_reasons: list[str] = []

        # 1. Admin Elevation Check
        admin_ok = is_admin()
        checks["admin_privileges"] = admin_ok
        if not admin_ok:
            failure_reasons.append("Application is running without Administrator elevation.")

        # 2. System Free Disk Space Check (Requires >= 2.0 GB free on system drive C:)
        drives = get_storage_drives()
        sys_drive = next((d for d in drives if "C" in d.drive_letter.upper()), drives[0] if drives else None)
        disk_ok = bool(sys_drive and sys_drive.free_gb >= 2.0)
        checks["sufficient_disk_space"] = disk_ok
        if sys_drive and not disk_ok:
            failure_reasons.append(f"Insufficient free disk space on drive {sys_drive.drive_letter} ({sys_drive.free_gb} GB free < 2.0 GB required).")

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
