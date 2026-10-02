# Kernelwise Labs — Reusable Developer Automation Toolkit (`kw-tools`)

[![CLI](https://img.shields.io/badge/CLI-kw--tools-blue)]()
[![Type](https://img.shields.io/badge/Toolkit-Open%20Source-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

An extensible command-line toolkit automating repetitive engineering workflows: developer environment auditing, automated crash triage, SemVer release note generation, and execution trace profiling.

---

## 1. Executive Summary & Capabilities
Developer friction costs engineering organizations tens of thousands of hours in unproductive triage and toolchain debugging.

`kw-tools` packages Kernelwise Labs' internal automation arsenal into an accessible CLI:
- **`env-doctor`:** Audits local workstations for required compilers (`arm-none-eabi-gcc`), Docker, ADB, Python, and QEMU.
- **`log-triage`:** Rapidly categorizes kernel panics, Android ANRs, OOM kills, and hardware bus timeouts.
- **`release-notes`:** Parses Conventional Commits and automatically proposes SemVer version bumps (`PATCH`, `MINOR`, `MAJOR`) with formatted Markdown changelogs.
- **`trace-analyzer`:** Identifies execution bottlenecks in firmware and backend traces.

---

## 2. Directory Structure
```
07-developer-automation-toolkit/
├── ABSTRACT.md             # Open-source positioning & inbound lead value
├── ARCHITECTURE.md         # Subcommand dispatcher architecture
├── SDLC_PLAN.md            # Ongoing maintenance & contribution plan
├── kw_tools/
│   ├── cli.py              # CLI entrypoint
│   ├── env_doctor.py       # Developer environment audit
│   ├── log_triage.py       # Crash & panic log analyzer
│   ├── release_notes.py    # SemVer changelog generator
│   └── trace_analyzer.py   # Execution trace profiler
├── tests/
│   └── test_toolkit.py     # Unit test suite
├── setup.py                # Pip package installer
└── README.md
```

---

## 3. Quickstart & Usage

### 1. Run Workstation Environment Doctor
```bash
python -m kw_tools.cli env-doctor
```

### 2. Triage Crash Logs
```bash
python -m kw_tools.cli log-triage
```

### 3. Generate Release Notes from Git History
```bash
python -m kw_tools.cli release-notes --current v1.2.0
```

### 4. Run Unit Test Suite
```bash
python -m unittest discover tests
```
