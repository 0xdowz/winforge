# WinForge Documentation Assets (`docs/images/`)

This directory contains visual documentation assets and terminal preview screenshots referenced by `README.md` and public GitHub release notes.

---

## Asset Checklist for Maintainer (@0xdowz)

To complete the visual presentation of WinForge, capture high-resolution Windows Terminal screenshots (or `.gif` recordings) of the following CLI commands and place them in this folder:

| Filename | Command / Screen to Capture | Description / Focus |
| :--- | :--- | :--- |
| `dashboard.png` | `WinForge.exe --scan` | Main Rich System Health Dashboard & health index progress bar |
| `scan-result.png` | `WinForge.exe --scan` | Diagnostic Hardware Specification Table & System Degradation Alerts |
| `dry-run.png` | `WinForge.exe --dry-run` | Simulation mode log output & session HTML report link |
| `benchmark.png` | `WinForge.exe benchmark` | Quantitative CPU, Memory, Disk, and DNS latency benchmark results |
| `technician-mode.png` | `WinForge.exe --tech` | Tweak Inspection Cards displaying risk scores & technical parameters |
| `demo.gif` | Full CLI Execution Flow | Recorded animation showing terminal scan, simulation, and report generation |

---

## Capture Guidelines

- **Terminal Environment**: Windows Terminal with `Cascadia Code` font or `JetBrains Mono`.
- **Theme**: Dark mode theme (e.g. One Half Dark, Dracula, or Windows Terminal Default Dark).
- **Window Size**: $120 \times 32$ columns/rows for optimal reading width on GitHub.
