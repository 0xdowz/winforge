# WinForge v1.0.8 — Production Release Notes

**Release Version**: `v1.0.8`  
**Release Date**: July 28, 2026  
**Developer & Maintainer**: `@0xdowz` (Anas Al-Jabour)  
**Target Platform**: Windows 10 / Windows 11 (x64)  
**License**: MIT Open Source  

---

## Highlights & Major Improvements

### 1. Elevation & Session Resume Lifecycle Fix
- **State-Persistence Resume Architecture (`--resume SESSION_ID`)**: Non-elevated execution serializes candidate tweaks, mode, and max risk parameters to `%LOCALAPPDATA%\WinForge\sessions\pending_execution.json` prior to requesting UAC elevation. The elevated instance automatically loads pending state and resumes execution seamlessly without state loss.
- **Absolute Path Resolution**: `relaunch_as_admin()` resolves absolute executable paths, script paths, and passes `get_executable_dir()` as the explicit working directory (`lpDirectory`) in `ShellExecuteW`, eliminating console closure crashes caused by default working directory shifts.

### 2. Robust Safety & Pre-Flight Verification
- **Disk Space Pre-Flight Safety Gate (>= 5.0 GB)**: Enforces a strict 5.0 GB free disk space requirement on system drive `C:\` before creating Volume Shadow Copy (VSS) System Restore Points or Registry exports. Low storage conditions trigger a formatted `[SAFETY GATE BLOCKED]` banner and halt execution safely.
- **Centralized Tweak Metadata Validation**: Schema validator automatically injects safe fallbacks (`"No rationale provided"`), eliminating `KeyError` crashes on incomplete recipe definitions.

### 3. Interactive Terminal Lifecycle Management
- **Interactive-Only Console Pauses**: `prompt_pause_if_interactive()` detects whether execution is running in an interactive terminal or frozen PE while automatically bypassing pauses in automated test environments (`PYTEST_CURRENT_TEST` or `WINFORGE_NON_INTERACTIVE`).

---

## Release Artifacts

| Artifact | File Path | Description |
| :--- | :--- | :--- |
| **Standalone Portable Binary** | `dist/WinForge.exe` | Zero-dependency standalone Windows executable (~38.77 MB) embedded with multi-resolution icon (`assets/icon.ico`) and configuration data bundles. |
| **Source Archive** | `winforge-1.0.8.tar.gz` | Source codebase and configuration database. |

---

## Verification & Test Results

- **PyTest Unit & Integration Suite**: **61 / 61 PASSED** (100% pass rate in 17.24s)
- **Standalone PE Executable Build**: **BUILD SUCCESS** (`python build.py`)
- **Runtime Log Audit**: `%LOCALAPPDATA%\WinForge\logs\startup.log` and `winforge.log` verified clean with zero unhandled exceptions.

---

## Known Limitations

- **Administrator Privileges**: Applying registry modifications under `HKLM` and Windows Service start-type changes requires Administrator privileges (UAC prompt).
- **Disk Space Requirement**: Creating System Restore Points requires at least 5.0 GB free disk space on system drive `C:\`.
