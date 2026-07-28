# WinForge :: Windows Performance Intelligence & Optimization Platform

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

**WinForge** is a professional Windows performance intelligence, health diagnostic, and system optimization CLI platform created by **@0xdowz**. Built specifically for IT technicians, system administrators, and performance enthusiasts, WinForge provides a safe, transparent, policy-driven, and 100% reversible environment for Windows performance tuning.

Unlike unverified PowerShell scripts or black-box optimizer utilities that corrupt system settings or trigger unrecoverable crashes, WinForge operates as a **transactional, state-machine-driven engine**. Every system modification is evaluated against policy guardrails, backed up prior to execution, and protected by an automated LIFO rollback mechanism.

---

## 1. Key Features

- **Hardware Intelligence Engine v2**: Auto-detects CPU topology, discrete vs. integrated GPU, RAM capacity, storage drive types (SSD/HDD), and power state to calculate tailored Gaming, Workstation, or Battery Efficiency profile recommendations with confidence scoring.
- **4-Phase Safety Architecture**: Guarantees non-privileged analysis and education previews before prompting for explicit user confirmation and Administrator elevation.
- **State-Persistence Elevation Resume (`--resume SESSION_ID`)**: Persists profile selections, candidate tweaks, and risk settings to `%LOCALAPPDATA%\WinForge\sessions\pending_execution.json` prior to elevation, allowing the elevated UAC process to automatically resume execution without losing user state.
- **Disk Space Safety Gate (>= 5.0 GB)**: Enforces a strict 5.0 GB minimum free disk space check on system drive `C:\` to prevent low-disk lockups.
- **Centralized Metadata Validation**: Protects against malformed tweak definitions with safe fallbacks (`"No rationale provided"`).
- **Quantitative Benchmark Suite**: Measures CPU execution latency (ms), memory throughput (MB/s), disk sequential write speed (MB/s), timer resolution (ms), and DNS latency (ms).
- **Security & Hygiene Health Inspector (`winforge security-check`)**: Audits Windows Defender, Firewall, UAC elevation, BitLocker, Windows Update, and Admin rights to calculate a Security Health Score (0–100).
- **Disaster Recovery & Rollback Engine**: One-command session rollback (`winforge rollback SESSION_ID`) parses transaction ledgers to reverse applied registry keys and service state modifications.
- **Standalone Portable Executable**: Zero-installer standalone portable binary (`WinForge.exe`, ~38.8 MB) with embedded multi-resolution icon (`assets/icon.ico`).

---

## 2. Screenshots & Terminal Interface

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

![WinForge CLI Preview](docs/images/winforge-terminal-demo.png)

*WinForge CLI running in interactive Client Mode featuring Rich terminal components, health dashboards, hardware tables, and safety lock cards.*

---

## 3. Architecture & Safety Shield

WinForge enforces a strict 4-layer transactional safety model:

```
┌─────────────────────────────────────────────────────────────┐
│                    WinForge CLI Frontend                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
 ┌─────────────────────────────▼─────────────────────────────┐
 │                Hardware & Policy Engine                   │
 └─────────────────────────────┬─────────────────────────────┘
                               │
 ┌─────────────────────────────▼─────────────────────────────┐
 │               4-Layer Safety Shield Core                  │
 │  ├─ 1. WMI System Restore Point (WINFORGE_SESSION_ID)      │
 │  ├─ 2. Atomic Registry Export (.reg) + Hive Normalization │
 │  ├─ 3. Pre-State System Snapshot (.json)                  │
 │  └─ 4. Atomic Transaction Ledger (rollback.json)          │
 └─────────────────────────────┬─────────────────────────────┘
                               │
 ┌─────────────────────────────▼─────────────────────────────┐
 │                 System Mutation Handlers                  │
 └───────────────────────────────────────────────────────────┘
```

### Safety Guarantees
1. **Single Restore Point**: Exactly **ONE** WMI System Restore Point is created per session.
2. **Registry Hive Normalization**: Shorthand or missing hive prefixes (`SOFTWARE\...`) are normalized to standard formats (`HKLM\SOFTWARE\...`) before `.reg` exports.
3. **Immutable Kernels**: Core Windows services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `WinDefend`, `LsaSrv`) are hard-coded as immutable and will never be modified.
4. **LIFO Rollback Engine**: Reverts applied actions in reverse chronological order if any tweak fails state verification.

---

## 4. Installation & Deployment

### Option A: Portable Standalone Executable (Recommended for IT Technicians)
1. Download the latest `WinForge.exe` from [GitHub Releases](https://github.com/0xdowz/winforge/releases).
2. Run `WinForge.exe` directly from PowerShell, Command Prompt, or Terminal. No installation or Python environment required.

### Option B: Developer Setup from Source Code
```bash
# 1. Clone repository
git clone https://github.com/0xdowz/winforge.git
cd winforge

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install in editable developer mode
pip install -e .

# 4. Run test suite
python -m pytest tests/ -vv

# 5. Build portable binary
python build.py
```

---

## 5. CLI Command Reference

| Command | Description | Privilege Level |
| :--- | :--- | :---: |
| `winforge info` | Displays version, author, loaded tweak counts, and privacy guarantees. | User |
| `winforge analyze` | Runs a non-interactive diagnostic scan and exports `system_report.json`. | User |
| `winforge security-check` | Performs a security health audit (Defender, Firewall, UAC, BitLocker). | User |
| `winforge tweaks list` | Lists all verified optimization recipes with risk ratings and descriptions. | User |
| `winforge doctor` | Checks OS compatibility, Admin status, hardware telemetry, and safety engine readiness. | User |
| `winforge benchmark` | Runs quantitative CPU, Memory, Disk, Timer, and DNS performance benchmarks. | User |
| `winforge dry-run` | Runs optimization simulation without applying system modifications. | User |
| `winforge optimize` | Executes production optimizations (prompts for UAC elevation if needed). | Administrator |
| `winforge --resume SESSION_ID` | Automatically resumes a pending optimization session after UAC elevation. | Administrator |
| `winforge rollback list` | Lists all available session rollback transaction ledgers. | User |
| `winforge rollback SESSION_ID` | Reverts all system modifications recorded in the session transaction ledger. | Administrator |

---

## 6. Storage & Application File Locations

WinForge operates entirely locally and stores logs, session data, and reports under `%LOCALAPPDATA%\WinForge\`:

```text
%LOCALAPPDATA%\WinForge\
 ├─ logs\
 │   └─ runtime.log                 # Continuous application runtime execution logs
 ├─ reports\
 │   └─ system_report.json          # System health diagnostic export
 └─ sessions\
     ├─ pending_execution.json      # Persistent execution state prior to UAC elevation
     └─ <SESSION_ID>\
         ├─ before.json             # Pre-optimization system telemetry snapshot
         ├─ findings.json           # Policy engine evaluation results
         ├─ backup.reg              # Pre-execution registry key export backup
         ├─ rollback.json           # Atomic transaction ledger for session reversion
         └─ report.html             # Human-readable HTML summary report
```

---

## 7. Disaster Recovery & Rollback System

If an optimization degrades performance or causes unexpected behavior, WinForge allows full system state reversion:

```bash
# List available rollback sessions
winforge rollback list

# Revert system state to before the session was applied
winforge rollback SESSION_20260728_193000_A1B2C3
```

The Rollback Engine reads `rollback.json` and performs inverse operations:
- **Registry Changes**: Imports `backup.reg` to restore original registry values.
- **Service Changes**: Restores original startup types (`sc.exe config <service> start= <original_type>`).

---

## 8. Troubleshooting & FAQ

#### Q: WinForge blocks execution with a "Disk Space Safety Gate" error.
**A**: WinForge requires a minimum of **5.0 GB** free space on system drive `C:\` to safely create restore points and backups. Free up disk space on `C:\` and re-run.

#### Q: Windows Defender flags WinForge.exe. Is it safe?
**A**: WinForge is 100% open-source and free. Because WinForge modifies Windows registry keys and service start types, automated heuristic scanners may flag unsigned binaries. You can inspect the source code, verify SHA-256 checksums, or build `WinForge.exe` directly from source using `python build.py`.

#### Q: Does WinForge send telemetry or connect to the cloud?
**A**: **No.** WinForge guarantees 100% offline local execution. There are zero telemetry daemons, tracking scripts, analytics calls, or remote servers.

---

## 9. Security & Privacy Policy

- **100% Offline Execution**: All telemetry, diagnostic reports, and backups remain on your local machine.
- **MIT License**: Free and open source. You should **NEVER** pay for WinForge.
- **Responsible Disclosure**: Please review [SECURITY.md](SECURITY.md) for security reporting guidelines.

---

## 10. Contributing & Community

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on code standards, tweak submission rules, and test suite requirements.

- **Developer**: [@0xdowz](https://github.com/0xdowz)
- **License**: [MIT License](LICENSE)
