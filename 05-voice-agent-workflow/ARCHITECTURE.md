# Project 05: Architecture Specification — Low-Latency Voice Agent

## 1. Streaming Voice Pipeline Architecture

```mermaid
flowchart LR
    subgraph Audio Input
        USER[Customer Voice Stream] --> STT[Streaming STT Layer: 140ms]
    end

    subgraph Intelligence & Tools
        STT --> DIALOG[Dialog State Machine & LLM: 175ms]
        DIALOG <-->|Tool Invocation: 45ms| TOOLS[Hardware DB & RMA Tools]
    end

    subgraph Audio Output
        DIALOG --> TTS[Streaming TTS Engine: 120ms]
        TTS --> AUDIO[Low-Latency Audio Chunk Stream: ~480ms Total]
    end

    subgraph Telemetry
        AUDIO --> PROF[Latency Profiler: TTFT / P50 / P95 / P99]
    end
```

---

## 2. Tool Calling Interfaces (`src/device_tools.py`)

### 2.1 `check_warranty(serial_number: str)`
- Checks warranty status against simulated hardware ERP database.
- Returns status (`ACTIVE`, `EXPIRED`), coverage tier, and registration date.

### 2.2 `trigger_remote_diagnostics(serial_number: str)`
- Simulates an on-device diagnostic query pinging the device.
- Returns current SoC temperature, battery health, and active error codes (e.g. `ERR_OVERHEAT_ZONE1`).

### 2.3 `schedule_rma_repair(serial_number: str, issue: str, slot: str)`
- Enters service ticket into CRM/calendar database and returns confirmation ticket ID.
