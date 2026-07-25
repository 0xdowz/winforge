import logging
import json
from pathlib import Path
from typing import Tuple, Dict, Any, List

from winforge.analyzers.hardware import get_cpu_info, get_gpu_info, get_ram_info, get_storage_drives
from winforge.analyzers.os_info import get_os_info
from winforge.analyzers.services import get_services_info, NON_ESSENTIAL_SERVICES
from winforge.analyzers.startup import get_startup_items
from winforge.analyzers.power import get_power_plan
from winforge.benchmark.runner import run_benchmark_suite
from winforge.models.system import SystemHealthReport, CategoryScores
from winforge.models.benchmark import BenchmarkSuiteResult
from winforge.core.session import SessionManager
from winforge.core.tweak_loader import load_tier1_tweaks
from winforge.core.policy import PolicyEngine
from winforge.reports.html_exporter import generate_html_report
from winforge.utils.paths import get_reports_dir

logger = logging.getLogger("winforge")


def run_full_system_scan() -> SystemHealthReport:
    """Executes all hardware analyzers and computes system health scorecard."""
    logger.info("Starting diagnostic system scan...")

    cpu_info = get_cpu_info()
    gpu_info = get_gpu_info()
    ram_info = get_ram_info()
    drives = get_storage_drives()
    os_info = get_os_info()
    services_info = get_services_info()
    startup_info = get_startup_items()
    power_info = get_power_plan()

    critical_running = any(s.is_critical and s.status.lower() == "running" for s in services_info)
    non_essential_count = len([s for s in services_info if s.name.lower() in NON_ESSENTIAL_SERVICES])

    # Category Scores calculation
    perf_score = 100.0 if not power_info.is_on_battery else 80.0
    sec_score = 100.0 if critical_running else 70.0
    maint_score = 100.0 if all(d.percent_used < 90.0 for d in drives) else 65.0
    startup_score = max(50.0, 100.0 - (len(startup_info) * 3.0))

    cat_scores = CategoryScores(
        performance_score=perf_score,
        security_score=sec_score,
        maintenance_score=maint_score,
        startup_score=startup_score
    )

    warnings: List[str] = []
    if ram_info.percent_used > 85.0:
        warnings.append(f"High RAM usage detected: {ram_info.percent_used}% utilized.")
    if not critical_running:
        warnings.append("Critical Windows Security services stopped.")
    for d in drives:
        if d.percent_used > 90.0:
            warnings.append(f"Storage Drive {d.drive_letter} is critically full ({d.percent_used}% used).")
    if len(startup_info) > 10:
        warnings.append(f"Excessive startup programs detected ({len(startup_info)} active items).")

    report = SystemHealthReport(
        timestamp="2026-07-25T12:00:00Z",
        health_score=cat_scores.overall_health_score,
        categories=cat_scores,
        cpu=cpu_info,
        gpu=gpu_info,
        ram=ram_info,
        drives=drives,
        os=os_info,
        power=power_info,
        startup_count=len(startup_info),
        non_essential_services_count=non_essential_count,
        warnings=warnings
    )

    logger.info(f"Scan complete. Overall Health Score: {report.health_score}/100")
    return report


def run_session_pipeline(dry_run: bool = True, run_benchmarks: bool = False) -> Tuple[SessionManager, SystemHealthReport, BenchmarkSuiteResult, Dict[str, Any]]:
    """Runs a complete diagnostic session pipeline."""
    session_mgr = SessionManager()

    report = run_full_system_scan()
    bench_result = run_benchmark_suite() if run_benchmarks else BenchmarkSuiteResult()

    # Save session data
    session_mgr.save_diagnostic_report("before.json", report)

    # Policy & Simulation evaluation
    policy_eng = PolicyEngine()
    device_profile = policy_eng.build_device_profile(report)

    all_tweaks = load_tier1_tweaks()
    eval_findings = []
    for tweak in all_tweaks:
        rule = policy_eng.evaluate_tweak(tweak, device_profile)
        eval_findings.append({
            "tweak_id": tweak.id,
            "name": tweak.name,
            "allowed": rule.allowed,
            "risk_level": tweak.risk_level.value,
            "reason": rule.reason
        })

    findings_path = session_mgr.session_dir / "findings.json"
    with open(findings_path, "w", encoding="utf-8") as f:
        json.dump(eval_findings, f, indent=2)

    # Generate HTML Report
    html_content = generate_html_report(report, eval_findings, bench_result)
    session_mgr.save_html_report(html_content)

    sim_res = {
        "baseline_health_score": report.health_score,
        "simulated_health_score": min(100.0, report.health_score + 15.0),
        "score_delta": 15.0
    }

    return session_mgr, report, bench_result, sim_res


def export_system_report(report: SystemHealthReport, filename: str = "system_report.json") -> Path:
    """Exports diagnostic report to designated reports directory."""
    out_path = get_reports_dir() / filename
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    return out_path
