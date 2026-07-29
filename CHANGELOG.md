# Changelog

All notable changes to **WinForge** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.8] - 2026-07-29

### Added
- **Human-Readable Optimization Explanations**: Extended tweak recipes with `friendly_name`, `what_it_does`, `why_it_exists`, and `exact_system_changes`. Added interactive `WinForge.exe explain [ID / #]` subcommand for non-destructive tweak education.
- **Granular Tweak Selector & Interactive Preview**: Added `render_tweak_selection_menu()` allowing users to toggle individual candidate tweaks (`[X]` / `[ ]`), view detail cards (`D 1`), select all (`A`), or clear all (`C`) prior to execution.
- **User-Visible Desktop Output Directory (`Desktop\WinForge Reports\`)**: Uses Windows Shell Known Folder API (`SHGetFolderPathW`) to store user-visible HTML reports, session ledgers, snapshots, session summaries, and human logs in `Desktop\WinForge Reports\`, while isolating internal UAC execution state in `%LOCALAPPDATA%\WinForge\`.
- **Resilient 3-Level Logging Fallback**: Centralized logger attempts Priority 1 (`Desktop\WinForge Reports\Logs\winforge.log`), falls back to Priority 2 (`%LOCALAPPDATA%\WinForge\logs\winforge.log`), and Priority 3 (`StreamHandler`). Logging initialization will never crash application startup.
- **State-Persistence Elevation Resume System (`--resume SESSION_ID`)**: Automatically persists selected profile, max risk, and candidate tweak choices to `%LOCALAPPDATA%\WinForge\sessions\pending_execution.json` prior to elevation, allowing the elevated UAC process to resume execution automatically without losing user state.
- **Centralized Tweak Schema Validation (`validate_tweak_schema`)**: Enforces required metadata fields (`id`, `name`, `description`, `rationale`, `risk_score`, `category`) and injects safe fallback values (`"No rationale provided"`), completely eliminating potential `KeyError` crashes on missing metadata.
- **Registry Key Path Normalization**: Automatically transforms shorthand or missing hive paths (e.g. `SOFTWARE\Microsoft\...` -> `HKLM\SOFTWARE\Microsoft\...`, `System\GameConfig` -> `HKLM\System\GameConfig`) to standard reg.exe export formats.
- **Disk Space Safety Gate (>= 5.0 GB)**: Enforces a strict 5.0 GB minimum free disk space check on system drive `C:\` prior to preflight safety execution, safely cancelling optimization if disk space is low.
- **Session-Level Transaction Restore Point Logic**: Restricts System Restore Point creation to **ONE** session-level checkpoint (`WinForge_SESSION_TIMESTAMP`), eliminating redundant per-tweak restore points.
- **Absolute Stable Path Architecture**: Updated `winforge/utils/paths.py` with `get_executable_dir()` ensuring PyInstaller frozen binaries and script dev modes resolve stable absolute paths regardless of working directory differences.

## [1.0.7] - 2026-07-26

### Added
- **Enterprise Intelligence Upgrade**: Product subtitle "Windows Performance Intelligence Platform" and engine architecture module tree.
- **Hardware Intelligence Engine v2**: Added hardware scoring engine calculating profile recommendation confidence (e.g. 92%) with explicit reasons.
- **Explain-Before-Execute Interactive Wizard**: Prompts with `[Y] Apply`, `[N] Cancel`, `[D] Detailed view` prior to any system mutation.
- **Safety Shield Activation & Rollback Engine**: Standardized "Safety Shield Activated" status cards and added `winforge rollback list` and `winforge rollback SESSION_ID`.
- **Security Health Module (`winforge security-check`)**: Scans Windows Defender, Firewall, UAC, BitLocker, Windows Update, and Admin rights to calculate a Security Health Score.
- **New Professional Commands**: Added `winforge info`, `winforge analyze`, `winforge tweaks list`, and `winforge security-check`.
- **Local Privacy Guarantee**: Clear offline, zero telemetry, zero cloud connection startup declaration.
