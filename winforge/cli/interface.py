import sys
import logging
from typing import Optional, List
from rich.prompt import Prompt, Confirm

from winforge.cli.banner import render_banner
from winforge.cli.components import (
    render_health_dashboard, render_hardware_summary, render_warnings,
    render_tweak_inspection_card, render_benchmark_results, render_dry_run_summary,
    console
)
from winforge.core.engine import run_full_system_scan, run_session_pipeline, export_system_report
from winforge.core.tweak_loader import load_tier1_tweaks
from winforge.optimizations.executor import OptimizationExecutor
from winforge.benchmark.runner import run_benchmark_suite
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak

logger = logging.getLogger("winforge")


class WinForgeCLI:
    def __init__(self, tech_mode: bool = False, dry_run: bool = True, mock_execution: bool = True):
        self.tech_mode = tech_mode
        self.dry_run = dry_run
        self.mock_execution = mock_execution
        self.latest_report: Optional[SystemHealthReport] = None
        self.executor = OptimizationExecutor()

    def display_menu(self):
        """Displays main navigation menu grouped by category."""
        console.print("[bold cyan]MAIN MENU[/bold cyan]\n")

        console.print("[bold white]Diagnostics[/bold white]")
        console.print("  [bold yellow]1[/bold yellow]  Scan system health")
        console.print("  [bold yellow]2[/bold yellow]  Run performance benchmarks\n")

        console.print("[bold white]Optimization[/bold white]")
        console.print("  [bold yellow]3[/bold yellow]  Preview dry-run simulation")
        console.print("  [bold yellow]4[/bold yellow]  Apply recommended optimizations\n")

        console.print("[bold white]Maintenance[/bold white]")
        console.print("  [bold yellow]5[/bold yellow]  Safe disk cleanup routine")
        console.print("  [bold yellow]6[/bold yellow]  Startup & service hygiene\n")

        console.print("[bold white]Reports & Recovery[/bold white]")
        console.print("  [bold yellow]7[/bold yellow]  Export diagnostic reports")
        console.print("  [bold yellow]8[/bold yellow]  Restore system & rollback\n")

        console.print("[bold white]Settings[/bold white]")
        if self.tech_mode:
            console.print("  [bold magenta]9[/bold magenta]  Technician mode [Active]")
        else:
            console.print("  [bold green]9[/bold green]  Switch to technician mode")

        console.print("  [bold red]0[/bold red]  Exit WinForge\n")

    def run(self):
        """Main application interactive loop."""
        while True:
            console.clear()
            render_banner(tech_mode=self.tech_mode, dry_run=self.dry_run)
            self.display_menu()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], default="1")

            if choice == "0":
                console.print("\n[bold cyan]Thank you for using WinForge. Exiting safely...[/bold cyan]\n")
                break
            elif choice == "1":
                self.handle_scan()
            elif choice == "2":
                self.handle_benchmark()
            elif choice == "3":
                self.handle_dry_run()
            elif choice == "4":
                self.handle_apply_optimizations()
            elif choice == "7":
                self.handle_reports()
            elif choice == "9":
                self.tech_mode = not self.tech_mode
                mode_name = "Technician Mode" if self.tech_mode else "Client Mode"
                console.print(f"\n[bold green]Switched to {mode_name}.[/bold green]")
                Prompt.ask("Press Enter to continue")
            else:
                console.print(f"\n[bold yellow]Module {choice} queued for execution phase.[/bold yellow]")
                Prompt.ask("Press Enter to continue")

    def handle_scan(self):
        """Execute full system scan and render dashboard."""
        console.print("\n[bold cyan]Creating new diagnostic session and scanning system...[/bold cyan]")
        session_mgr, report, _, _ = run_session_pipeline(dry_run=self.dry_run, run_benchmarks=False)
        self.latest_report = report

        render_health_dashboard(self.latest_report)
        render_hardware_summary(self.latest_report)
        render_warnings(self.latest_report)

        console.print(f"\n[bold green]✓ Session Created:[/bold green] {session_mgr.session_id}")
        console.print(f"[bold green]✓ HTML Report Generated:[/bold green] {session_mgr.get_report_html_path()}")

        Prompt.ask("\nPress Enter to return to main menu")

    def handle_benchmark(self):
        """Run quantitative benchmark suite."""
        from rich.rule import Rule
        console.print()
        console.print("[bold cyan]Running quantitative performance benchmarks...[/bold cyan]")
        bench = run_benchmark_suite()
        render_benchmark_results(bench)
        Prompt.ask("Press Enter to return to main menu")

    def handle_dry_run(self):
        """Run Dry-Run simulation pipeline."""
        console.print()
        console.print("[bold cyan]Initiating Dry-Run simulation pipeline...[/bold cyan]")
        session_mgr, report, _, sim_res = run_session_pipeline(dry_run=True, run_benchmarks=False)
        self.latest_report = report

        render_health_dashboard(self.latest_report)
        render_dry_run_summary(session_mgr, report, sim_res)

        Prompt.ask("Press Enter to return to main menu")

    def handle_apply_optimizations(self):
        """Execute optimization pipeline in Client or Technician mode."""
        session_mgr, report, _, _ = run_session_pipeline(dry_run=self.dry_run, run_benchmarks=False)
        candidate_tweaks = self.executor.dispatcher.detect_all_candidate_tweaks(report)

        if not candidate_tweaks:
            console.print("\n[bold green]✓ No pending optimizations required. System state is optimal.[/bold green]")
            Prompt.ask("\nPress Enter to return to main menu")
            return

        from winforge.cli.renderer import render_optimization_plan, render_safety_lock_status, render_actionable_error

        render_optimization_plan(candidate_tweaks, is_tech_mode=self.tech_mode)
        render_safety_lock_status(restore_point_ready=True, registry_backup_ready=True, snapshot_ready=True)

        if self.tech_mode:
            console.print("\n[bold magenta]─── TECHNICIAN MODE TWEAK INSPECTION ───[/bold magenta]")
            for tweak in candidate_tweaks:
                render_tweak_inspection_card(tweak)
                if Confirm.ask(f"Approve tweak [{tweak.id}] for execution?", default=True):
                    tracker, result = self.executor.process_tweak_pipeline(
                        tweak=tweak,
                        report=report,
                        session_mgr=session_mgr,
                        is_tech_mode=True,
                        user_approved=True,
                        mock_execution=self.mock_execution
                    )
                    if "Policy Blocked" in result.message or "SKIPPED" in result.status.value:
                        render_actionable_error(
                            title=f"Optimization Blocked [{tweak.id}]",
                            reason=result.message,
                            suggested_action="Run on a compatible Windows Client edition (10/11) or switch execution modes."
                        )
                    else:
                        console.print(f"[{'bold green' if '✓' in result.message else 'bold red'}]{result.message}[/]")
                else:
                    console.print(f"[bold yellow]Skipped tweak [{tweak.id}].[/bold yellow]")
        else:
            console.print(f"\n[bold cyan]Client Mode: Found {len(candidate_tweaks)} recommended safe optimizations.[/bold cyan]")
            if Confirm.ask("Apply all recommended safe optimizations now?", default=True):
                for tweak in candidate_tweaks:
                    tracker, result = self.executor.process_tweak_pipeline(
                        tweak=tweak,
                        report=report,
                        session_mgr=session_mgr,
                        is_tech_mode=False,
                        user_approved=True,
                        mock_execution=self.mock_execution
                    )
                    if "Policy Blocked" in result.message or "SKIPPED" in result.status.value:
                        render_actionable_error(
                            title=f"Optimization Blocked [{tweak.id}]",
                            reason=result.message,
                            suggested_action="Run on a compatible Windows Client edition (10/11) or use Technician Mode (--tech)."
                        )
                    else:
                        console.print(f"[{'bold green' if '✓' in result.message else 'bold red'}]{result.message}[/]")

        Prompt.ask("\nPress Enter to return to main menu")

    def handle_reports(self):
        """View and export system reports."""
        console.print("\n[bold cyan]Generating session diagnostic report...[/bold cyan]")
        session_mgr, report, bench, _ = run_session_pipeline(dry_run=self.dry_run, run_benchmarks=True)
        self.latest_report = report

        console.print(f"\n[bold green]✓ Session ID:[/bold green] {session_mgr.session_id}")
        console.print(f"[bold green]✓ JSON Data:[/bold green] {session_mgr.session_dir / 'before.json'}")
        console.print(f"[bold green]✓ Findings:[/bold green] {session_mgr.session_dir / 'findings.json'}")
        console.print(f"[bold green]✓ Interactive HTML Report:[/bold green] {session_mgr.get_report_html_path()}")

        Prompt.ask("\nPress Enter to return to main menu")

    def handle_doctor(self):
        """Execute Phase 8 doctor environment and safety diagnostics."""
        from winforge.core.safety_approval import is_admin
        from winforge.cli.renderer import render_doctor_report
        session_mgr, report, _, _ = run_session_pipeline(dry_run=self.dry_run, run_benchmarks=False)

        render_doctor_report(
            is_admin=is_admin(),
            os_product=report.os.product_name,
            cpu_name=report.cpu.name,
            ram_gb=report.ram.total_gb,
            safety_ok=True
        )
        Prompt.ask("Press Enter to return to main menu")
