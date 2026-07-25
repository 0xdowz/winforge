# WinForge: Phase 5 Execution Plan & Production Transition Strategy

## 1. Executive Summary & Goal

Phase 5 transitions **WinForge** from mock execution to production Windows optimization execution while maintaining **100% safety, transparency, and reversibility**.

Every real tweak applied to a customer PC will pass through the established 7-stage pipeline:
`Tweak Database` $\rightarrow$ `Policy Engine` $\rightarrow$ `Safety Approval Engine` $\rightarrow$ `Backup Subsystem` $\rightarrow$ `Execution Engine` $\rightarrow$ `Verification Engine` $\rightarrow$ `Transaction Ledger`.

---

## 2. Risk Scoring Architecture (0 - 100)

To provide granular safety controls between Client Mode and Technician Mode, every tweak is assigned a numeric **Risk Score (0-100)**:

| Risk Score Range | Classification | Target Mode | Execution Policy |
| :--- | :--- | :--- | :--- |
| **0 - 20** | **Safe** | Client & Technician | Automatic 1-click batch execution permitted. |
| **21 - 50** | **Moderate** | Client & Technician | Explicit user confirmation prompt required. |
| **51 - 80** | **Advanced** | Technician Only | Available only in Technician Mode (`--tech`). |
| **81 - 100** | **Technician Only** | Technician Only | Strict manual inspection card + individual approval required. |

---

## 3. Transition Strategy: From Mock to Production Execution

1. **Dual Execution Mode Preserved**:
   - The execution engine retains the `mock_execution: bool = False` flag.
   - Running with `--dry-run` or in test environments forces `mock_execution=True`.
   - Production execution mode sets `mock_execution=False` only after all backup pre-requisites are verified.
2. **Strict Handlers with Atomic Rollback Registration**:
   - All real system modifications are abstracted into low-level handlers (`registry_handler.py`, `service_handler.py`).
   - Every handler captures the exact pre-modification state from the live Windows Registry/WMI before applying changes and registers the inverse state into `TransactionManager`.

---

## 4. Planned Files Created & Modified

### New Files to Create

1. `winforge/optimizations/registry_handler.py`
   - Safe Win32 Registry reader/writer using `winreg`. Captures pre-value, writes new value, verifies write, and registers rollback data.
2. `winforge/optimizations/service_handler.py`
   - Safe Windows Service manager using `win32service` / `sc.exe`. Captures pre-start-type, applies change, verifies status.
3. Category Optimizer Modules (`winforge/optimizations/`):
   - `gaming.py`: GPU priority, system responsiveness, GameBar DVR tweaks.
   - `power.py`: Power plan GUID switching, PCIe link state, USB selective suspend.
   - `startup.py`: Telemetry startup items, Cortana deactivation, MapsBroker tuning.
   - `services.py`: DiagTrack, SysMain, RetailDemo service tuning.
   - `cleanup.py`: Windows Temp, User Temp, WER dump file purge.
   - `network.py`: Network throttling index tuning (Technician Only).
4. `build.py`
   - PyInstaller build script for compiling `ANASOptimizer.exe`.

### Existing Files to Modify

1. `winforge/models/tweak.py`: Add `risk_score: int` (0-100) and `RiskTier` enum.
2. `config/tweaks/*.json`: Update all Tier 1 tweak schemas with numeric risk scores and verification criteria.
3. `winforge/optimizations/verifier.py`: Extend to perform live Windows registry queries, service status checks, and power plan GUID checks.
4. `winforge/optimizations/executor.py`: Connect real category optimizer modules to the state machine pipeline.
5. `winforge/cli/interface.py`: Connect interactive optimization options for Client and Technician modes.

---

## 5. Implementation Order

```
[Step 1: Extend Tweak Schema & Update config/tweaks/*.json with Risk Scores (0-100)]
                                  │
                                  ▼
[Step 2: Implement Low-Level Handlers (registry_handler.py & service_handler.py)]
                                  │
                                  ▼
[Step 3: Implement Tier 1 Safe Category Optimizers (gaming, power, startup, services, cleanup, network)]
                                  │
                                  ▼
[Step 4: Upgrade TweakVerifier for Live Windows Inspection]
                                  │
                                  ▼
[Step 5: Wire Real Execution Pipeline in OptimizationExecutor]
                                  │
                                  ▼
[Step 6: Connect Rich CLI Menus & Technician Inspection Displays]
                                  │
                                  ▼
[Step 7: Automated Unit Testing & Rollback Verification Tests]
                                  │
                                  ▼
[Step 8: Standalone PyInstaller Executable Packaging (build.py)]
```

---

## 6. Testing Strategy

1. **Mock Test Suite Validation**:
   - Run existing PyTest test suite (25 tests) to ensure zero regressions in mock mode.
2. **Isolated Real Registry Key Tests**:
   - Execute live registry write/verify/rollback tests against an isolated non-critical key (`HKCU\Software\ANASOptimizerTest`).
3. **Rollback Reversion Validation**:
   - Verify that modifying a test value and calling `RollbackEngine.rollback_session()` restores the exact original value 100% of the time.
4. **Clean Machine Portable EXE Validation**:
   - Build `ANASOptimizer.exe` and test execution on a clean Windows virtual machine without Python installed.

---

## 7. Safety & Rollback Guarantees

- **No Execution Without Backup**: If System Restore Point creation or Registry `.reg` export fails, execution stops immediately. Zero changes are made.
- **State-Aware Restoration**: Rollback reads captured pre-execution state data from `snapshot.json` and `rollback.json` to restore previous configuration exactly.
- **Explicit Forbidden List**: Defender, Windows Update, System32 binaries, and critical kernel services remain 100% immutable.

---

Awaiting your architectural approval of `PHASE5_EXECUTION_PLAN.md` before commencing implementation.
