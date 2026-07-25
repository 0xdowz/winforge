from winforge.benchmark.runner import run_benchmark_suite


def test_benchmark_suite():
    result = run_benchmark_suite()
    assert result.cpu_latency_ms >= 0.0
    assert result.memory_throughput_mbs >= 0.0
    assert result.disk_io_write_mbs >= 0.0


def test_benchmark_json_export():
    result = run_benchmark_suite()
    d = result.model_dump()
    assert "cpu_latency_ms" in d
    assert "memory_throughput_mbs" in d
