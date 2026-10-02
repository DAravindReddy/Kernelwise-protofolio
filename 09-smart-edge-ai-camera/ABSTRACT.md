# Project 09: Smart Edge AI Vision Appliance (On-Device Inference & Thermal Anomaly Engine)

## 1. Executive Abstract
Smart cameras and smart appliances (refrigerators, industrial ovens, inspection cameras, and robotic vacuums) often require computer vision and thermal anomaly detection. However, streaming 1080p/4K raw video to cloud servers consumes massive cellular/Wi-Fi bandwidth, incurs thousands of dollars in cloud API costs, introduces 1-to-3 second latency, and creates severe customer privacy liabilities (GDPR/HIPAA).

**Kernelwise Labs** engineers **Low-Power On-Device Edge AI Systems**. This project showcases an edge inference appliance running INT8-quantized object detection and thermal anomaly classification directly on ARM Cortex-A/NPU hardware. Instead of transmitting raw video, the appliance processes video frames at 35+ FPS locally and broadcasts privacy-preserving bounding-box coordinates and thermal alert telemetry.

---

## 2. Customer Question Answered: "Can You Solve My Problem?"
> **Prospect Query:** *"We are developing a smart commercial kitchen appliance with an integrated camera and thermal sensor to detect food burning and machinery overheating. Cloud streaming is too expensive and our customers refuse to send video into the cloud. Can you run computer vision and thermal analytics entirely on our $15 ARM edge board?"*

### The Kernelwise Solution & Proof
- **Complete Edge Autonomy:** Inference executes entirely on the local microcontroller/SoC using quantized INT8 weights with < 15MB RAM footprint.
- **Privacy-by-Design:** Raw video frames never leave volatile RAM; only anonymized JSON event metadata and bounding boxes are published.
- **Ultra-Low Bandwidth:** Slashes data transmission bandwidth by **99.4%** compared to continuous RTSP/H.264 video streaming.
- **Multi-Modal Sensing:** Synchronously correlates optical vision (person, appliance, machinery) with infrared thermal zone matrix readings to catch overheating before fires start.

---

## 3. Commercial Positioning
- **Engagement Model:** 3-to-5 Week Fixed-Price OEM Delivery ($7,500 – $20,000 per device platform).
- **Target Market:** Smart appliance OEMs, industrial equipment makers, smart facility management.
- **Client Deliverable:** Edge inference daemon, quantized model pipeline, privacy filter, and web monitoring console.
