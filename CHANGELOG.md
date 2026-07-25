# Changelog

All notable changes to **WinForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
