import time


def run_memory_benchmark(block_size_mb: int = 64) -> float:
    """Measures memory throughput in MB/s."""
    data_size = block_size_mb * 1024 * 1024
    dummy_data = bytearray(data_size)
    
    start_time = time.perf_counter()
    # Memory copy benchmark
    copy_buf = bytearray(dummy_data)
    elapsed = time.perf_counter() - start_time
    
    if elapsed == 0:
        elapsed = 0.0001
        
    throughput_mbs = (block_size_mb / elapsed)
    return round(throughput_mbs, 1)
