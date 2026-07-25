import logging
from datetime import datetime
from typing import Optional

from winforge.models.benchmark import BenchmarkSuiteResult, BenchmarkComparison
from winforge.benchmark.cpu_bench import run_cpu_benchmark
from winforge.benchmark.memory_bench import run_memory_benchmark
from winforge.benchmark.disk_bench import run_disk_benchmark
from winforge.benchmark.net_bench import run_dns_latency_benchmark, run_timer_resolution_benchmark

logger = logging.getLogger("winforge")


def run_benchmark_suite() -> BenchmarkSuiteResult:
    """Executes full quantitative system performance benchmark suite."""
    logger.info("Executing quantitative benchmark suite...")

    cpu_latency = run_cpu_benchmark()
    mem_throughput = run_memory_benchmark()
    disk_write = run_disk_benchmark()
    timer_res = run_timer_resolution_benchmark()
    dns_lat = run_dns_latency_benchmark()

    res = BenchmarkSuiteResult(
        timestamp=datetime.now().isoformat(),
        cpu_latency_ms=cpu_latency,
        memory_throughput_mbs=mem_throughput,
        disk_io_write_mbs=disk_write,
        timer_resolution_ms=timer_res,
        dns_latency_ms=dns_lat
    )
    logger.info(f"Benchmark Suite complete: CPU {cpu_latency}ms, RAM {mem_throughput}MB/s, Disk {disk_write}MB/s, DNS {dns_lat}ms")
    return res


def compare_benchmarks(before: BenchmarkSuiteResult, after: BenchmarkSuiteResult) -> BenchmarkComparison:
    """Calculates percentage improvements between before and after benchmark runs."""
    def calc_delta(b_val: float, a_val: float, lower_is_better: bool = False) -> float:
        if b_val == 0:
            return 0.0
        if lower_is_better:
            return round(((b_val - a_val) / b_val) * 100.0, 1)
        else:
            return round(((a_val - b_val) / b_val) * 100.0, 1)

    deltas = {
        "cpu_latency": calc_delta(before.cpu_latency_ms, after.cpu_latency_ms, lower_is_better=True),
        "memory_throughput": calc_delta(before.memory_throughput_mbs, after.memory_throughput_mbs, lower_is_better=False),
        "disk_io_write": calc_delta(before.disk_io_write_mbs, after.disk_io_write_mbs, lower_is_better=False),
        "timer_resolution": calc_delta(before.timer_resolution_ms, after.timer_resolution_ms, lower_is_better=True),
        "dns_latency": calc_delta(before.dns_latency_ms, after.dns_latency_ms, lower_is_better=True),
    }

    return BenchmarkComparison(
        before=before,
        after=after,
        improvements_pct=deltas
    )
