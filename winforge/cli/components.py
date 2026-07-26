"""
WinForge CLI Components — Modern Terminal Presentation Library.
Provides clean visual hierarchy, section dividers, status badges, and hardware tables.
Enforces max 90-column width for clean rendering across CMD, PowerShell, and Windows Terminal.
"""

import shutil
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.rule import Rule

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak
from winforge.cli.formatting import format_status_badge, format_risk_badge

# Cap width to 90 columns for perfect rendering in CMD / PowerShell
_term_width = min(shutil.get_terminal_size((80, 24)).columns, 90)
console = Console(width=_term_width)


def _section_rule(label: str, style: str = "dim cyan"):
    """Prints a clean visual section separator rule."""
    console.print()
    console.print(Rule(f"[bold white]{label}[/bold white]", style=style))
    console.print()


def render_health_dashboard(report: SystemHealthReport):
    """Renders clean, structured System Health Overview."""
    score = round(report.health_score, 1)

    if score >= 85:
        score_style = "bold green"
        badge_text = "OPTIMAL"
    elif score >= 70:
        score_style = "bold yellow"
        badge_text = "NEEDS ATTENTION"
    else:
        score_style = "bold red"
        badge_text = "CRITICAL"

    _section_rule("System Health Overview", "dim cyan")

    console.print("  Health Score:")
    console.print(f"  [bold white]{score} / 100[/bold white]  [{score_style}]{badge_text}[/{score_style}]\n")

    console.print("  Category Breakdown:")
    
    perf = round(report.categories.performance_score, 1)
    sec = round(report.categories.security_score, 1)
    maint = round(report.categories.maintenance_score, 1)
    start = round(report.categories.startup_score, 1)

    p_icon = "[green]✓[/green]" if perf >= 80 else "[yellow]⚠[/yellow]"
    s_icon = "[green]✓[/green]" if sec >= 80 else "[yellow]⚠[/yellow]"
    m_icon = "[green]✓[/green]" if maint >= 80 else "[yellow]⚠[/yellow]"
    st_icon = "[green]✓[/green]" if start >= 80 else "[yellow]⚠[/yellow]"

    console.print(f"   {p_icon} Performance Score:          {perf} / 100")
    console.print(f"   {s_icon} Security & Privacy:         {sec} / 100")
    console.print(f"   {m_icon} Maintenance & Cleanliness: {maint} / 100")
    console.print(f"   {st_icon} Startup & Service Hygiene:  {start} / 100")


def render_hardware_summary(report: SystemHealthReport):
    """Renders hardware specification table with sleek layout."""
    _section_rule("Hardware Specification", "dim cyan")

    table = Table(
        header_style="bold yellow",
        border_style="dim cyan",
        expand=False,
        show_lines=False,
    )
    table.add_column("Component", style="bold cyan", width=22, no_wrap=True)
    table.add_column("Specification Details", style="bold white", max_width=58)

    table.add_row("Operating System", f"{report.os.product_name} ({report.os.architecture}) [Build {report.os.build_number}]")
    table.add_row("Processor (CPU)", f"{report.cpu.name} ({report.cpu.logical_cores} Cores)")

    gpu_name = report.gpu[0].name if report.gpu else "Generic Display Adapter"
    gpu_driver = report.gpu[0].driver_version if report.gpu else "Unknown"
    table.add_row("Graphics (GPU)", f"{gpu_name} (Driver: {gpu_driver})")

    table.add_row("System Memory (RAM)", f"{report.ram.total_gb} GB Installed")

    storage_parts = [f"{d.drive_letter} ({d.free_gb}/{d.total_gb} GB Free)" for d in report.drives]
    storage_str = "  ".join(storage_parts) if storage_parts else "N/A"
    table.add_row("Storage Drives", storage_str)
    table.add_row("Active Power Plan", f"{report.power.active_name} ({'On Battery' if report.power.is_on_battery else 'AC Power'})")

    console.print(table)


def render_warnings(report: SystemHealthReport):
    """Renders concise system degradation warnings list."""
    _section_rule("Detected System Issues", "dim yellow")

    if not report.warnings:
        console.print("  [bold green]✓ Zero critical system degradation issues detected.[/bold green]\n")
        return

    for warning in report.warnings:
        console.print(f"  [bold yellow]⚠  {warning}[/bold yellow]")
    console.print()


def render_benchmark_results(bench):
    """Renders quantitative performance benchmark table."""
    _section_rule("Performance Benchmark Results", "dim cyan")

    table = Table(
        header_style="bold yellow",
        border_style="dim cyan",
        show_lines=True,
        expand=False,
    )
    table.add_column("Benchmark Metric", style="bold cyan", width=30, no_wrap=True)
    table.add_column("Result", style="bold white", justify="right", width=16)
    table.add_column("Unit", style="dim white", width=10)

    table.add_row("CPU Execution Latency",        f"{bench.cpu_latency_ms}",         "ms")
    table.add_row("Memory Copy Throughput",        f"{bench.memory_throughput_mbs}",  "MB/s")
    table.add_row("Disk Sequential Write Speed",   f"{bench.disk_io_write_mbs}",      "MB/s")
    table.add_row("Timer Resolution",              f"{bench.timer_resolution_ms}",    "ms")
    table.add_row("DNS Resolution Latency",        f"{bench.dns_latency_ms}",         "ms")

    console.print(table)


def render_dry_run_summary(session_mgr, report, sim_res):
    """Renders structured Dry-Run simulation summary."""
    _section_rule("Dry-Run Simulation Complete", "dim green")

    if sim_res:
        baseline = sim_res.get("baseline_health_score", round(report.health_score, 1))
        projected = sim_res.get("simulated_health_score", baseline)
        delta = sim_res.get("score_delta", 0)

        console.print("  [bold white]Baseline Score:[/bold white]    " + f"[yellow]{baseline} / 100[/yellow]")
        console.print("  [bold white]Projected Score:[/bold white]   " + f"[green]{projected} / 100[/green]")
        console.print("  [bold white]Score Improvement:[/bold white] " + f"[cyan]+{delta} points[/cyan]\n")

    render_warnings(report)

    console.print("  [bold white]Session Reports:[/bold white]")
    console.print(f"   • Session ID:    [cyan]{session_mgr.session_id}[/cyan]")
    console.print(f"   • Simulation:    [dim]{session_mgr.session_dir / 'findings.json'}[/dim]")
    console.print(f"   • HTML Report:   [green]{session_mgr.get_report_html_path()}[/green]\n")


def render_tweak_inspection_card(tweak: Tweak):
    """Renders granular Technician Mode Tweak Inspection Card."""
    _section_rule(f"Tweak Inspection Card :: {tweak.id}", "dim magenta")

    table = Table(
        header_style="bold yellow",
        border_style="dim magenta",
        show_lines=False,
        expand=False,
    )
    table.add_column("Property", style="bold cyan", width=22, no_wrap=True)
    table.add_column("Specification / Details", style="bold white", max_width=58)

    table.add_row("Tweak Name", tweak.name)
    table.add_row("Category", tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category))
    table.add_row("Description", tweak.description)
    table.add_row("Risk Rating", format_risk_badge(tweak.risk_score))
    table.add_row("Performance Gain", str(tweak.performance_gain_estimate))
    table.add_row("User Visible Impact", str(tweak.user_visible_change))
    table.add_row("Rollback Method", tweak.rollback_method.get("type", "Automated inverse action").upper())
    table.add_row("Required Elevation", "Administrator Required" if tweak.requires_admin else "Standard User")

    console.print(table)
