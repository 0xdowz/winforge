import sys
import platform
import logging
from winforge.models.system import OSInfo

logger = logging.getLogger("winforge")


def get_os_info() -> OSInfo:
    """Gather Windows OS version, edition, build number, and domain state."""
    product_name = f"Windows {platform.system()} {platform.release()}"
    build_number = platform.version()
    edition = "Professional"
    arch = platform.architecture()[0]
    is_domain_joined = False
    domain_name = None

    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            try:
                build_number, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
            except FileNotFoundError:
                pass
            try:
                edition, _ = winreg.QueryValueEx(key, "EditionID")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception as e:
            logger.debug(f"Registry query for OS info failed: {e}")

        try:
            import win32api
            import win32net
            domain_info = win32net.NetGetJoinInformation()
            if domain_info and domain_info[1] == 3:  # NetSetupDomainName
                is_domain_joined = True
                domain_name = domain_info[0]
        except Exception:
            pass

    return OSInfo(
        product_name=product_name,
        build_number=build_number,
        edition=edition,
        architecture=arch,
        is_domain_joined=is_domain_joined,
        domain_name=domain_name
    )
