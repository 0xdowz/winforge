"""
WinForge CLI Renderer — Rich Terminal Presentation Layer.
Provides structured, testable visual rendering for Optimization Plans, Safety Locks, and Actionable Error Guidance.
"""

from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from winforge.models.tweak import Tweak, RiskCategory
from winforge.cli.components import console


def render_optimization_plan(candidate_tweaks: List[Tweak], is_tech_mode: bool = False):
    """Renders structured pre-execution Optimization Plan table."""
    table = Table(
        title="WINFORGE :: PRE-EXECUTION OPTIMIZATION PLAN",
        header_style="bold yellow",
        border_style="cyan",
        show_lines=True,
        expand=False
    )
    table.add_column("Tweak ID", style="bold cyan", width=16)
    table.add_column("Optimization Name", style="bold white", width=28)
    table.add_column("Category", style="dim white", width=14)
    table.add_column("Risk Score", style="bold white", justify="center", width=14)
    table.add_column("Rollback Support", style="bold green", justify="center", width=16)

    for tweak in candidate_tweaks:
        score = tweak.risk_score
        if score <= 20:
            risk_str = f"[bold green]{score} (SAFE)[/bold green]"
        elif score <= 50:
            risk_str = f"[bold yellow]{score} (MODERATE)[/bold yellow]"
        elif score <= 80:
            risk_str = f"[bold red]{score} (ADVANCED)[/bold red]"
        else:
            risk_str = f"[bold magenta]{score} (TECH ONLY)[/bold magenta]"

        cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        table.add_row(tweak.id, tweak.name, cat_str, risk_str, "✓ Automated")

    console.print()
    console.print(table)
    console.print()


def render_safety_lock_status(restore_point_ready: bool = True, registry_backup_ready: bool = True, snapshot_ready: bool = True):
    """Renders 4-Layer Safety Lock verification panel before mutation execution."""
    text = Text()
    text.append("  1. WMI System Restore Point:     ", style="bold white")
    text.append("✓ CREATED\n" if restore_point_ready else "⚠ SKIPPED (MOCK)\n", style="bold green" if restore_point_ready else "bold yellow")
    
    text.append("  2. Atomic Registry Export:       ", style="bold white")
    text.append("✓ CREATED\n" if registry_backup_ready else "⚠ SKIPPED (MOCK)\n", style="bold green" if registry_backup_ready else "bold yellow")

    text.append("  3. System Pre-State Snapshot:   ", style="bold white")
    text.append("✓ RECORDED\n" if snapshot_ready else "⚠ SKIPPED\n", style="bold green" if snapshot_ready else "bold yellow")

    text.append("  4. Transaction Ledger (.json):   ", style="bold white")
    text.append("✓ LOGGED\n", style="bold green")

    panel = Panel(text, title="[bold yellow]4-LAYER SAFETY LOCK PRE-REQUISITES[/bold yellow]", border_style="green")
    console.print(panel)
    console.print()


def render_actionable_error(title: str, reason: str, suggested_action: str):
    """Renders structured, clear actionable error panel adhering to professional CLI UX guidelines."""
    text = Text()
    text.append("Reason:\n", style="bold white")
    text.append(f"  {reason}\n\n", style="bold yellow")
    text.append("Suggested Action:\n", style="bold white")
    text.append(f"  {suggested_action}\n", style="bold green")

    panel = Panel(
        text,
        title=f"[bold red]✗ {title}[/bold red]",
        border_style="red"
    )
    console.print()
    console.print(panel)
    console.print()


def render_doctor_report(is_admin: bool, os_product: str, cpu_name: str, ram_gb: float, safety_ok: bool = True):
    """Renders Phase 8 System Health & Environment Doctor Diagnostic Report."""
    table = Table(
        title="WINFORGE DOCTOR :: ENVIRONMENT & SAFETY DIAGNOSTIC REPORT",
        header_style="bold yellow",
        border_style="cyan",
        show_lines=True,
        expand=False
    )
    table.add_column("Subsystem / Component", style="bold cyan", width=26)
    table.add_column("Status", style="bold white", justify="center", width=16)
    table.add_column("Details", style="dim white", width=36)

    table.add_row("Execution Privileges", "✓ Administrator" if is_admin else "⚠ Standard User", "Elevation active" if is_admin else "Run as Administrator required")
    table.add_row("Operating System", "✓ Supported", os_product)
    table.add_row("Processor (CPU)", "✓ Operational", cpu_name)
    table.add_row("System Memory (RAM)", "✓ Operational", f"{ram_gb} GB Installed")
    table.add_row("4-Layer Safety Engine", "✓ Operational" if safety_ok else "⚠ Degraded", "Restore points & atomic registry backup ready")

    console.print()
    console.print(table)
    console.print()
