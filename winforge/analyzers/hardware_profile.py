"""
WinForge Hardware Intelligence Engine v2.
Analyzes system hardware (CPU, GPU class, RAM, Storage, Power state) to generate profile recommendations with confidence scoring.
"""

import logging
from typing import Dict, Any, List, Optional
from winforge.models.system import SystemHealthReport

logger = logging.getLogger("winforge")


class HardwareIntelligenceEngine:
    """Hardware-aware optimization recommendation engine with confidence scoring and guaranteed API schema stability."""

    def analyze_hardware_profile(self, report: Optional[SystemHealthReport] = None) -> Dict[str, Any]:
        """
        Recommends profile based on CPU, GPU, RAM, Storage, and Power State with confidence rating.
        Guarantees complete schema stability even with missing or partial diagnostic reports.
        """
        try:
            if not report:
                return self._default_fallback_schema("No diagnostic report provided")

            is_battery = bool(report.power.is_on_battery) if report.power else False
            total_ram = float(report.ram.total_gb) if report.ram and report.ram.total_gb else 8.0
            cpu_cores = int(report.cpu.logical_cores) if report.cpu and report.cpu.logical_cores else 4

            gpu_name = ""
            if report.gpu and len(report.gpu) > 0 and report.gpu[0].name:
                gpu_name = str(report.gpu[0].name)
            
            gpu_lower = gpu_name.lower()
            has_discrete_gpu = any(vendor in gpu_lower for vendor in ["nvidia", "geforce", "radeon", "rtx", "gtx", "arc"])
            has_ssd = any(drive.is_ssd for drive in report.drives) if report.drives else True

            reasons: List[str] = []

            if is_battery:
                recommended_profile = "Battery Efficiency Profile"
                confidence = 95
                reasons.append("Mobile device running on battery power detected")
                reasons.append(f"System RAM: {total_ram:.1f} GB available")
                reasons.append("Thermal & power saving optimizations prioritized")
            elif has_discrete_gpu:
                recommended_profile = "Gaming Performance Profile"
                confidence = 92
                reasons.append(f"Dedicated GPU detected ({gpu_name if gpu_name else 'Discrete Graphics'})")
                reasons.append("AC main power supply connected")
                reasons.append(f"{total_ram:.1f} GB RAM installed for high-throughput gaming")
                if has_ssd:
                    reasons.append("High-speed SSD storage available for fast asset streaming")
            elif cpu_cores >= 8 and total_ram >= 16.0:
                recommended_profile = "Workstation Profile"
                confidence = 88
                reasons.append(f"Multi-core CPU detected ({cpu_cores} logical cores)")
                reasons.append(f"High-capacity memory ({total_ram:.1f} GB RAM)")
                reasons.append("AC main power supply connected")
            else:
                recommended_profile = "Balanced Client Profile"
                confidence = 85
                reasons.append("Standard Windows desktop configuration detected")
                reasons.append(f"CPU: {cpu_cores} cores, RAM: {total_ram:.1f} GB")

            rationale_str = " • ".join(reasons) if reasons else "Standard desktop configuration"

            return {
                "recommended_profile": recommended_profile,
                "confidence_percent": confidence,
                "reasons": reasons,
                "rationale": rationale_str,
                "has_discrete_gpu": has_discrete_gpu,
                "is_on_battery": is_battery,
            }
        except Exception as e:
            logger.warning(f"Error during hardware profile analysis: {e}. Falling back to default schema.")
            return self._default_fallback_schema(str(e))

    def _default_fallback_schema(self, reason: str) -> Dict[str, Any]:
        """Provides guaranteed default schema fallback if analysis fails."""
        default_reasons = ["Standard Windows desktop configuration assumed", f"Rationale note: {reason}"]
        return {
            "recommended_profile": "Balanced Client Profile",
            "confidence_percent": 80,
            "reasons": default_reasons,
            "rationale": " • ".join(default_reasons),
            "has_discrete_gpu": False,
            "is_on_battery": False,
        }


hardware_engine = HardwareIntelligenceEngine()
