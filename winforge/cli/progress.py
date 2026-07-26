"""
WinForge CLI Progress — Step Tracker & Rich Progress Indicators.
"""

from typing import List, Callable, Any
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from winforge.cli.components import console


class StepTracker:
    """Tracks multi-step pipeline execution with rich progress feedback."""

    def __init__(self, title: str, total_steps: int):
        self.title = title
        self.total_steps = total_steps
        self.current_step = 0

    def log_step(self, step_name: str, status: str = "COMPLETED", success: bool = True):
        """Logs individual step execution result."""
        self.current_step += 1
        icon = "✓" if success else "✗"
        color = "bold green" if success else "bold red"
        console.print(f"  [{color}][{self.current_step}/{self.total_steps}] {icon} {step_name}[/{color}] -> [dim white]{status}[/dim white]")

    def finish(self, summary_msg: str):
        """Prints completion summary."""
        console.print(f"\n[bold green]✓ {summary_msg}[/bold green]\n")
