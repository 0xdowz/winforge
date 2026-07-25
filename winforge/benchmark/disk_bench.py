import os
import time
import tempfile
from pathlib import Path


def run_disk_benchmark(file_size_mb: int = 32) -> float:
    """Measures disk write speed in MB/s on temporary directory."""
    temp_dir = Path(tempfile.gettempdir())
    test_file = temp_dir / "winforge_bench_test.tmp"
    chunk = b"X" * (1024 * 1024)
    
    try:
        start_time = time.perf_counter()
        with open(test_file, "wb") as f:
            for _ in range(file_size_mb):
                f.write(chunk)
            f.flush()
            os.fsync(f.fileno())
        elapsed = time.perf_counter() - start_time
    finally:
        if test_file.exists():
            try:
                os.remove(test_file)
            except Exception:
                pass
                
    if elapsed == 0:
        elapsed = 0.0001
        
    write_speed_mbs = (file_size_mb / elapsed)
    return round(write_speed_mbs, 1)
