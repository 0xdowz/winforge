"""
WinForge Hardware Intelligence Engine.
Analyzes system hardware (CPU cores, RAM, GPU class, battery state) to recommend optimal hardware profiles.
"""

from typing import Dict, Any
from winforge.models.system import SystemHealthReport


class HardwareIntelligenceEngine:
    """Hardware-aware optimization recommendation engine."""

    def analyze_hardware_profile(self, report: SystemHealthReport) -> Dict[str, Any]:
        """Recommends profile based on CPU, GPU, RAM, and Power State."""
        is_battery = report.power.is_on_battery if report.power else False
        total_ram = report.ram.total_gb if report.ram else 8.0
        cpu_cores = report.cpu.logical_cores if report.cpu else 4
        gpu_name = report.gpu[0].name.lower() if report.gpu and report.gpu[0].name else "generic"

        has_discrete_gpu = any(vendor in gpu_name for vendor in ["nvidia", "geforce", "radeon", "rtx", "gtx", "arc"])

        if is_battery:
            recommended_profile = "Battery Efficiency Profile"
            rationale = "Mobile device running on battery power detected. Prioritizing power saving & thermal longevity."
        elif has_discrete_gpu:
            recommended_profile = "Gaming Performance Profile"
            rationale = f"Dedicated graphics ({report.gpu[0].name}) & AC power detected. Tailored for low latency & frame pacing."
        elif cpu_cores >= 8 and total_ram >= 16.0:
            recommended_profile = "Productivity Workstation Profile"
            rationale = f"High-capacity CPU ({cpu_cores} cores) & RAM ({total_ram} GB) detected. Optimized for multi-tasking & throughput."
        else:
            recommended_profile = "Balanced Client Profile"
            rationale = "Standard Windows client hardware configuration detected. Optimized for overall stability & responsiveness."

        return {
            "recommended_profile": recommended_profile,
            "rationale": rationale,
            "has_discrete_gpu": has_discrete_gpu,
            "is_on_battery": is_battery,
        }


hardware_engine = HardwareIntelligenceEngine()
