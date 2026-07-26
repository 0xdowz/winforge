"""
WinForge CLI Formatting — Status Indicators, Badges & Unicode/ASCII Fallback.
Provides unified indicators across all terminal environments (CMD, PowerShell, Windows Terminal).
"""

import sys
from rich.text import Text

# Detect if terminal stdout supports UTF-8 Unicode characters
_USE_UNICODE = getattr(sys.stdout, "encoding", "utf-8") is not None and sys.stdout.encoding.lower().replace("-", "") in ("utf8", "utf16", "utf32")

# Consistent status indicators
ICON_SUCCESS = "✓" if _USE_UNICODE else "[OK]"
ICON_WARNING = "⚠" if _USE_UNICODE else "[WARN]"
ICON_ERROR   = "✗" if _USE_UNICODE else "[FAIL]"
ICON_RUNNING = "→" if _USE_UNICODE else "[RUN]"
ICON_PENDING = "○" if _USE_UNICODE else "[WAIT]"


def get_status_icon(kind: str) -> str:
    """Returns status indicator string based on kind."""
    k = kind.lower()
    if k in ("success", "ok", "completed"):
        return f"[bold green]{ICON_SUCCESS}[/bold green]"
    elif k in ("warning", "warn", "attention"):
        return f"[bold yellow]{ICON_WARNING}[/bold yellow]"
    elif k in ("error", "fail", "danger", "critical"):
        return f"[bold red]{ICON_ERROR}[/bold red]"
    elif k in ("running", "active", "current"):
        return f"[bold cyan]{ICON_RUNNING}[/bold cyan]"
    else:
        return f"[dim white]{ICON_PENDING}[/dim white]"


def format_status_badge(score: float) -> Text:
    """Format color-coded status badge based on health score."""
    text = Text()
    if score >= 85.0:
        text.append(" OPTIMAL ", style="bold black on green")
    elif score >= 70.0:
        text.append(" NEEDS ATTENTION ", style="bold black on yellow")
    else:
        text.append(" CRITICAL ", style="bold white on red")
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
        return f"[bold magenta]{risk_score}/100 (TECH ONLY)[/bold magenta]"
