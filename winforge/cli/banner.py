from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

BANNER_ART = r"""
██╗  ██╗  ██╗██╗███╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗
██║  ██║  ██║██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝
██║  ██║  ██║██║██╔██╗ ██║█████╗  ██║  ██║██████╔╝██║  ███╗█████╗  
██║  ███╗ ██║██║██║╚██╗██║██╔══╝  ██║  ██║██╔══██╗██║   ██║██╔══╝  
╚████╔████╔╝██║██║ ╚████║██║     ██████╔╝██║  ██║╚██████╔╝███████╗
 ╚═══╝╚═══╝ ╚═╝╚═╝  ╚═══╝╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""


def render_banner(tech_mode: bool = False, dry_run: bool = True):
    """Renders main WinForge Rich banner."""
    banner_text = Text()
    banner_text.append(BANNER_ART, style="bold cyan")
    banner_text.append("\n  Free Open-Source Windows System Diagnostic & Optimization CLI Tool\n", style="bold white")
    banner_text.append("  Developed & Maintained by @0xdowz\n\n", style="bold yellow")

    # Mode badges
    if dry_run:
        banner_text.append("  [SIMULATION / DRY-RUN ACTIVE] ", style="bold yellow")
    else:
        banner_text.append("  [PRODUCTION EXECUTION ACTIVE] ", style="bold red")

    if tech_mode:
        banner_text.append("[TECHNICIAN MODE]", style="bold magenta")
    else:
        banner_text.append("[CLIENT MODE]", style="bold green")

    panel = Panel(
        banner_text,
        border_style="cyan",
        title="[bold yellow]WINFORGE CLI v1.0.0[/bold yellow]",
        subtitle="[bold white]Safe • Transparent • Reversible • Open-Source IT Technician Tool[/bold white]"
    )

    console.print(panel)
