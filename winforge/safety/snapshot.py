import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from winforge.models.system import SystemHealthReport
from winforge.analyzers.services import get_services_info
from winforge.analyzers.power import get_power_plan

logger = logging.getLogger("winforge")


class SystemSnapshotManager:
    """Captures pre-modification system state snapshot."""

    def create_snapshot(self, report: SystemHealthReport, session_dir: Path) -> Path:
        """Serializes current service statuses, power plan, and drive info to snapshot.json."""
        snapshot_path = session_dir / "snapshot.json"
        
        services = get_services_info()
        power = get_power_plan()

        data = {
            "timestamp": datetime.now().isoformat(),
            "health_score": report.health_score,
            "overall_health_score": report.health_score,
            "services": [
                {
                    "name": s.name,
                    "status": s.status,
                    "start_type": s.start_type
                } for s in services
            ],
            "power_plan": {
                "active_guid": power.active_guid,
                "active_name": power.active_name
            },
            "drives": [
                {
                    "drive": d.drive_letter,
                    "free_gb": d.free_gb
                } for d in report.drives
            ]
        }

        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"System state snapshot written to: {snapshot_path}")
        return snapshot_path

    def read_snapshot(self, snapshot_path: Path) -> Optional[Dict[str, Any]]:
        """Reads snapshot JSON from file."""
        if not snapshot_path.exists():
            return None
        try:
            with open(snapshot_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed reading snapshot {snapshot_path}: {e}")
            return None

    def load_snapshot(self, snapshot_path: Path) -> Optional[Dict[str, Any]]:
        """Alias for read_snapshot."""
        return self.read_snapshot(snapshot_path)
