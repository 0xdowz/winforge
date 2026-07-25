# WinForge :: Windows System Diagnostic & Optimization CLI Framework

```
██╗  ██╗██╗███╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗
██║  ██║██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝
███████║██║██╔██╗ ██║█████╗  ██║  ██║██████╔╝██║  ███╗█████╗  
██╔══██║██║██║╚██╗██║██╔══╝  ██║  ██║██╔══██╗██║   ██║██╔══╝  
██║  ██║██║██║ ╚████║██║     ██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

[![CI](https://github.com/0xdowz/winforge/actions/workflows/ci.yml/badge.svg)](https://github.com/0xdowz/winforge/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6.svg)](https://microsoft.com/windows)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](CHANGELOG.md)

**WinForge** is a free, open-source, policy-driven Windows diagnostic and optimization toolkit created and maintained by **@0xdowz**. Designed for IT service technicians, system administrators, and performance enthusiasts, WinForge provides a safe, transparent, and fully reversible CLI environment for Windows health analysis and system tuning.

---

## Is WinForge Free?

**Yes.**

WinForge is a 100% free and open-source project released under the MIT License.

You should **NEVER** pay someone to download, activate, unlock, or use WinForge.

If someone sells you WinForge or claims they have a paid/premium version, you are likely being scammed.

The official releases are published exclusively through the official project GitHub repository: [https://github.com/0xdowz/winforge](https://github.com/0xdowz/winforge).

---

## Key Features

- **Diagnostic System Health Collector**: WMI and Win32 hardware inspection across CPU, GPU, RAM, Storage, OS Build, and Active Power Plans to generate a 0–100 System Health Score.
- **Quantitative Performance Benchmark Suite**: Measures CPU execution latency (ms), memory throughput (MB/s), disk write speeds (MB/s), timer resolution (ms), and DNS latency (ms).
- **4-Layer Safety Subsystem Lock**: Automatically creates Windows System Restore Points, targeted `.reg` registry backups, pre-state JSON snapshots, and atomic transaction ledgers before applying any modifications.
- **Automated LIFO Rollback Engine**: One-click restoration of system modifications if post-execution state verification fails.
- **11-State Execution Lifecycle Machine**: Driven by an orchestration state machine with Dry-Run simulation (`--dry-run`), Client Mode batch execution, and Technician Inspection Mode (`--tech`).
- **Risk Score Intelligence (0–100)**: Tweak risk categorization (`SAFE`, `MODERATE`, `ADVANCED`, `TECHNICIAN ONLY`) ensuring high-risk tweaks require explicit technician confirmation.
- **Rich Terminal User Experience**: Terminal dashboards, health progress bars, warning alerts, and Technician Tweak Inspection Cards powered by Rich.
- **Standalone Portable Binary (`WinForge.exe`)**: Self-contained executable with embedded UAC elevation manifest. Zero installation or Python dependencies required.

---

## Interface Screenshot

![WinForge Dashboard](docs/images/dashboard.png)

```
┌──────────────────── WINFORGE :: SYSTEM HEALTH DASHBOARD ────────────────────┐
│   SYSTEM HEALTH SCORE: 80.8/100 [NEEDS TUNING]                              │
│   HEALTH INDEX: [================....] 80.8%                                │
│                                                                             │
│   CATEGORY BREAKDOWN:                                                       │
│   * Performance Score:           100.0/100                                  │
│   * Security & Privacy Score:    100.0/100                                  │
│   * Maintenance & Cleanliness:  65.0/100                                    │
│   * Startup & Service Hygiene:   58.0/100                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Fast Start User Guide

### 1. Download Standalone Executable
Download `WinForge.exe` from the official [GitHub Releases](https://github.com/0xdowz/winforge/releases) page.

### 2. Run Non-Destructive Scan
```cmd
WinForge.exe --scan
```
*Evaluates system health, calculates health scores, and outputs diagnostic reports without modifying system state.*

### 3. Run Optimization Simulation
```cmd
WinForge.exe --dry-run
```
*Simulates optimization execution and calculates simulated health score gains.*

### 4. Execute Recommended Optimizations (Elevated Terminal)
```cmd
WinForge.exe --execute
```
*Creates System Restore Points, exports registry backups, applies safe tweaks, verifies changes, and generates an HTML report.*

### 5. Launch Technician Mode
```cmd
WinForge.exe --tech
```
*Enables individual Tweak Inspection Cards for granular manual approval.*

---

## CLI Command Reference

| Flag / Subcommand | Alias | Purpose | Risk Level | Expected Output |
| :--- | :--- | :--- | :---: | :--- |
| `--scan` | `scan` | Run diagnostic health scan | **LOW (0)** | Health dashboard, spec table, warnings |
| `--dry-run` | `dry-run` | Run optimization simulation | **LOW (0)** | Simulated score delta, findings log |
| `--execute` | `optimize` | Execute production optimizations | **MEDIUM** | Restore point creation, apply logs |
| `--tech` | `tech` | Launch Technician Inspection mode | **MEDIUM-HIGH** | Tweak Inspection Cards, Y/N prompts |
| `--license-info` | `license` | View Open Source Environment info | **LOW (0)** | Environment summary table |
| `benchmark` | - | Run quantitative micro-benchmarks | **LOW (0)** | CPU, RAM, Disk, DNS benchmark scores |

---

## Safety & Security Philosophy

1. **Non-Destructive Defaults**: `mock_execution=True` is enforced across all internal handlers by default.
2. **Immutable Protected Boundaries**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `Dhcp`, `Dnscache`, `LsaSrv`, `WinDefend`, `wuauserv`) and system directories (`C:\Windows\System32`, `SysWOW64`, `Drivers`) are strictly immutable.
3. **Automatic Pre-Flight Check**: Halts execution if disk space is $< 2.0\text{ GB}$, battery level $< 20\%$, or elevation is missing.
4. **Automated LIFO Rollback**: Restores original system state in reverse chronological order if post-apply verification fails.

---

## Supported Windows Versions

- Windows 11 (64-bit) — All builds supported.
- Windows 10 (64-bit) — Version 2004 or newer supported.

---

## Development & Building from Source

### Requirements
- Windows 10 / 11 (64-bit)
- Python 3.12 or newer

```cmd
git clone https://github.com/0xdowz/winforge.git
cd winforge
pip install -r requirements.txt
python build.py
```
*The output binary will be created at `dist/WinForge.exe` (~38.8 MB).*

### Running Tests
```cmd
python -m pytest tests/
```

---

## Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines on submitting pull requests, bug reports, and tweak suggestions.

---

## Support Development

If you find WinForge useful and want to support future development, you can optionally support the project through voluntary donations:

- [Sponsor on GitHub](https://github.com/sponsors/0xdowz)
- [Follow @0xdowz on GitHub](https://github.com/0xdowz)

*Donations are voluntary and never required.*

---

## Authors & Maintainers

Created and maintained by **@0xdowz**. See [AUTHORS.md](AUTHORS.md) for details.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
