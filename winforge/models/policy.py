from typing import List
from pydantic import BaseModel, Field


class DeviceProfile(BaseModel):
    is_laptop: bool = False
    is_server: bool = False
    is_domain_joined: bool = False
    is_on_battery: bool = False
    os_build: int = 22621
    total_ram_gb: float = 16.0


class PolicyRule(BaseModel):
    rule_id: str
    description: str
    allowed: bool
    reason: str
