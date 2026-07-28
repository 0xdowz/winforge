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


from pathlib import Path
from winforge.utils.paths import get_executable_dir


def relaunch_as_admin(custom_args: Optional[List[str]] = None) -> bool:
    """
    Relaunches the current WinForge binary or script with elevated Administrator privileges
    using Windows ShellExecuteW(runas) while preserving command arguments and profile choices.
    Resolves absolute executable and working directory paths to avoid CWD dependencies.
    """
    if sys.platform != "win32":
        logger.info("Non-Windows platform detected; skipping ShellExecuteW elevation.")
        return True

    args_list = custom_args if custom_args is not None else sys.argv[1:]

    is_frozen = getattr(sys, "frozen", False)
    working_dir = str(get_executable_dir().resolve())

    if is_frozen:
        executable = str(Path(sys.executable).resolve())
        params = " ".join([f'"{arg}"' for arg in args_list])
    else:
        executable = str(Path(sys.executable).resolve())
        main_script = str(Path(sys.argv[0]).resolve())
        params = f'"{main_script}" ' + " ".join([f'"{arg}"' for arg in args_list])

    logger.info(f"Relaunching elevated process: executable='{executable}', params='{params}', cwd='{working_dir}'")

    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            params,
            working_dir,  # Explicit absolute working directory
            1  # SW_SHOWNORMAL
        )
        # ShellExecuteW returns > 32 on success
        success = ret > 32
        if not success:
            logger.error(f"ShellExecuteW elevation failed with Win32 return code: {ret}")
        return success
    except Exception as e:
        logger.error(f"Failed to trigger UAC elevation: {e}", exc_info=True)
        return False


def request_elevation_if_needed(session_id: Optional[str] = None, mode: str = "BEGINNER", max_risk: int = 20, selected_tweaks: Optional[List[str]] = None, tech_mode: bool = False) -> bool:
    """
    Checks for Administrator privileges. If non-elevated, prompts the user professionally,
    saves persistent state, and triggers ShellExecuteW UAC elevation with --resume SESSION_ID.
    Returns True if already admin, or False if elevation was requested / cancelled.
    """
    if is_admin():
        return True

    from winforge.cli.theme import console, render_section_header
    from winforge.core.session import save_pending_execution, get_pending_execution_path

    render_section_header("WinForge Privilege Elevation Required", "yellow")
    console.print("  [bold white]WinForge optimization requires Administrator privileges to perform:[/bold white]")
    console.print("   • System Registry modifications & tuning")
    console.print("   • Windows Services & startup management")
    console.print("   • Power plan overlays & hardware configuration")
    console.print("   • System Restore Point & transaction ledger creation\n")

    choice = Prompt.ask("Select action [[bold green]Y[/bold green]] Restart as Administrator  [[bold red]N[/bold red]] Cancel", choices=["Y", "N", "y", "n"], default="Y").upper()

    if choice == "Y":
        cur_session = session_id or f"SESSION_{sys.maxsize}"
        state_file = save_pending_execution(
            session_id=cur_session,
            mode=mode,
            max_risk=max_risk,
            selected_tweaks=selected_tweaks,
            execute=True,
            dry_run=False,
            tech_mode=tech_mode
        )
        resume_args = ["--resume", cur_session]

        is_frozen = getattr(sys, "frozen", False)
        exe_path = str(Path(sys.executable).resolve()) if is_frozen else f'"{sys.executable}" "{Path(sys.argv[0]).resolve()}"'
        cmd_str = f"{exe_path} --resume {cur_session}"

        console.print(f"\n[ELEVATION]")
        console.print(f"Session:      {cur_session}")
        console.print(f"State file:   {state_file}")
        console.print(f"Resume cmd:   {cmd_str}\n")
        console.print("  [bold green]✓ Requesting Windows UAC Administrator Elevation...[/bold green]\n")

        success = relaunch_as_admin(custom_args=resume_args)
        if success:
            sys.exit(0)
        else:
            console.print("  [bold red][ELEVATION FAILED] Could not launch elevated UAC prompt.[/bold red]\n")
            return False
    else:
        console.print("  [bold yellow][ABORTED] Optimization cancelled by user.[/bold yellow]\n")
        return False
