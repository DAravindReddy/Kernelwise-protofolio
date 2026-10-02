# Project 01: SDLC Plan — Android Device Health Monitor

## 1. Project Metadata & Team Allocation
- **Project Lead:** Full-Stack / Data Engineer (Dashboard, Collector & Exporters)
- **Peer Reviewer:** Embedded / Linux Engineer (ADB shell commands, thermal sysfs validation)
- **Estimated Duration:** 2–3 Weeks (Sprint Model)
- **Target Deliverable:** Production-grade CLI & Web telemetry daemon, unit test suite, and live demo script.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Requirements & Feasibility (Days 1–3)
- **User Story 1.1:** As an Android fleet admin, I want continuous thermal monitoring so I can detect kiosk heat saturation.
- **User Story 1.2:** As an automated test engineer, I need JSON/CSV metric exports to correlate benchmark tests against regression runs.
- **Non-Functional Requirements:** Max collector footprint < 50MB RAM, zero third-party APK installations required on target device.

### Stage 2: Architecture & Interface Design (Days 4–6)
- Define standard metric schema (`DeviceMetrics`: timestamp, cpu_pct, ram_used_mb, ram_total_mb, battery_temp_c, thermal_zones, top_processes).
- Decouple hardware access via `ADBBridge` interface: supports both physical USB/TCP devices and high-fidelity synthetic emulator.
- Design alert threshold evaluation matrix (`WARNING`, `CRITICAL`, `NORMAL`).

### Stage 3: Implementation Sprints (Days 7–13)
- **Sprint 3A:** Core collector engine (`collector.py`), parsing regex for `dumpsys cpuinfo`, `meminfo`, and thermal sysfs paths.
- **Sprint 3B:** Alert rules engine (`alert_engine.py`) and metric recording buffer (`exporter.py`).
- **Sprint 3C:** Real-time web UI and live terminal dashboard (`dashboard.py`).

### Stage 4: Verification & QA Strategy (Days 14–16)
- **Unit Testing:** Pytest suite covering regex parsing across various Android versions (Android 10, 11, 12, 13, 14 mock dumps).
- **Stress Testing:** High-frequency polling (200ms intervals) for 2 hours to ensure zero memory creep in the collector daemon.
- **Hardware-in-the-Loop (HIL):** Verified against physical Android smartphone/board and headless Android emulator.

### Stage 5: Packaging & CI/CD (Days 17–18)
- Self-contained CLI executable / pip package.
- GitHub Actions workflow running automated linting (flake8), type checking (mypy), and pytest test suite.

### Stage 6: Client Handover & Video Presentation (Days 19–20)
- Record 2-minute video demo demonstrating simulated thermal throttle alert and real-time dashboard updates.
- Publish public README with copy-paste instructions and clear screenshot mockups.
