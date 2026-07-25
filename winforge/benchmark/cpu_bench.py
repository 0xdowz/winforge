import time
import math


def run_cpu_benchmark(iterations: int = 500_000) -> float:
    """Measures synthetic CPU iteration latency in milliseconds."""
    start_time = time.perf_counter()
    val = 0.0
    for i in range(1, iterations):
        val += math.sqrt(i) * math.sin(i)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return round(elapsed_ms, 2)
