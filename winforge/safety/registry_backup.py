import sys
import subprocess
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("winforge")


def normalize_registry_path(key_path: str) -> str:
    """
    Normalizes registry key paths to standard reg.exe export format with hive prefix.
    Supports: HKLM, HKCU, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, missing hive prefixes (SOFTWARE\\..., System\\...).
    """
    path = key_path.strip().replace("/", "\\")
    upper = path.upper()

    if upper.startswith("HKEY_LOCAL_MACHINE\\"):
        return "HKLM\\" + path[19:]
    elif upper.startswith("HKEY_CURRENT_USER\\"):
        return "HKCU\\" + path[18:]
    elif upper.startswith("HKLM\\") or upper.startswith("HKCU\\") or upper.startswith("HKU\\") or upper.startswith("HKCR\\"):
        return path

    # Auto-prefix missing hive
    if upper.startswith("SOFTWARE\\") or upper.startswith("SYSTEM\\") or upper.startswith("HARDWARE\\"):
        return "HKLM\\" + path
    else:
        return "HKLM\\" + path


def export_registry_key(key_path: str, output_reg_path: Path) -> Tuple[bool, str]:
    """
    Exports a targeted registry key to a .reg file using reg.exe export.
    Normalizes missing hive prefixes before export.
    """
    norm_key = normalize_registry_path(key_path)
    output_reg_path.parent.mkdir(parents=True, exist_ok=True)

    if sys.platform != "win32":
        # Mock file export for non-windows testing
        with open(output_reg_path, "w", encoding="utf-8") as f:
            f.write(f"; Mock Registry Backup for {norm_key}\n")
        logger.info(f"[MOCK] Registry exported for {norm_key} -> {output_reg_path}")
        return True, f"Mock Registry Exported to {output_reg_path.name}"

    try:
        cmd = f'reg.exe export "{norm_key}" "{output_reg_path}" /y'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

        if res.returncode == 0 and output_reg_path.exists():
            logger.info(f"Registry key '{norm_key}' exported successfully to {output_reg_path}")
            return True, f"Exported {norm_key} to {output_reg_path.name}"
        else:
            err = res.stderr.strip() or "reg.exe export failed"
            logger.warning(f"[BACKUP WARNING] Registry export failed for '{norm_key}'. Reason: {err} | Fallback: Pre-state snapshot available.")
            return False, f"Registry Export Warning: {err}"
    except Exception as e:
        logger.warning(f"[BACKUP WARNING] Exception exporting registry for '{norm_key}': {e}")
        return False, f"Exception exporting registry: {str(e)}"
