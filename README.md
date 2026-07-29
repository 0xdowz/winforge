# WinForge v1.0.8 — Autonomous Windows Optimization Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(x64)-0078D6.svg?logo=windows)](https://microsoft.com)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python)](https://python.org)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-61%2F61%20Passed-success.svg)]()

**WinForge** is an open-source, non-destructive command-line optimization framework for Windows 10 and Windows 11. Designed for system administrators, IT technicians, gamers, and privacy-conscious users, WinForge automates performance tuning, background telemetry mitigation, and system diagnostics while enforcing a strict 7-Step Safety Transaction Lifecycle.

---

## Why WinForge?

Unlike legacy batch scripts, PowerShell tweak gists, or opaque closed-source cleaning utilities, WinForge is built on transparency, safety, and atomicity.

| Feature / Capability | Typical Tweak Scripts / GUI Tools | WinForge Framework |
| :--- | :--- | :--- |
| **Code Transparency** | Hardcoded scripts or undocumented binaries | 100% Open Source declarative JSON recipes ([docs/tweak-system.md](docs/tweak-system.md)) |
| **Plain-English Explanations** | Unclear names ("Disable DiagTrack") | Multi-layer explanations (`WinForge.exe explain`) showing exact system changes |
| **Granular Preview & Control** | Bulk execution without preview | Interactive toggle screen (`[X]` / `[ ]`) with individual tweak inspection |
| **System Restore Points** | None or unreliable | Automatic native Volume Shadow Copy (VSS / WMI `SystemRestore`) creation |
| **Registry & Snapshot Backups** | None | Pre-state snapshots & `reg.exe` exports before any modification |
| **One-Click Session Rollback** | Non-reversible or manual fixes | Machine-readable `rollback.json` ledger (`WinForge.exe rollback <SESSION_ID>`) |
| **Privacy & Telemetry** | Often bundles analytics or remote calls | **100% Offline Local Execution**, zero network libraries, zero telemetry |

---

## Installation & Deployment

### Portable Executable (Recommended)
WinForge is distributed as a single portable binary requiring zero installation or Python runtime.

1. Download the latest `WinForge.exe` from the [Releases Page](https://github.com/0xdowz/winforge/releases).
2. Verify SHA-256 binary hash (optional):
   ```powershell
   Get-FileHash .\WinForge.exe -Algorithm SHA256
   ```
3. Run from PowerShell or Command Prompt:
   ```cmd
   WinForge.exe
   ```

> [!NOTE]
> **Windows SmartScreen Note**: As an unsigned open-source utility, Windows SmartScreen may display a warning on first launch. Click **"More Info" -> "Run Anyway"**. You can review the full source code and build instructions in [docs/developer-guide.md](docs/developer-guide.md).

### Developer Source Setup
```powershell
git clone https://github.com/0xdowz/winforge.git
cd winforge
pip install -e .
python -m winforge.main info
```

---

## CLI Command Reference

WinForge supports both guided interactive menus and non-interactive automation flags.

```cmd
WinForge.exe [SUBCOMMAND] [ARGUMENT]
```

| Subcommand / Flag | Description | Admin Needed |
| :--- | :--- | :---: |
| `welcome` | Guided 3-step wizard with hardware intelligence & profile selection | No |
| `explain [ID / #]` | Inspect plain-English explanations & exact registry changes without modifying system | No |
| `scan` | Non-interactive diagnostic scan & hardware analysis | No |
| `optimize` | Execute approved production optimizations | **Yes** |
| `dry-run` | Run complete optimization simulation without system mutations | No |
| `benchmark` | Run quantitative CPU, RAM, Storage, and DNS benchmark suite | No |
| `doctor` | Display System Health & Environment Doctor Diagnostic Report | No |
| `tweaks list` | List all 16 verified optimization recipes with Risk Scores & Categories | No |
| `security-check` | Audit Windows Security state (Defender, Firewall, UAC, Admin rights) | No |
| `rollback <SESSION_ID>`| Reverses all transaction actions for specified Session ID | **Yes** |
| `--demo` | Run non-interactive preview showcasing full workflow | No |

---

## Safety & One-Click Rollback

WinForge enforces a **7-Step Safety Transaction Lifecycle**:
1. **Pre-Flight Disk Safety Gate**: Requires >= 5.0 GB free space on system drive `C:\`.
2. **System Restore Point**: Creates a Windows VSS checkpoint (`WinForge_...`).
3. **Registry Hive Export**: Exports target `HKLM` & `HKCU` branches to `.reg` state files.
4. **Pre-State Snapshot**: Saves `snapshot.json` baseline.
5. **Optimization Execution**: Applies registry, service, or power plan modifications.
6. **Post-Apply Verification**: Audits system mutations using `TweakVerifier`.
7. **Rollback Ledger Commit**: Writes `rollback.json` for 1-click recovery.

### Reversing an Optimization Session
If you ever want to undo changes from an optimization session:
```powershell
WinForge.exe rollback SESSION_20260729_024936_893FE1
```

---

## User-Visible Reports & Output Directory

User reports are intentionally stored in a visible Desktop folder (`Desktop\WinForge Reports\`) because WinForge is an occasional maintenance tool, not a continuously running background service.

* **User-Facing Artifacts (`Desktop\WinForge Reports\`)**: Contains human-readable execution logs (`Logs\winforge.log`), HTML diagnostic scan exports (`Diagnostics\`), session ledgers, snapshots, and `session_summary.json` (`Sessions\SESSION_ID\`), alongside a `README.txt` guide.
* **Protected Internal State (`%LOCALAPPDATA%\WinForge\`)**: Internal crash traces (`startup.log`), pending UAC elevation state (`pending_execution.json`), and configuration checksums remain protected in AppData.
* **Configurable Output Mode**: Set environment variable `WINFORGE_OUTPUT_MODE="LOCALAPPDATA"` to keep outputs hidden inside AppData if required by enterprise policy.

---

## Documentation Index

Deep technical architecture, security specifications, and developer guides are organized under `docs/`:

* **[docs/architecture.md](docs/architecture.md)** — Package hierarchy, component dependency graphs, data flow sequence diagrams, and UAC elevation state machine.
* **[docs/security.md](docs/security.md)** — Offline privacy architecture, threat model, and privilege boundary isolation.
* **[docs/tweak-system.md](docs/tweak-system.md)** — Declarative JSON schema reference, human-friendly explanation fields, and risk scoring matrix (0–100).
* **[docs/developer-guide.md](docs/developer-guide.md)** — Source installation, build script workflow (`build.py`), PyInstaller spec, and test runner instructions (`pytest`).

---

## License

WinForge is free and open-source software licensed under the **[MIT License](LICENSE)**.

<p align="center">
  <b>WINFORGE v1.0.8</b> • Developed with precision by <b>@0xdowz</b><br>
  <i>Safe • Transparent • Reversible • Portable IT Technician Command Line Application</i>
</p>
