from winforge.analyzers.hardware import get_cpu_info, get_ram_info, get_storage_drives, get_gpu_info
from winforge.analyzers.power import get_power_plan


def test_cpu_analyzer():
    info = get_cpu_info()
    assert info.physical_cores >= 1
    assert info.logical_cores >= 1


def test_ram_analyzer():
    info = get_ram_info()
    assert info.total_gb > 0.0


def test_storage_analyzer():
    drives = get_storage_drives()
    assert len(drives) >= 1
    assert drives[0].drive_letter != ""


def test_power_analyzer():
    info = get_power_plan()
    assert info.active_name != ""
