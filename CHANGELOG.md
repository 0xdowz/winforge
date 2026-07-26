# Changelog

All notable changes to **WinForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.7] - 2026-07-26

### Added
- **Enterprise Intelligence Upgrade**: Product subtitle "Windows Performance Intelligence Platform" and engine architecture module tree.
- **Hardware Intelligence Engine v2**: Added hardware scoring engine calculating profile recommendation confidence (e.g. 92%) with explicit reasons.
- **Explain-Before-Execute Interactive Wizard**: Prompts with `[Y] Apply`, `[N] Cancel`, `[D] Detailed view` prior to any system mutation.
- **Safety Shield Activation & Rollback Engine**: Standardized "Safety Shield Activated" status cards and added `winforge rollback list` and `winforge rollback SESSION_ID`.
- **Security Health Module (`winforge security-check`)**: Scans Windows Defender, Firewall, UAC, BitLocker, Windows Update, and Admin rights to calculate a Security Health Score.
- **New Professional Commands**: Added `winforge info`, `winforge analyze`, `winforge tweaks list`, and `winforge security-check`.
- **Local Privacy Guarantee**: Clear offline, zero telemetry, zero cloud connection startup declaration.

## [1.0.6] - 2026-07-26

### Added
- **Enterprise Dark Cybersecurity Theme**: Cyber Cyan, Matrix Green, Amber, Red, and Slate Gray color tokens with strict typography hierarchy.
- **Hardware Intelligence Engine**: Auto-detects CPU, GPU, RAM, and Power State to recommend tailored Gaming, Battery Efficiency, or Workstation profiles.
- **Human Optimization Report**: Added detailed post-optimization report with storage recovery, performance percentage improvement, and rollback availability.
- **Print Statement Audit**: Removed raw `print()` calls in favor of managed `RendererManager` output queue across all CLI modules.
- **Detailed Tweak Explanation Cards**: Beginner-focused explanation cards detailing exact changes, reasons, expected benefits, and required knowledge.

## [1.0.5] - 2026-07-26

### Added
- **Commercial-Grade CLI Identity System**: Brand new fastfetch / cargo / docker inspired startup experience with ASCII logo, version tags, developer attribution, build mode, and security status.
- **Centralized `RendererManager` Engine**: Architectural rendering queue enforcing 80/90/120 column terminal safety, zero text overlaps, strict section lifecycle, and clean spacing.
- **Guided Optimization Wizard**: Interactive beginner onboarding wizard with profile tiering (`Safe / Beginner`, `Advanced`, `Technician`).
- **Beginner Education & Execution Summary**: Detailed tweak explanation cards and comprehensive post-optimization system improvement summary.
- **Session Safety Transaction Lifecycle**: Centralized `SafetyTransactionManager` executing single-session 4-layer safety initialization.

## [1.0.4] - 2026-07-26

### Added
- **Complete CLI Layer Audit**: Verified clean separation of terminal presentation (`winforge/cli/`) from core optimization state machine, policy rules, and system mutation handlers.

### Improved
- **Open-Source Release Hygiene**: Validated 100% clean tracked file tree, verified PyTest unit test coverage (46/46 passed), and verified PyInstaller binary packaging pipeline.

## [1.0.3] - 2026-07-26

### Added
- **Full Repository Cleanup & Audit**: Performed complete repository audit, verifying file classification, `.gitignore` rules, and tracked file trees for release readiness.

### Improved
- **CLI Architecture Separation**: Enforced strict separation between presentation rendering (`winforge/cli/renderer.py`, `themes.py`, `formatting.py`, `progress.py`) and underlying core business logic.

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
