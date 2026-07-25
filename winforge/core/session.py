import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from winforge.utils.paths import get_app_dir
from winforge.models.system import SystemHealthReport
from winforge.models.policy import PolicyRule
from winforge.models.rollback import RollbackTransaction


class SessionManager:
    """Manages unique scan/optimization session folders and artifacts."""

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
