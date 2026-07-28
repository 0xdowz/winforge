import logging
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakStatus, TweakExecutionResult, RiskCategory
from winforge.optimizations.state_machine import TweakState, TweakExecutionTracker
from winforge.optimizations.dispatcher import CategoryDispatcher
from winforge.core.policy import PolicyEngine
from winforge.core.safety_approval import SafetyApprovalEngine
from winforge.core.session import SessionManager
from winforge.safety.restore_point import create_system_restore_point
from winforge.safety.registry_backup import export_registry_key
from winforge.safety.snapshot import SystemSnapshotManager
from winforge.safety.transaction import TransactionManager
from winforge.safety.rollback_engine import RollbackEngine

logger = logging.getLogger("winforge")


class OptimizationExecutor:
    """Orchestrates end-to-end execution framework driven by Category Dispatcher & State Machine."""

    def __init__(
        self,
        dispatcher: Optional[CategoryDispatcher] = None,
        policy_engine: Optional[PolicyEngine] = None,
        safety_engine: Optional[SafetyApprovalEngine] = None
    ):
        self.dispatcher = dispatcher or CategoryDispatcher()
        self.policy_engine = policy_engine or PolicyEngine()
        self.safety_engine = safety_engine or SafetyApprovalEngine()

    def process_tweak_pipeline(
        self,
        tweak: Tweak,
        report: SystemHealthReport,
        session_mgr: SessionManager,
        is_tech_mode: bool = False,
        user_approved: bool = True,
        mock_execution: bool = True
    ) -> Tuple[TweakExecutionTracker, TweakExecutionResult]:
        """Runs an individual tweak through the full execution lifecycle state machine."""
        tracker = TweakExecutionTracker(tweak_id=tweak.id, name=tweak.name)

        # 1. DISCOVERED -> ANALYZED (Policy & Risk Tier Check)
        profile = self.policy_engine.build_device_profile(report)
        rule = self.policy_engine.evaluate_tweak(tweak, profile)

        # Enforce Client vs Technician Risk Restrictions
        if not is_tech_mode and (tweak.risk_score > 50 or tweak.technician_only or tweak.risk_category in (RiskCategory.ADVANCED, RiskCategory.TECHNICIAN_ONLY)):
            reason = f"RISK TIER RESTRICTED: Tweak {tweak.id} (Risk: {tweak.risk_score}) requires Technician Mode (--tech)."
            logger.warning(reason)
            tracker.transition_to(TweakState.FAILED, reason=reason)
            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.SKIPPED, timestamp="", message=reason, dry_run=mock_execution
            )
            return tracker, res

        tracker.transition_to(TweakState.ANALYZED, reason=rule.reason)
        if not rule.allowed:
            tracker.transition_to(TweakState.FAILED, reason=f"Policy Blocked: {rule.reason}")
            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.SKIPPED, timestamp="", message=f"Policy Blocked: {rule.reason}", dry_run=mock_execution
            )
            return tracker, res

        # 2. ANALYZED -> RECOMMENDED (Safety Approval Check)
        safety_res = self.safety_engine.evaluate_realtime_safety(mock=mock_execution)
        tracker.transition_to(TweakState.RECOMMENDED, reason=safety_res.reason)

        if not safety_res.approved:
            tracker.transition_to(TweakState.FAILED, reason=f"Safety Pre-flight Failed: {safety_res.reason}")
            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.SKIPPED, timestamp="", message=f"Safety Pre-flight Failed: {safety_res.reason}", dry_run=mock_execution
            )
            return tracker, res

        # 3. RECOMMENDED -> APPROVED (User Confirmation)
        if not user_approved:
            tracker.transition_to(TweakState.FAILED, reason="User rejected tweak approval.")
            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.SKIPPED, timestamp="", message="User skipped tweak approval.", dry_run=mock_execution
            )
            return tracker, res

        tracker.transition_to(TweakState.APPROVED, reason="User approved tweak execution.")

        # 4. APPROVED -> BACKUP_COMPLETED (Safety Subsystem Lock)
        logger.info(f"Enforcing safety backup pre-requisites for {tweak.id}...")

        # 4a. Restore Point Creation (Skip if session restore point is active or mock execution)
        if not mock_execution and not getattr(session_mgr, "has_session_restore_point", False):
            rp_ok, rp_msg = create_system_restore_point(f"WINFORGE_OPT_{tweak.id}")
            if not rp_ok:
                tracker.transition_to(TweakState.FAILED, reason=f"Backup Failure: {rp_msg}")
                res = TweakExecutionResult(
                    tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                    status=TweakStatus.FAILED, timestamp="", message=f"EXECUTION ABORTED (Restore Point Failed): {rp_msg}", dry_run=mock_execution
                )
                return tracker, res

        # 4b. Registry Backup
        if "key" in tweak.apply_method:
            reg_key = tweak.apply_method.get("key", "")
            reg_out = session_mgr.session_dir / "registry_backups" / f"{tweak.id}.reg"
            reg_ok, reg_msg = export_registry_key(reg_key, reg_out)
            if not reg_ok and not mock_execution:
                tracker.transition_to(TweakState.FAILED, reason=f"Backup Failure: {reg_msg}")
                res = TweakExecutionResult(
                    tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                    status=TweakStatus.FAILED, timestamp="", message=f"EXECUTION ABORTED (Registry Backup Failed): {reg_msg}", dry_run=mock_execution
                )
                return tracker, res

        # 4c. Snapshot & Transaction Ledger
        snap_mgr = SystemSnapshotManager()
        snap_mgr.create_snapshot(report, session_mgr.session_dir)

        tx_mgr = TransactionManager(session_mgr.session_id, session_mgr.session_dir)
        tx_mgr.record_action(
            tweak_id=tweak.id,
            action_type=tweak.apply_method.get("type", "registry").upper(),
            target=tweak.apply_method.get("key", tweak.name),
            previous_value=str(tweak.rollback_method.get("value_data", "default")),
            new_value=str(tweak.apply_method.get("value_data", "new"))
        )

        tracker.transition_to(TweakState.BACKUP_COMPLETED, reason="Restore Point + Registry Export + Snapshot + Ledger created.")

        # 5. BACKUP_COMPLETED -> EXECUTING (Dispatched via CategoryDispatcher)
        tracker.transition_to(TweakState.EXECUTING, reason="Invoking category optimizer via CategoryDispatcher.")
        apply_ok, apply_msg = self.dispatcher.apply_tweak(tweak, mock=mock_execution)

        if not apply_ok:
            logger.error(f"Execution failed for tweak {tweak.id}: {apply_msg}")
            tracker.transition_to(TweakState.FAILED, reason=f"Apply Failed: {apply_msg}")
            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.FAILED, timestamp="", message=f"Apply Failed: {apply_msg}", dry_run=mock_execution
            )
            return tracker, res

        # 6. EXECUTING -> VERIFIED
        v_ok, v_msg = self.dispatcher.verify_tweak(tweak, mock=mock_execution)
        if not v_ok:
            logger.error(f"Verification failed for tweak {tweak.id}: {v_msg}")
            tracker.transition_to(TweakState.FAILED, reason=f"Verification Mismatch: {v_msg}")
            tracker.transition_to(TweakState.ROLLBACK_PENDING, reason="Verification failed. Initiating automatic rollback...")

            # Automated Rollback Trigger
            rb_eng = RollbackEngine()
            rb_ok, rb_logs = rb_eng.rollback_session(session_mgr.session_dir)
            tracker.transition_to(TweakState.ROLLED_BACK, reason=f"Rollback completed: {'; '.join(rb_logs)}")

            res = TweakExecutionResult(
                tweak_id=tweak.id, name=tweak.name, category=tweak.category,
                status=TweakStatus.FAILED, timestamp="", message=f"Verification Failed & Automatically Rolled Back: {v_msg}", dry_run=mock_execution
            )
            return tracker, res

        tracker.transition_to(TweakState.VERIFIED, reason=v_msg)

        # 7. VERIFIED -> COMPLETED
        tracker.transition_to(TweakState.COMPLETED, reason="Tweak successfully applied and verified.")
        res = TweakExecutionResult(
            tweak_id=tweak.id, name=tweak.name, category=tweak.category,
            status=TweakStatus.SIMULATED if mock_execution else TweakStatus.APPLIED,
            timestamp="", message=f"✓ Tweak {tweak.name} successfully executed and verified.", dry_run=mock_execution
        )

        return tracker, res
