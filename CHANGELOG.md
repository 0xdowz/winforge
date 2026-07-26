# Changelog

All notable changes to **WinForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`--demo` Mode**: Non-interactive read-only preview mode that runs a full system scan, benchmark suite, and renders all output panels without user prompts. Terminal stays open with a structured completion summary panel until user presses Enter. Suitable for screenshots and presentations.
- **`benchmark` Subcommand**: Non-interactive benchmark-only mode (`WinForge.exe benchmark`) now exits cleanly after printing results instead of falling through to the interactive menu.

### Improved
- **Responsive Terminal Layout**: All Rich console instances now detect terminal width via `shutil.get_terminal_size()` at startup, capping at 160 columns. Tables and panels degrade gracefully from 80 to 160-column terminals without overflow.
- **Structured Dry-Run Output**: `--dry-run` now renders a `SCORE PROJECTION` panel (baseline vs. projected vs. delta) and a `SESSION REPORT GENERATED` panel with file paths, replacing plain `print()` lines.
- **Benchmark Results Table**: Benchmark output is now a 3-column aligned Rich table (`Metric / Result / Unit`) instead of plain bullet points.
- **Shared Console Instance**: `winforge.cli.components` and `winforge.cli.interface` now share one width-aware `Console` instance, eliminating double rendering artefacts.
- **CI Pipeline**: Added Python matrix (3.12, 3.13), pip dependency caching, explicit step names, and post-install CLI import smoke test.

### Fixed
- `benchmark` subcommand previously launched the interactive menu instead of running benchmarks non-interactively.
- `interface.py` created a second `Console()` instance independently of `components.py`, causing potential width inconsistency.

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
