# WinForge Developer & Build Guide

This document covers source installation, developer testing workflows, and the portable executable compilation process for WinForge v1.0.8.

---

## 1. Source Environment Setup

```powershell
# 1. Clone repository
git clone https://github.com/0xdowz/winforge.git
cd winforge

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies in editable mode
pip install -e .
```

---

## 2. Test Execution Workflow

WinForge maintains a 61-test unit and integration suite.

```powershell
# Run full test suite with verbose output
python -m pytest tests/ -vv
```

---

## 3. Building Standalone Binary

WinForge uses PyInstaller driven by a centralized build script (`build.py`).

```powershell
# Execute build script
python build.py
```

- Output executable path: `dist/WinForge.exe` (~38.77 MB)
- Embedded resources: `assets/icon.ico`, `config/`, `VERSION`, `CHANGELOG.md`, `BUILD_INFO`.
