"""
WinForge CLI Renderer — Modern Terminal Presentation Layer.
Provides structured visual rendering for Optimization Plans, Safety Locks, Doctor Diagnostics, and Actionable Errors.
"""

from typing import List, Optional
from rich.text import Text

from winforge.models.tweak import Tweak, RiskCategory
from winforge.cli.theme import renderer, console, render_section_header
from winforge.cli.formatting import format_risk_badge, get_status_icon, ICON_SUCCESS, ICON_WARNING, ICON_ERROR


def render_optimization_plan(candidate_tweaks: List[Tweak], is_tech_mode: bool = False):
    """Renders structured pre-execution Optimization Plan summary as an aligned text list."""
    render_section_header("Optimization Preview", "cyan")

    console.print(f"  [bold white]Changes Planned:[/bold white] [bold cyan]{len(candidate_tweaks)} optimizations[/bold cyan]\n")

    for tweak in candidate_tweaks:
        cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        risk_badge = format_risk_badge(tweak.risk_score)
        console.print(f"   [bold cyan]+ {tweak.id:<20}[/bold cyan] [bold white]{tweak.name:<28}[/bold white] [dim white]{cat_str:<12}[/dim white] {risk_badge}")

    console.print()


def render_safety_lock_status(restore_point_ready: bool = True, registry_backup_ready: bool = True, snapshot_ready: bool = True):
    """Renders 4-Layer Safety Lock verification status."""
    render_section_header("Safety Verification", "green")

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
    """Renders concise 3-part Action Blocked error header without oversized panels."""
    render_section_header("Action Blocked / Execution Error", "red")

    console.print("  [bold white]Problem:[/bold white]")
    console.print(f"   [bold red]{title}[/bold red]\n")

    console.print("  [bold white]Why It Happened:[/bold white]")
    console.print(f"   [bold yellow]{reason}[/bold yellow]\n")

    console.print("  [bold white]Suggested Solution:[/bold white]")
    console.print(f"   [bold green]{suggested_action}[/bold green]\n")


def render_doctor_report(is_admin: bool, os_product: str, cpu_name: str, ram_gb: float, safety_ok: bool = True):
    """Renders System Health & Environment Doctor Diagnostic Report as an aligned text list."""
    render_section_header("WinForge Doctor", "cyan")

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
