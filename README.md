# WinForge :: Windows Performance Intelligence Platform

```
██╗  ██╗  ██╗██╗███╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗
██║  ██║  ██║██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝
██║  ██║  ██║██║██╔██╗ ██║█████╗  ██║  ██║██████╔╝██║  ███╗█████╗  
██║  ███╗ ██║██║██║╚██╗██║██╔══╝  ██║  ██║██╔══██╗██║   ██║██╔══╝  
╚████╔████╔╝ ██║██║ ╚████║██║     ██████╔╝██║  ██║╚██████╔╝███████╗
 ╚═══╝╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══════╝
```

[![CI](https://github.com/0xdowz/winforge/actions/workflows/ci.yml/badge.svg)](https://github.com/0xdowz/winforge/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6.svg)](https://microsoft.com/windows)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-1.0.8-orange.svg)](CHANGELOG.md)

---

## Overview

**WinForge** is an open-source Windows performance intelligence, diagnostic, and optimization CLI platform developed by **@0xdowz**. Designed for system administrators, IT technicians, and power users, WinForge provides a transparent, policy-driven, and fully reversible framework for inspecting system health and tuning performance parameters.

WinForge is built on a **transactional state-machine architecture**. System modifications are evaluated against policy rules, backed up prior to execution, and protected by an automated LIFO rollback engine.

---

## Features

- **Hardware Intelligence Engine v2**: Auto-detects CPU topology, discrete vs. integrated GPU, installed RAM, storage drive configurations, and AC vs. battery power state to generate profile recommendations (`Gaming Performance Profile`, `Workstation Profile`, `Battery Efficiency Profile`).
- **4-Phase Transactional Safety Shield**:
  - Phase 1: Non-privileged diagnostic analysis & recommendation preview.
  - Phase 2: Explicit user approval (`Execute N optimizations now? [Y/n]`).
  - Phase 3: Administrator privilege check & state-persistence setup.
  - Phase 4: Elevated pre-flight safety locks (Restore Point, Registry Backup, Snapshot) & execution.
- **State-Persistence Elevation Resume (`--resume SESSION_ID`)**: Persists session parameters to `%LOCALAPPDATA%\WinForge\sessions\pending_execution.json` prior to elevation, enabling the elevated process to automatically resume execution without user state loss.
- **Disk Space Safety Gate (>= 5.0 GB)**: Halts pre-flight execution if free space on system drive `C:\` is under 5.0 GB.
- **Centralized Schema Validation**: Validates tweak metadata and injects safe fallbacks (`"No rationale provided"`).
- **Quantitative Benchmark Suite**: Measures CPU execution latency (ms), memory throughput (MB/s), disk sequential write speed (MB/s), timer resolution (ms), and DNS latency (ms).
- **Security Health Inspector (`winforge security-check`)**: Audits Windows Defender, Firewall, UAC, BitLocker, Windows Update, and Admin status to calculate a Security Health Score (0–100).
- **Disaster Recovery Rollback Engine**: One-command session reversion (`winforge rollback SESSION_ID`) using `rollback.json` transaction ledgers.
- **Standalone Portable Binary**: Built with embedded UAC administrator manifest (`requestedExecutionLevel="requireAdministrator"`) and custom multi-resolution icon (`assets/icon.ico`).

---

## Screenshots

```
─── System Health Overview ───

  Health Score:
  80.8 / 100  NEEDS ATTENTION

  Category Breakdown:
   ✓ Performance Score:          100.0 / 100
   ✓ Security & Privacy:         100.0 / 100
   ⚠ Maintenance & Cleanliness: 65.0 / 100
   ⚠ Startup & Service Hygiene:  58.0 / 100

─── Hardware Specification ───

 Component               Specification Details                                 
 Operating System        Windows 10 Pro (64bit) [Build 26200]                  
 Processor (CPU)         12th Gen Intel(R) Core(TM) i3-12100 (8 Cores)         
 Graphics (GPU)          Intel(R) UHD Graphics 730 (Driver: 32.0.101.6129)     
 System Memory (RAM)     15.77 GB Installed                                    
 Storage Drives          C:\ (2.13/231.9 GB Free)  D:\ (295.13/465.76 GB Free) 
 Active Power Plan       High Performance (AC Power)                           
```

![WinForge CLI Interface](docs/images/winforge-terminal-demo.png)

*WinForge CLI running in interactive Client Mode featuring Rich terminal dashboards, health scores, hardware tables, and safety status indicators.*

---

## Installation & Deployment

### Portable Standalone Executable (Recommended)
1. Download `WinForge.exe` from [GitHub Releases](https://github.com/0xdowz/winforge/releases).
2. Right-click and **Run as Administrator** (or execute directly from an elevated terminal).

### Developer Installation from Source
```cmd
:: 1. Clone repository
git clone https://github.com/0xdowz/winforge.git
cd winforge

:: 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

:: 3. Install in editable mode
pip install -e .

:: 4. Run test suite
python -m pytest tests/ -vv

:: 5. Build portable binary
python build.py
```

---

## CLI Command Reference

| Command | Description | Privilege Level |
| :--- | :--- | :---: |
| `winforge info` | Displays version, developer attribution, loaded recipe count, and privacy guarantee. | User / Admin |
| `winforge analyze` | Runs a non-interactive diagnostic scan and exports `system_report.json`. | User / Admin |
| `winforge security-check` | Performs a security health audit (Defender, Firewall, UAC, BitLocker). | User / Admin |
| `winforge tweaks list` | Lists all verified optimization recipes with risk ratings and descriptions. | User / Admin |
| `winforge doctor` | Checks OS compatibility, Admin status, hardware telemetry, and safety readiness. | User / Admin |
| `winforge benchmark` | Runs quantitative CPU, Memory, Disk, Timer, and DNS performance benchmarks. | User / Admin |
| `winforge dry-run` | Runs optimization simulation without applying system modifications. | User / Admin |
| `winforge optimize` | Executes production optimizations. | Administrator |
| `winforge --resume SESSION_ID` | Automatically resumes a pending optimization session after elevation. | Administrator |
| `winforge rollback list` | Lists all available session rollback transaction ledgers. | User / Admin |
| `winforge rollback SESSION_ID` | Reverts all system modifications recorded in the session transaction ledger. | Administrator |

---

## Safety Architecture & Rollback System

WinForge enforces a 4-layer pre-flight safety shield prior to executing any system modification:

1. **WMI System Restore Point**: Creates `WinForge_SESSION_TIMESTAMP` checkpoint.
2. **Atomic Registry Backup**: Exports targeted `.reg` backups with automatic hive normalization (`SOFTWARE\...` -> `HKLM\SOFTWARE\...`).
3. **Pre-State System Snapshot**: Captures telemetry into `before.json`.
4. **Atomic Transaction Ledger**: Logs exact previous and new values into `rollback.json`.

### Reverting Changes
To reverse optimizations applied in a previous session:
```cmd
winforge rollback list
winforge rollback SESSION_20260728_193000_A1B2C3
```

---

## Privacy & Security Statement

- **100% Offline Local Execution**: All telemetry, reports, and backups are stored locally under `%LOCALAPPDATA%\WinForge\`.
- **Zero Telemetry**: WinForge contains no analytics daemons, tracking scripts, or external network connections.
- **Immutable Boundaries**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `WinDefend`, `LsaSrv`) are strictly immutable.

---

## Release Information — v1.0.8

- **Elevated Startup Manifest**: Built with PyInstaller `--uac-admin` (`requestedExecutionLevel="requireAdministrator"`).
- **Embedded Multi-Resolution Icon**: `assets/icon.ico` supporting 16x16 through 256x256 resolutions.
- **State-Persistence Resume**: Persistent pending state file handling via `%LOCALAPPDATA%\WinForge\sessions\pending_execution.json`.
- **Disk Space Safety Gate**: 5.0 GB minimum free disk space check on drive `C:\`.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code guidelines, tweak submission requirements, and testing policies.

- **Developer**: [@0xdowz](https://github.com/0xdowz)
- **License**: [MIT License](LICENSE)
