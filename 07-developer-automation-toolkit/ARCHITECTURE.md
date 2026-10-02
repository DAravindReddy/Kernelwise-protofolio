# Project 07: Architecture Specification — Developer Automation Toolkit

## 1. CLI Dispatcher Architecture

```mermaid
flowchart TD
    CLI[kw-tools CLI Dispatcher] --> SUB1[env-doctor: Workstation Audit]
    CLI --> SUB2[log-triage: Crash & Panic Scanner]
    CLI --> SUB3[release-notes: SemVer Changelog Generator]
    CLI --> SUB4[trace-analyzer: Performance Bottleneck Profiler]

    SUB1 --> RES1[Diagnostic Table & Path Status]
    SUB2 --> RES2[Fatal Error Summary & Line Numbers]
    SUB3 --> RES3[Markdown Release Notes & Tag Proposal]
    SUB4 --> RES4[Top 5 Slowest Execution Bottlenecks]
```

---

## 2. Command Interfaces

- `kw-tools env-doctor`: Checks installation status and versions of Git, Python, ADB, GCC, Docker, and QEMU.
- `kw-tools log-triage [--file <path>]`: Analyzes logs from file or pipe, filtering out noise and presenting high-priority failures.
- `kw-tools release-notes [--since <tag>]`: Summarizes git history into categorized `Features`, `Bug Fixes`, and `Documentation`.
- `kw-tools trace-analyzer [--file <path>]`: Computes P50, P95, and maximum execution duration of traced events.
