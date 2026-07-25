from winforge.utils.paths import get_app_dir, get_bundle_dir, get_logs_dir, get_reports_dir, get_config_dir


def test_paths():
    app_dir = get_app_dir()
    assert app_dir.exists()
    assert "WinForge" in str(app_dir)

    logs_dir = get_logs_dir()
    assert logs_dir.exists()

    reports_dir = get_reports_dir()
    assert reports_dir.exists()

    config_dir = get_config_dir()
    assert config_dir.exists()
