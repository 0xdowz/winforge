import sys
import psutil
import logging
from typing import List
from winforge.models.system import ServiceDetail

logger = logging.getLogger("winforge")

# Critical Windows System Services that must never be disabled or stopped
CRITICAL_SERVICES = {
    "rpcss", "dcomlaunch", "eventlog", "plugplay", "cryptsvc",
    "dhcp", "dnscache", "lsass", "windefend", "wdnissvc",
    "sense", "wuauserv", "samss", "gpsvc", "seclogon"
}

# Non-essential telemetry or optional bloat services
NON_ESSENTIAL_SERVICES = {
    "diagtrack", "sysmain", "mapsbroker", "dmwappushservice",
    "retaildemo", "remoteaccess", "fax", "wisvc"
}


def get_services_info() -> List[ServiceDetail]:
    """Inspect installed Windows services."""
    services: List[ServiceDetail] = []
    if sys.platform != "win32":
        # Mock service list for non-windows testing
        return [
            ServiceDetail(name="DiagTrack", display_name="Connected User Experiences and Telemetry", status="Running", start_type="Automatic", is_critical=False),
            ServiceDetail(name="RpcSs", display_name="Remote Procedure Call", status="Running", start_type="Automatic", is_critical=True),
            ServiceDetail(name="SysMain", display_name="SysMain / Superfetch", status="Running", start_type="Automatic", is_critical=False),
            ServiceDetail(name="WinDefend", display_name="Windows Defender Antivirus Service", status="Running", start_type="Automatic", is_critical=True),
        ]

    try:
        for svc in psutil.win_service_iter():
            try:
                info = svc.as_dict()
                name = info.get("name", "").lower()
                display_name = info.get("display_name", "") or name
                status = info.get("status", "unknown")
                start_type = info.get("start_type", "unknown")
                is_critical = name in CRITICAL_SERVICES

                services.append(ServiceDetail(
                    name=info.get("name", ""),
                    display_name=display_name,
                    status=status,
                    start_type=str(start_type),
                    is_critical=is_critical
                ))
            except Exception:
                continue
    except Exception as e:
        logger.error(f"Failed to scan Windows services: {e}")

    return services
