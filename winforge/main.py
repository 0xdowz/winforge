import argparse
import sys
import logging
from rich.prompt import Confirm

# Ensure UTF-8 output encoding for legacy Windows console compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from winforge import __version__, __author__
from winforge.core.logger import setup_logger
from winforge.core.privileges import require_admin, is_admin
from winforge.core.engine import run_full_system_scan, run_session_pipeline, export_system_report
from winforge.core.checksums import verify_tweak_checksums
from winforge.cli.components import (
    render_health_dashboard, render_hardware_summary, render_warnings,
    render_benchmark_results, render_dry_run_summary, console
)
from winforge.cli.interface import WinForgeCLI
from winforge.licensing.policy import LicensePolicyManager

logger = logging.getLogger("winforge")


def main():
    parser = argparse.ArgumentParser(
        prog="WinForge",
        description="WINFORGE :: Free Open-Source Windows System Optimization CLI Tool",
        epilog="Safe • Transparent • Reversible • Portable IT Technician Command Line Application | Developed by @0xdowz"
    )

    # Command Flags
    parser.add_argument("--scan", action="store_true", help="Run non-interactive system diagnostic scan and exit")
    parser.add_argument("--dry-run", action="store_true", help="Run optimization simulation without system mutations")
    parser.add_argument("--execute", action="store_true", help="Execute approved production optimizations (Requires Admin)")
    parser.add_argument("--safe", action="store_true", help="Run Beginner profile optimizations (Risk <= 20)")
    parser.add_argument("--advanced", action="store_true", help="Run Advanced profile optimizations (Risk <= 50)")
    parser.add_argument("--tech", action="store_true", help="Launch in Technician Mode with advanced controls & inspection cards")
    parser.add_argument("--license-info", action="store_true", help="Display Open Source Environment Information")
    parser.add_argument("--license-check", action="store_true", help="Perform offline verification and environment check")
    parser.add_argument("--demo", action="store_true", help="Run non-interactive demo/preview mode for screenshots (read-only)")
    parser.add_argument("--version", action="version", version=f"WINFORGE v{__version__} by @{__author__}")

    # Subcommand positional aliases
    parser.add_argument(
        "command",
        nargs="?",
        choices=["welcome", "scan", "analyze", "optimize", "dry-run", "benchmark", "doctor", "license", "tech"],
        help="Subcommand shortcut (e.g. welcome, scan, optimize, doctor, benchmark, tech)"
    )

    args = parser.parse_args()

    # Initialize Logger
    setup_logger()

    # Checksum Verification Check
    valid_checksums, integrity_warnings = verify_tweak_checksums()

    # Resolve positional subcommand aliases
    cmd = args.command
    is_welcome = cmd == "welcome"
    is_scan = args.scan or cmd in ("scan", "analyze")
    is_dry_run = args.dry_run or cmd == "dry-run"
    is_execute = args.execute or cmd == "optimize"
    is_safe_profile = args.safe
    is_adv_profile = args.advanced
    is_tech = args.tech or cmd == "tech"
    is_license = args.license_info or args.license_check or cmd == "license"
    is_doctor = cmd == "doctor"
    is_demo = args.demo

    logger.info(f"Launching WINFORGE v{__version__} by @{__author__} (Cmd: {cmd}, TechMode: {is_tech}, DryRun: {is_dry_run}, Execute: {is_execute})")

    # Subcommand 1: Welcome Journey
    if is_welcome:
        app = WinForgeCLI(tech_mode=is_tech, dry_run=True, mock_execution=True)
        app.handle_welcome()
        sys.exit(0)

    # Subcommand 2: Doctor Check
    if is_doctor:
        from winforge.core.safety_approval import is_admin
        from winforge.cli.renderer import render_doctor_report
        report = run_full_system_scan()
        render_doctor_report(
            is_admin=is_admin(),
            os_product=report.os.product_name,
            cpu_name=report.cpu.name,
            ram_gb=report.ram.total_gb,
            safety_ok=True
        )
        sys.exit(0)

    # Subcommand 3: Environment Info / Check
    if is_license:
        lic_mgr = LicensePolicyManager()
        val_res = lic_mgr.get_active_license()

        print("\n==================================================")
        print("    WINFORGE OPEN SOURCE ENVIRONMENT INFORMATION  ")
        print("==================================================")
        print(f" Software License:   Free & Open-Source (MIT)")
        print(f" Creator & Author:   @{__author__}")
        print(f" Environment State:  {val_res.state.value}")
        print(f" Integrity State:    {'Validated' if valid_checksums else 'Modified Configuration Warning'}")
        print(f" Capability Profile: {val_res.capabilities.tier.value}")
        print(f" Status Message:     {val_res.message}")
        print(f" Technician Mode:    {'Allowed' if val_res.capabilities.technician_mode_allowed else 'Restricted'}")
        print(f" Max Risk Score:     {val_res.capabilities.max_risk_score_allowed}/100")
        print("==================================================\n")
        sys.exit(0)

    # Display integrity warnings for scan / dry-run / execute
    if not valid_checksums:
        print("\n[CONFIG INTEGRITY WARNING]")
        for w in integrity_warnings:
            print(f" ! {w}")

    # Subcommand 4: Scan / Analyze
    if is_scan:
        report = run_full_system_scan()
        render_health_dashboard(report)
        render_hardware_summary(report)
        render_warnings(report)
        filepath = export_system_report(report)
        print(f"\n[SCAN COMPLETE] Diagnostic report generated: {filepath}")
        sys.exit(0)

    # Subcommand 5: Dry-Run Simulation
    if is_dry_run:
        console.print("\n[DRY-RUN SIMULATION MODE]")
        session_mgr, report, _, sim_res = run_session_pipeline(dry_run=True, run_benchmarks=False)
        render_health_dashboard(report)
        render_dry_run_summary(session_mgr, report, sim_res)
        sys.exit(0)

    # Subcommand 6: Benchmark
    if cmd == "benchmark":
        from winforge.benchmark.runner import run_benchmark_suite
        console.print("\n[bold cyan]Running quantitative performance benchmarks...[/bold cyan]")
        bench = run_benchmark_suite()
        render_benchmark_results(bench)
        sys.exit(0)

    # Subcommand 7: Profile-based optimization flags (--safe / --advanced / --tech)
    if is_safe_profile or is_adv_profile:
        app = WinForgeCLI(tech_mode=is_tech, dry_run=not is_execute, mock_execution=not is_execute)
        max_risk = 20 if is_safe_profile else 50
        profile_name = "Safe / Beginner" if is_safe_profile else "Advanced"
        app.run_profile_optimization(max_risk=max_risk, profile_name=profile_name)
        sys.exit(0)

    # Subcommand 8: Production Execution / Optimize
    if is_execute:
        admin_ok = require_admin()
        if not admin_ok:
            print("\n[CRITICAL ERROR] Production execution requires Administrator privileges.")
            sys.exit(1)

        if not valid_checksums:
            print("\n[SECURITY AUDIT] Modified or unverified tweak configuration files detected.")
            if not Confirm.ask("Do you want to proceed with execution despite checksum warnings?", default=False):
                print("[ABORTED] Production execution cancelled by user.")
                sys.exit(1)

        print("\n[PRODUCTION EXECUTION MODE]")
        app = WinForgeCLI(tech_mode=is_tech, dry_run=False, mock_execution=False)
        app.run()
        sys.exit(0)

    # Default Interactive Menu CLI
    app = WinForgeCLI(tech_mode=is_tech, dry_run=True, mock_execution=True)
    app.run()


if __name__ == "__main__":
    main()
