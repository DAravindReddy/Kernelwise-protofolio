# Project 08: SDLC Plan — Smart Device Matter Edge Gateway

## 1. Project Metadata & Team Allocation
- **Project Lead:** Embedded Engineer (Matter Data Model, BLE/Zigbee abstraction)
- **Co-Lead:** Full-Stack Engineer (Local gateway daemon, REST/WebSocket API, Web UI)
- **Peer Reviewer:** Technical Lead (Architecture governance, CSA compliance checklist)
- **Estimated Duration:** 3–4 Weeks (Sprint Model)
- **Target Deliverable:** Edge gateway daemon, Matter cluster engine, interactive Web UI, and unit test suite.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Protocol Scope & Cluster Selection (Days 1–3)
- Define supported Matter Device Types:
  - Extended Color Light (Device Type 0x010D).
  - Temperature Sensor (Device Type 0x0302).
  - Door Lock (Device Type 0x000A).
- Define cluster specifications and attribute maps.

### Stage 2: Gateway Architecture & Data Model (Days 4–7)
- Architect endpoint topology: Root Node (Endpoint 0) and Aggregator/Bridged Nodes (Endpoints 1..N).
- Define local JSON/REST and WebSocket message format for real-time bi-directional status streaming.

### Stage 3: Core Implementation (Days 8–16)
- **Sprint 3A:** Matter Data Model abstraction (`matter_model.py`).
- **Sprint 3B:** Gateway daemon with commissioning state machine (`gateway_daemon.py`).
- **Sprint 3C:** Web control console with device pairing modal (`dashboard.py`).

### Stage 4: QA, Conformance & Concurrency Testing (Days 17–20)
- Test simultaneous actuation of 20 virtual smart devices under high-frequency polling.
- Verify state recovery after gateway crash or power interruption.
- Pytest test suite covering cluster command mutations.

### Stage 5: Packaging & Embedded Linux Deployment (Days 21–23)
- Package daemon as a systemd service for Raspberry Pi / ARM Linux gateways.
- Containerize with Docker for edge appliances.

### Stage 6: Client Handover & Video Demonstration (Days 24–25)
- Record 2-minute video commissioning a new smart light, adjusting dimming levels, and toggling door locks with sub-10ms latency.
