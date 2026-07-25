import sys
import logging
from typing import Tuple, Any, Optional

logger = logging.getLogger("winforge")

HIVE_MAP = {}
if sys.platform == "win32":
    import winreg
    HIVE_MAP = {
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKCR": winreg.HKEY_CLASSES_ROOT,
        "HKU": winreg.HKEY_USERS
    }


class RegistryHandler:
    """Safe Win32 Registry Handler supporting read, write, and mock modes."""

    def read_registry_value(self, hive_str: str, key_path: str, value_name: str) -> Tuple[bool, Any, str]:
        """Reads value from registry without modifying state."""
        if sys.platform != "win32":
            logger.info(f"[MOCK READ] Registry {hive_str}\\{key_path} -> {value_name}")
            return True, None, "Mock environment read."

        try:
            import winreg
            hive = HIVE_MAP.get(hive_str.upper(), winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)
            return True, val, "Registry read success."
        except Exception as e:
            logger.debug(f"Registry query failed for {hive_str}\\{key_path}\\{value_name}: {e}")
            return False, None, str(e)

    def write_registry_value(
        self,
        hive_str: str,
        key_path: str,
        value_name: str,
        value_type_str: str,
        value_data: Any,
        mock: bool = True
    ) -> Tuple[bool, str]:
        """Writes value to registry. Default mock=True disables real mutations."""
        if mock or sys.platform != "win32":
            logger.info(f"[MOCK WRITE] Registry {hive_str}\\{key_path}\\{value_name} = {value_data} (Type: {value_type_str})")
            return True, f"[MOCK WRITE] Set {value_name} = {value_data}"

        try:
            import winreg
            hive = HIVE_MAP.get(hive_str.upper(), winreg.HKEY_LOCAL_MACHINE)
            key = winreg.CreateKeyEx(hive, key_path, 0, winreg.KEY_SET_VALUE)
            
            val_type = winreg.REG_DWORD if value_type_str == "REG_DWORD" else winreg.REG_SZ
            winreg.SetValueEx(key, value_name, 0, val_type, value_data)
            winreg.CloseKey(key)
            
            logger.info(f"Registry updated: {hive_str}\\{key_path}\\{value_name} = {value_data}")
            return True, f"Successfully set {value_name} = {value_data}"
        except Exception as e:
            logger.error(f"Registry write failed for {hive_str}\\{key_path}\\{value_name}: {e}")
            return False, f"Registry write failed: {str(e)}"
