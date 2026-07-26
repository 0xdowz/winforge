"""
WinForge CLI Formatting — Visual Status Badges & Text Formatter.
"""

from rich.text import Text


def format_status_badge(score: float) -> Text:
    """Format color-coded status badge based on health score."""
    text = Text()
    if score >= 85.0:
        text.append(" [OPTIMAL STATE] ", style="bold black on green")
    elif score >= 70.0:
        text.append(" [NEEDS TUNING] ", style="bold black on yellow")
    else:
        text.append(" [CRITICAL DEGRADATION] ", style="bold white on red")
    return text


def format_risk_badge(risk_score: int) -> str:
    """Format risk rating string for tables and inspection cards."""
    if risk_score <= 20:
        return f"[bold green]{risk_score}/100 (SAFE)[/bold green]"
    elif risk_score <= 50:
        return f"[bold yellow]{risk_score}/100 (MODERATE)[/bold yellow]"
    elif risk_score <= 80:
        return f"[bold red]{risk_score}/100 (ADVANCED)[/bold red]"
    else:
        return f"[bold magenta]{risk_score}/100 (TECHNICIAN ONLY)[/bold magenta]"
