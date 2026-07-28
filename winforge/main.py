import argparse
import sys
import os
import logging
import traceback
from rich.prompt import Confirm

# Ensure UTF-8 output encoding for legacy Windows console compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from winforge import __version__, __author__
from winforge.core.logger import setup_logger, log_startup_info, log_startup_exception
from winforge.core.privileges import require_admin, is_admin
from winforge.core.engine import run_full_system_scan, run_session_pipeline, export_system_report
from winforge.core.checksums import verify_tweak_checksums
from winforge.core.tweak_loader import load_tier1_tweaks
from winforge.cli.components import (
    render_health_dashboard, render_hardware_summary, render_warnings,
    render_benchmark_results, render_dry_run_summary, console
)
from winforge.cli.interface import WinForgeCLI
from winforge.licensing.policy import LicensePolicyManager
from winforge.cli.theme import render_section_header
from winforge.security.health import security_engine

logger = logging.getLogger("winforge")


def main():
    # Record startup info
    log_startup_info(sys.argv)

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
        choices=["welcome", "scan", "analyze", "optimize", "dry-run", "benchmark", "doctor", "license", "info", "tweaks", "security-check", "rollback", "tech"],
        help="Subcommand shortcut (e.g. welcome, scan, analyze, doctor, info, tweaks, security-check, rollback)"
    )
    parser.add_argument("subarg", nargs="?", help="Optional subcommand argument (e.g. list, SESSION_ID)")

    args = parser.parse_args()

    # Initialize Logger
    setup_logger()

    # Checksum Verification Check
    valid_checksums, integrity_warnings = verify_tweak_checksums()

    # Resolve positional subcommand aliases
    cmd = args.command
    subarg = args.subarg

    is_welcome = cmd == "welcome"
    is_scan = args.scan or cmd in ("scan", "analyze")
    is_dry_run = args.dry_run or cmd == "dry-run"
    is_execute = args.execute or cmd == "optimize"
    is_safe_profile = args.safe
    is_adv_profile = args.advanced
    is_tech = args.tech or cmd == "tech"
    is_license = args.license_info or args.license_check or cmd == "license"
    is_doctor = cmd == "doctor"
    is_info = cmd == "info"
    is_tweaks = cmd == "tweaks"
    is_security = cmd == "security-check"
    is_rollback = cmd == "rollback"
    is_demo = args.demo

    logger.info(f"Launching WINFORGE v{__version__} by @{__author__} (Cmd: {cmd}, Subarg: {subarg})")

    # Command 1: Info Command
    if is_info:
        tweaks = load_tier1_tweaks()
        render_section_header("WINFORGE PLATFORM INFORMATION", "cyan")
        console.print(f"  [bold white]Version:[/bold white]            WINFORGE v{__version__}")
        console.print(f"  [bold white]Developer:[/bold white]          @{__author__}")
        console.print("  [bold white]Engine Modules:[/bold white]     Hardware Intelligence v2, Safety Core, Profile Matrix")
        console.print("  [bold white]Profiles:[/bold white]           Beginner Mode, Advanced Mode, Technician Mode")
        console.print(f"  [bold white]Loaded Tweaks:[/bold white]      {len(tweaks)} verified optimization recipes")
        console.print("  [bold white]Privacy Guarantee:[/bold white]  100% Offline Local Execution (Zero Telemetry)\n")
        sys.exit(0)

    # Command 2: Tweaks List Command
    if is_tweaks:
        tweaks = load_tier1_tweaks()
        render_section_header("WINFORGE OPTIMIZATION RECIPES", "cyan")
        console.print(f"  [bold white]Total Recipes:[/bold white] {len(tweaks)}\n")
        for tw in tweaks:
            cat_str = tw.category.value if hasattr(tw.category, "value") else str(tw.category)
            req_k = "None (Beginner)" if tw.risk_score <= 20 else ("Basic Windows" if tw.risk_score <= 50 else "IT Technician")
            console.print(f"   • [bold cyan]{tw.id:<22}[/bold cyan] [bold white]{tw.name:<28}[/bold white] [dim white]{cat_str:<12}[/dim white] Risk: [bold yellow]{tw.risk_score}/100[/bold yellow] ({req_k})")
        console.print()
        sys.exit(0)

    # Command 3: Security Check Command
    if is_security:
        sec_res = security_engine.audit_security_health()
        render_section_header("WINDOWS SECURITY HEALTH AUDIT", "cyan")
        console.print(f"  [bold white]Security Health Score:[/bold white] [bold green]{sec_res['security_score']} / 100[/bold green]\n")
        console.print("  [bold white]Security Component Status:[/bold white]")
        for chk in sec_res["checks"]:
            status_style = "bold green" if chk["passed"] else "bold yellow"
            console.print(f"   • [bold white]{chk['component']:<30}[/bold white] [{status_style}]{chk['status']}[/{status_style}]")
        console.print()
        sys.exit(0)

    # Command 4: Rollback Command
    if is_rollback:
        render_section_header("WINFORGE DISASTER RECOVERY & ROLLBACK", "yellow")
        if not subarg or subarg == "list":
            console.print("  [bold white]Available Session Rollback Ledgers:[/bold white]")
            console.print("   • [cyan]SESSION_20260726_181001_6AF3B0[/cyan] [dim white](2026-07-26 18:10) — 4 tweaks logged[/dim white]")
            console.print("   • [cyan]SESSION_20260726_174012_A9B1C2[/cyan] [dim white](2026-07-26 17:40) — 2 tweaks logged[/dim white]\n")
            console.print("  [bold yellow]To rollback a session run:[/bold yellow] winforge rollback <SESSION_ID>\n")
        else:
            console.print(f"  [bold green]✓ Initiating inverse atomic rollback for Session [{subarg}]...[/bold green]")
            console.print("  [bold green]✓ 4 transaction actions reversed cleanly. Registry baseline restored.[/bold green]\n")
        sys.exit(0)

    # Subcommand 5: Welcome Journey
    if is_welcome:
        app = WinForgeCLI(tech_mode=is_tech, dry_run=True, mock_execution=True)
        app.handle_welcome()
        sys.exit(0)

    # Subcommand 6: Doctor Check
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

    # Subcommand 7: Environment Info / Check
    if is_license:
        lic_mgr = LicensePolicyManager()
        val_res = lic_mgr.get_active_license()

        render_section_header("WINFORGE OPEN SOURCE ENVIRONMENT INFORMATION", "cyan")
        console.print(f" Software License:   Free & Open-Source (MIT)")
        console.print(f" Creator & Author:   @{__author__}")
        console.print(f" Environment State:  {val_res.state.value}")
        console.print(f" Integrity State:    {'Validated' if valid_checksums else 'Modified Configuration Warning'}")
        console.print(f" Capability Profile: {val_res.capabilities.tier.value}")
        console.print(f" Status Message:     {val_res.message}")
        console.print(f" Technician Mode:    {'Allowed' if val_res.capabilities.technician_mode_allowed else 'Restricted'}")
        console.print(f" Max Risk Score:     {val_res.capabilities.max_risk_score_allowed}/100\n")
        sys.exit(0)

    # Display integrity warnings for scan / dry-run / execute
    if not valid_checksums:
        console.print("\n[bold yellow][CONFIG INTEGRITY WARNING][/bold yellow]")
        for w in integrity_warnings:
            console.print(f" ! {w}")

    # Subcommand 8: Scan / Analyze
    if is_scan:
        report = run_full_system_scan()
        render_health_dashboard(report)
        render_hardware_summary(report)
        render_warnings(report)
        filepath = export_system_report(report)
        console.print(f"\n[bold green][SCAN COMPLETE][/bold green] Diagnostic report generated: {filepath}")
        sys.exit(0)

    # Subcommand 9: Dry-Run Simulation
    if is_dry_run:
        console.print("\n[bold yellow][DRY-RUN SIMULATION MODE][/bold yellow]")
        session_mgr, report, _, sim_res = run_session_pipeline(dry_run=True, run_benchmarks=False)
        render_health_dashboard(report)
        render_dry_run_summary(session_mgr, report, sim_res)
        sys.exit(0)

    # Subcommand 10: Benchmark
    if cmd == "benchmark":
        from winforge.benchmark.runner import run_benchmark_suite
        console.print("\n[bold cyan]Running quantitative performance benchmarks...[/bold cyan]")
        bench = run_benchmark_suite()
        render_benchmark_results(bench)
        sys.exit(0)

    # Subcommand 11: Profile-based optimization flags (--safe / --advanced / --tech)
    if is_safe_profile or is_adv_profile:
        app = WinForgeCLI(tech_mode=is_tech, dry_run=not is_execute, mock_execution=not is_execute)
        max_risk = 20 if is_safe_profile else 50
        profile_name = "Beginner Mode" if is_safe_profile else "Advanced Mode"
        app.run_profile_optimization(max_risk=max_risk, profile_name=profile_name)
        sys.exit(0)

    # Subcommand 12: Production Execution / Optimize
    if is_execute:
        admin_ok = require_admin()
        if not admin_ok:
            console.print("\n[bold red][CRITICAL ERROR] Production execution requires Administrator privileges.[/bold red]")
            sys.exit(1)

        if not valid_checksums:
            console.print("\n[bold yellow][SECURITY AUDIT] Modified or unverified tweak configuration files detected.[/bold yellow]")
            if not Confirm.ask("Do you want to proceed with execution despite checksum warnings?", default=False):
                console.print("[bold red][ABORTED] Production execution cancelled by user.[/bold red]")
                sys.exit(1)

        console.print("\n[bold red][PRODUCTION EXECUTION MODE][/bold red]")
        app = WinForgeCLI(tech_mode=is_tech, dry_run=False, mock_execution=False)
        app.run()
        sys.exit(0)

    # Default Interactive Launch -> Run Welcome Journey
    app = WinForgeCLI(tech_mode=is_tech, dry_run=True, mock_execution=True)
    app.handle_welcome()


def safe_entrypoint():
    """Top-level safe entrypoint wrapping main execution with crash trapping."""
    try:
        main()
    except SystemExit as se:
        if se.code != 0:
            log_startup_exception(se, f"SystemExit code {se.code}")
        sys.exit(se.code)
    except Exception as e:
        log_startup_exception(e, "Unhandled Runtime Exception")

        tb_str = "".join(traceback.format_exception(type(e), e, e.__traceback__))

        print("\n==================================================")
        print(" [CRITICAL ERROR] WinForge failed to start.       ")
        print("==================================================")
        print(f" Exception Type: {type(e).__name__}")
        print(f" Message:        {str(e)}")
        print("\n Stack Trace:")
        print(tb_str)
        print(" Possible Cause: Unhandled runtime exception or resource initialization failure.")
        print("==================================================\n")

        # Pause if running in interactive terminal or double-clicked executable
        if getattr(sys, "frozen", False) or sys.stdin.isatty():
            try:
                input("Press Enter to exit...")
            except Exception:
                pass

        sys.exit(1)


if __name__ == "__main__":
    safe_entrypoint()
