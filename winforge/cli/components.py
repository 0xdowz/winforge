"""
WinForge CLI Components — Modern Terminal Presentation Library.
Provides clean visual hierarchy, section dividers, status badges, and hardware tables.
Uses responsive width detection to adapt gracefully to all terminal windows.
"""

import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak
from winforge.cli.formatting import format_status_badge, format_risk_badge

# Single shared console with terminal-aware width
_term_width = min(shutil.get_terminal_size((120, 32)).columns, 160)
console = Console(width=_term_width)

_NARROW = _term_width < 100
_COMPONENT_COL = 18 if _NARROW else 24
_SPEC_COL_FIXED = 40 if _NARROW else None


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
        badge_text = "OPTIMAL STATE"
    elif score >= 70:
        score_style = "bold yellow"
        badge_text = "NEEDS ATTENTION"
    else:
        score_style = "bold red"
        badge_text = "CRITICAL DEGRADATION"

    _section_rule("System Health Overview", "dim cyan")

    score_text = Text()
    score_text.append("  Health Score:  ", style="bold white")
    score_text.append(f"{score} / 100", style=score_style)
    score_text.append(f"  [{badge_text}]\n\n", style=score_style)

    score_text.append("  Category Breakdown:\n", style="bold cyan")
    score_text.append(f"   • Performance Score:          {round(report.categories.performance_score, 1)} / 100\n", style="bold white")
    score_text.append(f"   • Security & Privacy:         {round(report.categories.security_score, 1)} / 100\n", style="bold white")
    score_text.append(f"   • Maintenance & Cleanliness: {round(report.categories.maintenance_score, 1)} / 100\n", style="bold white")
    score_text.append(f"   • Startup & Service Hygiene:  {round(report.categories.startup_score, 1)} / 100\n", style="bold white")

    console.print(score_text)


def render_hardware_summary(report: SystemHealthReport):
    """Renders hardware specification table with sleek layout."""
    _section_rule("Hardware Specification", "dim cyan")

    table = Table(
        header_style="bold yellow",
        border_style="dim cyan",
        expand=False,
        show_lines=False,
    )
    table.add_column("Component", style="bold cyan", width=_COMPONENT_COL, no_wrap=True)
    table.add_column("Specification Details", style="bold white", max_width=_SPEC_COL_FIXED)

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
    table.add_column("Benchmark Metric", style="bold cyan", width=32, no_wrap=True)
    table.add_column("Result", style="bold white", justify="right", width=18)
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

        score_text = Text()
        score_text.append("  Baseline Score:      ", style="bold white")
        score_text.append(f"{baseline} / 100\n", style="bold yellow")
        score_text.append("  Projected Score:     ", style="bold white")
        score_text.append(f"{projected} / 100\n", style="bold green")
        score_text.append("  Score Improvement:   ", style="bold white")
        score_text.append(f"+{delta} points\n", style="bold cyan")

        console.print(Panel(score_text, title="[bold yellow]Score Projection[/bold yellow]", border_style="green"))
        console.print()

    render_warnings(report)

    path_text = Text()
    path_text.append("  Session ID:       ", style="bold white")
    path_text.append(f"{session_mgr.session_id}\n", style="bold cyan")
    path_text.append("  Simulation Log:   ", style="bold white")
    path_text.append(f"{session_mgr.session_dir / 'findings.json'}\n", style="dim white")
    path_text.append("  HTML Report:      ", style="bold white")
    path_text.append(f"{session_mgr.get_report_html_path()}\n", style="bold green")

    console.print(Panel(path_text, title="[bold yellow]Session Report Generated[/bold yellow]", border_style="cyan"))
    console.print()


def render_tweak_inspection_card(tweak: Tweak):
    """Renders granular Technician Mode Tweak Inspection Card."""
    _section_rule(f"Tweak Inspection Card :: {tweak.id}", "dim magenta")

    table = Table(
        header_style="bold yellow",
        border_style="dim magenta",
        show_lines=False,
        expand=False,
    )
    table.add_column("Property", style="bold cyan", width=24, no_wrap=True)
    table.add_column("Specification / Details", style="bold white")

    table.add_row("Tweak Name", tweak.name)
    table.add_row("Category", tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category))
    table.add_row("Description", tweak.description)
    table.add_row("Risk Rating", format_risk_badge(tweak.risk_score))
    table.add_row("Performance Gain", str(tweak.performance_gain_estimate))
    table.add_row("User Visible Impact", str(tweak.user_visible_change))
    table.add_row("Rollback Method", tweak.rollback_method.get("type", "Automated inverse action").upper())
    table.add_row("Required Elevation", "Administrator Required" if tweak.requires_admin else "Standard User")

    console.print(table)
