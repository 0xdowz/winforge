"""
WinForge CLI Components — Modern Terminal Presentation Library.
Provides clean visual hierarchy, short section headers, status badges, and hardware tables.
Enforces max 90-column width for clean rendering across CMD, PowerShell, and Windows Terminal.
"""

from rich.table import Table
from rich.text import Text

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak
from winforge.cli.theme import console, CONSOLE_WIDTH, render_section_header, format_short_path
from winforge.cli.formatting import (
    format_status_badge,
    format_risk_badge,
    get_status_icon,
)


def render_health_dashboard(report: SystemHealthReport):
    """Renders clean, structured System Health Overview as aligned text."""
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

    render_section_header("System Health Overview", "cyan")

    console.print("  Health Score:")
    console.print(f"  [bold white]{score} / 100[/bold white]  [{score_style}]{badge_text}[/{score_style}]\n")

    console.print("  Category Breakdown:")
    
    perf = round(report.categories.performance_score, 1)
    sec = round(report.categories.security_score, 1)
    maint = round(report.categories.maintenance_score, 1)
    start = round(report.categories.startup_score, 1)

    p_icon = get_status_icon("success" if perf >= 80 else "warning")
    s_icon = get_status_icon("success" if sec >= 80 else "warning")
    m_icon = get_status_icon("success" if maint >= 80 else "warning")
    st_icon = get_status_icon("success" if start >= 80 else "warning")

    console.print(f"   {p_icon} Performance Score:          {perf} / 100")
    console.print(f"   {s_icon} Security & Privacy:         {sec} / 100")
    console.print(f"   {m_icon} Maintenance & Cleanliness: {maint} / 100")
    console.print(f"   {st_icon} Startup & Service Hygiene:  {start} / 100")


def render_hardware_summary(report: SystemHealthReport):
    """Renders hardware specification table cleanly with box=None, padding=(0, 1)."""
    render_section_header("Hardware Specification", "cyan")

    table = Table(
        box=None,
        expand=False,
        padding=(0, 1),
        header_style="bold yellow",
    )
    table.add_column("Component", style="bold cyan", width=22, no_wrap=True)
    table.add_column("Specification Details", style="bold white", max_width=62)

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
    """Renders concise system degradation warnings list as aligned text."""
    render_section_header("Detected System Issues", "yellow")

    if not report.warnings:
        warn_icon = get_status_icon("success")
        console.print(f"  {warn_icon} [bold green]Zero critical system degradation issues detected.[/bold green]\n")
        return

    warn_icon = get_status_icon("warning")
    for warning in report.warnings:
        console.print(f"  {warn_icon} [bold yellow]{warning}[/bold yellow]")
    console.print()


def render_benchmark_results(bench):
    """Renders quantitative performance benchmark table cleanly with box=None, padding=(0, 1)."""
    render_section_header("Performance Benchmark Results", "cyan")

    table = Table(
        box=None,
        expand=False,
        padding=(0, 1),
        header_style="bold yellow",
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
    """Renders structured Dry-Run simulation summary with short paths."""
    render_section_header("Dry-Run Simulation Complete", "green")

    if sim_res:
        baseline = sim_res.get("baseline_health_score", round(report.health_score, 1))
        projected = sim_res.get("simulated_health_score", baseline)
        delta = sim_res.get("score_delta", 0)

        console.print("  [bold white]Baseline Score:[/bold white]    " + f"[yellow]{baseline} / 100[/yellow]")
        console.print("  [bold white]Projected Score:[/bold white]   " + f"[green]{projected} / 100[/green]")
        console.print("  [bold white]Score Improvement:[/bold white] " + f"[cyan]+{delta} points[/cyan]\n")

    console.print("  [bold white]Session Reports Generated:[/bold white]")
    console.print(f"   • Session ID:  [cyan]{session_mgr.session_id}[/cyan]")
    console.print(f"   • Log File:    [dim]{format_short_path(session_mgr.session_dir / 'findings.json')}[/dim]")
    console.print(f"   • HTML Report: [green]{format_short_path(session_mgr.get_report_html_path())}[/green]\n")


def render_tweak_inspection_card(tweak: Tweak):
    """Renders granular Technician Mode Tweak Inspection Card as aligned text list."""
    render_section_header(f"Tweak Inspection Card :: {tweak.id}", "magenta")

    console.print(f"  [bold cyan]Tweak Name:[/bold cyan]        [bold white]{tweak.name}[/bold white]")
    cat_val = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
    console.print(f"  [bold cyan]Category:[/bold cyan]          [dim white]{cat_val}[/dim white]")
    console.print(f"  [bold cyan]Description:[/bold cyan]       [bold white]{tweak.description}[/bold white]")
    console.print(f"  [bold cyan]Risk Rating:[/bold cyan]       {format_risk_badge(tweak.risk_score)}")
    console.print(f"  [bold cyan]Performance Gain:[/bold cyan]  {tweak.performance_gain_estimate}")
    console.print(f"  [bold cyan]User Visible Impact:[/bold cyan]{tweak.user_visible_change}")
    rollback_t = tweak.rollback_method.get("type", "Automated inverse action").upper()
    console.print(f"  [bold cyan]Rollback Method:[/bold cyan]   [bold green]{rollback_t}[/bold green]")
    elev_str = "Administrator Required" if tweak.requires_admin else "Standard User"
    console.print(f"  [bold cyan]Elevation:[/bold cyan]         {elev_str}\n")
