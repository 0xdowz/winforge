from typing import Optional, Dict
from pydantic import BaseModel, Field


class BenchmarkSuiteResult(BaseModel):
    timestamp: str = "2026-07-25T12:00:00Z"
    cpu_latency_ms: float = Field(default=0.0, description="CPU execution latency in ms for synthetic benchmark loop")
    memory_throughput_mbs: float = Field(default=0.0, description="Memory copy throughput in MB/s")
    disk_io_write_mbs: float = Field(default=0.0, description="Disk write performance in MB/s")
    timer_resolution_ms: float = Field(default=0.0, description="System timer resolution in ms")
    dns_latency_ms: float = Field(default=0.0, description="DNS query resolution latency in ms")


class BenchmarkComparison(BaseModel):
    before: BenchmarkSuiteResult
    after: Optional[BenchmarkSuiteResult] = None
    improvements_pct: Dict[str, float] = Field(default_factory=dict)
