import os
import sys
import shutil
import subprocess
from pathlib import Path


def build_executable():
    """Build standalone portable executable WinForge.exe via PyInstaller."""
    print("==================================================")
    print("  WINFORGE: PyInstaller Portable Build Script")
    print("==================================================")

    project_root = Path(__file__).resolve().parent
    dist_dir = project_root / "dist"
    main_script = project_root / "winforge" / "main.py"

    # Clean existing dist file if unlocked
    target_exe = dist_dir / ("WinForge.exe" if sys.platform == "win32" else "WinForge")
    if target_exe.exists():
        try:
            target_exe.unlink()
        except Exception:
            # If locked by Windows Defender or OS handle, move aside
            try:
                bak = dist_dir / "WinForge.exe.old"
                if bak.exists():
                    bak.unlink(missing_ok=True)
                target_exe.rename(bak)
            except Exception:
                pass

    # PyInstaller command configuration
    sep = ";" if sys.platform == "win32" else ":"

    # Find pyinstaller executable dynamically
    pyinstaller_path = shutil.which("pyinstaller")
    if pyinstaller_path:
        cmd = [pyinstaller_path]
    else:
        cmd = [sys.executable, "-m", "PyInstaller"]

    cmd.extend([
        "--noconfirm",
        "--onefile",
        "--uac-admin",
        "--name", "WinForge",
        "--add-data", f"config{sep}config",
        "--add-data", f"VERSION{sep}.",
        "--add-data", f"CHANGELOG.md{sep}.",
        "--add-data", f"BUILD_INFO{sep}.",
        str(main_script)
    ])

    print(f"\n[BUILD] Running command: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, cwd=str(project_root), check=True)
        if res.returncode == 0:
            exe_path = dist_dir / ("WinForge.exe" if sys.platform == "win32" else "WinForge")
            if exe_path.exists():
                size_mb = round(os.path.getsize(exe_path) / (1024 * 1024), 2)
                print(f"\n[BUILD SUCCESS] Standalone Portable Executable created successfully:")
                print(f" -> Path: {exe_path}")
                print(f" -> Size: {size_mb} MB")
                return True
            else:
                print("\n[BUILD ERROR] Executable file not found in dist directory.")
                return False
    except Exception as e:
        print(f"\n[BUILD ERROR] PyInstaller build failed: {e}")
        return False


if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
