import json
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from winforge.utils.paths import get_app_dir
from winforge.models.system import SystemHealthReport
from winforge.models.policy import PolicyRule
from winforge.models.rollback import RollbackTransaction

logger = logging.getLogger("winforge")


class SessionManager:
    """Manages unique scan/optimization session folders and persistent execution state."""

    def __init__(self, session_id: Optional[str] = None):
        if not session_id:
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_hash = uuid.uuid4().hex[:6].upper()
            session_id = f"SESSION_{now_str}_{short_hash}"

        self.session_id: str = session_id
        self.sessions_root: Path = get_app_dir() / "sessions"
        self.session_dir: Path = self.sessions_root / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def save_before_scan(self, report: SystemHealthReport) -> Path:
        """Serialize diagnostic scan report into before.json."""
        target_path = self.session_dir / "before.json"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        return target_path

    def save_diagnostic_report(self, filename: str, report: SystemHealthReport) -> Path:
        """Serialize diagnostic report to specified filename in session directory."""
        target_path = self.session_dir / filename
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        return target_path

    def save_findings(self, findings: List[Dict[str, Any]]) -> Path:
        """Serialize Policy Engine evaluation findings into findings.json."""
        target_path = self.session_dir / "findings.json"
        payload = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "recommendations": findings
        }
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return target_path

    def save_html_report(self, html_content: str) -> Path:
        """Save HTML report to report.html."""
        target_path = self.get_report_html_path()
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return target_path

    def save_rollback_ledger(self, transaction: RollbackTransaction) -> Path:
        """Serialize rollback ledger into rollback.json."""
        target_path = self.session_dir / "rollback.json"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(transaction.model_dump_json(indent=2))
        return target_path

    def get_report_html_path(self) -> Path:
        """Return target path for session report.html."""
        return self.session_dir / "report.html"


def get_pending_execution_path() -> Path:
    """Returns stable path to pending execution state file."""
    return get_app_dir() / "sessions" / "pending_execution.json"


def save_pending_execution(
    session_id: str,
    mode: str = "BEGINNER",
    max_risk: int = 20,
    selected_tweaks: Optional[List[str]] = None,
    execute: bool = True,
    dry_run: bool = False,
    tech_mode: bool = False
) -> Path:
    """
    Saves persistent execution state prior to Administrator elevation.
    Allows elevated process to automatically resume execution without user interaction.
    """
    target_path = get_pending_execution_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    state = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "mode": mode,
        "max_risk": max_risk,
        "selected_tweaks": selected_tweaks or [],
        "execute": execute,
        "dry_run": dry_run,
        "tech_mode": tech_mode,
        "resume_required": True
    }
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    logger.info(f"[ELEVATION] Persistent state saved to: {target_path} for Session {session_id}")
    return target_path


def load_pending_execution() -> Optional[Dict[str, Any]]:
    """Loads and returns pending execution state if available."""
    target_path = get_pending_execution_path()
    if not target_path.exists():
        return None

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        logger.info(f"[RESUME] Loaded session: {state.get('session_id')} | Pending tweaks: {len(state.get('selected_tweaks', []))}")
        return state
    except Exception as e:
        logger.error(f"Failed loading pending execution state from {target_path}: {e}")
        return None


def clear_pending_execution():
    """Removes pending execution state file after successful session resume."""
    target_path = get_pending_execution_path()
    if target_path.exists():
        try:
            target_path.unlink()
            logger.info("Cleared pending execution state file.")
        except Exception as e:
            logger.warning(f"Failed unlinking pending execution state file: {e}")
