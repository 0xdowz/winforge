# WinForge Security & Privacy Architecture

This document specifies the privacy model, threat boundaries, and security architecture of WinForge v1.0.8.

---

## 1. Offline Execution & Zero Telemetry Guarantee

WinForge is designed for high-security environments, enterprise IT workstations, and privacy-conscious users.

* **Zero HTTP Client Dependencies**: The codebase contains no network libraries (`requests`, `urllib3`, `httpx`). WinForge cannot initiate network connections or remote API requests.
* **Zero Telemetry / Analytics**: WinForge collects no telemetry, hardware serial numbers, MAC addresses, or usage metrics.
* **100% Embedded Configuration**: All optimization recipe definitions and policies are packaged locally inside the application bundle.
* **Local Isolated Logging & Report Storage**: User-facing reports, HTML diagnostics, session ledgers, and human logs (`winforge.log`) are stored in a visible Desktop folder (`Desktop\WinForge Reports\`) because WinForge is an occasional maintenance tool. Internal temporary execution states and crash traces (`startup.log`) remain protected in `%LOCALAPPDATA%\WinForge\`.

---

## 2. Privilege Boundary & UAC Elevation Isolation

WinForge strictly enforces the principle of least privilege:

1. **Non-Elevated Diagnostics**: Scans, benchmarks, health audits, doctor checks, tweak explanations (`WinForge.exe explain`), and dry-run simulations execute unprivileged.
2. **Explicit Consent & Approval**: Privilege elevation via `ShellExecuteW(runas)` is requested only after the user explicitly approves optimization execution.
3. **Audit Trail**: Every elevated action is recorded in a machine-readable JSON transaction ledger (`rollback.json`) for post-execution compliance review.

---

## 3. Configuration & Database Integrity

* **SHA-256 Checksum Validation**: Tweak definition JSON files are validated against SHA-256 integrity hashes in `config/checksums.json`. If a configuration file is tampered with, WinForge displays an explicit integrity warning banner before execution.
* **Schema Validation & Fallback Injections**: `validate_tweak_schema()` verifies all incoming recipe objects, ensuring missing or malformed fields default to safe, non-destructive values.
