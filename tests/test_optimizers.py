from pathlib import Path
from winforge.optimizations.gaming import GamingOptimizer
from winforge.optimizations.power import PowerOptimizer
from winforge.optimizations.startup import StartupOptimizer
from winforge.optimizations.services import ServicesOptimizer
from winforge.optimizations.cleanup import CleanupOptimizer
from winforge.optimizations.network import NetworkOptimizer
from winforge.core.engine import run_full_system_scan


def test_gaming_optimizer():
    opt = GamingOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)
    assert len(tweaks) >= 1

    for t in tweaks:
        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True
        assert "[MOCK" in msg or "Successfully" in msg

        v_ok, v_msg = opt.verify_tweak(t, mock=True)
        assert v_ok is True

        rb_ok, rb_msg = opt.rollback(t, Path("."))
        assert rb_ok is True


def test_power_optimizer():
    opt = PowerOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)

    if not report.power.is_on_battery:
        assert len(tweaks) >= 1
        t = tweaks[0]
        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True
        assert "[MOCK POWER]" in msg

        rb_ok, rb_msg = opt.rollback(t, Path("."))
        assert rb_ok is True


def test_startup_optimizer_protection_rules():
    opt = StartupOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)
    assert isinstance(tweaks, list)

    for t in tweaks:
        name_lower = t.name.lower()
        # Verify protected keywords are not returned
        assert "windefend" not in name_lower
        assert "antivirus" not in name_lower

        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True


def test_services_optimizer_immutable_protection():
    opt = ServicesOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)

    for t in tweaks:
        svc_name = t.apply_method.get("service_name", "").lower()
        # Critical services must never be in detected tweaks
        assert svc_name not in ["rpcss", "dcomlaunch", "eventlog", "plugplay", "cryptsvc", "windefend"]

        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True


def test_cleanup_optimizer_safety():
    opt = CleanupOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)
    assert len(tweaks) >= 1

    for t in tweaks:
        target = t.apply_method.get("target_dir", "").lower()
        assert "system32" not in target
        assert "drivers" not in target

        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True
        assert "[CLEANUP AUDIT LOG]" in msg or "[MOCK CLEANUP]" in msg


def test_network_optimizer():
    opt = NetworkOptimizer()
    report = run_full_system_scan()
    tweaks = opt.detect(report)
    assert len(tweaks) >= 1

    for t in tweaks:
        ok, msg = opt.apply_tweak(t, mock=True)
        assert ok is True
