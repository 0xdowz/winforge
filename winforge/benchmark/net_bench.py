import socket
import time


def run_dns_latency_benchmark(host: str = "one.one.one.one") -> float:
    """Measures DNS query resolution latency in milliseconds."""
    start_time = time.perf_counter()
    try:
        socket.gethostbyname(host)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return round(elapsed_ms, 2)
    except Exception:
        return 999.0


def run_timer_resolution_benchmark() -> float:
    """Measures system timer resolution precision in milliseconds."""
    samples = []
    for _ in range(10):
        t1 = time.perf_counter()
        time.sleep(0.001)
        t2 = time.perf_counter()
        samples.append((t2 - t1) * 1000.0)
    avg = sum(samples) / len(samples)
    return round(avg, 2)
