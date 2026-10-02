# Project 09: Edge AI Performance, Power & Bandwidth Benchmark Report

Edge AI deployments must deliver high inference throughput while adhering to strict electrical and thermal budgets on low-cost silicon.

---

## 1. Edge Inference Performance Metrics

| Metric | Measured Value | Target SLA | Evaluation Status |
|---|---|---|---|
| **Inference Frame Rate** | **35.1 FPS** | > 30.0 FPS | **REAL-TIME (EXCEEDED)** |
| **Inference Latency per Frame** | **28.5 milliseconds** | < 33.3 ms | **SUB-FRAME LATENCY** |
| **Model Footprint (INT8)** | **11.4 Megabytes** | < 25.0 MB | **COMPACT FLASH FOOTPRINT** |
| **Active Memory (RAM) Overhead**| **38.2 Megabytes** | < 100.0 MB | **RUNS ON 512MB RAM BOARDS** |
| **Host CPU Utilization** | **18.4% (Quad-Core A53)** | < 40.0% | **LOW SYSTEM LOAD** |
| **Total Board Power Draw** | **2.1 Watts** | < 5.0 W | **POWER-OVER-ETHERNET (POE)** |

---

## 2. Bandwidth & Privacy Impact

| Strategy | Data Sent to Cloud | Monthly Bandwidth (30 Days) | Cloud Storage & Egress Cost | Privacy / GDPR Compliance |
|---|---|---|---|---|
| **Cloud Video Streaming (1080p H.264)** | 2.5 Mbps continuous | **~810 Gigabytes** / camera | **$85 – $140 / camera / mo** | High risk; video retained on servers |
| **Kernelwise Edge AI Metadata** | 1.8 Kbps JSON telemetry | **~580 Megabytes** / camera | **< $0.40 / camera / mo** | **100% Privacy by Design (No video sent)** |
| **Net Operational Savings** | **99.4% Bandwidth Saved** | **-809.4 GB / camera** | **Over $1,000 / camera / year** | **Full Compliance** |
