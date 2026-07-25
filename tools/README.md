# WinForge Developer & Maintainer Utilities (`tools/`)

> **DEVELOPER NOTICE**: The scripts in `tools/internal/` are standalone offline maintenance utilities intended exclusively for project maintainers. **They are strictly excluded from compiled release binaries (`WinForge.exe`).**

---

## Directory Structure

```
tools/
├── README.md                              # Maintainer documentation
└── internal/                              # Offline Maintainer Tools
    ├── key_generator.py                   # RSA-2048 offline key pair generator
    └── license_creator.py                 # RSA-PSS signature payload creator
```

---

## Utility Overview

### 1. `tools/internal/key_generator.py`
- **Purpose**: Generates RSA-2048 keypairs (`private_key.pem` and `public_key.pem`) for testing offline PKCS#1 / RSA-PSS digital signatures.
- **Security Guarantee**: `private_key.pem` MUST NEVER be committed to Git or shipped in client binaries.

### 2. `tools/internal/license_creator.py`
- **Purpose**: Signs license payload structures using `private_key.pem` via RSA-PSS and SHA-256 for testing offline verifier models.

---

## Exclusion Guarantee

These scripts are excluded during PyInstaller binary packaging (`build.py`) and are not required for standard WinForge CLI diagnostic scanning, benchmarking, or optimization execution.
