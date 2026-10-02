# Kernelwise Labs — Android Device Health Monitor (ADB Telemetry)

[![Architecture](https://img.shields.io/badge/Architecture-ARM64%20%7C%20x86__64-blue)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

An enterprise-grade telemetry collection and thermal/performance monitoring daemon for Android fleets (kiosks, POS systems, smart robotics, and tablets).

---

## 1. The Problem We Solve
Android kiosks and retail POS systems freeze, drop frames, and crash due to silent thermal throttling and background memory leaks. 
- Traditional monitoring tools require heavy APKs or root access that void warranties.
- Our solution operates **non-invasively over ADB** (USB or TCP/IP port 5555), streaming high-resolution metrics without modifying device firmware.

---

## 2. Key Features
- **Non-Invasive ADB Collection:** Extracts CPU, RAM, thermal zone temperatures, battery degradation, and top active processes via `dumpsys` and `/sys/class/thermal/`.
- **Intelligent Threshold Alerts:** Automated warnings for thermal throttling (> 48°C), CPU saturation (> 85%), and Android Low Memory Killer (LMK) risks.
- **Dual Dashboard Modes:** Live ASCII terminal dashboard + built-in web UI dashboard (`http://localhost:8080`).
- **Telemetry Streaming & Export:** Automatically outputs point-in-time metrics to CSV and structured JSON in `logs/`.
- **Synthetic Device Simulator:** Includes a built-in ARM64 device emulator for instant testing without physical hardware plugged in.

---

## 3. Quickstart & Execution

### Run with Synthetic Emulator (No physical Android device needed)
```bash
python main.py --mock --web --cycles 5
```

### Run with Physical USB or Networked Android Device
```bash
# Verify ADB sees the device
adb devices

# Run telemetry monitor on port 8080
python main.py --web
```

### Run Unit Test Suite
```bash
python -m unittest discover tests
```

---

## 4. Sample Terminal Output

```text
====================================================================
 [KERNELWISE LABS] ANDROID HEALTH MONITOR | Target: sim-kiosk-arm64
====================================================================
 CPU Total:  74.2%  [User: 53.4% | Kernel: 20.8%]
 RAM Usage:  72.6%  [2974 MB / 4096 MB]
 SoC Temp :  58.8°C  | Battery: 49.6°C (88%)
--------------------------------------------------------------------
 Top Processes:
   * com.kiosk.posapp         (PID: 1420 ) ->  32.0% CPU
   * system_server            (PID: 650  ) ->  16.6% CPU
   * surfaceflinger           (PID: 480  ) ->   8.4% CPU
--------------------------------------------------------------------
 ! [CRITICAL ALERT] THERMAL_THROTTLE_DANGER: SoC Temperature 58.8°C exceeds critical threshold (58.0°C). Imminent hardware throttling or shutdown!
====================================================================
```

---

## 5. Repository Documentation
- [Project Abstract & Business Case](ABSTRACT.md)
- [Comprehensive SDLC Execution Plan](SDLC_PLAN.md)
- [System Architecture Specification](ARCHITECTURE.md)
