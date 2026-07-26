# Security Policy

## Supported Versions

| Version | Supported |
| :--- | :---: |
| 1.0.x (latest) | ✅ Yes |
| < 1.0.0 | ❌ No |

---

## Reporting Security Issues

We take the safety and security of **WinForge** seriously. As a Windows system diagnostic and optimization tool that operates with Administrator privileges and touches system settings, any security vulnerability must be handled responsibly.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, use one of these private channels:

1. **GitHub Security Advisories** (preferred):  
   [https://github.com/0xdowz/winforge/security/advisories/new](https://github.com/0xdowz/winforge/security/advisories/new)

2. **Direct contact**:  
   Reach the maintainer [@0xdowz](https://github.com/0xdowz) via GitHub.

---

## Responsible Disclosure Timeline

| Stage | Target Response Time |
| :--- | :--- |
| Initial acknowledgement | Within **72 hours** of report |
| Triage and severity assessment | Within **7 days** |
| Patch or mitigation available | Within **30 days** (critical), **90 days** (moderate) |
| Public disclosure | After patch is released, coordinated with reporter |

We follow a **90-day coordinated disclosure window**. If a fix cannot be delivered within 90 days, we will coordinate with the reporter on an extended timeline or interim mitigation advice.

---

## Scope — What to Report

**In Scope:**
- Privilege escalation vulnerabilities in the execution pipeline
- Unsafe `subprocess` calls that could allow command injection
- Path traversal vulnerabilities in session or report file operations
- Registry operations that could affect paths outside defined scope
- Bypassing the 4-layer safety lock or rollback integrity checks
- Sensitive data leakage (credentials, tokens, local paths) in logs or reports

**Out of Scope:**
- Issues in third-party dependencies (report those upstream)
- Social engineering or physical access attacks
- Theoretical vulnerabilities without proof-of-concept
- Issues only reproducible on end-of-life Windows versions (< Windows 10 2004)

---

## Safety & Operating Guarantees

1. **Non-Destructive Defaults**: All internal Registry and Service modification handlers run in safe mock/simulation mode unless explicitly overridden with `--execute`.
2. **Immutable Protected Boundaries**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `Dhcp`, `Dnscache`, `LsaSrv`, `WinDefend`, `wuauserv`) and system directories (`C:\Windows\System32`, `SysWOW64`, `Drivers`) are strictly immutable.
3. **Automatic Pre-Flight Check**: Execution halts automatically if free disk space is < 2.0 GB, laptop battery is < 20%, or Administrator privileges are missing.
4. **4-Layer Safety Lock**: Automatic WMI System Restore Point creation, targeted `.reg` backups, pre-state JSON snapshots, and atomic transaction ledgers precede any system mutation.
5. **No Telemetry**: WinForge contains no telemetry daemons, tracking scripts, analytics hooks, or cloud communication of any kind.

---

## Is WinForge Free? (Scam Warning)

**Yes. WinForge is 100% free and open source (MIT License).**

- You should **NEVER** pay someone to download, activate, unlock, or use WinForge.
- If someone tries to sell you WinForge or claims to offer a "paid/premium edition", you are likely being scammed.
- Official binaries are published **exclusively** through the [official GitHub releases page](https://github.com/0xdowz/winforge/releases).
