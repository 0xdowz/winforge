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

        console.print("  [bold white]Select your experience level:[/bold white]\n")

        console.print("  [bold green]1. Beginner Mode[/bold green]")
        console.print('     • Description:        "I want my PC faster. I have no technical knowledge."')
        console.print("     • Risk Tier:          Very Low / Low")
        console.print("     • Required Knowledge: None (100% Automated & Safe)\n")

        console.print("  [bold yellow]2. Advanced Mode[/bold yellow]")
        console.print('     • Description:        "I understand Windows settings."')
        console.print("     • Risk Tier:          Medium")
        console.print("     • Required Knowledge: Basic Windows Administration\n")

        console.print("  [bold magenta]3. Technician Mode[/bold magenta]")
        console.print('     • Description:        "I manage systems professionally."')
        console.print("     • Risk Tier:          High / Technician Tier")
        console.print("     • Required Knowledge: IT Engineering & Registry Experience\n")

        console.print("  [bold red]4. Cancel[/bold red]\n")

        return Prompt.ask("Select mode [1-4]", choices=["1", "2", "3", "4"], default="1")

    def render_tweak_education_card(self, tweak: Tweak):
        """Renders comprehensive beginner education card for a tweak."""
        renderer.render_section(f"Optimization :: {tweak.name}", color="cyan")

        cat_val = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        rollback_str = "Available (Automated Rollback Ledger)" if tweak.rollback_method else "Manual Baseline Restore"
        req_knowledge = "None (Beginner Safe)" if tweak.risk_score <= 20 else ("Basic Windows Settings" if tweak.risk_score <= 50 else "IT System Administrator")

        console.print(f"  [bold cyan]Name:[/bold cyan]              [bold white]{tweak.name}[/bold white]")
        console.print(f"  [bold cyan]What it changes:[/bold cyan]   [bold white]{tweak.description}[/bold white]")
        console.print(f"  [bold cyan]Why recommended:[/bold cyan]   [dim white]System health report identified optimization potential in {cat_val}[/dim white]")
        console.print(f"  [bold cyan]Expected benefit:[/bold cyan]  [bold green]{tweak.performance_gain_estimate} ({tweak.user_visible_change})[/bold green]")
        console.print(f"  [bold cyan]Risk Rating:[/bold cyan]       {format_risk_badge(tweak.risk_score)}")
        console.print(f"  [bold cyan]Rollback:[/bold cyan]          [bold green]{rollback_str}[/bold green]")
        console.print(f"  [bold cyan]Required knowledge:[/bold cyan][bold yellow] {req_knowledge}[/bold yellow]\n")

    def prompt_explain_action(self) -> str:
        """Prompts user prior to system mutations with Explain Before Execute options."""
        console.print("  [bold white]Execution Actions:[/bold white]")
        console.print("   [bold green][Y] Apply optimizations[/bold green]   [bold red][N] Cancel execution[/bold red]   [bold cyan][D] Detailed view[/bold cyan]\n")
        return Prompt.ask("Select action [Y/N/D]", choices=["Y", "N", "D", "y", "n", "d"], default="Y").upper()


wizard = OptimizationWizard()
