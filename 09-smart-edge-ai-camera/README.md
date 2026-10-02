# Kernelwise Labs — Smart Edge AI Vision & Thermal Anomaly Appliance

[![Edge AI](https://img.shields.io/badge/Inference-35%2B%20FPS-purple)]()
[![Hardware](https://img.shields.io/badge/Target-ARM64%20%7C%20NPU-red)]()
[![Privacy](https://img.shields.io/badge/Privacy-GDPR%20Zero--Video-brightgreen)]()
[![Bandwidth](https://img.shields.io/badge/Bandwidth-99.4%25%20Reduction-blue)]()

An on-device computer vision and thermal infrared anomaly detection engine for smart appliances and industrial inspection cameras, streaming privacy-preserving metadata rather than raw video.

---

## 1. Executive Summary & Capabilities
Streaming high-definition video to cloud AI models consumes massive bandwidth, creates privacy compliance violations, and suffers from network latency.

This repository demonstrates Kernelwise Labs' embedded Edge AI engineering:
- **Real-Time INT8 Inference Engine (`src/edge_infer.py`):** Runs optimized object detection and AMG8833 thermal grid analysis at 35+ FPS on low-power ARM64 Cortex-A53 / NPU silicon.
- **Privacy-Preserving Metadata Filter (`src/privacy_filter.py`):** Automatically purges raw raster pixel buffers after frame processing, emitting only anonymized bounding boxes and thermal telemetry.
- **Real-Time Web Console (`src/dashboard.py`):** Interactive browser console (`http://localhost:8086`) visualizing live bounding boxes, frame-rate meters, and critical thermal hotspot alerts.
- **99.4% Bandwidth Savings:** Slashes data transmission from 800+ GB/mo down to under 600 MB/mo per device.

---

## 2. Directory Structure
```
09-smart-edge-ai-camera/
├── ABSTRACT.md                 # Executive problem statement & customer ROI
├── ARCHITECTURE.md             # Multi-modal edge vision block diagram
├── SDLC_PLAN.md                # 3–4 week OEM development SDLC plan
├── BENCHMARK_PROFILING_REPORT.md # 35 FPS, 2.1W power & bandwidth metrics
├── src/
│   ├── edge_infer.py           # On-device inference & thermal engine
│   ├── privacy_filter.py       # Privacy-preserving metadata filter
│   └── dashboard.py            # Live interactive browser console
├── tests/
│   └── test_edge_ai.py         # Unit tests
└── main.py                     # Edge camera launcher
```

---

## 3. Quickstart & Execution

### Run Edge Inference Simulation
```bash
python main.py --frames 10
```

### Launch Interactive Live Browser Console
```bash
python main.py --web --port 8086
```
*Open `http://localhost:8086` in your browser.*

### Run Unit Test Suite
```bash
python -m unittest discover tests
```
