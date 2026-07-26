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
[![Version](https://img.shields.io/badge/version-1.0.2-orange.svg)](CHANGELOG.md)

---

Professional Windows system diagnostic and optimization CLI framework built with safety-first architecture, policy engine guardrails, and automated rollback capabilities.

---

## 1. Overview

**WinForge** is a policy-driven, non-destructive Windows system diagnostic and optimization CLI framework created and maintained by **@0xdowz**. Designed for IT technicians, system administrators, and performance enthusiasts, WinForge provides a safe, transparent, and fully reversible environment for Windows health inspection and performance tuning.

Unlike scripts that execute unverified system modifications, WinForge evaluates settings against policy matrix guardrails, creates pre-mutation safety backups, and enforces automated LIFO rollback if post-execution state verification fails.

---

## 2. Features

- **System Diagnostic Inspector**: Collects detailed hardware and OS telemetry to compute an internal **WinForge System Health Score (0–100)**.
- **Quantitative Performance Benchmarks**: Measures CPU latency (ms), memory throughput (MB/s), disk sequential write speed (MB/s), timer resolution (ms), and DNS latency (ms).
- **Environment Doctor (`winforge doctor`)**: Verifies Administrator elevation, OS compatibility, hardware status, and 4-Layer Safety Engine readiness.
- **Policy-Driven Optimizations**: 6 category modules targeting Gaming latency, Power scheme policies, Startup hygiene, Service optimization, Disk cleanup, and Network settings.
- **Risk Score Intelligence**: Categorizes tweaks (`SAFE`, `MODERATE`, `ADVANCED`, `TECHNICIAN ONLY`) with risk weighting (0–100) ensuring high-risk tweaks require technician confirmation.
- **Technician Inspection Mode (`--tech`)**: Displays granular Tweak Inspection Cards in terminal for manual approval.
- **`--demo` Mode**: Non-interactive read-only preview mode that runs a full system scan and benchmark suite for screenshot generation.
- **Rich Terminal User Experience**: Responsive terminal dashboards, tables, step trackers, and actionable error panels powered by Rich.
- **Portable Binary Execution**: Available as a standalone portable executable (`WinForge.exe`, ~38.8 MB) with embedded UAC elevation manifest.

---

## 3. Screenshots

![WinForge CLI Terminal Preview](docs/images/winforge-terminal-demo.png)

*WinForge CLI running in Simulation / Dry-Run Client Mode. The terminal interface provides access to diagnostics, benchmarks, optimization workflows, reports, rollback tools, and technician controls.*

---

## 4. Why WinForge?

Traditional Windows debloat scripts and optimization tweaks rely on unverified registry key deletions or disabling core security components. When settings degrade performance or break features, reversing those changes is often impossible without reinstalling Windows.

WinForge addresses this by treating system optimization as a **transactional, state-machine-driven engineering process**:

- **Safety-First Non-Destructive Defaults**: All operations run in simulation mode (`--dry-run`) by default.
- **4-Layer Safety Lock**: Creates Windows System Restore Points, targeted `.reg` backups, pre-state JSON snapshots, and atomic transaction ledgers before applying system mutations.
- **Automated LIFO Rollback Engine**: Reverts modifications in reverse chronological order if post-apply verification checks fail.
- **Protected Immutable Boundaries**: Core Windows kernel and security services (`RpcSs`, `EventLog`, `WinDefend`, `CryptSvc`, `Dhcp`) can never be disabled by WinForge policies.

---

## 5. Installation

### Option 1: Standalone Binary (Recommended for Technicians)
Download `WinForge.exe` from the official [GitHub Releases](https://github.com/0xdowz/winforge/releases) page. No Python installation required.

### Option 2: Python Installation
```cmd
pip install git+https://github.com/0xdowz/winforge.git
```

### Option 3: Build from Source
```cmd
git clone https://github.com/0xdowz/winforge.git
cd winforge
pip install -r requirements.txt
python build.py
```
*The compiled binary will be placed at `dist/WinForge.exe`.*

---

## 6. Usage

WinForge provides a predictable CLI command interface:

```cmd
# Run non-interactive diagnostic scan
WinForge.exe scan

# Run environment & safety doctor checks
WinForge.exe doctor

# Run dry-run optimization simulation (read-only)
WinForge.exe dry-run

# Run quantitative benchmark suite
WinForge.exe benchmark

# Run non-interactive read-only demo mode
WinForge.exe --demo

# Run production optimization pipeline (Requires Admin)
WinForge.exe optimize

# Launch Technician Mode with granular inspection cards
WinForge.exe tech
```

### CLI Command Matrix

| Command / Flag | Alias | Admin Required? | Modifies System? | Primary Output |
| :--- | :--- | :---: | :---: | :--- |
| `scan` | `--scan` | No | No | Diagnostic spec summary & JSON telemetry |
| `doctor` | - | No | No | System health & safety engine status table |
| `dry-run` | `--dry-run` | No | No | Score projection delta & HTML session report |
| `benchmark` | - | No | No | CPU, RAM, Disk, Timer, DNS benchmark scores |
| `--demo` | - | No | No | Non-interactive full scan & benchmark preview |
| `optimize` | `--execute` | **Yes** | **Yes** | 4-Layer Safety Lock & verified tweaks |
| `tech` | `--tech` | Conditional | Prompted | Granular Tweak Inspection Cards (Y/N) |

---

## 7. Architecture

WinForge follows a decoupled 7-layer architecture:

```
┌─────────────────────────────────────────────────────────┐
│                      CLI Layer                          │
│   (interface.py, renderer.py, themes.py, progress.py)   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    Policy Engine                        │
│   (Evaluates Windows OS version & Server guardrails)   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               4-Layer Safety Lock Subsystem             │
│   (Restore Point + .reg Backup + Snapshot + Ledger)     │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               Category Dispatcher & Handlers            │
│   (Gaming, Power, Services, Startup, Cleanup, Network)  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            State Machine & Verification Engine          │
│       (Verifies post-apply state / Triggers Rollback)   │
└─────────────────────────────────────────────────────────┘
```

1. **CLI Layer (`winforge.cli`)**: Terminal presentation layer handling dashboards, tables, step progress tracking, and theme tokens.
2. **Policy Engine (`winforge.core.policy`)**: Enforces compatibility rules and blocks unsafe tweaks on Windows Server OS.
3. **Safety Layer (`winforge.safety`)**: Manages WMI System Restore Points, atomic `.reg` exports, pre-state JSON snapshots, and transaction ledgers.
4. **Optimization Engine (`winforge.optimizations`)**: Category handlers executing atomic Windows modifications.
5. **Benchmark Subsystem (`winforge.benchmark`)**: Quantitative performance profiling suite.

---

## 8. Development & Automated Testing

### Installing Dependencies
```cmd
pip install -e .
```

### Running Unit Tests
WinForge includes a comprehensive PyTest test suite (46 automated tests):
```cmd
python -m pytest tests/ -vv
```

### Building Portable Binary
```cmd
python build.py
```

---

## 9. Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines on submitting pull requests, bug reports, and tweak suggestions.

---

## 10. Security

WinForge takes Windows safety seriously. For security disclosures or vulnerability reports, please review our [SECURITY.md](SECURITY.md) guidelines.

---

## 11. License

This project is released under the **MIT License** — see the [LICENSE](LICENSE) file for details.
