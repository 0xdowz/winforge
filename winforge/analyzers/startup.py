import sys
import logging
from typing import List
from winforge.models.system import StartupItem

logger = logging.getLogger("winforge")


def get_startup_items() -> List[StartupItem]:
    """Scan Registry run keys for startup applications."""
    items: List[StartupItem] = []

    if sys.platform == "win32":
        import winreg
        run_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "HKLM Run"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "HKCU Run")
        ]

        for hive, path, loc_name in run_keys:
            try:
                key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
                count = winreg.QueryInfoKey(key)[1]
                for i in range(count):
                    try:
                        name, val, _ = winreg.EnumValue(key, i)
                        items.append(StartupItem(
                            name=name,
                            command=str(val),
                            location=loc_name,
                            enabled=True
                        ))
                    except Exception:
                        continue
                winreg.CloseKey(key)
            except Exception as e:
                logger.debug(f"Failed opening startup registry key {path}: {e}")
    else:
        # Mock items for non-windows testing
        items = [
            StartupItem(name="OneDrive", command="C:\\Users\\User\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe /background", location="HKCU Run", enabled=True),
            StartupItem(name="UpdateChecker", command="C:\\Program Files\\App\\checker.exe", location="HKLM Run", enabled=True)
        ]

    return items
