# Project 03: Architecture Specification — Embedded CI/CD Pipeline

## 1. End-to-End Pipeline Workflow

```mermaid
flowchart TD
    subgraph Developer Environment
        DEV[Developer git push] --> GITHUB[GitHub / GitLab Repo]
    end

    subgraph CI Runner Container: Dockerized ARM Toolchain
        GITHUB --> S1[Stage 1: Static Analysis & MISRA-C]
        S1 -->|Cppcheck Pass| S2[Stage 2: Native Unit Testing]
        S2 -->|Unity Tests 100% Pass| S3[Stage 3: ARM Cross-Compilation]
        S3 -->|GCC Cortex-M4 Pass| S4[Stage 4: Virtual QEMU Emulation]
        S4 -->|QEMU Smoke Test Pass| S5[Stage 5: Artifact Packaging]
    end

    subgraph Release Output
        S5 --> ART1[firmware-v1.0.bin]
        S5 --> ART2[firmware-v1.0.elf]
        S5 --> ART3[checksums.sha256]
        S5 --> ART4[test-report.xml]
    end
```

---

## 2. Pipeline Stage Gates & Quality Criteria

| Stage | Tooling | Quality Gate / Exit Condition | Action on Failure |
|---|---|---|---|
| **1. Static Analysis** | Cppcheck 2.10+ | Zero errors, warnings, or style violations | Pipeline halts; prints filename & line number |
| **2. Native Unit Tests** | GCC (Host) + Unity Test | 100% assertions passed; zero memory leaks | Pipeline halts; outputs JUnit test XML |
| **3. Cross-Compilation** | `arm-none-eabi-gcc` 12.3+ | Zero compiler warnings with `-Wall -Wextra -Werror` | Pipeline halts; outputs build diagnostics |
| **4. QEMU Emulation** | `qemu-system-arm` | System boots and emits heartbeat pulse within 5 seconds | Pipeline halts; dumps serial log |
| **5. Artifact Packaging** | Python / SHA256 | Valid `.bin`, `.hex`, `.elf` and generated checksums | Halts release creation |
