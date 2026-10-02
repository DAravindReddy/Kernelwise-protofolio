"""
Kernelwise Labs — Freelance Job Lead Radar & Proposal Generator
Automatically matches client job descriptions to your portfolio showcases
and generates customized, high-converting Upwork / LinkedIn proposals.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


SHOWCASE_CATALOG = [
    {
        "id": "02-embedded-linux-bringup",
        "domain": "Embedded Linux & Board Bring-Up",
        "keywords": ["linux", "bringup", "bring-up", "device tree", "dts", "kernel", "yocto", "bsp", "arm64", "cortex-a", "nxp", "i.mx", "bcm2711"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/02-embedded-linux-bringup",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/02-embedded-linux-bringup/DEBUGGING_CASE_STUDY.md",
        "proof_hook": "Complete BCM2711 ARM64 Device Tree mapping, custom C I2C kernel driver with threaded IRQs, and Yocto rootfs layer.",
        "pitch_sprint": "2-Week Fast-Track Bring-Up Sprint ($2,500 – $5,000): Schematics review, virtual DTS emulation, and bench hardware stress testing."
    },
    {
        "id": "03-embedded-firmware-cicd",
        "domain": "Microcontroller Firmware CI/CD & Testing",
        "keywords": ["ci/cd", "cicd", "firmware", "qemu", "cmake", "unity", "c99", "cortex-m", "stm32", "testing", "pipeline", "docker"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/03-embedded-firmware-cicd",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/03-embedded-firmware-cicd/BENCHMARK_REPORT.md",
        "proof_hook": "Dockerized toolchain with CMake/Ninja, Unity C99 unit tests, and virtualized QEMU ARM Cortex-M smoke tests (93% faster builds).",
        "pitch_sprint": "1 to 2-Week CI/CD Automation Sprint ($2,500 – $4,000): Full GitHub Actions pipeline, QEMU smoke runner, and SHA256 release manifests."
    },
    {
        "id": "01-android-adb-telemetry",
        "domain": "Android POS / Kiosk Fleet Health & Telemetry",
        "keywords": ["android", "adb", "kiosk", "pos", "overheating", "thermal", "throttling", "crash", "lmk", "memory leak", "freeze"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/01-android-adb-telemetry",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/01-android-adb-telemetry/ARCHITECTURE.md",
        "proof_hook": "Non-invasive zero-root ADB telemetry daemon capturing SoC thermals, CPU kernel load, and memory leaks with real-time web UI.",
        "pitch_sprint": "Fleet Diagnostics Sprint ($2,500) or Monthly SLA Retainer ($1,500 – $4,000/mo): Automated crash triage and thermal profiling."
    },
    {
        "id": "09-smart-edge-ai-camera",
        "domain": "On-Device Edge AI Computer Vision & Thermal",
        "keywords": ["edge ai", "vision", "camera", "npu", "thermal", "infrared", "hotspot", "amg8833", "int8", "object detection", "gdpr"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/09-smart-edge-ai-camera",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/09-smart-edge-ai-camera/BENCHMARK_PROFILING_REPORT.md",
        "proof_hook": "Real-time INT8 computer vision + AMG8833 thermal grid anomaly detection at 35+ FPS on ARM64 Cortex-A with 99.4% video bandwidth reduction.",
        "pitch_sprint": "Edge AI Sprint ($4,500 – $7,500): Quantized INT8 model integration, thermal fusion, and GDPR privacy-preserving metadata pipeline."
    },
    {
        "id": "06-iot-sensor-to-cloud",
        "domain": "IoT Sensor-to-Cloud (STM32/ESP32 to AWS)",
        "keywords": ["iot", "aws", "aws iot", "stm32", "esp32", "mqtt", "mtls", "sensor", "cloud", "dynamodb", "terraform"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/06-iot-sensor-to-cloud",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/06-iot-sensor-to-cloud/WIRING_DIAGRAM.md",
        "proof_hook": "Multi-node STM32/ESP32 firmware acquisition with mTLS X.509, Terraform AWS IoT Core provisioning, and live browser dashboards.",
        "pitch_sprint": "Turnkey Sensor-to-Cloud Sprint ($6,000 – $12,000): End-to-end device firmware, secure cloud broker, and live web telemetry console."
    },
    {
        "id": "08-smart-device-matter-gateway",
        "domain": "Matter 1.2 Smart Home Edge Gateway",
        "keywords": ["matter", "zigbee", "thread", "ble", "smart home", "gateway", "csa", "home assistant", "apple home", "clusters"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/08-smart-device-matter-gateway",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/08-smart-device-matter-gateway/ARCHITECTURE.md",
        "proof_hook": "CSA Matter 1.2 edge gateway bridging proprietary BLE/Zigbee devices to standard clusters with sub-10ms LAN actuation.",
        "pitch_sprint": "Matter OEM Integration ($5,000 – $15,000): Data model mapping, local edge daemon, and commissionable endpoint bridge."
    },
    {
        "id": "05-voice-agent-workflow",
        "domain": "Sub-Second Low-Latency Voice AI Assistant",
        "keywords": ["voice", "audio", "voice agent", "stt", "tts", "llm", "sub-second", "latency", "rma", "call center", "support"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/05-voice-agent-workflow",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/05-voice-agent-workflow/LATENCY_BENCHMARK_REPORT.md",
        "proof_hook": "Sub-500ms streaming voice assistant (P50 423ms) with real-time hardware telemetry lookups and automated RMA appointment booking.",
        "pitch_sprint": "Voice AI Workflow ($4,000 – $10,000): Streaming STT/LLM/TTS pipeline, custom API tool bindings, and latency telemetry profiler."
    },
    {
        "id": "04-ai-rootcause-agent",
        "domain": "AI Root-Cause Diagnostic & Log Triage",
        "keywords": ["diagnostic", "root cause", "log triage", "dmesg", "panic", "crash log", "rag", "vector", "anr"],
        "repo_url": "https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/04-ai-rootcause-agent",
        "case_study": "https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/04-ai-rootcause-agent/BENCHMARK_ACCURACY_REPORT.md",
        "proof_hook": "Semantic vector RAG engine diagnosing kernel panics and bus lockups in <50ms with 100% top-1 accuracy across 12 benchmarks.",
        "pitch_sprint": "AI Diagnostic Deployment ($3,500 – $6,000): Log parser ingestion, vector failure database, and step-by-step remediation runbook generator."
    },
]

SAMPLE_LEADS = [
    {
        "source": "Upwork Enterprise",
        "title": "Need Senior Embedded Linux Engineer for Custom ARM Board Bring-Up",
        "budget": "$5,000 Fixed-Price",
        "text": "We designed a custom board based on BCM2711 / Quad Cortex-A72 with on-board I2C environmental sensors and SPI storage. The boards just arrived from PCBA manufacturing. We need an experienced embedded engineer to configure the device tree (DTS), write or adapt the Linux kernel drivers, verify GPIO interrupts, and build a minimal Yocto image. Fast delivery needed."
    },
    {
        "source": "Contra / LinkedIn",
        "title": "Automate Firmware CI/CD with Unity & QEMU Smoke Tests",
        "budget": "$3,500 Project",
        "text": "Our firmware releases on STM32 Cortex-M4 are currently tested manually with ST-Link programmers, which takes 2 days per sprint. We want a containerized GitHub Actions CI/CD pipeline using CMake, Cppcheck static analysis, native Unity unit tests for circular buffers and packet encoders, and a virtual QEMU smoke test before releases are tagged."
    },
    {
        "source": "Upwork",
        "title": "Android Kiosk App Overheating & Freezing in Retail Field Deployment",
        "budget": "$2,000 / month retainer",
        "text": "We have 150 Android POS kiosks in retail stores running 24/7. Some units freeze randomly after 8 hours of continuous operation or report thermal warnings. Root access is strictly prohibited by our merchant partners. We need a non-invasive ADB telemetry collection tool to monitor temperatures, RAM, and identify which process is causing thermal throttling."
    },
    {
        "source": "Hacker News Freelance",
        "title": "Edge AI Camera with Anomaly Hotspot Detection",
        "budget": "$8,000 Fixed",
        "text": "Looking for an edge computer vision specialist to deploy object detection and infrared thermal sensor fusion on low-power ARM64 camera modules. The camera must run at 30+ FPS without streaming raw video over the cellular network due to customer GDPR privacy concerns. Only metadata bounding boxes and hotspot alerts should be transmitted."
    },
]


def match_lead(text: str) -> Dict:
    text_lower = text.lower()
    best_match = None
    best_score = -1

    for showcase in SHOWCASE_CATALOG:
        score = 0
        for kw in showcase["keywords"]:
            if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                score += 1
        if score > best_score:
            best_score = score
            best_match = showcase

    if not best_match or best_score == 0:
        best_match = SHOWCASE_CATALOG[0]

    return best_match


def generate_proposal(lead_title: str, lead_text: str, client_name: str = "Client") -> str:
    match = match_lead(lead_title + " " + lead_text)

    proposal = f"""
======================================================================
 [KERNELWISE LABS] CUSTOM PROPOSAL READY TO SEND
 Target Domain : {match['domain']}
 Matching Repo : {match['id']}
======================================================================

Hi {client_name},

I saw your requirement regarding: "{lead_title}".

Rather than starting from scratch, I have already architected and published a production-grade working implementation for this exact architecture at Kernelwise Labs:

* Code Showcase: {match['repo_url']}
* Technical Case Study: {match['case_study']}
* What We Have Built: {match['proof_hook']}

How We De-Risk Your Milestone:
We execute via a structured {match['pitch_sprint']}
* Daily asynchronous Slack / Loom video standups.
* Clean, well-commented source code with full automated test suites.
* 100% intellectual property ownership transferred to your team upon milestone signoff.

You can inspect our verified engineering portfolio and architecture contracts here:
-> https://daravindreddy.github.io/Kernelwise-protofolio/

Are you available for a brief 15-minute technical discovery call this week?

Best regards,
Aravind Reddy
Principal Systems Engineer, Kernelwise Labs
Email: engineering@kernelwiselabs.com
======================================================================
"""
    return proposal


def run_radar_interactive():
    print("=" * 70)
    print("      KERNELWISE LABS // FREELANCE JOB LEAD RADAR & PROPOSALS     ")
    print("=" * 70)
    print("Select an option:")
    print("  1) Analyze Sample Active Client Leads (Upwork / LinkedIn)")
    print("  2) Paste a Real Client Job Posting to Generate Instant Proposal")
    print("  3) View Showcase Project Match Catalog")
    print("  Q) Quit")
    print("=" * 70)

    choice = input("Enter choice (1-3, Q): ").strip().upper()

    if choice == "1":
        print("\n--- Scanning Curated Client Leads ---\n")
        for i, lead in enumerate(SAMPLE_LEADS, 1):
            print(f"[{i}] [{lead['source']}] {lead['title']} (Budget: {lead['budget']})")
        
        sel = input(f"\nSelect lead (1-{len(SAMPLE_LEADS)}) to generate proposal: ").strip()
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(SAMPLE_LEADS):
                l = SAMPLE_LEADS[idx]
                prop = generate_proposal(l["title"], l["text"])
                print(prop)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

    elif choice == "2":
        print("\nPaste the client job title:")
        title = input("> ").strip()
        print("\nPaste the client job description:")
        desc = input("> ").strip()
        if not title and not desc:
            print("No text provided.")
            return
        prop = generate_proposal(title, desc)
        print(prop)

    elif choice == "3":
        print("\n--- Kernelwise Labs Showcase Matching Engine ---\n")
        for s in SHOWCASE_CATALOG:
            print(f"• Domain: {s['domain']}")
            print(f"  Repo:   {s['repo_url']}")
            print(f"  Proof:  {s['proof_hook']}\n")


def main():
    parser = argparse.ArgumentParser(description="Kernelwise Labs Freelance Job Radar")
    parser.add_argument("--scan", action="store_true", help="Scan sample client leads")
    parser.add_argument("--job", type=str, default=None, help="Inline job description to generate proposal for")
    args = parser.parse_args()

    if args.job:
        print(generate_proposal("Custom Client Project", args.job))
        return

    if args.scan:
        for lead in SAMPLE_LEADS:
            print(generate_proposal(lead["title"], lead["text"]))
        return

    run_radar_interactive()


if __name__ == "__main__":
    main()
