# Kernelwise Labs — AI Root-Cause Diagnostic Agent

[![AI Agent](https://img.shields.io/badge/Agent-RAG%20Reasoning-purple)]()
[![Accuracy](https://img.shields.io/badge/Accuracy-95.0%25%20Top--1-brightgreen)]()
[![Latency](https://img.shields.io/badge/Latency-%3C50ms-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

An intelligent diagnostic agent that parses raw device telemetry, system logs, and kernel stack traces to deliver automated root-cause isolation and step-by-step remediation runbooks.

---

## 1. Executive Summary & Capabilities
When edge devices and Linux systems crash in the field, support teams drown in cryptic logs (`dmesg`, `logcat`, `syslog`).

This repository combines deep systems debugging domain expertise with a high-speed RAG engine:
- **Multi-Format Log Parser (`src/log_parser.py`):** Automatically structures timestamped logs, isolates stack traces, and extracts anomalous signatures.
- **Embedded Failure Knowledge Base (`knowledge_base/failure_patterns.json`):** Curated database of kernel panics, I2C/SPI bus locks, Android LMK crashes, and thermal emergencies.
- **Semantic RAG Engine (`src/rag_engine.py`):** Zero-dependency TF-IDF and Cosine similarity vector search matching new incidents to historical post-mortems in < 50ms.
- **Actionable Remediation Generator (`src/diagnostic_agent.py`):** Outputs concrete shell commands, register fixes, and hardware checks rather than generic advice.

---

## 2. Directory Structure
```
04-ai-rootcause-agent/
├── ABSTRACT.md                 # Executive problem statement & customer ROI
├── ARCHITECTURE.md             # RAG block diagram & schema contracts
├── SDLC_PLAN.md                # 3-week sprint SDLC engineering plan
├── BENCHMARK_ACCURACY_REPORT.md# 95% accuracy benchmark documentation
├── knowledge_base/
│   └── failure_patterns.json   # Systems fault knowledge base
├── src/
│   ├── log_parser.py           # Multi-format log parser
│   ├── rag_engine.py           # Vector retrieval engine
│   ├── diagnostic_agent.py     # Diagnostic reasoning engine
│   └── benchmark_runner.py     # Automated benchmark suite
├── tests/
│   └── test_agent.py           # Pytest unit tests
└── main.py                     # CLI entrypoint
```

---

## 3. Quickstart & Execution

### Run Sample Incident Diagnosis
```bash
python main.py
```

### Diagnose a Specific Log File or Stdin Pipe
```bash
python main.py --file /path/to/dmesg.log
# Or via pipeline:
cat crash.log | python main.py
```

### Run Automated Accuracy Benchmark (20 Test Cases)
```bash
python main.py --benchmark
```

### Run Unit Test Suite
```bash
python -m unittest discover tests
```
