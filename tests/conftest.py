import pytest
from unittest.mock import patch
from winforge.core.engine import run_full_system_scan
from winforge.models.system import SystemHealthReport, OSInfo, PowerPlan, RAMInfo, CPUInfo


@pytest.fixture
def client_system_report() -> SystemHealthReport:
    """Fixture providing a deterministic Windows 10/11 Client SystemHealthReport."""
    report = run_full_system_scan()
    # Explicitly normalize OS and power status to Client OS for deterministic unit testing
    report.os.product_name = "Windows 10 Pro"
    report.os.is_domain_joined = False
    report.power.is_on_battery = False
    return report


@pytest.fixture
def server_system_report() -> SystemHealthReport:
    """Fixture providing a deterministic Windows Server SystemHealthReport."""
    report = run_full_system_scan()
    report.os.product_name = "Windows Server 2022 Datacenter"
    report.os.is_domain_joined = False
    report.power.is_on_battery = False
    return report


@pytest.fixture
def mock_admin_privileges():
    """Fixture patching admin privileges check to True for unit tests."""
    with patch("winforge.core.safety_approval.is_admin", return_value=True):
        yield
