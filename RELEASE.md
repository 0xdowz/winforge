# WinForge Release Checklist & Build Instructions

This document outlines the release checklist for publishing new versions of WinForge.

---

## Pre-Release Checklist

1. **Test Suite Verification**:
   ```cmd
   python -m pytest tests/
   ```
   *Requirement: 100% pass rate (42/42 tests passing).*

2. **Configuration Checksum Generation**:
   Verify or update SHA-256 hashes in `config/checksums.json` if tweak database JSON files were modified.

3. **Version Number Sync**:
   Ensure the version string matches `1.0.0` in:
   - `VERSION`
   - `pyproject.toml`
   - `winforge/__init__.py`
   - `CHANGELOG.md`

4. **Standalone PyInstaller Build**:
   ```cmd
   python build.py
   ```
   *Requirement: Generates `dist/WinForge.exe` (~38.8 MB).*

5. **Executable Smoke Test**:
   ```cmd
   .\dist\WinForge.exe --help
   .\dist\WinForge.exe --scan
   .\dist\WinForge.exe --license-info
   ```

---

## Tagging & Publishing Releases

1. Commit all verified changes:
   ```cmd
   git add .
   git commit -m "rel: Release v1.0.0"
   git tag -a v1.0.0 -m "WinForge v1.0.0 Release"
   ```

2. Push to GitHub:
   ```cmd
   git push origin main --tags
   ```

3. Attach `dist/WinForge.exe` to the GitHub Tag Release page.
