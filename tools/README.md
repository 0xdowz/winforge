# WinForge Developer Utilities (`tools/`)

> **DEVELOPER NOTICE**: The scripts in this directory are standalone offline maintenance utilities intended exclusively for project maintainers and developers. **They are strictly excluded from compiled release binaries (`WinForge.exe`).**

---

## Contents & Utility Overview

### 1. `key_generator.py`
- **Purpose**: Generates RSA-2048 keypairs (`private_key.pem` and `public_key.pem`) for testing offline PKCS#1 / RSA-PSS digital signatures.
- **Security Note**: `private_key.pem` MUST NEVER be committed to Git or shipped in client binaries.

### 2. `license_creator.py`
- **Purpose**: Signs license payload structures using `private_key.pem` via RSA-PSS and SHA-256 for testing offline verifier models.

---

## Exclusion Guarantee

These scripts are ignored during PyInstaller binary packaging (`build.py`) and are not required for standard WinForge CLI diagnostic scanning, benchmarking, or optimization execution.
