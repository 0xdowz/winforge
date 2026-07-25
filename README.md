# WinForge :: Windows System Diagnostic & Optimization CLI Framework

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
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](CHANGELOG.md)

**WinForge** is a policy-driven, non-destructive Windows system diagnostic and optimization toolkit created and maintained by **@0xdowz**. Designed for IT service technicians, system administrators, and performance enthusiasts, WinForge provides a safe, transparent, and fully reversible CLI environment for Windows health inspection and system tuning.

---

## Overview

WinForge provides structured system inspection, quantitative performance benchmarks, and policy-driven Windows optimizations. Unlike scripts that perform destructive, unverified system changes, WinForge evaluates settings against safety thresholds and enforces automated rollback if post-execution state verification fails.

### Target Audience
- **IT Technicians**: Portable USB diagnostic utility (`WinForge.exe`) for auditing client PCs and generating interactive HTML diagnostic reports.
- **System Administrators**: Non-interactive diagnostic scanning (`--scan`) and automated JSON telemetry reporting.
- **Power Users & Gamers**: Reversible latency tuning, power scheme configuration, and startup hygiene management.

---

## Why WinForge?

Traditional Windows debloat scripts and optimization packs often rely on opaque PowerShell execution, blind registry key deletion, or disabling core Windows security components. When settings degrade performance or break system features, reversing those scripts is often impossible without reinstalling the operating system.

WinForge addresses this by treating system optimization as a **transactional, state-machine-driven engineering process**:

- **Non-Destructive Defaults**: All operations run in simulation mode (`--dry-run`) by default.
- **4-Layer Safety Lock**: Creates Windows System Restore Points, targeted `.reg` backups, pre-state JSON snapshots, and atomic transaction ledgers before applying system mutations.
- **Automated LIFO Rollback Engine**: Reverts modifications in reverse chronological order if post-apply verification checks fail.
- **Protected Immutable Boundaries**: Critical Windows kernel and security services (`RpcSs`, `EventLog`, `WinDefend`, `CryptSvc`, `Dhcp`) can never be disabled by WinForge policies.

---

## Is WinForge Free?

**Yes.** WinForge is 100% free and open-source software released under the [MIT License](LICENSE).

- You should **never** pay someone to download, activate, or use WinForge.
- Official release binaries are published exclusively on the official GitHub repository: [https://github.com/0xdowz/winforge](https://github.com/0xdowz/winforge).

---

## Core Features

- **System Diagnostic Inspector**: Collects detailed hardware and OS telemetry using Windows native WMI and Win32 interfaces to generate an internal **WinForge System Health Score (0–100)**.
- **Quantitative Performance Benchmarks**: Measures CPU execution latency (ms), memory throughput (MB/s), disk sequential write speed (MB/s), timer resolution (ms), and DNS latency (ms).
- **Policy-Driven Optimizations**: 6 category modules targeting Gaming latency, Power scheme policies, Startup hygiene, Service optimization, Disk cleanup, and Network stack settings.
- **Risk Score Intelligence**: Categorizes tweaks (`SAFE`, `MODERATE`, `ADVANCED`, `TECHNICIAN ONLY`) with risk weighting (0–100) ensuring high-risk tweaks require explicit technician approval.
- **Technician Inspection Mode (`--tech`)**: Displays granular Tweak Inspection Cards in terminal for manual Y/N approval.
- **Configuration Integrity Engine**: Validates SHA-256 integrity hashes for configuration files (`config/checksums.json`) prior to execution.
- **Rich Terminal User Experience**: Terminal dashboards, spec overview tables, degradation alerts, and health progress bars powered by Rich.
- **Portable Binary Execution**: Available as a standalone portable executable (`WinForge.exe`, ~38.8 MB) with embedded UAC elevation manifest.

---

## Terminal Dashboard Preview

![WinForge Dashboard](docs/images/dashboard.png)

```
┌──────────────────── WINFORGE :: SYSTEM HEALTH DASHBOARD ────────────────────┐
│   WINFORGE HEALTH SCORE: 80.8/100 [NEEDS TUNING]                            │
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

## Quick Start Guide

### Option 1: Standalone Binary (Recommended for Technicians)
Download `WinForge.exe` from the official [GitHub Releases](https://github.com/0xdowz/winforge/releases) page. Zero Python installation required.

### Option 2: Build from Source
```cmd
git clone https://github.com/0xdowz/winforge.git
cd winforge
pip install -r requirements.txt
python build.py
```
*The output binary will be created at `dist/WinForge.exe`.*

---

## CLI Usage Reference

### Non-Interactive Diagnostic Scan
```cmd
WinForge.exe --scan
```
- **Permission**: Standard User (No Admin required).
- **Mutations**: None (Read-only).
- **Output**: Diagnostic telemetry table, WinForge Health Score, and `reports/system_report.json`.

### Optimization Simulation (Dry-Run)
```cmd
WinForge.exe --dry-run
```
- **Permission**: Standard User (No Admin required).
- **Mutations**: None (Simulated).
- **Output**: Calculated score gain log and interactive session HTML report (`sessions/<ID>/report.html`).

### Production Execution (Elevated Terminal)
```cmd
WinForge.exe --execute
```
- **Permission**: **Administrator Privileges Required** (`uac_admin`).
- **Mutations**: Applies safe registry & service policies.
- **Output**: Creates Restore Point, exports `.reg` backups, applies safe tweaks, verifies state, and logs transaction ledgers.

### Technician Inspection Mode
```cmd
WinForge.exe --tech
```
- **Permission**: Standard User or Admin.
- **Mutations**: User-approved per tweak.
- **Output**: Displays individual Tweak Inspection Cards with risk score badges and Y/N prompts.

### Environment Information
```cmd
WinForge.exe --license-info
```
- **Permission**: Standard User.
- **Mutations**: None.
- **Output**: Open Source Environment details, status message, and capability profile.

---

## CLI Command Matrix

| Flag / Subcommand | Alias | Admin Required? | Modifies System? | Primary Output |
| :--- | :--- | :---: | :---: | :--- |
| `--scan` | `scan` | No | No | Diagnostic spec summary & JSON telemetry |
| `--dry-run` | `dry-run` | No | No | Calculated score delta & session HTML report |
| `--execute` | `optimize` | **Yes** | **Yes** | Restore point creation & verified tweaks |
| `--tech` | `tech` | Conditional | Prompted | Granular Tweak Inspection Cards (Y/N) |
| `--license-info` | `license` | No | No | Open Source Environment status table |
| `benchmark` | - | No | No | CPU, RAM, Disk, DNS benchmark scores |

---

## Safety Architecture & Boundary Security

```
[ Pre-Flight Safety Approval Check ] ──► (Verify Admin, Disk Space >= 2GB, Battery >= 20%)
                 │
                 ▼
[ 4-Layer Safety Subsystem Lock ] ──► (1. System Restore Point  2. .reg Registry Backup)
                 │                   (3. State Snapshot JSON    4. Transaction Ledger)
                 ▼
[ Optimization Execution Engine ] ──► (Apply Safe Registry & Service Mutations)
                 │
                 ▼
[ Post-Apply State Verification ] ──► [PASS] Commit HTML Session Report
                 │
                 └──────────────────► [FAIL] Execute Automated LIFO Rollback
```

1. **Non-Destructive Defaults**: Handlers operate with `mock_execution=True` by default.
2. **Immutable Boundary Protection**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `Dhcp`, `Dnscache`, `LsaSrv`, `WinDefend`, `wuauserv`) and core directories (`C:\Windows\System32`, `SysWOW64`, `Drivers`) cannot be modified or disabled.
3. **Automated Pre-Flight Gate**: Execution halts if free disk space is $< 2.0\text{ GB}$, laptop battery is $< 20\%$, or Administrator privileges are missing.
4. **Transactional Rollback Engine**: Reverts modifications in reverse chronological order if post-apply verification checks fail.

---

## Supported Platforms

- **Windows 11** (64-bit) — All builds supported.
- **Windows 10** (64-bit) — Version 2004 or newer supported.

---

## Frequently Asked Questions (FAQ)

#### Q: Will WinForge disable Windows Defender or Windows Update?
**No.** WinForge hard-gates core security services (`WinDefend`, `wuauserv`, `CryptSvc`) as strictly immutable. They cannot be modified or disabled.

#### Q: How do I undo changes made by WinForge?
WinForge creates a System Restore Point (`WINFORGE_OPT_`), exports a targeted `.reg` file backup, and logs an atomic transaction ledger before applying changes. You can revert changes automatically via the LIFO rollback engine or manually import the exported `.reg` backup file.

#### Q: Does WinForge require internet access?
**No.** WinForge operates 100% offline. It contains no telemetry daemons, tracking scripts, or cloud dependencies.

---

## Development & Automated Testing

### Running Unit Tests
WinForge includes a PyTest test suite (43 automated tests):
```cmd
python -m pytest tests/
```

### Verification Pipeline
Before submitting pull requests, ensure:
1. All 43 unit tests pass cleanly.
2. Non-destructive dry-run execution completes without errors (`python -m winforge.main --dry-run`).
3. Binary compilation builds cleanly (`python build.py`).

---

## Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines on submitting pull requests, bug reports, and tweak suggestions.

---

## Security Policy

For security disclosures or vulnerability reporting, please review our [SECURITY.md](SECURITY.md) guidelines. Please do not open public issues for zero-day vulnerability reports.

---

## Support Development

WinForge is 100% free software. If you find WinForge useful and wish to support future development, you can optionally support the maintainer:

- [Sponsor @0xdowz on GitHub](https://github.com/sponsors/0xdowz)
- [Follow @0xdowz on GitHub](https://github.com/0xdowz)

---

## Authors & Maintainers

Created and maintained by **@0xdowz**. See [AUTHORS.md](AUTHORS.md) for details.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
