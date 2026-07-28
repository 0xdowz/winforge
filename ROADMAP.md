# WinForge Project Roadmap

This document outlines the architectural roadmap, planned features, and release history for **WinForge**.

---

## 🟢 Version 1.0.8 — Current Stable Release

- [x] **Diagnostic Telemetry Engine**: WMI and Win32 hardware inspection (CPU, GPU, RAM, Storage, Power Plan).
- [x] **Hardware Intelligence Engine v2**: Auto-detects hardware profile recommendations with confidence scoring.
- [x] **State-Persistence Elevation Resume System (`--resume SESSION_ID`)**: Persists state to `pending_execution.json` prior to elevation and auto-resumes after UAC launch.
- [x] **Disk Space Safety Gate (>= 5.0 GB)**: Enforces a strict 5.0 GB minimum free disk space safety check on system drive `C:\`.
- [x] **Centralized Tweak Schema Validation**: Auto-injects safe defaults for missing metadata (`"No rationale provided"`).
- [x] **Registry Hive Path Normalization**: Auto-prefixes shorthand key paths (`SOFTWARE\...` -> `HKLM\SOFTWARE\...`).
- [x] **Multi-Resolution Embedded Icon**: Integrates custom multi-resolution RGBA icon (`assets/icon.ico`) into `WinForge.exe`.
- [x] **WinForge System Health Score (0–100)**: Internal health metrics based on system degradation parameters.
- [x] **4-Layer Safety Subsystem Lock**: Windows Restore Points, targeted `.reg` exports, state JSON snapshots, and atomic transaction ledgers.
- [x] **Automated LIFO Rollback Engine**: One-click restoration of applied system tweaks (`winforge rollback SESSION_ID`).
- [x] **Quantitative Micro-Benchmarks**: CPU latency, RAM throughput, disk sequential write speed, timer resolution, and DNS performance.
- [x] **Security & Hygiene Health Module (`winforge security-check`)**: Audits Windows Defender, Firewall, UAC, BitLocker, Windows Update, and Admin privileges.
- [x] **Technician Inspection Mode (`--tech`)**: Granular terminal inspection cards for manual confirmation.
- [x] **Standalone Portable Binary**: PyInstaller single-file build (`WinForge.exe`, ~38.8 MB).

---

## 🟡 Version 1.1.0 — Advanced Telemetry & Automation (Q3 2026)

- [ ] **Extended Diagnostic Profiler**: Advanced NVMe S.M.A.R.T. health monitoring and GPU thermal throttling detection.
- [ ] **Headless Automation Flag (`--headless`)**: Silently outputs JSON/CSV diagnostic telemetry for enterprise RMM integrations.
- [ ] **Enhanced Network Diagnostic Suite**: MTU path discovery, TCP window size analyzer, and bufferbloat testing.
- [ ] **Custom Tweak Policy Exporter**: Export custom tweak rule JSON profiles for team-wide deployment across multiple client PCs.

---

## 🔵 Version 1.2.0 — Extended Systems Analysis (Q4 2026)

- [ ] **Event Log Forensic Analyzer**: Automatic extraction and categorization of critical Windows Kernel Event IDs (Kernel-Power, WHEA-Logger, BSOD dump analysis).
- [ ] **Windows Update Policy Auditor**: Inspection of active Group Policy Objects (GPO) and WSUS update rules.
- [ ] **Driver Integrity Verifier**: Detection of unsigned third-party drivers and stale device driver packages.

---

## Feature Requests & Feedback

Have a suggestion for the roadmap? Feel free to open a feature request on [GitHub Issues](https://github.com/0xdowz/winforge/issues).
