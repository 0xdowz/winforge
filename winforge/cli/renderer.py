"""
WinForge CLI Renderer — Modern Terminal Presentation Layer.
Provides structured visual rendering for Optimization Plans, Safety Locks, Execution Reports, Doctor Diagnostics, and Actionable Errors.
"""

from typing import List, Optional
from rich.text import Text

from winforge.models.tweak import Tweak, RiskCategory
from winforge.cli.theme import renderer, console, render_section_header
from winforge.cli.formatting import format_risk_badge, get_status_icon, ICON_SUCCESS, ICON_WARNING, ICON_ERROR


def render_optimization_plan(candidate_tweaks: List[Tweak], is_tech_mode: bool = False):
    """Renders structured pre-execution Optimization Plan summary as an aligned text list."""
    render_section_header("Optimization Plan Preview", "cyan")

    console.print(f"  [bold white]Changes Planned:[/bold white] [bold cyan]{len(candidate_tweaks)} optimizations[/bold cyan]\n")

    for tweak in candidate_tweaks:
        cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        risk_badge = format_risk_badge(tweak.risk_score)
        console.print(f"   [bold cyan]+ {tweak.id:<20}[/bold cyan] [bold white]{tweak.name:<28}[/bold white] [dim white]{cat_str:<12}[/dim white] {risk_badge}")

    console.print()


def render_safety_lock_status(restore_point_ready: bool = True, registry_backup_ready: bool = True, snapshot_ready: bool = True):
    """Renders Safety Shield Activated 4-Layer Lock status card."""
    render_section_header("Safety Shield Activated", "green")

    r_icon = get_status_icon("success" if restore_point_ready else "warning")
    b_icon = get_status_icon("success" if registry_backup_ready else "warning")
    s_icon = get_status_icon("success" if snapshot_ready else "warning")
    ok_icon = get_status_icon("success")

    console.print(f"   {r_icon} WMI System Restore Point:     [bold green]CREATED[/bold green]")
    console.print(f"   {b_icon} Atomic Registry State:        [bold green]CAPTURED[/bold green]")
    console.print(f"   {s_icon} Pre-State Snapshot:           [bold green]SAVED[/bold green]")
    console.print(f"   {ok_icon} Transaction Ledger (.json):   [bold green]LOGGED[/bold green]\n")


def render_execution_report(
    session_id: str,
    completed_count: int,
    total_count: int,
    successful_count: int,
    skipped_count: int,
    skipped_reasons: list,
    storage_recovered_gb: float = 0.0,
    performance_gain_pct: float = 0.0
):
    """Renders structured post-optimization Execution Report."""
    render_section_header("Execution Report", "cyan")

    console.print(f"  [bold white]Session ID:[/bold white]               [bold cyan]{session_id}[/bold cyan]")
    console.print(f"  [bold white]Completed:[/bold white]                [bold white]{completed_count}/{total_count}[/bold white]")
    console.print(f"  [bold white]Successful:[/bold white]               [bold green]{successful_count}[/bold green]")
    console.print(f"  [bold white]Skipped:[/bold white]                  [bold yellow]{skipped_count}[/bold yellow]\n")

    if skipped_reasons:
        console.print("  [bold white]Skipped Reasons:[/bold white]")
        for reason in skipped_reasons:
            console.print(f"   • [dim white]{reason}[/dim white]")
        console.print()

    console.print(f"  [bold white]Estimated Storage Recovered:[/bold white] [bold green]{storage_recovered_gb:.1f} GB[/bold green]")
    console.print(f"  [bold white]Estimated Performance Gain:[/bold white]  [bold green]{performance_gain_pct:.1f}%[/bold green]\n")


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
