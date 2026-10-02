# Project 04: SDLC Plan — AI Root-Cause Diagnostic Agent

## 1. Project Metadata & Team Allocation
- **Project Lead:** AI / Automation Engineer (RAG vector indexer, diagnostic reasoning engine)
- **Peer Reviewer:** Cloud / DevOps Engineer (Log ingestion pipeline, benchmark framework)
- **Estimated Duration:** 3–4 Weeks (Sprint Model)
- **Target Deliverable:** CLI & REST diagnostic agent, failure knowledge base, benchmark evaluator, and accuracy report.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Problem Definition & Knowledge Base Curation (Days 1–4)
- Curate 20+ canonical failure patterns from real-world embedded systems:
  - Linux Kernel Panics (Null pointer dereference, DMA unaligned access, RCU stalls).
  - Memory Failures (Android Low Memory Killer, OOM killer invocations, slab fragmentation).
  - Bus & Peripheral Hangs (I2C timeout, SPI transfer lockup, PCIe link training errors).
  - System Services (Android Binder transaction buffer overflow, systemd service watchdogs).
- Define diagnostic output schema (`DiagnosticReport`: root_cause, confidence, affected_subsystem, evidence_lines, remediation_steps).

### Stage 2: Architecture & Vector Retrieval Design (Days 5–8)
- Implement modular RAG engine:
  - Tokenization, stop-word removal, and domain-specific n-gram vectorizer.
  - Cosine similarity vector search over indexed historical failure signatures.
  - Self-contained implementation (zero cloud API dependencies required for base tier, optional OpenAI/Gemini adapter).

### Stage 3: Diagnostic Reasoning & Parsing Engine (Days 9–15)
- Implement `log_parser.py`: Robust regex extraction of timestamps, log levels, process names, and call stack backtraces.
- Implement `diagnostic_agent.py`: Multi-factor reasoning combining vector similarity, keyword heuristics, and confidence calibration.

### Stage 4: Benchmarking & Accuracy Evaluation (Days 16–19)
- Build automated evaluator (`benchmark_runner.py`).
- Run 20 real-world ground-truth failure scenarios to measure accuracy, precision, and latency.
- Generate `BENCHMARK_ACCURACY_REPORT.md`.

### Stage 5: Packaging & API Server (Days 20–22)
- CLI entrypoint (`main.py`) supporting direct stdin pipe (`dmesg | python main.py`) or file analysis.
- Unit testing with pytest covering edge cases (corrupted logs, empty logs, multi-stack dumps).

### Stage 6: Client Demonstration & Case Study (Days 23–24)
- Record 2-minute video diagnosing a live simulated kernel panic and generating remediation commands in real time.
