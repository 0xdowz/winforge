"""
WinForge Hardware Intelligence Engine v2.
Analyzes system hardware (CPU, GPU class, RAM, Storage, Power state) to generate profile recommendations with confidence scoring.
"""

from typing import Dict, Any, List
from winforge.models.system import SystemHealthReport


class HardwareIntelligenceEngine:
    """Hardware-aware optimization recommendation engine with confidence scoring."""

    def analyze_hardware_profile(self, report: SystemHealthReport) -> Dict[str, Any]:
        """Recommends profile based on CPU, GPU, RAM, Storage, and Power State with confidence rating."""
        is_battery = report.power.is_on_battery if report.power else False
        total_ram = report.ram.total_gb if report.ram else 8.0
        cpu_cores = report.cpu.logical_cores if report.cpu else 4
        gpu_name = report.gpu[0].name.lower() if report.gpu and report.gpu[0].name else "generic"

        has_discrete_gpu = any(vendor in gpu_name for vendor in ["nvidia", "geforce", "radeon", "rtx", "gtx", "arc"])
        has_ssd = any(drive.is_ssd for drive in report.drives) if report.drives else True

        reasons: List[str] = []

        if is_battery:
            recommended_profile = "Battery Efficiency Profile"
            confidence = 95
            reasons.append("Mobile device running on battery power detected")
            reasons.append(f"System RAM: {total_ram} GB available")
            reasons.append("Thermal & power saving optimizations prioritized")
        elif has_discrete_gpu:
            recommended_profile = "Gaming Performance Profile"
            confidence = 92
            reasons.append(f"Dedicated GPU detected ({report.gpu[0].name})")
            reasons.append("AC main power supply connected")
            reasons.append(f"{total_ram} GB RAM installed for high-throughput gaming")
            if has_ssd:
                reasons.append("High-speed SSD storage available for fast asset streaming")
        elif cpu_cores >= 8 and total_ram >= 16.0:
            recommended_profile = "Workstation Profile"
            confidence = 88
            reasons.append(f"Multi-core CPU detected ({cpu_cores} logical cores)")
            reasons.append(f"High-capacity memory ({total_ram} GB RAM)")
            reasons.append("AC main power supply connected")
        else:
            recommended_profile = "Balanced Client Profile"
            confidence = 85
            reasons.append("Standard Windows desktop configuration detected")
            reasons.append(f"CPU: {cpu_cores} cores, RAM: {total_ram} GB")

        return {
            "recommended_profile": recommended_profile,
            "confidence_percent": confidence,
            "reasons": reasons,
            "has_discrete_gpu": has_discrete_gpu,
            "is_on_battery": is_battery,
        }


hardware_engine = HardwareIntelligenceEngine()
