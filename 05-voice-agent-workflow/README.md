# Kernelwise Labs — Low-Latency Voice Agent Workflow Engine

[![Voice AI](https://img.shields.io/badge/AI-Voice%20Agent-purple)]()
[![Latency](https://img.shields.io/badge/Latency-Sub--500ms-brightgreen)]()
[![Tools](https://img.shields.io/badge/Tools-Hardware%20Diagnostics%20%7C%20RMA-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

An ultra-responsive voice assistant engineered for smart device support, remote hardware telemetry queries, and automated RMA service appointment booking.

---

## 1. Executive Summary & Capabilities
Traditional voice bots suffer from 3-to-5 second latency gaps that ruin user experiences and cause callers to talk over the agent.

This repository demonstrates Kernelwise Labs' sub-second streaming voice workflow:
- **Low-Latency Streaming Pipeline (`src/voice_pipeline.py`):** Coordinated STT, LLM decision, and streaming TTS delivering total round-trip response times < 500ms.
- **Hardware Diagnostic & RMA Tools (`src/device_tools.py`):** Real-time database lookup for warranty coverage, live device telemetry queries, and automated calendar ticket booking.
- **Microsecond Latency Profiler (`src/latency_profiler.py`):** Continuous instrumentation calculating P50, P95, and P99 latency percentiles across every conversational turn.

---

## 2. Directory Structure
```
05-voice-agent-workflow/
├── ABSTRACT.md                 # Executive problem statement & customer ROI
├── ARCHITECTURE.md             # Streaming pipeline block diagram
├── SDLC_PLAN.md                # 2–3 week sprint engineering plan
├── LATENCY_BENCHMARK_REPORT.md # Sub-500ms P50 latency benchmark metrics
├── src/
│   ├── device_tools.py         # Hardware diagnostic & RMA booking tools
│   ├── latency_profiler.py     # Microsecond latency profiler
│   └── voice_pipeline.py       # Full conversational streaming engine
├── tests/
│   └── test_voice_agent.py     # Unit test suite
└── main.py                     # Interactive CLI & benchmark simulator
```

---

## 3. Quickstart & Execution

### Run Automated Latency Benchmark & Conversational Simulation
```bash
python main.py
```

### Run Interactive Text/Voice Dialogue
```bash
python main.py --interactive
```

### Run Unit Test Suite
```bash
python -m unittest discover tests
```
