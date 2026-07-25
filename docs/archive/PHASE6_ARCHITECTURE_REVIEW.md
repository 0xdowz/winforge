> **HISTORICAL DEVELOPMENT DOCUMENT**: Current official project identity: **WinForge** maintained by **@0xdowz**.

# WinForge: Phase 6 Commercial Licensing & Machine Fingerprinting Architecture Review

## 1. Executive Summary & Core Decoupling Philosophy

Phase 6 establishes the **Commercial Licensing & Machine Fingerprinting Subsystem** for WinForge. The primary architectural objective is to enable commercial node-locking, offline activation key verification, and business tier enforcement **without tightly coupling licensing logic to the Core Optimization Engine**.

---

## 2. Licensing Architecture & Module Organization

To enforce strict security boundaries, licensing functionality is separated between client runtime modules and vendor offline tooling:

```
WINFORGE/
├── winforge/
│   └── licensing/               # CLIENT RUNTIME ONLY
│       ├── __init__.py
│       ├── models.py            # License data schemas & ValidationState enum
│       ├── fingerprint.py       # FingerprintProvider & scoring engine
│       ├── verifier.py          # RSA-PSS signature verifier
│       └── policy.py            # Business tier capability manager
│
└── tools/                       # VENDOR OFFLINE TOOLING ONLY (NOT IN EXE)
    ├── key_generator.py         # Vendor RSA-2048 keypair generator
    └── license_creator.py       # Vendor private key license signing tool
```

> [!CAUTION]
> **Zero Key Leakage Guarantee**: The client executable (`WinForge.exe`) contains **ONLY** the RSA-2048 Public Verification Key (`public_key.pem`) and signature verification logic (`verifier.py`). Private signing keys (`private_key.pem`) and signing tools reside exclusively in vendor offline tooling (`tools/`).

---

## 3. Dynamic Fingerprint Scoring Engine (`FingerprintProvider`)

### A. Flexible Scoring Engine Architecture
Rather than relying on hardcoded constant weights, hardware signals are processed through the `FingerprintProvider` dynamic scoring engine.

Each hardware signal evaluates three dynamic factors:
- `availability_score` (0.0 - 1.0): Whether the identifier is present and non-null.
- `reliability_score` (0.0 - 1.0): Metric stability across system reboots or driver updates.
- `confidence_weight` (0.0 - 1.0): Relative contribution weight.

```
Raw Hardware Data (WMI / Win32 / psutil)
                 │
                 ▼
     Normalization Engine (Strip Whitespace, Uppercase)
                 │
                 ▼
  Per-License Salted SHA-256 Hashing Engine
                 │
                 ▼
Dynamic Fingerprint Record (fingerprint_version: 1)
```

> [!IMPORTANT]
> **Privacy Guarantee**: Raw hardware identifiers (serial numbers, MAC addresses) are **NEVER** stored on disk, logged in event logs, or embedded in license keys. All hardware signals are normalized and hashed using SHA-256 with a per-license salt.

### B. Dynamic Matching Engine Output Schema
The matching engine compares current hardware signals against the license record and produces:

```json
{
  "match_score": 85.0,
  "matched_components": ["MOTHERBOARD_UUID", "CPU_PROCESSOR_ID", "PRIMARY_DISK_SERIAL"],
  "changed_components": ["PRIMARY_NIC_MAC"],
  "activation_decision": true,
  "threshold_required": 75.0
}
```

### C. Hardware Replacement & Upgrade Scenarios

| Hardware Scenario | Matched Signals | Score | Decision | Behavior |
| :--- | :--- | :---: | :---: | :--- |
| **Same Machine** | Motherboard, CPU, Disk, MAC | **100%** | **VALID** | Exact match. |
| **SSD / Drive Replacement** | Motherboard, CPU, MAC | **85%** | **VALID** | Hardware upgrade tolerated ($\ge 75\%$). |
| **NIC / Adapter Replacement** | Motherboard, CPU, Disk | **85%** | **VALID** | Hardware upgrade tolerated ($\ge 75\%$). |
| **Windows OS Reinstall** | Motherboard, CPU, Disk, MAC | **100%** | **VALID** | Identifiers unchanged by OS reinstall. |
| **Motherboard Replacement** | CPU, Disk, MAC | **60%** | **MISMATCH**| Score $< 75\%$; requires license transfer. |

---

## 4. Cryptographic RSA-PSS Licensing & Offline Validation

### A. RSA-PSS Signature Scheme
- **Algorithm**: RSA-2048 with **RSA-PSS** (Probabilistic Signature Scheme) padding and **SHA-256**.
- **Offline Operation**: Validation operates 100% offline. `WinForge.exe` uses `public_key.pem` to verify digital signatures in `licenses/license.json`.

### B. Validation State Enum (`ValidationState`)
```python
class ValidationState(str, Enum):
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    MACHINE_MISMATCH = "MACHINE_MISMATCH"
    CLOCK_SUSPICIOUS = "CLOCK_SUSPICIOUS"
    CORRUPTED_LICENSE = "CORRUPTED_LICENSE"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
```

### C. Safe Fail & Non-Blocking Guarantee
If `LicenseManager` returns any state other than `VALID` (e.g. `EXPIRED` or `MACHINE_MISMATCH`), the application falls back safely to `FREE_EDITION` mode. Core diagnostic scans, category health scores, benchmarks, and HTML report exports are **NEVER** disabled or blocked.

---

## 5. Extended License Model Schema (`licenses/license.json`)

```json
{
  "schema_version": "2.0.0",
  "license_id": "LIC-2026-TECH-99482",
  "license_type": "TECHNICIAN",
  "customer_id": "CUST-ACME-8841",
  "created_at": "2026-07-25T00:00:00Z",
  "expires_at": "2027-07-25T23:59:59Z",
  "fingerprint_version": 1,
  "machine_fingerprint": "a3f8c92e10b4d7e901f4c28b3a7d1e89f4b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8",
  "feature_flags": {
    "technician_mode_allowed": true,
    "unlimited_machines": true,
    "custom_branding_allowed": true,
    "offline_activation": true
  },
  "max_activations": 1,
  "activation_history": [
    {
      "timestamp": "2026-07-25T12:00:00Z",
      "machine_hash": "a3f8c92e10b4..."
    }
  ],
  "revocation_status": false,
  "signature": "MEUCIQDx4B9...Base64EncodedRSAPSSSignature..."
}
```

---

## 6. Business Tier Capability Matrix

| Capability | Free Edition | Personal | Professional | Technician |
| :--- | :---: | :---: | :---: | :---: |
| **Diagnostic Scan & Health Score** | ✓ | ✓ | ✓ | ✓ |
| **Benchmark Suite & HTML Reports** | ✓ | ✓ | ✓ | ✓ |
| **Client Optimizations (Risk 0-20)** | ✗ | ✓ | ✓ | ✓ |
| **Moderate Optimizations (Risk 21-50)**| ✗ | ✓ | ✓ | ✓ |
| **Technician Mode (`--tech`)** | ✗ | ✗ | ✓ | ✓ |
| **Tweak Inspection Cards (Risk 51-100)**| ✗ | ✗ | ✗ | ✓ |
| **Deployment Mode** | Local Scan | 1 PC | 5 PCs | Portable USB |

---

## 7. Testing Strategy (`tests/test_licensing.py`)

Automated PyTest test suite covering:
1. **Valid License Acceptance**: RSA-PSS signature verification succeeds.
2. **Expired License Rejection**: Returns `ValidationState.EXPIRED`.
3. **Corrupted Signature Rejection**: Returns `ValidationState.INVALID_SIGNATURE`.
4. **Hardware Upgrade Simulation**:
   - `profile_A` (Same Machine): Score 100% $\rightarrow$ `VALID`.
   - `profile_B` (SSD Changed): Score 85% $\rightarrow$ `VALID`.
   - `profile_C` (NIC Changed): Score 85% $\rightarrow$ `VALID`.
   - `profile_D` (Motherboard Changed): Score 60% $\rightarrow$ `MACHINE_MISMATCH`.
5. **Clock Rollback Detection**: Returns `ValidationState.CLOCK_SUSPICIOUS`.
6. **Missing Identifiers**: Handles absent serials gracefully without throwing unhandled exceptions.

---

## 8. Migration & Zero-Regression Guarantee

Phase 6 code will be confined to `winforge/licensing/`, `tools/`, and `tests/test_licensing.py`. All 38 existing unit tests, the Phase 5 execution framework, the 4-layer backup subsystem, and CLI modes will continue passing with 100% success.
