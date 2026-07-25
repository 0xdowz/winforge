import sys
import subprocess
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("winforge")


def export_registry_key(key_path: str, output_reg_path: Path) -> Tuple[bool, str]:
    """Exports a targeted registry key to a .reg file using reg export."""
    output_reg_path.parent.mkdir(parents=True, exist_ok=True)

    if sys.platform != "win32":
        # Mock file export for non-windows testing
        with open(output_reg_path, "w", encoding="utf-8") as f:
            f.write(f"; Mock Registry Backup for {key_path}\n")
        logger.info(f"[MOCK] Registry exported for {key_path} -> {output_reg_path}")
        return True, f"Mock Registry Exported to {output_reg_path.name}"

    try:
        cmd = f'reg.exe export "{key_path}" "{output_reg_path}" /y'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

        if res.returncode == 0 and output_reg_path.exists():
            logger.info(f"Registry subkey '{key_path}' exported successfully to {output_reg_path}")
            return True, f"Exported {key_path} to {output_reg_path.name}"
        else:
            err = res.stderr.strip() or "reg.exe export failed"
            logger.error(f"Registry export failed for '{key_path}': {err}")
            return False, f"Registry Export Failed: {err}"
    except Exception as e:
        logger.error(f"Exception during registry export for '{key_path}': {e}")
        return False, f"Exception exporting registry: {str(e)}"
