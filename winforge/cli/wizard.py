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
        f_name = tweak.friendly_name or tweak.name
        renderer.render_section(f"Optimization Details :: {f_name}", color="cyan")

        cat_val = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
        rollback_str = "Available (Automated Rollback Ledger)" if tweak.rollback_method else "Manual Baseline Restore"
        reboot_str = "Yes (System reboot recommended)" if tweak.requires_reboot else "No (Immediate effect)"
        req_knowledge = "None (Beginner Safe)" if tweak.risk_score <= 20 else ("Basic Windows Settings" if tweak.risk_score <= 50 else "IT System Administrator")

        console.print(f"  [bold cyan]Optimization Name:[/bold cyan]  [bold white]{f_name}[/bold white] [dim white]({tweak.id})[/dim white]")
        console.print(f"  [bold cyan]What it does:[/bold cyan]       [bold white]{tweak.what_it_does or tweak.description}[/bold white]")
        console.print(f"  [bold cyan]Why recommended:[/bold cyan]    [dim white]{tweak.why_it_exists or tweak.rationale}[/dim white]")
        console.print(f"  [bold cyan]Exact System Changes:[/bold cyan][bold yellow] {tweak.exact_system_changes}[/bold yellow]")
        console.print(f"  [bold cyan]Expected Benefit:[/bold cyan]   [bold green]{tweak.performance_gain_estimate} ({tweak.user_visible_change})[/bold green]")
        console.print(f"  [bold cyan]Risk Rating:[/bold cyan]        {format_risk_badge(tweak.risk_score)}")
        console.print(f"  [bold cyan]Rollback Status:[/bold cyan]    [bold green]{rollback_str}[/bold green]")
        console.print(f"  [bold cyan]Requires Reboot:[/bold cyan]    [bold white]{reboot_str}[/bold white]")
        console.print(f"  [bold cyan]Required Knowledge:[/bold cyan] [bold yellow]{req_knowledge}[/bold yellow]\n")

    def prompt_explain_action(self) -> str:
        """Prompts user prior to system mutations with Explain Before Execute options."""
        console.print("  [bold white]Execution Actions:[/bold white]")
        console.print("   [bold green][Y] Apply optimizations[/bold green]   [bold red][N] Cancel execution[/bold red]   [bold cyan][D] Detailed view[/bold cyan]\n")
        return Prompt.ask("Select action [Y/N/D]", choices=["Y", "N", "D", "y", "n", "d"], default="Y").upper()

    def render_tweak_selection_menu(self, candidate_tweaks: List[Tweak]) -> Optional[List[Tweak]]:
        """
        Renders interactive tweak preview & granular selection screen.
        Allows users to inspect details, toggle individual optimizations on/off, or proceed.
        """
        import os
        from winforge.cli.theme import prompt_pause_if_interactive

        # Non-interactive CLI fast-path preservation
        if os.environ.get("WINFORGE_NON_INTERACTIVE") == "1":
            return candidate_tweaks

        if not candidate_tweaks:
            return []

        selected_mask = [True] * len(candidate_tweaks)

        while True:
            renderer.render_section("Optimization Preview & Customization", color="cyan")
            console.print("  [bold white]Review candidate optimizations below:[/bold white]\n")

            for idx, tweak in enumerate(candidate_tweaks, 1):
                checkbox = "[bold green][X][/bold green]" if selected_mask[idx - 1] else "[dim white][ ][/dim white]"
                f_name = tweak.friendly_name or tweak.name
                risk_badge = format_risk_badge(tweak.risk_score)
                cat_str = tweak.category.value if hasattr(tweak.category, "value") else str(tweak.category)
                console.print(f"   {checkbox} [bold cyan]{idx:>2}. {f_name:<36}[/bold cyan] [dim white]{cat_str:<10}[/dim white] {risk_badge}")

            active_count = sum(selected_mask)
            console.print(f"\n  [bold white]Selected:[/bold white] [bold green]{active_count}/{len(candidate_tweaks)} optimizations[/bold green]\n")
            console.print("  [bold white]Actions:[/bold white]")
            console.print("   [bold green][Y] Apply selected[/bold green]   [bold red][N] Cancel[/bold red]   [bold cyan][D #] View details[/bold cyan]   [bold yellow][T #] Toggle item[/bold yellow]   [bold white][A] Select All[/bold white]   [bold white][C] Clear All[/bold white]\n")

            choice = Prompt.ask("Action [Y/N/D #/T #/A/C]", default="Y").strip()
            choice_upper = choice.upper()

            if choice_upper == "Y":
                final_selected = [t for i, t in enumerate(candidate_tweaks) if selected_mask[i]]
                if not final_selected:
                    console.print("\n  [bold yellow]No optimizations selected. Select at least one item or cancel.[/bold yellow]\n")
                    continue
                return final_selected
            elif choice_upper == "N":
                return None
            elif choice_upper == "A":
                selected_mask = [True] * len(candidate_tweaks)
            elif choice_upper == "C":
                selected_mask = [False] * len(candidate_tweaks)
            elif choice_upper.startswith("D"):
                parts = choice_upper.split()
                if len(parts) > 1 and parts[1].isdigit():
                    t_idx = int(parts[1]) - 1
                    if 0 <= t_idx < len(candidate_tweaks):
                        self.render_tweak_education_card(candidate_tweaks[t_idx])
                        prompt_pause_if_interactive("Press Enter to return to selection list")
                else:
                    console.print("  [bold yellow]Usage for details: D 1 (or D 2)[/bold yellow]\n")
            elif choice_upper.startswith("T") or choice_upper.isdigit():
                num_str = choice_upper[1:].strip() if choice_upper.startswith("T") else choice_upper
                if num_str.isdigit():
                    t_idx = int(num_str) - 1
                    if 0 <= t_idx < len(candidate_tweaks):
                        selected_mask[t_idx] = not selected_mask[t_idx]


wizard = OptimizationWizard()
