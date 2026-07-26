"""
WinForge CLI Progress — Step Tracker & Progress Indicators.
Provides clean step-by-step pipeline tracking:
✓ Completed
→ Current
○ Pending
"""

from typing import List, Optional
from winforge.cli.components import console
from winforge.cli.formatting import get_status_icon, ICON_SUCCESS, ICON_ERROR, ICON_RUNNING, ICON_PENDING


class StepTracker:
    """Tracks multi-step pipeline execution with clear step indicators."""

    def __init__(self, title: str, total_steps: int):
        self.title = title
        self.total_steps = total_steps
        self.current_step = 0
        console.print(f"\n[bold white]{self.title}[/bold white]")

    def log_step(self, step_name: str, status: str = "COMPLETED", success: bool = True):
        """Logs individual step execution result."""
        self.current_step += 1
        icon = get_status_icon("success" if success else "error")
        color = "bold white" if success else "bold red"
        console.print(f"  [{self.current_step}/{self.total_steps}] {icon} [{color}]{step_name}[/{color}] -> [dim white]{status}[/dim white]")

    def finish(self, summary_msg: str):
        """Prints completion summary."""
        icon = get_status_icon("success")
        console.print(f"\n  {icon} [bold green]{summary_msg}[/bold green]\n")
