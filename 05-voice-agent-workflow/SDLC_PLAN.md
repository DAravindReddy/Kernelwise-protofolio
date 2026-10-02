# Project 05: SDLC Plan — Low-Latency Voice Agent Workflow

## 1. Project Metadata & Team Allocation
- **Project Lead:** AI / Automation Engineer (Voice dialog manager, streaming pipeline)
- **Peer Reviewer:** Full-Stack / Data Engineer (Tool execution, REST API, CRM integration)
- **Estimated Duration:** 2–3 Weeks (Sprint Model)
- **Target Deliverable:** Real-time voice agent CLI simulator, tool calling engine, latency profiler, and benchmark report.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Conversational Scope & Tool Contracts (Days 1–3)
- Define target conversation flows:
  - Technical support triage (gathering serial number, symptoms).
  - Live remote device health query (checking temperature and error codes).
  - Warranty validation and RMA booking slot confirmation.
- Define JSON function schemas for tools (`check_warranty`, `trigger_diagnostics`, `book_appointment`).

### Stage 2: Streaming Architecture & Latency Budget (Days 4–6)
- Allocate maximum latency budget (< 500ms total):
  - Streaming STT: max 150ms.
  - LLM Dialog / Function Decision: max 180ms.
  - CRM / Database Tool Call: max 50ms.
  - Streaming TTS First Chunk: max 120ms.

### Stage 3: Implementation Sprints (Days 7–13)
- **Sprint 3A:** Conversational State Machine & Tool Caller (`voice_pipeline.py`).
- **Sprint 3B:** Mock hardware backend tools (`device_tools.py`).
- **Sprint 3C:** Real-time latency instrumentation profiler (`latency_profiler.py`).

### Stage 4: QA & Latency Benchmarking (Days 14–16)
- Test multi-turn conversations with interruptions and invalid serial inputs.
- Measure P50, P95, and P99 latency percentiles over 50 simulated calls.
- Compile `LATENCY_BENCHMARK_REPORT.md`.

### Stage 5: Packaging & API Server (Days 17–18)
- Interactive CLI demo and Webhook REST endpoint.
- Unit test suite verifying slot extraction and tool execution.

### Stage 6: Client Demonstration & Video (Days 19–20)
- Record 2-minute live demo showing natural customer dialogue, sub-second audio response, and automatic calendar RMA booking.
