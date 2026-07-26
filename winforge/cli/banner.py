"""
WinForge CLI Banner — Brand Identity & Header System.
Provides professional ASCII art startup banner and compact header.
"""

from rich.text import Text
from winforge import __version__, __author__
from winforge.cli.theme import console

ASCII_LOGO = r"""
  ██╗  ██╗  ██╗██╗███╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗
  ██║  ██║  ██║██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝
  ██║  ██║  ██║██║██╔██╗ ██║█████╗  ██║  ██║██████╔╝██║  ███╗█████╗  
  ██║  ███╗ ██║██║██║╚██╗██║██╔══╝  ██║  ██║██╔══██╗██║   ██║██╔══╝  
  ╚████╔████╔╝ ██║██║ ╚████║██║     ██████╔╝██║  ██║╚██████╔╝███████╗
   ╚═══╝╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══════╝
"""


def render_welcome_banner(tech_mode: bool = False, dry_run: bool = True):
    """Renders full professional brand identity startup banner."""
    mode_badge = "SIMULATION / DRY-RUN" if dry_run else "PRODUCTION EXECUTION"
    mode_color = "bold yellow" if dry_run else "bold red"

    tech_badge = "TECHNICIAN MODE" if tech_mode else "CLIENT MODE"
    tech_color = "bold magenta" if tech_mode else "bold green"

    console.print(ASCII_LOGO, style="bold cyan")

    brand_text = Text()
    brand_text.append(f"  WinForge CLI v{__version__}", style="bold white")
    brand_text.append("  —  Windows Performance & Safety Framework\n", style="dim white")
    brand_text.append(f"  Author: @{__author__}  |  GitHub: ", style="dim white")
    brand_text.append("https://github.com/0xdowz/winforge\n", style="bold cyan")
    brand_text.append(f"  [{mode_badge}]", style=mode_color)
    brand_text.append("  ", style="dim white")
    brand_text.append(f"[{tech_badge}]\n", style=tech_color)

    console.print(brand_text)


def render_banner(tech_mode: bool = False, dry_run: bool = True):
    """Renders compact brand header for navigation screens."""
    mode_badge = "SIMULATION / DRY-RUN" if dry_run else "PRODUCTION EXECUTION"
    mode_color = "bold yellow" if dry_run else "bold red"

    tech_badge = "TECHNICIAN MODE" if tech_mode else "CLIENT MODE"
    tech_color = "bold magenta" if tech_mode else "bold green"

    header_text = Text()
    header_text.append(f"WINFORGE {__version__}", style="bold cyan")
    header_text.append("  |  Windows System Optimization Assistant\n", style="bold white")
    header_text.append(f"[{mode_badge}]", style=mode_color)
    header_text.append("  ", style="dim white")
    header_text.append(f"[{tech_badge}]", style=tech_color)

    console.print()
    console.print(header_text)
    console.print()
