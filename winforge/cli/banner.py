"""
WinForge CLI Banner — Clean Modern Header Renderer.
Replaces heavy multi-line ASCII art with a lightweight, professional CLI header.
"""

from rich.console import Console
from rich.text import Text
from rich.rule import Rule

from winforge import __version__

console = Console()


def render_banner(tech_mode: bool = False, dry_run: bool = True):
    """Renders clean, modern brand header for WinForge CLI."""
    mode_badge = "SIMULATION / DRY-RUN" if dry_run else "PRODUCTION EXECUTION"
    mode_color = "bold yellow" if dry_run else "bold red"

    tech_badge = "TECHNICIAN MODE" if tech_mode else "CLIENT MODE"
    tech_color = "bold magenta" if tech_mode else "bold green"

    header_text = Text()
    header_text.append(f"WINFORGE {__version__}", style="bold cyan")
    header_text.append("  |  Windows System Optimization Assistant\n", style="bold white")
    header_text.append(f"[{mode_badge}]", style=mode_color)
    header_text.append("  ", style="dim white")
    header_text.append(f"[{tech_badge}]\n", style=tech_color)

    console.print()
    console.print(header_text)
    console.print(Rule(style="dim cyan"))
    console.print()
