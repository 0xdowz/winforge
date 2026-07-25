# WinForge: Security Model & Safety Boundaries

## 1. Executive Summary & Safety Philosophy

WinForge is a commercial-grade Windows System Optimization CLI designed specifically for IT technicians and system administrators. Unlike standard consumer "debloat" scripts or aggressive registry tweaks, WinForge prioritizes **safety, transparency, predictability, and complete reversibility**.

Every optimization action executed by WinForge must strictly satisfy the **Non-Destructive Operating Principles**:
- **Transparency**: Every change recommended by the software must be explicitly detailed to the technician before execution.
- **Explicit Consent**: Zero silent modifications. Every tweak requires confirmation (or explicit batch approval in Technician Mode).
- **Mandatory Safety Pre-requisites**: No system setting is mutated without first creating a System Restore Point, exporting affected Registry keys, and writing a pre-modification state snapshot to disk.
- **Guaranteed Reversibility**: Every tweak in the system must possess a verified, tested inverse (rollback) method recorded in an atomic transaction log (`logs/rollback.json`).

---

## 2. Admin Privileges & Elevation Boundaries

- **Elevation Requirement**: WinForge requires Windows Administrator privileges to inspect and optimize system services, power schemes, network adapters, and system registry hives.
- **Privilege Enforcement**: At startup, `winforge/core/privileges.py` verifies elevation via `ctypes.windll.shell32.IsUserAnAdmin()`. If not elevated, execution halts gracefully with clear instructions on launching an elevated PowerShell or Command Prompt.
- **Non-Escalation Guarantee**: WinForge does not install persistent background services, kernel drivers, or background daemons. It operates exclusively while running as an interactive CLI application.

---

## 3. Explicitly Forbidden Operations (Strict Non-Negotiable Boundaries)

WinForge strictly prohibits the following operations under any circumstances:

1. **NEVER Disable Windows Defender or Antivirus**:
   - `WinDefend`, `WdNisSvc`, `Sense`, or associated security services will never be disabled, delayed, or tampered with.
2. **NEVER Permanently Disable Windows Security Updates**:
   - `wuauserv` (Windows Update) will never be permanently disabled or removed. (Safe deferral of feature updates or setting active hours via official policy is acceptable only if configured by technician).
3. **NEVER Delete Operating System Binaries or System Files**:
   - Deletion is strictly confined to temporary directories (`%TEMP%`, `C:\Windows\Temp`, Prefetch, user browser caches). Critical system files, DLLs, WinSxS stores, or system drivers will never be modified or deleted.
4. **NEVER Remove or Stop Critical Kernel/OS Services**:
   - Core operating system services (RPC, DCOM, EventLog, PlugPlay, CryptSvc, Dhcp, Dnscache, LsaSrv) are marked immutable in the Policy Engine and cannot be stopped or disabled.
5. **NEVER Modify Active Directory or Domain Security Policies**:
   - When running on domain-joined machines, tweaks affecting domain security, Kerberos, group policies, or network authentication are automatically filtered and blocked by the Policy Engine.

---

## 4. Policy Engine & Context-Aware Safety Constraints

The **Policy Engine** (`winforge/core/policy.py`) evaluates device context before allowing any tweak to be recommended or applied:

| Device Profile | Restricted Operations | Rationale |
| :--- | :--- | :--- |
| **Laptop / Mobile Device** | Aggressive High Performance Power Plans, Disabling Battery Saver | Prevents severe battery drain and thermal throttling. |
| **Server OS (Win Server)** | Desktop gaming optimizations, Timer resolution tweaks, Service delays | Preserves server workload stability. |
| **Domain-Joined Client** | Network DNS overrides, Telemetry policies governed by GPO | Prevents breaking enterprise network policies. |
| **Low Battery (< 20%)** | Heavy disk cleanup, Restore Point creation, System benchmarks | Prevents sudden power loss during system backup/optimization. |

---

## 5. Pre-Modification Safety Protocol & Rollback Guarantee

Before applying any single optimization or batch suite, WinForge executes a 3-step safety lock:

```
[User Confirmation]
       │
       ▼
1. Create Windows System Restore Point (via WMI/VSS)
       │
       ▼
2. Export Registry Subkeys to `.reg` files (via `reg export`)
       │
       ▼
3. Record Pre-Optimization State Snapshot to `logs/snapshot_<timestamp>.json`
       │
       ▼
[Apply Optimization Steps]
       │
       ▼
4. Record Transaction & Inverse Action to `logs/rollback.json`
```

### Rollback Engine Mechanics
- If an optimization causes unexpected system behavior, the technician can trigger Option 8 (`System Rollback & Restoration`) or run `--rollback`.
- The Rollback Engine parses `logs/rollback.json` in reverse chronological order and applies the inverse methods (e.g. restoring previous registry values, re-enabling service startup types, re-importing `.reg` backups).
- If individual tweak reversal is insufficient, the system provides 1-click restoration to the pre-optimization Windows System Restore Point.

---

## 6. Dry-Run Engine & Simulation Guarantee

- The `--dry-run` flag allows technicians to perform a full system scan and optimization run without making **any** changes to the system.
- In Dry-Run mode:
  - Detection logic executes normally.
  - All recommended tweaks are displayed with expected impact.
  - Registry modifications, service state transitions, and disk cleanup actions are calculated and printed as a detailed simulation log.
  - Zero state mutations occur on disk or registry.

---

## 7. Audit Logging & Transparency

All actions, diagnostic outputs, policy decisions, and errors are logged to:
- `logs/optimization.log`: Human-readable detailed event and debug log with timestamps.
- `logs/system_report.json`: Machine-readable diagnostic snapshot of system health, hardware specs, and category health scores.
- `logs/rollback.json`: Atomic transaction ledger of all applied tweaks and inverse rollback parameters.
