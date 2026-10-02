# Project 03: SDLC Plan — Embedded Firmware CI/CD Automation

## 1. Project Metadata & Team Allocation
- **Project Lead:** Cloud / DevOps Engineer (Docker containers, CI/CD pipeline-as-code)
- **Peer Reviewer:** Embedded / Linux Engineer (C firmware code, compiler flags, QEMU emulator)
- **Estimated Duration:** 2 Weeks (Fast-Track Delivery)
- **Target Deliverable:** Fully automated GitHub Actions & GitLab CI pipeline, Dockerized toolchain, sample C firmware with Unity tests, and benchmark report.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Pipeline Requirements & Audit (Days 1–2)
- Define target toolchains: `arm-none-eabi-gcc` 12.3+, CMake 3.25+, Ninja, Cppcheck 2.10+.
- Target microcontroller: ARM Cortex-M4 (STM32F4 series).
- Quality gates: 0 static analysis warnings, 100% unit test pass rate, code coverage > 85%.

### Stage 2: Architecture & Pipeline Design (Days 3–4)
- Design multi-stage CI pipeline:
  - **Stage 1 (Lint & Static Analysis):** Cppcheck + Clang-Format verification.
  - **Stage 2 (Unit Testing):** Native compilation and execution of Unity tests.
  - **Stage 3 (ARM Cross-Compilation):** Cross-compiling `.elf`, `.bin`, and `.hex` binaries.
  - **Stage 4 (Emulation Verification):** Running binary in QEMU ARM Cortex-M target.
  - **Stage 5 (Artifact Publishing):** Uploading signed release binaries with SHA256 checksums.

### Stage 3: Docker & Firmware Implementation (Days 5–8)
- Build reproducible `Dockerfile.embedded` with stripped footprint (< 600MB).
- Write robust, MISRA-compliant C firmware modules:
  - `ring_buffer.c`: Thread-safe, lockless circular buffer for UART/DMA.
  - `sensor_packet.c`: Packet framing with CRC16-CCITT integrity verification.
- Write unit tests using Unity test framework (`test_firmware.c`).

### Stage 4: QA, Verification & Benchmarking (Days 9–11)
- Execute local pipeline runner (`scripts/run_pipeline_local.py`) to benchmark execution times.
- Inject intentional defects (buffer boundary breach, invalid CRC) to verify that pipeline fails reliably.

### Stage 5: CI Integration (Days 12–13)
- Author `.github/workflows/firmware_ci.yml` and `.gitlab-ci.yml`.
- Verify GitHub Actions execution on push and pull requests.

### Stage 6: Client Handover & Metrics Report (Day 14)
- Generate `BENCHMARK_REPORT.md` with quantifiable before/after performance numbers.
- Deliver README and video walkthrough for engineering management.
