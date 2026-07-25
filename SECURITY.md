# Security Policy

## Reporting Security Issues

We take the safety and security of **WinForge** very seriously. As a Windows system diagnostic and optimization tool, WinForge operates with Administrator privileges and touches system settings.

If you discover a security vulnerability, crash condition, or unsafe edge case in WinForge, please report it directly via GitHub Security Advisories or by contacting the project maintainer:

**@0xdowz**  
Project Creator & Maintainer

Please **do not** open public issues for zero-day security vulnerabilities until they have been reviewed and resolved.

---

## Safety & Operating Guarantees

1. **Non-Destructive Defaults**: All internal Registry and Service modification handlers run in safe mock/simulation mode unless explicitly overridden with `--execute`.
2. **Immutable Protected Boundaries**: Critical Windows kernel services (`RpcSs`, `DcomLaunch`, `EventLog`, `PlugPlay`, `CryptSvc`, `Dhcp`, `Dnscache`, `LsaSrv`, `WinDefend`, `wuauserv`) and system directories (`C:\Windows\System32`, `SysWOW64`, `Drivers`) are strictly immutable.
3. **Automatic Pre-Flight Check**: Execution halts automatically if free disk space is $< 2.0\text{ GB}$, laptop battery is $< 20\%$, or Administrator privileges are missing.
4. **4-Layer Safety Lock**: Automatic WMI System Restore Point creation, targeted `.reg` backups, pre-state JSON snapshots, and atomic transaction ledgers precede any system mutation.

---

## Is WinForge Free? (Scam Warning)

**Yes. WinForge is 100% free and open source.**

- You should **NEVER** pay someone to download, activate, unlock, or use WinForge.
- If someone tries to sell you WinForge or claims to offer a "paid/premium edition", you are likely being scammed.
- Official binaries are published **exclusively** through the official GitHub releases page.
