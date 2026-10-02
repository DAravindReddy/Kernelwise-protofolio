# Kernelwise Labs — Complete Embedded & AI Systems Portfolio

**GitHub Profile:** [https://github.com/DAravindReddy](https://github.com/DAravindReddy)  
**Engineering Portfolio Monorepo:** [DAravindReddy/kernelwise-portfolio](https://github.com/DAravindReddy)

Welcome to the **Kernelwise Labs** engineering portfolio by **Aravind Reddy**. This monorepo demonstrates production-grade capabilities across embedded systems, Linux kernel bring-up, microcontroller firmware CI/CD, on-device Edge AI, low-latency streaming voice workflows, and IoT cloud pipelines.

---

## 🔗 Official Links

* **GitHub Profile:** [https://github.com/DAravindReddy](https://github.com/DAravindReddy)
* **Agency / Portfolio Repositories:** [https://github.com/DAravindReddy?tab=repositories](https://github.com/DAravindReddy?tab=repositories)
* **Brand Domain (Planned):** `https://kernelwiselabs.com` *(DNS/hosting to be pointed upon public release)*
* **Contact Email:** `engineering@kernelwiselabs.com` / `hello@kernelwiselabs.com`

---

## 🚀 Quick Execution Guide

You can execute the projects **interactively** or **one-by-one via command-line flags**.

### Option A: Interactive Menu Runner
Run the unified menu to launch or test any project with a single keystroke:
```bash
python run_portfolio.py
```
*(Or in PowerShell: `.\run_portfolio.ps1`)*

### Option B: Run Any Project Individually (1–9)
```bash
# Project 1: Android ADB Telemetry Daemon
python run_portfolio.py --project 1

# Project 2: Embedded Linux Board Bring-Up
python run_portfolio.py --project 2

# Project 3: Embedded Firmware CI/CD & QEMU Automation
python run_portfolio.py --project 3

# Project 4: AI Root-Cause Diagnostic Agent
python run_portfolio.py --project 4

# Project 5: Low-Latency Voice Agent Workflow
python run_portfolio.py --project 5

# Project 6: IoT Sensor-to-Cloud System (AWS IoT)
python run_portfolio.py --project 6

# Project 7: Developer Automation Toolkit (kw-tools)
python run_portfolio.py --project 7

# Project 8: Matter Smart Device Edge Gateway
python run_portfolio.py --project 8

# Project 9: Smart Edge AI Vision & Thermal Camera
python run_portfolio.py --project 9
```

### Option C: Run All Projects Sequentially End-to-End
```bash
python run_portfolio.py --all
```

### Option D: Run Unit Test Suites for All Projects
```bash
python run_portfolio.py --test-all
```

---

## 📂 Project Directory Index & Standalone Commands

If you prefer to enter each directory and run each project directly:

| # | Project | Directory | Standalone Execution Command | Live Web UI | GitHub Remote Target |
|---|---|---|---|---|---|
| **01** | **Android ADB Telemetry** | [`01-android-adb-telemetry/`](01-android-adb-telemetry/) | `cd 01-android-adb-telemetry && python main.py --mock --cycles 5` | `http://localhost:8080` (`--web`) | `DAravindReddy/android-adb-telemetry` |
| **02** | **Linux Board Bring-Up** | [`02-embedded-linux-bringup/`](02-embedded-linux-bringup/) | `cd 02-embedded-linux-bringup && python scripts/simulate_bringup.py` | N/A | `DAravindReddy/embedded-linux-bringup` |
| **03** | **Firmware CI/CD Pipeline** | [`03-embedded-firmware-cicd/`](03-embedded-firmware-cicd/) | `cd 03-embedded-firmware-cicd && python scripts/run_pipeline_local.py` | N/A | `DAravindReddy/embedded-firmware-cicd` |
| **04** | **AI Root-Cause Agent** | [`04-ai-rootcause-agent/`](04-ai-rootcause-agent/) | `cd 04-ai-rootcause-agent && python main.py` | N/A | `DAravindReddy/ai-rootcause-agent` |
| **05** | **Voice Agent Workflow** | [`05-voice-agent-workflow/`](05-voice-agent-workflow/) | `cd 05-voice-agent-workflow && python main.py` | N/A | `DAravindReddy/voice-agent-workflow` |
| **06** | **IoT Sensor-to-Cloud** | [`06-iot-sensor-to-cloud/`](06-iot-sensor-to-cloud/) | `cd 06-iot-sensor-to-cloud && python main.py --nodes 2 --cycles 5` | `http://localhost:8082` (`--web`) | `DAravindReddy/iot-sensor-to-cloud` |
| **07** | **Developer Automation** | [`07-developer-automation-toolkit/`](07-developer-automation-toolkit/) | `cd 07-developer-automation-toolkit && python -m kw_tools.cli env-doctor` | N/A | `DAravindReddy/developer-automation-toolkit` |
| **08** | **Matter Edge Gateway** | [`08-smart-device-matter-gateway/`](08-smart-device-matter-gateway/) | `cd 08-smart-device-matter-gateway && python main.py` | `http://localhost:8084` (`--web`) | `DAravindReddy/smart-device-matter-gateway` |
| **09** | **Smart Edge AI Camera** | [`09-smart-edge-ai-camera/`](09-smart-edge-ai-camera/) | `cd 09-smart-edge-ai-camera && python main.py --frames 10` | `http://localhost:8086` (`--web`) | `DAravindReddy/smart-edge-ai-camera` |

---

## 🌐 Launching Web Dashboards (Continuous Live Mode)

When you run any dashboard with the `--web` flag, the server **remains continuously active** until you press `Ctrl+C` in your terminal:

```bash
# Android Health Monitor Dashboard -> http://localhost:8080
python run_portfolio.py --project 1 --web

# IoT Multi-Node Sensor Dashboard -> http://localhost:8082
python run_portfolio.py --project 6 --web

# Matter Smart Device Control Console -> http://localhost:8084
python run_portfolio.py --project 8 --web

# Edge AI Computer Vision & Thermal Hotspot Console -> http://localhost:8086
python run_portfolio.py --project 9 --web
```
