"""
WinForge CLI Guided Optimization Wizard & Beginner Education System.
Provides step-by-step profile selection and detailed tweak education cards.
"""

from typing import List, Optional
from rich.prompt import Prompt, Confirm
from winforge.models.tweak import Tweak
from winforge.cli.theme import renderer, console, CLITheme
from winforge.cli.formatting import format_risk_badge


class OptimizationWizard:
    """Guided Beginner & Technician Optimization Wizard."""

    def render_profile_menu(self) -> str:
        """Displays guided optimization profile selection menu."""
        renderer.render_section("Guided Optimization Wizard", color="cyan")

        console.print("  [bold white]Choose an Optimization Profile suitable for your system:[/bold white]\n")

        console.print("  [bold green]1. SAFE OPTIMIZATIONS (Beginner)[/bold green]")
        console.print("     • Tweaks:   Temp Cleanup, Basic Power & Visual Adjustments")
        console.print("     • Risk:     Very Low / Low")
        console.print("     • Requires: None (Fully Automated & 100% Safe)\n")

        console.print("  [bold yellow]2. ADVANCED OPTIMIZATIONS[/bold yellow]")
        console.print("     • Tweaks:   Network Latency, Service Hygiene & Cache Tuning")
        console.print("     • Risk:     Medium")
        console.print("     • Requires: Basic Windows System Knowledge\n")

        console.print("  [bold magenta]3. TECHNICIAN ONLY MODE[/bold magenta]")
        console.print("     • Tweaks:   Registry Optimization, High-Risk System Parameters")
        console.print("     • Risk:     High / Technician Tier")
        console.print("     • Requires: Administrator & IT System Engineering Experience\n")

        console.print("  [bold red]4. Cancel[/bold red]\n")

        return Prompt.ask("Select profile [1-4]", choices=["1", "2", "3", "4"], default="1")

    def render_tweak_education_card(self, tweak: Tweak):
        """Renders comprehensive beginner education card for a tweak."""
        renderer.render_section(f"Tweak Education :: {tweak.name}", color="cyan")

        cat_val = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        rollback_str = "Automated Inverse Action Available" if tweak.rollback_method else "Manual Baseline Restore"
        tech_level = "Beginner (Safe)" if tweak.risk_score <= 20 else ("Advanced" if tweak.risk_score <= 50 else "Technician Only")

        console.print(f"  [bold cyan]Name:[/bold cyan]            [bold white]{tweak.name}[/bold white]")
        console.print(f"  [bold cyan]Category:[/bold cyan]        [dim white]{cat_val}[/dim white]")
        console.print(f"  [bold cyan]What It Does:[/bold cyan]    [bold white]{tweak.description}[/bold white]")
        console.print(f"  [bold cyan]Expected Impact:[/bold cyan] {tweak.performance_gain_estimate} ({tweak.user_visible_change})")
        console.print(f"  [bold cyan]Risk Rating:[/bold cyan]     {format_risk_badge(tweak.risk_score)}")
        console.print(f"  [bold cyan]Rollback Method:[/bold cyan] [bold green]{rollback_str}[/bold green]")
        console.print(f"  [bold cyan]Technical Level:[/bold cyan] [bold yellow]{tech_level}[/bold yellow]\n")


wizard = OptimizationWizard()
