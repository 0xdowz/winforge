import logging
from typing import List, Dict, Any
from copy import deepcopy

from winforge.models.system import SystemHealthReport, CategoryScores
from winforge.models.tweak import Tweak, TweakCategory, TweakStatus, TweakExecutionResult
from winforge.models.policy import DeviceProfile
from winforge.core.policy import PolicyEngine

logger = logging.getLogger("winforge")


class DryRunSimulator:
    """Simulates optimization pipelines without applying mutations to system state."""

    def __init__(self, policy_engine: Optional[PolicyEngine] = None):
        self.policy_engine = policy_engine or PolicyEngine()

    def simulate_optimizations(
        self,
        report: SystemHealthReport,
        candidate_tweaks: List[Tweak]
    ) -> Dict[str, Any]:
        """Simulate optimization execution and compute expected score improvements."""
        logger.info("Initiating Dry-Run optimization simulation...")
        profile = self.policy_engine.build_device_profile(report)

        results: List[TweakExecutionResult] = []
        simulated_actions: List[Dict[str, Any]] = []

        boost_perf = 0.0
        boost_sec = 0.0
        boost_maint = 0.0
        boost_startup = 0.0

        for tweak in candidate_tweaks:
            rule = self.policy_engine.evaluate_tweak(tweak, profile)
            if not rule.allowed:
                results.append(TweakExecutionResult(
                    tweak_id=tweak.id,
                    name=tweak.name,
                    category=tweak.category,
                    status=TweakStatus.SKIPPED,
                    timestamp="",
                    message=rule.reason,
                    dry_run=True
                ))
                continue

            # Simulate tweak impact
            if tweak.category == TweakCategory.GAMING or tweak.category == TweakCategory.POWER:
                boost_perf += 5.0
            elif tweak.category == TweakCategory.SECURITY_PRIVACY:
                boost_sec += 5.0
            elif tweak.category == TweakCategory.CLEANUP:
                boost_maint += 7.5
            elif tweak.category == TweakCategory.STARTUP or tweak.category == TweakCategory.SERVICES:
                boost_startup += 6.0

            simulated_actions.append({
                "tweak_id": tweak.id,
                "name": tweak.name,
                "category": tweak.category.value,
                "action": tweak.apply_method,
                "rollback": tweak.rollback_method
            })

            results.append(TweakExecutionResult(
                tweak_id=tweak.id,
                name=tweak.name,
                category=tweak.category,
                status=TweakStatus.SIMULATED,
                timestamp="",
                message="[DRY-RUN SIMULATION] Tweak validated and queued for safe execution.",
                dry_run=True
            ))

        # Calculate simulated post-optimization health scores
        cats = report.categories
        sim_cats = CategoryScores(
            performance_score=min(100.0, cats.performance_score + boost_perf),
            security_score=min(100.0, cats.security_score + boost_sec),
            maintenance_score=min(100.0, cats.maintenance_score + boost_maint),
            startup_score=min(100.0, cats.startup_score + boost_startup)
        )

        return {
            "dry_run": True,
            "baseline_health_score": report.health_score,
            "simulated_health_score": sim_cats.overall_health_score,
            "score_delta": round(sim_cats.overall_health_score - report.health_score, 1),
            "simulated_categories": sim_cats,
            "results": results,
            "simulated_actions": simulated_actions
        }
