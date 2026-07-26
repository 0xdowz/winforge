"""
WinForge CLI Renderer — Modern Terminal Presentation Layer.
Provides structured visual rendering for Optimization Plans, Safety Locks, Doctor Diagnostics, and Actionable Errors.
"""

from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from winforge.models.tweak import Tweak, RiskCategory
from winforge.cli.components import console
from winforge.cli.formatting import format_risk_badge, get_status_icon, ICON_SUCCESS, ICON_WARNING, ICON_ERROR


def render_optimization_plan(candidate_tweaks: List[Tweak], is_tech_mode: bool = False):
    """Renders structured pre-execution Optimization Plan summary as an aligned text list."""
    console.print()
    console.print(Rule("[bold white]Optimization Preview[/bold white]", style="dim cyan"))
    console.print()

    console.print(f"  [bold white]Changes Planned:[/bold white] [bold cyan]{len(candidate_tweaks)} optimizations[/bold cyan]\n")

    for tweak in candidate_tweaks:
        cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        risk_badge = format_risk_badge(tweak.risk_score)
        console.print(f"   [bold cyan]+ {tweak.id:<20}[/bold cyan] [bold white]{tweak.name:<28}[/bold white] [dim white]{cat_str:<12}[/dim white] {risk_badge}")

    console.print()


def render_safety_lock_status(restore_point_ready: bool = True, registry_backup_ready: bool = True, snapshot_ready: bool = True):
    """Renders 4-Layer Safety Lock verification status."""
    console.print(Rule("[bold white]Safety Verification[/bold white]", style="dim green"))
    console.print()

    r_icon = get_status_icon("success" if restore_point_ready else "warning")
    b_icon = get_status_icon("success" if registry_backup_ready else "warning")
    s_icon = get_status_icon("success" if snapshot_ready else "warning")
    ok_icon = get_status_icon("success")

    r_msg = "[bold green]CREATED[/bold green]" if restore_point_ready else "[bold yellow]SKIPPED (SIMULATION)[/bold yellow]"
    b_msg = "[bold green]CREATED[/bold green]" if registry_backup_ready else "[bold yellow]SKIPPED (SIMULATION)[/bold yellow]"
    s_msg = "[bold green]RECORDED[/bold green]" if snapshot_ready else "[bold yellow]SKIPPED[/bold yellow]"

    console.print(f"   {r_icon} WMI System Restore Point:     {r_msg}")
    console.print(f"   {b_icon} Atomic Registry Export:       {b_msg}")
    console.print(f"   {s_icon} System Pre-State Snapshot:   {s_msg}")
    console.print(f"   {ok_icon} Transaction Ledger (.json):   [bold green]LOGGED[/bold green]\n")


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
    """Renders System Health & Environment Doctor Diagnostic Report as an aligned text list."""
    console.print()
    console.print(Rule("[bold white]WinForge Doctor[/bold white]", style="dim cyan"))
    console.print()

    admin_icon = get_status_icon("success" if is_admin else "warning")
    admin_msg = "[bold green]Active[/bold green]" if is_admin else "[bold yellow]Run as Administrator required[/bold yellow]"
    safety_icon = get_status_icon("success" if safety_ok else "warning")
    safety_msg = "[bold green]Ready[/bold green] (Restore points & atomic registry export ready)" if safety_ok else "[bold yellow]Degraded[/bold yellow]"

    console.print("  [bold white]Environment[/bold white]")
    console.print(f"   {get_status_icon('success')} Operating System: {os_product}")
    console.print(f"   {admin_icon} Administrator:    {admin_msg}\n")

    console.print("  [bold white]System Readiness[/bold white]")
    console.print(f"   {get_status_icon('success')} Processor (CPU):  {cpu_name}")
    console.print(f"   {get_status_icon('success')} System Memory:    {ram_gb} GB Installed")
    console.print(f"   {safety_icon} Safety Engine:    {safety_msg}\n")
