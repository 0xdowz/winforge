"""
WinForge CLI Themes — Terminal Color Palettes & Visual Styling Tokens.
Supports Dark, Minimal, and High-Contrast Accessibility Themes.
"""

from typing import Dict, Any


THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "primary": "cyan",
        "secondary": "bold yellow",
        "accent": "magenta",
        "success": "bold green",
        "warning": "bold yellow",
        "danger": "bold red",
        "muted": "dim white",
        "border": "cyan",
    },
    "minimal": {
        "primary": "white",
        "secondary": "bold white",
        "accent": "white",
        "success": "white",
        "warning": "white",
        "danger": "bold white",
        "muted": "dim white",
        "border": "white",
    },
    "accessibility": {
        "primary": "bold blue",
        "secondary": "bold yellow",
        "accent": "bold magenta",
        "success": "bold green",
        "warning": "bold yellow",
        "danger": "bold red",
        "muted": "bold white",
        "border": "yellow",
    }
}


class ThemeManager:
    """Manages active CLI color palette theme."""

    def __init__(self, theme_name: str = "dark"):
        self.active_theme = THEMES.get(theme_name.lower(), THEMES["dark"])
        self.theme_name = theme_name.lower()

    def get_style(self, token: str) -> str:
        """Retrieve rich style string for given token."""
        return self.active_theme.get(token, "bold white")
