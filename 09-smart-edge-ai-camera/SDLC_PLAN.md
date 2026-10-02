# Project 09: SDLC Plan — Smart Edge AI Vision Appliance

## 1. Project Metadata & Team Allocation
- **Project Lead:** AI / Automation Engineer (Quantization, on-device inference, bounding-box engine)
- **Co-Lead:** Embedded / Linux Engineer (ARM NEON optimization, thermal I2C driver integration)
- **Peer Reviewer:** Technical Lead (Edge hardware profiling, power budget audit)
- **Estimated Duration:** 3–4 Weeks (Sprint Model)
- **Target Deliverable:** Edge AI daemon, INT8 inference engine, privacy metadata publisher, and web visualization console.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Hardware Specs & Model Selection (Days 1–3)
- Target Hardware: Quad ARM Cortex-A53 @ 1.4GHz, 512MB RAM, optional NPU accelerator.
- Model architecture: MobileNetV2-SSD / YOLO-Nano pruned and quantized to INT8 precision.
- Latency target: > 30 FPS (< 33ms per frame).

### Stage 2: Architecture & Privacy Pipeline Design (Days 4–6)
- Multi-modal pipeline: RGB Optical Frame (640x480) + 8x8 AMG8833 Thermal Infrared Matrix.
- Privacy filter architecture: discard raw raster buffers after inference; serialize only `DetectedObject` coordinates.

### Stage 3: Core Implementation (Days 7–15)
- **Sprint 3A:** Edge inference engine with INT8 matrix operations (`edge_infer.py`).
- **Sprint 3B:** Thermal hotspot anomaly correlator and privacy metadata serializer (`privacy_filter.py`).
- **Sprint 3C:** Real-time web visualization console (`dashboard.py`).

### Stage 4: QA, Benchmarking & Stress Testing (Days 16–19)
- Benchmark frame rates under thermal stress.
- Measure CPU and RAM consumption under continuous 24-hour execution.
- Compile `BENCHMARK_PROFILING_REPORT.md`.

### Stage 5: Systemd Packaging & Linux Integration (Days 20–22)
- Configure out-of-memory protections and systemd watchdog for headless smart appliance operation.

### Stage 6: Client Demonstration & Case Study (Days 23–24)
- Record 2-minute video demonstrating 35 FPS object tracking and instant thermal hotspot warning.
