# WinForge: Deployment & Portable Execution Architecture

## 1. Executive Summary & Product Vision

**WinForge** is a standalone, portable Windows technician tool designed for commercial PC optimization services. IT technicians deploy WinForge on customer computers via a USB drive or direct download to analyze, optimize, benchmark, and report on system health without requiring Python installation, administrative installer scripts, or internet connectivity.

---

## 2. Deployment Modes Strategy

WinForge supports two distinct distribution models tailored to commercial deployment scenarios:

### Mode A: Technician Edition (Folder-Based Portable Deployment)
- **Target User**: IT Technicians, System Administrators, Field Engineers.
- **Distribution Format**: Portable folder structure carried on technician USB drives or zip packages:
  ```
  ANASOptimizer_Technician/
  ├── ANASOptimizer.exe           # Core Portable Executable
  ├── config/
  │   ├── tweaks.json             # Modifiable external tweak database
  │   └── windows_compatibility.json # Version matrix
  ├── logs/                       # Technician event logs
  ├── reports/                    # Exported PDF/HTML reports
  └── sessions/                   # Unique session records
  ```
- **Key Advantage**: Technicians can update `config/tweaks.json` or `windows_compatibility.json` immediately without needing to recompile the executable binary.

### Mode B: Client Edition (Single Executable Distribution)
- **Target User**: End Customers, Self-Service Client Diagnostics.
- **Distribution Format**: Standalone single executable file: `ANASOptimizer_Client.exe`.
- **Key Advantage**: Zero extra files or folders. Configs and default tweaks are bundled internally (`sys._MEIPASS`). Automatically extracts session reports into a local `reports/` folder upon execution.

---

## 3. Update & Configuration Strategy

1. **Config-Driven Tweak Updates**:
   - `config/tweaks.json` contains versioned tweak definitions (`schema_version: "2.0.0"`).
   - In Technician Edition, updating `tweaks.json` immediately updates detection rules, risk ratings, and recommended apply/rollback methods without rebuilding `ANASOptimizer.exe`.
2. **Compatibility Matrix Updates**:
   - `config/windows_compatibility.json` maps Windows build numbers (e.g. Windows 10 22H2 build 19045, Windows 11 23H2 build 22631, Windows Server 2022 build 20348) to supported tweak categories.

---

## 4. Session Management Architecture

Every scan and optimization run creates a isolated, timestamped Session Directory:

```
sessions/
└── SESSION_20260725_191500_A8F2/
     ├── before.json          # Pre-optimization system scan & baseline state
     ├── findings.json        # Policy engine recommendations & risk classifications
     ├── report.html          # Interactive, printable technician HTML report
     └── rollback.json        # Atomic transaction log for inverse actions
```

### Session Workflow
1. Technician launches `ANASOptimizer.exe`.
2. System generates a unique `Session ID` (e.g. `SESSION_20260725_191500_A8F2`).
3. Diagnostic scan results are serialized into `before.json`.
4. Policy Engine evaluates `before.json` against device context and writes `findings.json`.
5. Dry-Run or Optimization routine records state changes into `rollback.json`.
6. HTML exporter renders `report.html` embedding scan metrics, category health scores, and before/after benchmarks.

---

## 5. Runtime Path Resolution (`winforge/utils/paths.py`)

Dynamic path resolution handles both Technician Edition, Client Edition, development mode, and frozen execution mode:

```python
import sys
import os
from pathlib import Path

def get_app_dir() -> Path:
    """Return the root working directory of the executable or script."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent.parent

def get_bundle_dir() -> Path:
    """Return path to internal bundled resources (sys._MEIPASS when frozen)."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return get_app_dir()
```

---

## 6. Local Privacy & Security Guarantees

1. **Zero External Network Connections**:
   - WinForge does not perform cloud uploads, external telemetry tracking, or background phone-home pings.
2. **Zero Personal File Collection**:
   - Diagnostics inspect system metadata only (hardware specs, OS build, running services, temp file size counters). Customer documents and browser files are never accessed.
3. **Local Storage Only**:
   - All reports, snapshots, logs, sessions, and rollback data remain 100% strictly local inside `logs/`, `reports/`, and `sessions/`.

---

## 7. PyInstaller Packaging Configuration (`build.py`)

- **Technician Edition Command**:
  ```bash
  pyinstaller --noconfirm --onedir --uac-admin --name "ANASOptimizer_Tech" \
    --add-data "config/windows_compatibility.json;config" \
    winforge/main.py
  ```
- **Client Edition Command**:
  ```bash
  pyinstaller --noconfirm --onefile --uac-admin --name "ANASOptimizer_Client" \
    --add-data "config/tweaks.json;config" \
    --add-data "config/windows_compatibility.json;config" \
    winforge/main.py
  ```
