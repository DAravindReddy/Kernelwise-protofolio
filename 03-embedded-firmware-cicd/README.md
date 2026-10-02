# Kernelwise Labs — Embedded Firmware CI/CD & QEMU Automation Pipeline

[![Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20GitLab-blue)]()
[![Target](https://img.shields.io/badge/Target-ARM%20Cortex--M4-red)]()
[![Container](https://img.shields.io/badge/Toolchain-Dockerized%20GCC-brightgreen)]()
[![Test](https://img.shields.io/badge/Unit%20Tests-Unity%20%2F%20C99-orange)]()

Automated pipeline-as-code delivering containerized cross-compilation, static code analysis, unit testing, and virtualized QEMU smoke tests for embedded C firmware.

---

## 1. Executive Summary & Capabilities
Manual firmware flashing and release verification creates agonizing delays and allows regressions to brick client devices in the field.

This repository provides an enterprise-grade CI/CD pipeline tailored specifically for embedded microcontroller firmware:
- **Dockerized Immutable Toolchain (`docker/Dockerfile.embedded`):** Bundles CMake, Ninja, `arm-none-eabi-gcc`, Cppcheck, and QEMU into a deterministic build image.
- **Pre-Commit Static Analysis:** Enforces MISRA-C and Cppcheck zero-defect thresholds.
- **Native Unit Testing (Unity/C99):** Tests circular ring buffer logic and CRC16-CCITT packet framing.
- **QEMU ARM Emulation Smoke Test:** Boots the cross-compiled binary in a virtualized Cortex-M target to verify boot stability before publishing.
- **Artifact Traceability:** Generates SHA256 cryptographic manifests for every build.

---

## 2. Directory Structure
```
03-embedded-firmware-cicd/
├── .github/workflows/firmware_ci.yml   # GitHub Actions pipeline
├── .gitlab-ci.yml                      # GitLab CI pipeline
├── ABSTRACT.md                         # Business case & problem solved
├── ARCHITECTURE.md                     # Pipeline stage gates & diagram
├── SDLC_PLAN.md                        # 2-week fast-track SDLC plan
├── BENCHMARK_REPORT.md                 # 93% build time reduction report
├── docker/
│   └── Dockerfile.embedded             # Containerized toolchain spec
├── src/
│   ├── ring_buffer.h / .c              # Lockless circular buffer
│   └── sensor_packet.h / .c            # CRC16 packet serializer
├── tests/
│   ├── test_firmware.c                 # Unity C unit test suite
│   └── test_pipeline_unit.py           # Pipeline configuration tests
├── scripts/
│   └── run_pipeline_local.py           # Local 5-stage pipeline runner
└── CMakeLists.txt                      # Multi-target build definition
```

---

## 3. Quickstart & Local Pipeline Execution

### Run the Complete 5-Stage CI Pipeline Locally
```bash
python scripts/run_pipeline_local.py
```

### Run Pipeline Configuration Unit Tests
```bash
python -m unittest tests/test_pipeline_unit.py
```
