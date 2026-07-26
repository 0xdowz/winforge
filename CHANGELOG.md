# Changelog

All notable changes to **WinForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-07-26

### Added
- **Repository Quality Overhaul**: Cleaned obsolete scratch logs and reorganized documentation structure to enterprise open-source standards.
- **Enhanced Architecture Section in README**: Detailed 7-layer ASCII system workflow diagram outlining CLI presentation, Policy matrix guardrails, 4-Layer Safety Lock, Category Dispatcher, and Verification engine.

### Improved
- **Open-Source README Presentation**: Redesigned README.md with standard shields badges, structured Quick Start guides, CLI command matrix, safety architecture details, and PyTest validation commands.

## [1.0.1] - 2026-07-26

### Added
- **Professional CLI Design System**: Tokenized color palette theme manager (`winforge/cli/themes.py`), status & risk badges (`winforge/cli/formatting.py`), and interactive prompts (`winforge/cli/prompts.py`).
- **`winforge doctor` Subcommand**: Environment and 4-Layer Safety Engine diagnostic tool checking Administrator elevation, OS compatibility, CPU/RAM status, and restore point readiness.
- **Pre-Execution Optimization Plan & 4-Layer Safety Lock Panels**: Rendered via [`winforge/cli/renderer.py`](file:///c:/Users/Admin/Desktop/Twek/winforge/cli/renderer.py) before any mutations occur.
- **3-Part Actionable Error Panels**: Provides clear 3-step error reporting (*What happened*, *Why it happened*, *Suggested action*) for policy blocks and execution errors.
- **`StepTracker` Progress Tracker**: Multi-step pipeline execution tracker in [`winforge/cli/progress.py`](file:///c:/Users/Admin/Desktop/Twek/winforge/cli/progress.py).
- **`--demo` Mode**: Non-interactive read-only preview mode that runs full system scan and benchmark suite for documentation screenshot generation.

### Improved
- **CI Reliability & OS Isolation**: Added deterministic `client_system_report` and `server_system_report` pytest fixtures in `tests/conftest.py` ensuring unit tests pass deterministically on Windows Server CI runners while preserving 100% of Server OS protection guardrails.
- **Responsive Terminal Layout**: All Rich console instances detect terminal width via `shutil.get_terminal_size()`, handling 80 to 160-column terminal windows gracefully without line wrapping or border overflow.

### Fixed
- Fixed unit test policy evaluation failures on Windows Server CI runners (`windows-latest`).
- Fixed service handler test flake by querying universal `RpcSs` service instead of consumer telemetry `DiagTrack`.

---

## [1.0.0] - 2026-07-25

### Added
- **Diagnostic Engine**: WMI and Win32 hardware inspection across CPU, GPU, RAM, Storage, OS Build, and Active Power Plans.
- **Quantitative Benchmark Suite**: Micro-benchmark metrics measuring CPU execution latency (ms), memory throughput (MB/s), disk write speeds (MB/s), timer resolution (ms), and DNS resolution latency (ms).
- **4-Layer Safety Subsystem Lock**: Automated WMI System Restore Point creation (`WINFORGE_OPT_`), targeted `.reg` exports, pre-execution system state snapshots, and atomic transaction ledgers.
- **Automated LIFO Rollback Engine**: One-click restoration of system modifications if post-execution state verification fails.
- **11-State Execution Lifecycle Machine**: State machine for tracking discovery, analysis, backup, application, verification, and rollback states.
- **Risk Score Intelligence**: Categorization (`SAFE`, `MODERATE`, `ADVANCED`, `TECHNICIAN ONLY`) with risk thresholds (0–100).
- **Technician Inspection Mode (`--tech`)**: Granular manual inspection cards for reviewing individual tweaks.
- **Rich Terminal User Experience**: Terminal dashboards, progress bars, hardware spec tables, degradation alerts, and warning cards.
- **Configuration Integrity Verification**: SHA-256 hash checksum verification (`config/checksums.json`) for tweak JSON database files.
- **Open Source Preparation**: Rebranded package to `WinForge`, created `.github` workflows, issue templates, PR templates, and open-source documentation (`AUTHORS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `RELEASE.md`).
