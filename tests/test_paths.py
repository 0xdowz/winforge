from winforge.utils.paths import (
    get_app_dir, get_bundle_dir, get_logs_dir, get_internal_logs_dir,
    get_reports_dir, get_sessions_dir, get_config_dir,
    get_desktop_dir, get_user_reports_root, get_output_mode
)


def test_paths():
    app_dir = get_app_dir()
    assert app_dir.exists()
    assert "WinForge" in str(app_dir)

    logs_dir = get_logs_dir()
    assert logs_dir.exists()
    assert "Logs" in str(logs_dir)

    internal_logs_dir = get_internal_logs_dir()
    assert internal_logs_dir.exists()
    assert "logs" in str(internal_logs_dir).lower()

    reports_dir = get_reports_dir()
    assert reports_dir.exists()
    assert "Diagnostics" in str(reports_dir)

    sessions_dir = get_sessions_dir()
    assert sessions_dir.exists()
    assert "Sessions" in str(sessions_dir)

    config_dir = get_config_dir()
    assert config_dir.exists()


def test_desktop_dir_and_user_reports_root():
    desktop = get_desktop_dir()
    assert desktop is not None
    assert desktop.exists()

    root = get_user_reports_root()
    assert root.exists()
    assert "WinForge Reports" in str(root)

    readme = root / "README.txt"
    assert readme.exists()
    content = readme.read_text(encoding="utf-8")
    assert "WINFORGE USER REPORTS" in content
    assert "rollback" in content


def test_configurable_output_mode(monkeypatch):
    monkeypatch.setenv("WINFORGE_OUTPUT_MODE", "LOCALAPPDATA")
    assert get_output_mode() == "LOCALAPPDATA"
    root = get_user_reports_root()
    assert "UserReports" in str(root)
