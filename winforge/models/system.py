from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CPUInfo(BaseModel):
    name: str = Field(default="Unknown CPU")
    physical_cores: int = Field(default=1)
    logical_cores: int = Field(default=1)
    max_frequency_mhz: float = Field(default=0.0)
    current_usage_pct: float = Field(default=0.0)


class GPUInfo(BaseModel):
    name: str = Field(default="Unknown GPU")
    vram_mb: int = Field(default=0)
    driver_version: str = Field(default="Unknown")


class RAMInfo(BaseModel):
    total_gb: float = Field(default=0.0)
    available_gb: float = Field(default=0.0)
    used_gb: float = Field(default=0.0)
    percent_used: float = Field(default=0.0)
    speed_mhz: Optional[int] = None


class StorageDrive(BaseModel):
    drive_letter: str
    file_system: str = "NTFS"
    total_gb: float = 0.0
    free_gb: float = 0.0
    used_gb: float = 0.0
    percent_used: float = 0.0
    is_ssd: bool = True
    trim_enabled: bool = True


class OSInfo(BaseModel):
    product_name: str = "Windows"
    build_number: str = "0"
    edition: str = "Standard"
    architecture: str = "64-bit"
    is_domain_joined: bool = False
    domain_name: Optional[str] = None


class ServiceDetail(BaseModel):
    name: str
    display_name: str
    status: str  # e.g., Running, Stopped
    start_type: str  # e.g., Automatic, Manual, Disabled
    is_critical: bool = False


class StartupItem(BaseModel):
    name: str
    command: str
    location: str
    enabled: bool = True


class NetworkAdapter(BaseModel):
    name: str
    mac_address: str = "00:00:00:00:00:00"
    ip_address: str = "127.0.0.1"
    link_speed_mbps: int = 1000


class PowerPlan(BaseModel):
    active_guid: str = ""
    active_name: str = "Balanced"
    is_high_performance: bool = False
    is_on_battery: bool = False


class CategoryScores(BaseModel):
    performance_score: float = Field(default=100.0, ge=0.0, le=100.0)
    security_score: float = Field(default=100.0, ge=0.0, le=100.0)
    maintenance_score: float = Field(default=100.0, ge=0.0, le=100.0)
    startup_score: float = Field(default=100.0, ge=0.0, le=100.0)

    @property
    def overall_health_score(self) -> float:
        """Weighted Overall System Health Score (0-100)"""
        return round(
            (self.performance_score * 0.25) +
            (self.security_score * 0.25) +
            (self.maintenance_score * 0.25) +
            (self.startup_score * 0.25),
            1
        )


class SystemHealthReport(BaseModel):
    timestamp: str
    health_score: float
    categories: CategoryScores
    cpu: CPUInfo
    gpu: List[GPUInfo]
    ram: RAMInfo
    drives: List[StorageDrive]
    os: OSInfo
    power: PowerPlan
    startup_count: int
    non_essential_services_count: int
    warnings: List[str] = Field(default_factory=list)
