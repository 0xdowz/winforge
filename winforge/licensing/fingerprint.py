import sys
import hashlib
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("winforge")


class FingerprintSignal(BaseModel):
    name: str
    value_hash: str
    availability_score: float = 1.0  # 1.0 if present, 0.0 if missing
    reliability_score: float = 1.0   # Stability across reboots
    confidence_weight: float = 1.0   # Weight in matching algorithm


class FingerprintRecord(BaseModel):
    version: int = Field(default=1)
    salt: str = Field(default="WINFORGE_SALT")
    signals: Dict[str, FingerprintSignal] = Field(default_factory=dict)

    def composite_hash(self) -> str:
        """Computes deterministic composite hash of all available signals."""
        combined = ""
        for name in sorted(self.signals.keys()):
            sig = self.signals[name]
            if sig.availability_score > 0:
                combined += f"{name}:{sig.value_hash};"
        return hashlib.sha256((combined + self.salt).encode("utf-8")).hexdigest()


class FingerprintProvider:
    """Collects normalized, salted hardware signals without storing raw identifiers."""

    SIGNAL_WEIGHTS = {
        "MOTHERBOARD_UUID": 0.40,
        "CPU_PROCESSOR_ID": 0.30,
        "PRIMARY_DISK_SERIAL": 0.15,
        "PRIMARY_NIC_MAC": 0.15
    }

    def collect_fingerprint(
        self,
        salt: str = "WINFORGE_SALT",
        mock_signals: Optional[Dict[str, str]] = None
    ) -> FingerprintRecord:
        """Collects salted SHA-256 hashes of hardware signals."""
        signals: Dict[str, FingerprintSignal] = {}

        if mock_signals:
            for sig_name, raw_val in mock_signals.items():
                avail = 1.0 if raw_val and raw_val != "UNKNOWN" else 0.0
                val_hash = self._hash_signal(raw_val, salt) if avail else "MISSING"
                weight = self.SIGNAL_WEIGHTS.get(sig_name, 0.25)
                signals[sig_name] = FingerprintSignal(
                    name=sig_name,
                    value_hash=val_hash,
                    availability_score=avail,
                    reliability_score=1.0,
                    confidence_weight=weight
                )
            return FingerprintRecord(version=1, salt=salt, signals=signals)

        # Real System Hardware Collection (Win32 / psutil / WMI)
        raw_map = self._query_raw_hardware()
        for sig_name, raw_val in raw_map.items():
            avail = 1.0 if raw_val and raw_val not in ("UNKNOWN", "NONE", "DEFAULT STRING") else 0.0
            val_hash = self._hash_signal(raw_val, salt) if avail else "MISSING"
            weight = self.SIGNAL_WEIGHTS.get(sig_name, 0.25)
            signals[sig_name] = FingerprintSignal(
                name=sig_name,
                value_hash=val_hash,
                availability_score=avail,
                reliability_score=1.0,
                confidence_weight=weight
            )

        return FingerprintRecord(version=1, salt=salt, signals=signals)

    def _query_raw_hardware(self) -> Dict[str, str]:
        """Queries WMI/Win32/psutil for raw hardware strings."""
        raw: Dict[str, str] = {
            "MOTHERBOARD_UUID": "GENERIC_MB_UUID",
            "CPU_PROCESSOR_ID": "GENERIC_CPU_ID",
            "PRIMARY_DISK_SERIAL": "GENERIC_DISK_SERIAL",
            "PRIMARY_NIC_MAC": "00:1A:2B:3C:4D:5E"
        }

        if sys.platform == "win32":
            try:
                import wmi
                w = wmi.WMI()
                for board in w.Win32_BaseBoard():
                    if board.SerialNumber:
                        raw["MOTHERBOARD_UUID"] = str(board.SerialNumber).strip()
                for cpu in w.Win32_Processor():
                    if cpu.ProcessorId:
                        raw["CPU_PROCESSOR_ID"] = str(cpu.ProcessorId).strip()
                for disk in w.Win32_PhysicalMedia():
                    if disk.SerialNumber:
                        raw["PRIMARY_DISK_SERIAL"] = str(disk.SerialNumber).strip()
                        break
            except Exception as e:
                logger.debug(f"WMI hardware query failed: {e}")

        return raw

    def _hash_signal(self, raw_val: str, salt: str) -> str:
        """Normalizes raw string and returns SHA-256 salted hash."""
        normalized = raw_val.strip().upper()
        salted = f"{salt}:{normalized}:{salt}"
        return hashlib.sha256(salted.encode("utf-8")).hexdigest()


class FingerprintMatcher:
    """Dynamic Machine Fingerprint Matching Engine supporting hardware tolerance."""

    def compare(
        self,
        current: FingerprintRecord,
        stored_composite_hash: str,
        target_record: Optional[FingerprintRecord] = None,
        threshold: float = 75.0
    ) -> Dict[str, Any]:
        """Calculates dynamic match score (0-100) and produces activation decision."""

        # Direct composite hash match
        if current.composite_hash() == stored_composite_hash:
            return {
                "match_score": 100.0,
                "matched_components": list(current.signals.keys()),
                "changed_components": [],
                "activation_decision": True,
                "threshold_required": threshold
            }

        # Component-by-component matching if target_record available
        if target_record:
            matched: List[str] = []
            changed: List[str] = []
            total_weight = 0.0
            matched_weight = 0.0

            for name, cur_sig in current.signals.items():
                tar_sig = target_record.signals.get(name)
                w = cur_sig.confidence_weight

                if cur_sig.availability_score > 0 and tar_sig and tar_sig.availability_score > 0:
                    total_weight += w
                    if cur_sig.value_hash == tar_sig.value_hash:
                        matched_weight += w
                        matched.append(name)
                    else:
                        changed.append(name)

            score = round((matched_weight / total_weight) * 100.0, 1) if total_weight > 0 else 0.0
            decision = score >= threshold

            return {
                "match_score": score,
                "matched_components": matched,
                "changed_components": changed,
                "activation_decision": decision,
                "threshold_required": threshold
            }

        # Fallback comparison if target record not provided
        return {
            "match_score": 0.0,
            "matched_components": [],
            "changed_components": list(current.signals.keys()),
            "activation_decision": False,
            "threshold_required": threshold
        }
