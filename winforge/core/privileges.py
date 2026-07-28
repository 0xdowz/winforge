"""
WinForge Administrative Privilege Architecture & Dynamic Elevation Helper.
Provides non-blocking admin detection and ShellExecuteW(runas) dynamic elevation.
"""

import sys
import ctypes
import os
import logging
from typing import List, Optional
from rich.prompt import Prompt

logger = logging.getLogger("winforge")


def is_admin() -> bool:
    """Check if the current process is running with Administrative privileges."""
    if sys.platform != "win32":
        # Non-windows environment (e.g. testing)
        return os.environ.get("MOCK_ADMIN", "1") == "1"

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logger.warning(f"Failed to check admin status: {e}")
        return False


def require_admin() -> bool:
    """Verify admin privileges and log warning if not elevated."""
    admin_status = is_admin()
    if not admin_status:
        logger.warning("WinForge is running without Administrator privileges! Some modifications will fail.")
    return admin_status


def relaunch_as_admin(custom_args: Optional[List[str]] = None) -> bool:
    """
    Relaunches the current WinForge binary or script with elevated Administrator privileges
    using Windows ShellExecuteW(runas) while preserving command arguments and profile choices.
    """
    if sys.platform != "win32":
        logger.info("Non-Windows platform detected; skipping ShellExecuteW elevation.")
        return True

    args_list = custom_args if custom_args is not None else sys.argv[1:]

    is_frozen = getattr(sys, "frozen", False)
    if is_frozen:
        executable = sys.executable
        params = " ".join([f'"{arg}"' for arg in args_list])
    else:
        executable = sys.executable
        main_script = sys.argv[0]
        params = f'"{main_script}" ' + " ".join([f'"{arg}"' for arg in args_list])

    logger.info(f"Relaunching elevated process: {executable} {params}")

    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            params,
            None,
            1  # SW_SHOWNORMAL
        )
        # ShellExecuteW returns > 32 on success
        return ret > 32
    except Exception as e:
        logger.error(f"Failed to trigger UAC elevation: {e}")
        return False


def request_elevation_if_needed(custom_args: Optional[List[str]] = None) -> bool:
    """
    Checks for Administrator privileges. If non-elevated, prompts the user professionally
    and triggers ShellExecuteW UAC elevation.
    Returns True if already admin, or False if elevation was requested / cancelled.
    """
    if is_admin():
        return True

    from winforge.cli.theme import console, render_section_header

    render_section_header("WinForge Privilege Elevation Required", "yellow")
    console.print("  [bold white]WinForge optimization requires Administrator privileges to perform:[/bold white]")
    console.print("   • System Registry modifications & tuning")
    console.print("   • Windows Services & startup management")
    console.print("   • Power plan overlays & hardware configuration")
    console.print("   • System Restore Point & transaction ledger creation\n")

    choice = Prompt.ask("Select action [[bold green]Y[/bold green]] Restart as Administrator  [[bold red]N[/bold red]] Cancel", choices=["Y", "N", "y", "n"], default="Y").upper()

    if choice == "Y":
        console.print("  [bold green]✓ Requesting Windows UAC Administrator Elevation...[/bold green]\n")
        success = relaunch_as_admin(custom_args=custom_args)
        if success:
            sys.exit(0)
        else:
            console.print("  [bold red][ELEVATION FAILED] Could not launch elevated UAC prompt.[/bold red]\n")
            return False
    else:
        console.print("  [bold yellow][ABORTED] Optimization cancelled by user.[/bold yellow]\n")
        return False
