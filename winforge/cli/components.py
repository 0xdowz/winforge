import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak

console = Console()


def render_health_dashboard(report: SystemHealthReport):
    """Renders high-level System Health Scorecard dashboard."""
    score = round(report.health_score, 1)

    # Determine color badge
    if score >= 85:
        score_color = "bold green"
        badge = "OPTIMAL STATE"
    elif score >= 70:
        score_color = "bold yellow"
        badge = "NEEDS TUNING"
    else:
        score_color = "bold red"
        badge = "CRITICAL DEGRADATION"

    # Safe progress bar visual
    total_blocks = 20
    filled_blocks = int((score / 100.0) * total_blocks)
    bar_str = "=" * filled_blocks + "." * (total_blocks - filled_blocks)

    dashboard_text = Text()
    dashboard_text.append(f"  SYSTEM HEALTH SCORE: ", style="bold white")
    dashboard_text.append(f"{score}/100 ", style=score_color)
    dashboard_text.append(f"[{badge}]\n", style=score_color)
    dashboard_text.append(f"  HEALTH INDEX: ", style="bold white")
    dashboard_text.append(f"[{bar_str}] {score}%\n\n", style=score_color)

    dashboard_text.append("  CATEGORY BREAKDOWN:\n", style="bold cyan")
    dashboard_text.append(f"  * Performance Score:           {round(report.categories.performance_score, 1)}/100\n", style="bold white")
    dashboard_text.append(f"  * Security & Privacy Score:    {round(report.categories.security_score, 1)}/100\n", style="bold white")
    dashboard_text.append(f"  * Maintenance & Cleanliness:  {round(report.categories.maintenance_score, 1)}/100\n", style="bold white")
    dashboard_text.append(f"  * Startup & Service Hygiene:   {round(report.categories.startup_score, 1)}/100\n", style="bold white")

    panel = Panel(
        dashboard_text,
        title="[bold yellow]WINFORGE :: SYSTEM HEALTH DASHBOARD[/bold yellow]",
        border_style="cyan"
    )
    console.print("\n")
    console.print(panel)


def render_hardware_summary(report: SystemHealthReport):
    """Renders hardware specification table."""
    table = Table(title="DIAGNOSTIC HARDWARE SPECIFICATION", header_style="bold yellow", border_style="blue")
    table.add_column("Component", style="bold cyan", width=22)
    table.add_column("Specification Details", style="bold white")

    table.add_row("Operating System", f"{report.os.product_name} ({report.os.architecture}) [Build {report.os.build_number}]")
    table.add_row("Processor (CPU)", f"{report.cpu.name} ({report.cpu.logical_cores} Cores)")

    gpu_name = report.gpu[0].name if report.gpu else "Generic Display Adapter"
    gpu_driver = report.gpu[0].driver_version if report.gpu else "Unknown"
    table.add_row("Graphics (GPU)", f"{gpu_name} (Driver: {gpu_driver})")

    table.add_row("System Memory (RAM)", f"{report.ram.total_gb} GB Installed")

    storage_str = ", ".join([f"{d.drive_letter} ({d.free_gb}/{d.total_gb} GB Free)" for d in report.drives])
    table.add_row("Storage Drives", storage_str if storage_str else "N/A")
    table.add_row("Active Power Plan", f"{report.power.active_name} ({'On Battery' if report.power.is_on_battery else 'AC Power'})")

    console.print("\n")
    console.print(table)


def render_warnings(report: SystemHealthReport):
    """Renders detected system warnings panel."""
    if not report.warnings:
        console.print("\n[bold green]Zero critical system degradation issues detected.[/bold green]")
        return

    text = Text()
    for warning in report.warnings:
        text.append(f"  ! {warning}\n", style="bold yellow")

    panel = Panel(text, title="[bold yellow]DETECTED SYSTEM DEGRADATION WARNINGS[/bold yellow]", border_style="yellow")
    console.print("\n")
    console.print(panel)


def render_tweak_inspection_card(tweak: Tweak):
    """Renders detailed Technician Mode Tweak Inspection Card."""
    table = Table(title=f"TWEAK INSPECTION CARD :: [{tweak.id}]", header_style="bold yellow", border_style="magenta")
    table.add_column("Property", style="bold cyan", width=24)
    table.add_column("Specification / Details", style="bold white")

    table.add_row("Tweak Name", tweak.name)
    table.add_row("Category", tweak.category.value if hasattr(tweak.category, 'value') else str(tweak.category))
    table.add_row("Description", tweak.description)

    # Risk badge formatting
    score = tweak.risk_score
    if score <= 20:
        risk_str = f"[bold green]{score}/100 (SAFE)[/bold green]"
    elif score <= 50:
        risk_str = f"[bold yellow]{score}/100 (MODERATE)[/bold yellow]"
    elif score <= 80:
        risk_str = f"[bold red]{score}/100 (ADVANCED)[/bold red]"
    else:
        risk_str = f"[bold magenta]{score}/100 (TECHNICIAN ONLY)[/bold magenta]"

    table.add_row("Risk Rating", risk_str)
    table.add_row("Performance Gain", str(tweak.performance_gain_estimate))
    table.add_row("User Visible Impact", str(tweak.user_visible_change))
    table.add_row("Rollback Method", tweak.rollback_method.get("type", "Automated inverse action").upper())
    table.add_row("Required Elevation", "Administrator Privileges Required" if tweak.requires_admin else "Standard User")

    console.print("\n")
    console.print(table)
