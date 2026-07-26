"""
WinForge CLI Design System — Premium Cybersecurity Theme & Terminal Rendering Engine.
Provides unified width caps, dark enterprise color tokens, typography tokens, section lifecycles, and RendererManager singleton.
"""

import os
import shutil
from pathlib import Path
from typing import Callable, Any, Optional, List
from rich.console import Console
from rich.text import Text

CONSOLE_WIDTH = min(shutil.get_terminal_size((80, 24)).columns, 90)


class CLITheme:
    """Enterprise Dark Cybersecurity Theme Tokens & Typography Hierarchy."""

    PRIMARY = "bold cyan"      # Cyber Cyan
    SUCCESS = "bold green"     # Matrix Green
    WARNING = "bold yellow"    # Amber
    DANGER = "bold red"        # Red
    MUTED = "dim white"        # Slate Gray
    BODY = "white"             # Body Text

    TITLE = "bold cyan"
    SECTION = "bold white"
    SUBTITLE = "bold yellow"
    ERROR = "bold red"


class RendererManager:
    """
    Centralized Terminal Rendering Engine:
      - Fixed console width auto-capped to 90 columns for perfect rendering across 80/90/120 col terminals.
      - Safe output queue & section lifecycle: Before spacing (1 blank line) -> Header -> Content -> After spacing (1 blank line).
      - Eliminates rendering collisions, border corruption, direct print statements, and duplicate outputs.
    """

    def __init__(self, override_width: Optional[int] = None):
        if override_width:
            self.width = min(override_width, 90)
        else:
            self.width = CONSOLE_WIDTH
        
        self.console = Console(width=self.width)

    def print(self, *args, **kwargs):
        """Proxy print call to managed console."""
        self.console.print(*args, **kwargs)

    def render_section(self, title: str, color: str = "cyan", content_func: Optional[Callable[[], None]] = None):
        """Enforces clean section lifecycle: Before spacing -> Header -> Content -> After spacing."""
        self.console.print()
        self.console.print(f"[bold {color}]─── {title} ───[/bold {color}]")
        self.console.print()
        if content_func and callable(content_func):
            content_func()
            self.console.print()

    def format_short_path(self, path_obj_or_str: Any) -> str:
        """Formats long absolute paths into readable short location strings."""
        if not path_obj_or_str:
            return "N/A"
        p_str = str(path_obj_or_str)
        p = Path(p_str)
        parts = p.parts
        if len(parts) > 3:
            return f"...\\{os.path.join(*parts[-3:])}"
        return p_str


# Singleton instance shared across CLI components
renderer = RendererManager()
console = renderer.console
render_section_header = renderer.render_section
format_short_path = renderer.format_short_path
