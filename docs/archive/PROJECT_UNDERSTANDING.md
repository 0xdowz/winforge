# WinForge: Comprehensive Technical & Architectural Blueprint

---

## Part One: Project Identity & Purpose

### 1. What WinForge Is
**WinForge** is a commercial-grade, portable Windows System Diagnostic & Optimization CLI tool designed for IT service technicians, system administrators, and performance engineers. Built with a **Terminal-First** philosophy, it delivers non-destructive system diagnostics, category-based health scoring, risk-rated tweak intelligence, a 4-layer safety subsystem lock, and offline cryptographic RSA-PSS signature verification.

### 2. Why It Exists & Problem Solved
Conventional Windows "debloat" scripts or opaque GUI registry cleaners are frequently unsafe, unverified, and non-reversible. They modify system settings silently without backups, often breaking OS stability, disabling Windows Update, or crashing critical background services.

WinForge exists to provide a **safe, transparent, verifiable, and completely reversible** alternative for IT service professionals who require commercial reliability when servicing customer computers.

### 3. Target Audience
- **IT Field Technicians**: Servicing customer PCs using a portable USB executable without pre-installing Python or third-party frameworks.
- **System Administrators**: Auditing and tuning Windows 10/11 workstations across enterprise networks.
- **Power Users & Gamers**: Fine-tuning system responsiveness, GPU scheduling, and network latency safely.

### 4. Product Vision & Commercial Purpose
WinForge is designed for commercial service operations. Technicians perform paid PC optimization routines for clients, using the tool's automated safety locks, risk score badges, and standalone HTML diagnostic report exports to demonstrate tangible performance improvements.

### 5. Why CLI Is the Correct Format
- **Zero Overhead & Portability**: Runs as a single portable binary (`ANASOptimizer.exe`) from any USB drive without requiring installers, desktop window managers, web runtimes, or GUI frameworks.
- **Remote & Headless Administration**: Can be invoked via WinRM, PowerShell, SSH, or batch automation scripts across enterprise workstations.
- **Terminal Efficiency**: IT technicians work faster in terminal environments where system state, diagnostic scorecards, and tweak specifications are rendered concisely using Rich terminal formatting.
- **Terminal Identity**: Built with the tool philosophy of Unix/Linux CLI software like `git`, `docker`, `kubectl`, `btop`, and `neofetch`.

---

## Part Two: Internal Architecture

WinForge follows a clean modular architecture:

```
ANAS_OPTIMIZER/
├── winforge/
│   ├── analyzers/            # WMI & System Diagnostic Collectors
│   ├── benchmark/            # Quantitative Latency & Throughput Benchmark Suite
│   ├── cli/                  # Rich Terminal User Interface (Banners, Tables, Dashboards)
│   ├── core/                 # Engine, Policy Engine, Safety Approval, Privileges
│   ├── licensing/            # RSA-PSS Cryptographic Verifier & Fingerprint Provider
│   ├── models/               # Pydantic Schemas (System, Tweak, Policy, License)
│   ├── optimizations/        # Category Optimizers, Handlers, Dispatcher, Executor
│   ├── reports/              # Interactive HTML & JSON Standalone Exporters
│   ├── safety/               # Restore Point, Registry Backup, Snapshot, Rollback
│   └── utils/                # Relative Path Resolution & Helper Utilities
│
├── config/                   # External Tweak DB (JSON) & OS Compatibility Matrix
├── tools/                    # Vendor Offline RSA-2048 Key Generator & License Signer
└── tests/                    # 42 Automated PyTest Unit & Integration Tests
```

### Module Responsibilities & System Architecture:
1. **Diagnostic Collectors (`winforge/analyzers/`)**:
   - `cpu.py`, `gpu.py`, `ram.py`, `storage.py`, `os_info.py`, `services.py`, `startup.py`, `power.py`, `network.py`: Query WMI, Win32 API, and `psutil` metrics to construct `SystemHealthReport`.
2. **Policy Engine (`winforge/core/policy.py`)**:
   - Evaluates Windows OS build compatibility and device profiles (Laptop vs Desktop).
3. **Execution Framework & Dispatcher (`winforge/optimizations/`)**:
   - `dispatcher.py`: `CategoryDispatcher` routes tweaks to category-specific optimizers (`GamingOptimizer`, `PowerOptimizer`, `StartupOptimizer`, `ServicesOptimizer`, `CleanupOptimizer`, `NetworkOptimizer`).
   - `registry_handler.py` & `service_handler.py`: Low-level Win32 Registry and Windows Service abstractions with `mock_execution=True` defaults.
   - `executor.py`: `OptimizationExecutor` orchestrates tweak execution through an 11-state lifecycle state machine.
   - `verifier.py`: `TweakVerifier` checks post-execution registry/service state.
4. **Safety Subsystem Lock (`winforge/safety/`)**:
   - `restore_point.py`: Creates Windows System Restore Points via WMI/PowerShell.
   - `registry_backup.py`: Exports targeted registry subkeys to `.reg` files.
   - `snapshot.py`: Captures complete pre-optimization system state in `snapshot.json`.
   - `transaction.py` & `rollback_engine.py`: Atomic transaction ledger (`rollback.json`) and automated LIFO rollback engine.
5. **Licensing Subsystem (`winforge/licensing/`)**:
   - `fingerprint.py`: `FingerprintProvider` collects normalized, salted SHA-256 hashes of hardware signals (Motherboard, CPU, Disk, MAC) with dynamic similarity matching ($\ge 75\%$ threshold).
   - `verifier.py`: `LicenseVerifier` verifies RSA-2048 PKCS#1 v1.5 / RSA-PSS signatures offline using embedded `public_key.pem`.
   - `policy.py`: `LicensePolicyManager` enforces feature gating without blocking diagnostic scans.
6. **CLI Interface (`winforge/cli/`)**:
   - Built on `Rich` library. Renders interactive navigation menus, health dashboards, hardware summaries, and Technician Tweak Inspection Cards.

---

## Part Three: Execution Lifecycle

Every optimization command follows a strict non-bypassable 11-state lifecycle pipeline:

```
[CLI User Command: anasoptimizer --execute | --tech | --dry-run | --scan]
                               │
                               ▼
[1. DISCOVERED: Diagnostic Scan & Tweak DB Loaded]
                               │
                               ▼
[2. ANALYZED: Policy Engine Device & Windows OS Compatibility Check]
                               │
                               ▼
[3. RECOMMENDED: Safety Approval Pre-Flight Check]
  ├── Administrator Elevation Verified
  ├── Free Disk Space >= 2.0 GB
  └── Battery Charge >= 20%
                               │
                               ▼
[4. APPROVED: User Confirmation (Client Batch or Technician Inspection Card)]
                               │
                               ▼
[5. BACKUP_COMPLETED: 4-Layer Safety Lock]
  ├── System Restore Point Created
  ├── Targeted Registry Keys Exported to .reg
  ├── System Pre-State Snapshot Saved
  └── Transaction Ledger (rollback.json) Initialized
  └── IF ANY BACKUP FAILS -> EXECUTION ABORTED IMMEDIATELY
                               │
                               ▼
[6. EXECUTING: Category Optimizer & Win32 Handler Execution]
                               │
                               ▼
[7. VERIFIED: Post-Execution Verification Check]
  ├── If Verification Passes -> Transition to COMPLETED
  └── If Verification Fails -> AUTOMATIC ROLLBACK TRIGGERED
                               │
                               ▼
[8. ROLLED_BACK / 9. COMPLETED: Session Logged & Standalone HTML Report Generated]
```

### Detailed Lifecycle Stage Breakdown:
- **Discovered**: Scans hardware components and loads candidate tweaks from `config/tweaks/`.
- **Analyzed**: Policy Engine checks OS compatibility and device parameters (e.g. laptop vs desktop power plans).
- **Recommended**: Safety Approval Engine runs real-time pre-flight checks (elevation, disk space, battery level).
- **Approved**: User approves batch execution in Client Mode, or technician approves individual tweak via Technician Inspection Card (`--tech`).
- **Backup Completed**: 4-Layer Safety Lock writes system restore point, `.reg` export, JSON snapshot, and `rollback.json` ledger. If any backup fails, execution halts immediately with `CRITICAL_SAFETY_FAULT`.
- **Executing**: Dispatched to category optimizer (`GamingOptimizer`, `PowerOptimizer`, etc.) via low-level handlers (`RegistryHandler`, `ServiceHandler`).
- **Verified**: `TweakVerifier` checks post-execution registry/service state.
- **Rolled Back / Completed**: If verification fails, `RollbackEngine` executes automated LIFO rollback. If verified, transaction commits and exports standalone HTML diagnostic report.

---

## Part Four: Security & Safety Model

WinForge enforces multi-layered security controls:

1. **Mock Execution Guarantee (`mock_execution=True`)**:
   - Hardcoded default across all category optimizers and handlers. Zero registry keys are modified, zero services reconfigured, and zero files deleted unless `--execute` is explicitly passed alongside verified Administrator elevation.
2. **Forbidden Operations & Immutable Components**:
   - **Kernel Services**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `Dhcp`, `Dnscache`, `LsaSrv`, `WinDefend`, `wuauserv`) are hardcoded immutable. Any tweak attempting modification is immediately rejected.
   - **System Directories**: Cleaning `C:\Windows\System32`, `SysWOW64`, or `Drivers` is strictly prohibited.
   - **Startup Protection**: Antivirus, Defender, and display/audio drivers are filtered out from auto-start tuning.
3. **4-Layer Safety Lock & LIFO Rollback**:
   - Automatically initializes Windows System Restore Points, `.reg` exports, `snapshot.json`, and `rollback.json` transaction ledgers.
   - `RollbackEngine` performs automated LIFO (Last-In, First-Out) state reversal if post-execution state verification fails.
4. **Offline Cryptographic RSA-PSS Security**:
   - Signature Scheme: RSA-2048 with RSA-PSS padding and SHA-256.
   - Private signing keys (`private_key.pem`) and signing scripts (`tools/`) are strictly isolated outside the client binary and excluded from PyInstaller builds. The client binary contains ONLY the public key (`public_key.pem`).
5. **Salted SHA-256 Machine Fingerprinting**:
   - `FingerprintProvider` collects Motherboard UUID, CPU Processor ID, System Disk Serial, and Primary NIC MAC signals. Raw hardware strings are normalized and hashed using SHA-256 with a per-license salt. Plaintext hardware serials or MAC addresses are never stored or logged.
   - Matching Engine (`FingerprintMatcher`) evaluates dynamic similarity ($\ge 75\%$ threshold), tolerating minor hardware swaps (SSD swap, NIC replacement).

---

## Part Five: Commercial Product Model

WinForge implements non-blocking feature gating policies:

| Capability | Free Edition | Personal | Professional | Technician |
| :--- | :---: | :---: | :---: | :---: |
| **Diagnostic Scan & Health Scorecard** | ✓ | ✓ | ✓ | ✓ |
| **Quantitative Benchmarks & HTML Reports**| ✓ | ✓ | ✓ | ✓ |
| **Client Optimizations (Risk 0–20)** | ✗ | ✓ | ✓ | ✓ |
| **Moderate Optimizations (Risk 21–50)** | ✗ | ✓ | ✓ | ✓ |
| **Technician Mode (`--tech`)** | ✗ | ✗ | ✓ | ✓ |
| **Tweak Inspection Cards (Risk 51–100)**| ✗ | ✗ | ✗ | ✓ |
| **Deployment Model** | Local Scan | 1 PC | 5 PCs | Portable USB |

### Non-Blocking Diagnostic Scan Guarantee:
Unlicensed executions or invalid/expired license files fall back safely to `FREE_EDITION` mode. Core diagnostic scans, category health scores, hardware specifications, quantitative benchmarks, and standalone HTML report exports are **NEVER disabled or blocked**.
