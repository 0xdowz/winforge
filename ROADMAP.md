# WinForge Project Roadmap

This document outlines the architectural roadmap, planned features, and release history for **WinForge**.

---

## 🟢 Version 1.0.0 — Initial Stable Release (Current)

- [x] **Diagnostic Telemetry Engine**: WMI and Win32 hardware inspection (CPU, GPU, RAM, Storage, Power Plan).
- [x] **WinForge System Health Score (0–100)**: Internal health metrics based on system degradation parameters.
- [x] **4-Layer Safety Subsystem Lock**: Windows Restore Points, targeted `.reg` exports, state JSON snapshots, and atomic transaction ledgers.
- [x] **Automated LIFO Rollback Engine**: One-click restoration of applied system tweaks.
- [x] **Quantitative Micro-Benchmarks**: CPU latency, RAM throughput, disk sequential write speed, timer resolution, and DNS performance.
- [x] **Risk Score Intelligence**: Categorization of tweaks (`SAFE`, `MODERATE`, `ADVANCED`, `TECHNICIAN`) with risk weighting.
- [x] **Technician Inspection Mode (`--tech`)**: Granular terminal inspection cards for manual confirmation.
- [x] **Configuration Integrity Engine**: SHA-256 integrity hash verification (`config/checksums.json`).
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
