import sys
import subprocess
import logging
from typing import Tuple

logger = logging.getLogger("winforge")


def create_system_restore_point(description: str = "WINFORGE_OPT_RESTORE") -> Tuple[bool, str]:
    """Creates a Windows System Restore Point using PowerShell WMI invocation."""
    if sys.platform != "win32":
        logger.info(f"[MOCK SAFETY] Simulated System Restore Point creation: {description}")
        return True, f"[MOCK SAFETY] Created Restore Point: {description}"

    try:
        ps_cmd = f'Checkpoint-Computer -Description "{description}" -RestorePointType "MODIFY_SETTINGS"'
        cmd = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "{ps_cmd}"'

        logger.info(f"Initiating System Restore Point creation: {description}")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if res.returncode == 0:
            logger.info(f"System Restore Point created successfully: {description}")
            return True, f"System Restore Point '{description}' created successfully."
        else:
            err = res.stderr.strip() or "PowerShell Checkpoint-Computer failed."
            logger.error(f"Failed creating System Restore Point: {err}")
            return False, f"Failed creating System Restore Point: {err}"
    except Exception as e:
        logger.error(f"Exception during System Restore Point creation: {e}")
        return False, f"Exception during System Restore Point creation: {str(e)}"
