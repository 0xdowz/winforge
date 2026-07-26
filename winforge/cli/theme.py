"""
WinForge CLI Design System & Theme Constants.
Provides unified width caps, section dividers, path truncators, and styling tokens.
"""

import os
import shutil
from pathlib import Path
from rich.console import Console

# Unified 90-column terminal width cap
CONSOLE_WIDTH = min(shutil.get_terminal_size((80, 24)).columns, 90)
console = Console(width=CONSOLE_WIDTH)


def render_section_header(title: str, color: str = "cyan"):
    """Renders short centered section divider with clean newline separation."""
    console.print()
    console.print(f"[bold {color}]─── {title} ───[/bold {color}]")
    console.print()


def format_short_path(path_obj_or_str) -> str:
    """Formats long absolute paths into readable short location strings."""
    if not path_obj_or_str:
        return "N/A"
    p_str = str(path_obj_or_str)
    p = Path(p_str)
    parts = p.parts
    if len(parts) > 3:
        return f"...\\{os.path.join(*parts[-3:])}"
    return p_str
