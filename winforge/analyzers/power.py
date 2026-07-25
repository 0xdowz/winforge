import sys
import psutil
import logging
from winforge.models.system import PowerPlan

logger = logging.getLogger("winforge")


def get_power_plan() -> PowerPlan:
    """Detect current Windows power scheme and battery status."""
    is_on_battery = False
    try:
        battery = psutil.sensors_battery()
        if battery:
            is_on_battery = not battery.power_plugged
    except Exception:
        pass

    active_name = "Balanced"
    active_guid = "381b4222-f694-41f0-9685-ff5bb260df2e"
    is_high_perf = False

    if sys.platform == "win32":
        try:
            import subprocess
            out = subprocess.check_output("powercfg /getactivescheme", shell=True, text=True)
            if "High performance" in out or "Ultimate Performance" in out:
                is_high_perf = True
                active_name = "High Performance" if "High performance" in out else "Ultimate Performance"
            elif "Power saver" in out:
                active_name = "Power Saver"
        except Exception as e:
            logger.debug(f"powercfg query failed: {e}")

    return PowerPlan(
        active_guid=active_guid,
        active_name=active_name,
        is_high_performance=is_high_perf,
        is_on_battery=is_on_battery
    )
