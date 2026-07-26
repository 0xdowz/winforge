"""
WinForge CLI Prompts — Interactive User Input & Confirmation Prompts.
"""

from rich.prompt import Confirm, Prompt
from winforge.cli.components import console


def confirm_optimization_execution(count: int, is_tech_mode: bool = False) -> bool:
    """Prompts user to confirm pre-execution optimization plan."""
    mode_str = "Technician Mode" if is_tech_mode else "Client Mode"
    console.print(f"\n[bold cyan]({mode_str}) Ready to apply {count} optimization(s).[/bold cyan]")
    return Confirm.ask("[bold yellow]Proceed with optimization plan?[/bold yellow]", default=True)


def prompt_menu_choice(options: list) -> str:
    """Prompts user for menu navigation choice."""
    return Prompt.ask("Select an option", choices=options, default="1")
