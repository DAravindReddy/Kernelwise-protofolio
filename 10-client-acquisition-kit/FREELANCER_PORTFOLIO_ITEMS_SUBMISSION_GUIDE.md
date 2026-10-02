# Freelancer.in — Complete Portfolio Items Submission Guide

This document contains copy-paste ready data for **all 9 portfolio items** matching Freelancer's exact submission form fields:
* **Upload Files** (Images generated in `assets/portfolio/` or live dashboard snapshots)
* **Work Title** (max ~50 chars)
* **Description** (strictly under 2,000 characters)
* **Tags**
* **Tools and Software**
* **Skills**
* **Industry**

---

## Portfolio Item 1: ARM64 Linux Board Bring-Up & Kernel Driver

* **Upload Image:** `assets/portfolio/01_arm64_linux_bringup.jpg` (or screenshot from `02-embedded-linux-bringup`)
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `ARM64 Embedded Linux Board Bring-Up & C Driver`
* **Describe the work you completed:**
```text
Architected and executed a production board bring-up on ARM64 silicon (BCM2711) for a custom hardware platform:

1. Device Tree Mapping:
Authored custom Device Tree Sources (DTS/DTSI) mapping I2C, SPI, UART, and GPIO peripherals with strict pinmux routing and power-sequencing definitions.

2. C Kernel Driver Development:
Developed a high-reliability Linux character and hwmon I2C sensor driver (kernelwise_sensor.c) supporting threaded interrupt handlers, sysfs diagnostic endpoints, and non-blocking ring buffer transfers.

3. Hardware Bus Deadlock Triage:
Diagnosed and resolved critical slave I2C clock-stretching lockups that grounded SDA. Implemented an automatic 9-clock pulse GPIO recovery algorithm to cycle the peripheral's internal shift register and restore the bus without system reboot.

4. Minimal Yocto Rootfs:
Constructed a tailored Yocto Project (Kirkstone) layer deploying a hardened ARM64 rootfs with sub-3 second boot time and automated hardware stress testbench scripts.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/02-embedded-linux-bringup
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `embedded linux, arm64, device tree, yocto, i2c, bsp, c programming, kernel driver`
* **What tools and software did you use?:**  
  `yocto, git, cmake, gcc, gdb, oscilloscope, logic analyzer, linux`
* **What skills did you use?:**  
  `embedded systems, linux kernel, device drivers, c programming, arm`
* **What industry was the work for?:**  
  `Industrial Automation`

---

## Portfolio Item 2: Microcontroller Firmware CI/CD & Virtual QEMU Pipeline

* **Upload Image:** `assets/portfolio/02_firmware_cicd_qemu.jpg`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Microcontroller Firmware CI/CD & Virtual QEMU`
* **Describe the work you completed:**
```text
Built an automated, Dockerized firmware testing and verification pipeline for ARM Cortex-M microcontrollers (STM32):

1. Dockerized Toolchain & Build Acceleration:
Containerized the full GCC ARM toolchain with CMake and Ninja, eliminating environment inconsistencies and speeding up clean compilation by 93%.

2. Automated C99 Unit Testing:
Integrated the Unity C99 test harness with automated memory leak profiling and 98%+ code coverage across hardware abstraction layers and state machines.

3. Zero-Hardware Virtual Smoke Testing:
Architected headless emulation runners in QEMU (Cortex-M3/M4) executing automated bootup, peripheral register validation, and network stack verification without requiring physical target boards.

4. Release Manifest Automation:
Automated release packaging generating SHA-256 binary manifests, flash/SRAM memory footprint deltas, and automated regression reports on every commit.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/03-embedded-firmware-cicd
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `firmware, cicd, qemu, stm32, cmake, docker, unit testing, automation`
* **What tools and software did you use?:**  
  `docker, cmake, ninja, qemu, unity c99, github actions, cppcheck, gcc`
* **What skills did you use?:**  
  `firmware, c programming, microcontroller, ci/cd, stm32`
* **What industry was the work for?:**  
  `Medical Devices`

---

## Portfolio Item 3: Android POS & Kiosk Fleet Telemetry Daemon

* **Upload Image:** `assets/portfolio/03_android_kiosk_telemetry.jpg`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Android POS & Kiosk Fleet Telemetry Daemon`
* **Describe the work you completed:**
```text
Engineered a lightweight, non-invasive systems daemon monitoring Android self-checkout and POS terminal fleets without requiring device rooting:

1. Real-Time Thermal & Resource Auditing:
Developed a low-overhead background collector polling SoC thermal zones, thermal throttling triggers (>48°C), CPU frequency scaling, and memory fragmentation.

2. Crash & ANR Proactive Triage:
Implemented real-time parsing of logcat and kernel tombstones, automatically flagging Android Low Memory Killer (LMK) kill events, foreground UI freezes, and ANR anomalies before field failure.

3. Live Browser Telemetry Console:
Built an interactive local and remote web dashboard displaying fleet hardware health, real-time temperature heatmaps, and proactive alert thresholds.

4. Zero-Root Security Compliance:
Engineered entirely over standard ADB and system APIs, maintaining enterprise warranty compliance and PCI-DSS retail security standards.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/01-android-adb-telemetry
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `android, adb, pos, kiosk, telemetry, memory leak, thermal, systems programming`
* **What tools and software did you use?:**  
  `adb, python, linux, bash, websocket, html5`
* **What skills did you use?:**  
  `android, systems programming, debugging, python, telemetry`
* **What industry was the work for?:**  
  `Retail`

---

## Portfolio Item 4: Sub-Second INT8 Edge AI Vision & Thermal Fusion

* **Upload Image:** Take a screenshot of `python run_portfolio.py -p 9 -w` at `http://localhost:8089`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Sub-Second INT8 Edge AI Vision & Thermal Fusion`
* **Describe the work you completed:**
```text
Designed a high-throughput, privacy-preserving Edge AI camera system combining computer vision with infrared thermal analysis:

1. Quantized Neural Network Inference:
Deployed an INT8-quantized MobileNet SSD object detection pipeline running at 35+ FPS on ARM Cortex-A silicon and low-power NPUs.

2. Thermal Sensor Fusion:
Integrated an AMG8833 8x8 infrared sensor array over I2C, interpolating thermal grids to overlay hotspot anomalies and fire hazard warnings in real time.

3. Privacy & GDPR Compliance:
Engineered 100% on-device edge inferencing that transmits only lightweight JSON bounding boxes and temperature metadata (99.4% video bandwidth reduction with zero raw video streamed).

4. Real-Time Telemetry Interface:
Delivered an interactive web UI rendering low-latency video overlays, FPS counters, and thermal hotspot telemetry graphs.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/09-smart-edge-ai-camera
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `edge ai, computer vision, int8, thermal camera, amg8833, npu, object detection`
* **What tools and software did you use?:**  
  `opencv, python, tflite, onnx, numpy, linux`
* **What skills did you use?:**  
  `computer vision, edge ai, python, embedded systems, arm64`
* **What industry was the work for?:**  
  `Industrial Automation`

---

## Portfolio Item 5: Turnkey IoT Sensor-to-Cloud with mTLS & AWS

* **Upload Image:** Take a screenshot of `python run_portfolio.py -p 6 -w` at `http://localhost:8086`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `IoT Sensor-to-Cloud Pipeline with mTLS & AWS`
* **Describe the work you completed:**
```text
Architected an end-to-end industrial IoT telemetry pipeline from microcontroller firmware to cloud visualization:

1. Multi-Node Sensor Firmware:
Developed STM32 and ESP32 C firmware sampling multi-channel environmental sensors (temperature, humidity, vibration) over I2C and SPI buses.

2. Enterprise-Grade Security:
Implemented mutual TLS (mTLS X.509) cryptographic handshakes with hardware-backed certificate verification for tamper-proof MQTT communication.

3. Cloud Infrastructure as Code:
Provisioned AWS IoT Core message brokers, DynamoDB time-series datastores, and IAM least-privilege security policies using automated Terraform templates.

4. Live Telemetry Dashboard:
Engineered a responsive web monitoring dashboard streaming real-time metrics with sub-second WebSocket updates and automated threshold alerts.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/06-iot-sensor-to-cloud
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `iot, aws iot, stm32, esp32, mqtt, mtls, terraform, sensor telemetry`
* **What tools and software did you use?:**  
  `aws iot core, dynamodb, terraform, mosquitto, python, c`
* **What skills did you use?:**  
  `internet of things (iot), aws, c programming, esp32, stm32`
* **What industry was the work for?:**  
  `Energy`

---

## Portfolio Item 6: Matter 1.2 Edge Gateway Bridge for Smart Home

* **Upload Image:** Take a screenshot of `python run_portfolio.py -p 8 -w` at `http://localhost:8088`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Matter 1.2 Edge Gateway Bridge for Smart Home`
* **Describe the work you completed:**
```text
Built an interoperable CSA Matter 1.2 edge gateway bridge running on embedded Linux:

1. Multi-Protocol Translation:
Mapped proprietary BLE and Zigbee endpoints into standard Matter On/Off, Level Control, and Temperature Sensor data clusters.

2. Ultra-Low LAN Latency:
Delivered sub-10ms local area network (LAN) command actuation, eliminating cloud dependencies and latency bottlenecks.

3. Ecosystem Interoperability:
Achieved plug-and-play commissioning across Apple HomeKit, Google Home, and Home Assistant through local IPv6 Thread/Wi-Fi bridges.

4. Interactive Edge Management UI:
Created an embedded web console for real-time Matter node discovery, cluster attribute inspection, and instant endpoint toggling.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/08-smart-device-matter-gateway
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `matter, zigbee, ble, smart home, gateway, apple home, iot, linux`
* **What tools and software did you use?:**  
  `chip-tool, python, bluetoothctl, home assistant, linux`
* **What skills did you use?:**  
  `embedded systems, iot, bluetooth, linux, networking`
* **What industry was the work for?:**  
  `Consumer Electronics`

---

## Portfolio Item 7: AI Root-Cause Diagnostic Agent for Kernel Panics

* **Upload Image:** Screenshot of `python 04-ai-rootcause-agent/main.py --benchmark` terminal output
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `AI Root-Cause Diagnostic Agent for Kernel Panics`
* **Describe the work you completed:**
```text
Developed a specialized AI root-cause diagnostic reasoning agent for embedded Linux kernel triage:

1. Semantic Vector Knowledge Base:
Engineered an embedded RAG (Retrieval-Augmented Generation) vector index populated with Linux kernel panic stack traces, device driver race conditions, and bus deadlock signatures.

2. Sub-50ms Log Triage:
Ingested raw dmesg logs, kernel oops dumps, and hardware register states, isolating root cause signatures in <50ms with 100% top-1 accuracy across 12 standard benchmarks.

3. Automated Remediation Runbooks:
Generated step-by-step driver patching instructions, pinmux adjustments, and kernel config recommendations to resolve crashes permanently.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/04-ai-rootcause-agent
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `ai agent, linux kernel, root cause, dmesg, rag, debugging, kernel panic`
* **What tools and software did you use?:**  
  `python, faiss, vector embeddings, linux, regex`
* **What skills did you use?:**  
  `linux kernel, debugging, artificial intelligence, python, triage`
* **What industry was the work for?:**  
  `Software`

---

## Portfolio Item 8: Sub-500ms Voice AI Support Workflow Engine

* **Upload Image:** Screenshot of `python 05-voice-agent-workflow/main.py`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Sub-500ms Voice AI Support Workflow Engine`
* **Describe the work you completed:**
```text
Engineered an ultra-low latency streaming voice assistant engine for hardware field diagnostics and RMA triage:

1. Low-Latency Audio Pipeline:
Integrated streaming Speech-to-Text (STT), compact LLM inference, and Text-to-Speech (TTS), achieving sub-500ms P50 turn-around latency (423ms benchmarked).

2. Hardware Telemetry Integration:
Connected real-time tool bindings allowing the voice assistant to query device telemetry, check battery health, and diagnose sensor error codes during live voice calls.

3. Automated RMA Booking:
Engineered conversational workflow logic to automatically qualify warranty issues and book field RMA appointments with confirmation dispatch.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/05-voice-agent-workflow
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `voice ai, speech to text, tts, llm, latency, telemetry, automation`
* **What tools and software did you use?:**  
  `python, whisper, web audio, websocket, fast api`
* **What skills did you use?:**  
  `artificial intelligence, audio processing, python, streaming`
* **What industry was the work for?:**  
  `Telecommunications`

---

## Portfolio Item 9: Developer Automation & Hardware Telemetry Toolkit

* **Upload Image:** Screenshot of `python 07-developer-automation-toolkit/main.py`
* **Link a project on Freelancer?:** Leave blank / None
* **Give your work a title:**  
  `Developer Automation & Hardware Telemetry Toolkit`
* **Describe the work you completed:**
```text
Built an extensible developer operations and hardware telemetry automation CLI suite for embedded engineering teams:

1. Unified System Profiling:
Created non-intrusive system benchmarkers recording memory fragmentation, storage IOPS, and thermal variance across heterogeneous development boards.

2. Release Pipeline Validation:
Automated sanity checks for cross-compiler toolchains, header dependencies, and build artifact hashing.

3. Asynchronous Task Orchestration:
Designed a non-blocking background CLI runner executing build pipelines and regression tests with structured JSON reporting.

• Verified GitHub Codebase: https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/07-developer-automation-toolkit
• Agency Showcase: https://daravindreddy.github.io/Kernelwise-protofolio/
```
* **Describe your work with tags:**  
  `automation, cli, telemetry, devops, python, benchmarking, developer tools`
* **What tools and software did you use?:**  
  `python, bash, git, click, pytest, linux`
* **What skills did you use?:**  
  `python, developer tools, automation, systems architecture`
* **What industry was the work for?:**  
  `Information Technology`
