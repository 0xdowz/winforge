import logging
from typing import List
from winforge.models.system import (
    CPUInfo, RAMInfo, StorageDrive, OSInfo, PowerPlan,
    ServiceDetail, StartupItem, CategoryScores, SystemHealthReport
)

logger = logging.getLogger("winforge")


def calculate_category_scores(
    cpu: CPUInfo,
    ram: RAMInfo,
    drives: List[StorageDrive],
    power: PowerPlan,
    services: List[ServiceDetail],
    startup_items: List[StartupItem],
    warnings: List[str]
) -> CategoryScores:
    """Computes individual component health scores (0-100) and returns CategoryScores."""

    # 1. Performance Score (0-100)
    perf_score = 100.0
    if ram.percent_used > 85.0:
        perf_score -= 25.0
        warnings.append(f"High RAM usage detected: {ram.percent_used}% utilized.")
    elif ram.percent_used > 70.0:
        perf_score -= 10.0

    if cpu.current_usage_pct > 80.0:
        perf_score -= 20.0
        warnings.append(f"High CPU workload detected: {cpu.current_usage_pct}% load.")

    if not power.is_high_performance and not power.is_on_battery:
        perf_score -= 5.0  # Balanced plan opportunity for boost

    perf_score = max(0.0, min(100.0, perf_score))

    # 2. Security & Privacy Hygiene Score (0-100)
    sec_score = 100.0
    critical_services_stopped = [s for s in services if s.is_critical and s.status.lower() == "stopped"]
    if critical_services_stopped:
        sec_score -= 30.0
        stopped_names = ", ".join([s.name for s in critical_services_stopped])
        warnings.append(f"Critical Windows Security services stopped: {stopped_names}")

    telemetry_running = [s for s in services if s.name.lower() in ("diagtrack", "sysmain", "dmwappushservice") and s.status.lower() == "running"]
    if telemetry_running:
        sec_score -= 15.0

    sec_score = max(0.0, min(100.0, sec_score))

    # 3. Maintenance & Disk Score (0-100)
    maint_score = 100.0
    for drive in drives:
        if drive.percent_used > 90.0:
            maint_score -= 30.0
            warnings.append(f"Storage Drive {drive.drive_letter} is critically full ({drive.percent_used}% used).")
        elif drive.percent_used > 80.0:
            maint_score -= 15.0

    maint_score = max(0.0, min(100.0, maint_score))

    # 4. Startup & Service Hygiene Score (0-100)
    startup_score = 100.0
    active_startups = [i for i in startup_items if i.enabled]
    if len(active_startups) > 10:
        startup_score -= 30.0
        warnings.append(f"Excessive startup programs detected ({len(active_startups)} active items).")
    elif len(active_startups) > 5:
        startup_score -= 15.0

    startup_score = max(0.0, min(100.0, startup_score))

    return CategoryScores(
        performance_score=round(perf_score, 1),
        security_score=round(sec_score, 1),
        maintenance_score=round(maint_score, 1),
        startup_score=round(startup_score, 1)
    )
