# WinForge Optimization & Tweak Schema System

This document specifies the declarative JSON schema format, human-friendly explanation model, and risk scoring matrix used by WinForge v1.0.8.

---

## 1. Tweak Recipe JSON Schema Format

All tweaks are defined as declarative JSON objects stored under `config/tweaks/`. Every recipe is deserialized into the `Tweak` domain model ([winforge/models/tweak.py](file:///c:/Users/Admin/Desktop/Twek/winforge/models/tweak.py)).

### Complete JSON Recipe Example
```json
{
  "id": "TWEAK_GAME_001",
  "name": "GPU Scheduling Priority Optimization",
  "friendly_name": "Optimize GPU Priority for Games",
  "description": "Sets GPU scheduling priority to 8 (High) in the Multimedia SystemProfile.",
  "what_it_does": "Sets GPU scheduling priority to 8 (High) in the Windows Multimedia SystemProfile.",
  "why_it_exists": "Ensures foreground games get prioritized access to GPU resources over background tasks.",
  "exact_system_changes": "Registry DWORD: HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\\GPU Priority = 8",
  "rationale": "Configures Windows Multimedia Task Scheduler GPU Priority to maximum for active games.",
  "category": "GAMING",
  "risk_level": "LOW",
  "risk_score": 15,
  "risk_category": "SAFE",
  "schema_version": "2.0.0",
  "requires_admin": true,
  "requires_reboot": false,
  "performance_gain_estimate": "Medium",
  "user_visible_change": "Higher FPS & Smooth Frame Pacing",
  "technician_only": false,
  "detection_logic": {
    "type": "REGISTRY_DWORD",
    "key": "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games",
    "value_name": "GPU Priority",
    "expected_value": 8
  },
  "apply_method": {
    "type": "REGISTRY_DWORD",
    "key": "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games",
    "value_name": "GPU Priority",
    "value_data": 8
  },
  "rollback_method": {
    "type": "REGISTRY_DWORD",
    "key": "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games",
    "value_name": "GPU Priority",
    "value_data": 2
  }
}
```

---

## 2. Risk Score & Capability Tier Matrix

```
       0 ────────────── 20 ────────────────── 50 ────────────────── 100
Risk:  │   BEGINNER MODE   │    ADVANCED MODE    │  TECHNICIAN MODE   │
       └───────────────────┴─────────────────────┴────────────────────┘
```

| Profile Mode | Max Risk Score | Target User | Safety Profile |
| :--- | :---: | :--- | :--- |
| **Beginner Mode** | `20` | Non-technical home users | 100% safe, universally reversible, zero OS risk |
| **Advanced Mode** | `50` | Power users & gamers | Safe for modern hardware; modifies USB/PCIe power states & telemetry services |
| **Technician Mode** | `100` | IT System Administrators | Requires explicit `--tech` flag; modifies low-level graphics preemption & kernel policies |
