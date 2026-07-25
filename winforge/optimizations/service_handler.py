import sys
import subprocess
import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger("winforge")


class ServiceHandler:
    """Safe Windows Service Handler supporting state query, start type update, and mock modes."""

    def get_service_status(self, service_name: str) -> Tuple[bool, Dict[str, Any]]:
        """Query service status and startup type."""
        if sys.platform != "win32":
            return True, {"name": service_name, "status": "Running", "start_type": "Automatic"}

        try:
            import psutil
            for svc in psutil.win_service_iter():
                if svc.name().lower() == service_name.lower():
                    info = svc.as_dict()
                    return True, {
                        "name": info.get("name"),
                        "status": info.get("status"),
                        "start_type": info.get("start_type")
                    }
            return False, {"error": f"Service {service_name} not found"}
        except Exception as e:
            logger.error(f"Failed querying service {service_name}: {e}")
            return False, {"error": str(e)}

    def set_service_start_type(
        self,
        service_name: str,
        start_type: str,
        mock: bool = True
    ) -> Tuple[bool, str]:
        """Sets Windows service startup type (e.g. demand, auto, disabled). Default mock=True disables real mutations."""
        if mock or sys.platform != "win32":
            logger.info(f"[MOCK SERVICE] Service {service_name} start_type set to {start_type}")
            return True, f"[MOCK SERVICE] Set {service_name} startup to {start_type}"

        try:
            cmd = f'sc.exe config "{service_name}" start= {start_type}'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"Service {service_name} startup type set to {start_type}")
                return True, f"Service {service_name} startup set to {start_type}"
            else:
                err = res.stderr.strip() or "sc.exe config failed"
                logger.error(f"Failed configuring service {service_name}: {err}")
                return False, f"Service config failed: {err}"
        except Exception as e:
            logger.error(f"Exception configuring service {service_name}: {e}")
            return False, f"Exception configuring service: {str(e)}"
