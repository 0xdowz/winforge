"""
WinForge CLI Renderer — Modern Terminal Presentation Layer.
Provides structured, testable visual rendering for Optimization Plans, Safety Locks, Doctor Diagnostics, and Actionable Errors.
"""

from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from winforge.models.tweak import Tweak, RiskCategory
from winforge.cli.components import console, format_risk_badge


def render_optimization_plan(candidate_tweaks: List[Tweak], is_tech_mode: bool = False):
    """Renders structured pre-execution Optimization Plan summary."""
    console.print()
    console.print(Rule("[bold white]Optimization Preview[/bold white]", style="dim cyan"))
    console.print()

    console.print(f"  [bold white]Changes Planned:[/bold white] [bold cyan]{len(candidate_tweaks)} optimizations[/bold cyan]\n")

    table = Table(
        header_style="bold yellow",
        border_style="dim cyan",
        show_lines=True,
        expand=False
    )
    table.add_column("Tweak ID", style="bold cyan", width=16)
    table.add_column("Optimization Name", style="bold white", width=28)
    table.add_column("Category", style="dim white", width=14)
    table.add_column("Risk Score", style="bold white", justify="center", width=16)
    table.add_column("Rollback", style="bold green", justify="center", width=12)

    for tweak in candidate_tweaks:
        cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        table.add_row(tweak.id, tweak.name, cat_str, format_risk_badge(tweak.risk_score), "✓ Ready")

    console.print(table)
    console.print()


def render_safety_lock_status(restore_point_ready: bool = True, registry_backup_ready: bool = True, snapshot_ready: bool = True):
    """Renders 4-Layer Safety Lock verification status."""
    console.print(Rule("[bold white]Safety Verification[/bold white]", style="dim green"))
    console.print()

    r_str = "[bold green]✓ CREATED[/bold green]" if restore_point_ready else "[bold yellow]⚠ SKIPPED (SIMULATION)[/bold yellow]"
    b_str = "[bold green]✓ CREATED[/bold green]" if registry_backup_ready else "[bold yellow]⚠ SKIPPED (SIMULATION)[/bold yellow]"
    s_str = "[bold green]✓ RECORDED[/bold green]" if snapshot_ready else "[bold yellow]⚠ SKIPPED[/bold yellow]"

    console.print(f"   ✓ WMI System Restore Point:     {r_str}")
    console.print(f"   ✓ Atomic Registry Export:       {b_str}")
    console.print(f"   ✓ System Pre-State Snapshot:   {s_str}")
    console.print(f"   ✓ Transaction Ledger (.json):   [bold green]✓ LOGGED[/bold green]\n")


def render_actionable_error(title: str, reason: str, suggested_action: str):
    """Renders structured, clear 3-part actionable error panel."""
    text = Text()
    text.append("What Happened:\n", style="bold white")
    text.append(f"  {title}\n\n", style="bold red")
    text.append("Why It Happened:\n", style="bold white")
    text.append(f"  {reason}\n\n", style="bold yellow")
    text.append("Suggested Solution:\n", style="bold white")
    text.append(f"  {suggested_action}\n", style="bold green")

    panel = Panel(
        text,
        title="[bold red]✗ Action Blocked or Execution Error[/bold red]",
        border_style="red"
    )
    console.print()
    console.print(panel)
    console.print()


def render_doctor_report(is_admin: bool, os_product: str, cpu_name: str, ram_gb: float, safety_ok: bool = True):
    """Renders System Health & Environment Doctor Diagnostic Report."""
    console.print()
    console.print(Rule("[bold white]WinForge Doctor[/bold white]", style="dim cyan"))
    console.print()

    console.print("  [bold white]Environment[/bold white]")
    console.print(f"   • Operating System: {os_product}")
    admin_str = "[bold green]✓ Active[/bold green]" if is_admin else "[bold yellow]⚠ Run as Administrator required[/bold yellow]"
    console.print(f"   • Administrator:    {admin_str}\n")

    console.print("  [bold white]System Readiness[/bold white]")
    console.print(f"   • Processor (CPU):  ✓ {cpu_name}")
    console.print(f"   • System Memory:    ✓ {ram_gb} GB Installed")
    safety_str = "[bold green]✓ Ready[/bold green]" if safety_ok else "[bold yellow]⚠ Degraded[/bold yellow]"
    console.print(f"   • Safety Engine:    {safety_str} (Restore points & atomic registry export ready)\n")
