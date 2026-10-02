# Kernelwise Labs — 30-Minute Technical Discovery Call & Sales Script

This guide provides the exact verbal script, qualifying framework, screen-share demo walkthrough, and objection handling for conducting client discovery calls.

---

## 1. Discovery Call Structure (30 Minutes Total)

```
[00:00 - 05:00] Rapport & Agenda Setting
[05:00 - 15:00] Technical Qualification & Pain Discovery
[15:00 - 22:00] Live Code & Terminal Demonstration (Proof of Work)
[22:00 - 28:00] Scoping the 2-Week Fast-Track Sprint ($2,500 – $5,000)
[28:00 - 30:00] Immediate Next Steps & SOW Delivery Agreement
```

---

## 2. Step-by-Step Call Script

### 1. Agenda Setting (Minutes 00:00 – 05:00)
> *"Hi [Client Name], great to connect today. The goal for our 30 minutes is simple:*
> *First, I want to learn about your current hardware prototype revision, your target silicon, and where you're currently facing delays or driver friction.*
> *Second, I'll briefly screen-share how we've solved similar bring-up, CI/CD, or Edge AI challenges in production with our open-source codebase.*
> *Finally, if there's a strong fit, we can outline a low-risk 2-Week Fast-Track Sprint to de-risk your hardware milestone. Sound good?"*

---

### 2. Pain Discovery & Qualification Questions (Minutes 05:00 – 15:00)
Ask these diagnostic questions. **Take detailed notes and let the client speak 70% of the time:**

1. **Hardware & Silicon Architecture:**
   * *"What SoC or microcontroller are you using? (e.g. NXP i.MX8, STM32MP1, BCM2711, ESP32)?"*
   * *"Are your prototype PCBs already manufactured and sitting on your bench, or are you waiting for fab delivery?"*
2. **Technical Bottlenecks:**
   * *"Where is your team currently losing the most engineering hours — device tree configuration, custom kernel driver crashes, or manual flashing and test cycles?"*
   * *"Are you seeing any intermittent bus lockups on I2C/SPI or thermal throttling issues in the field?"*
3. **Timeline & Urgency:**
   * *"What is your target milestone date for getting the first image booting or showing a working demo to investors/management?"*
   * *"What happens if this bring-up milestone slips by 3 or 4 weeks?"*
4. **Budget & Decision Authority:**
   * *"Have you allocated a fixed-price budget for an external specialist to handle this sprint, or are you looking for an ongoing retainer partner?"*

---

### 3. Live Demonstration Walkthrough (Minutes 15:00 – 22:00)

Share your screen and demonstrate your real code and live terminal runner:

#### Step 1: Open Terminal & Run Portfolio Runner
Run in front of the client:
```powershell
python run_portfolio.py --project 2
```
* **Script:** [02-embedded-linux-bringup/scripts/simulate_bringup.py](file:///C:/Users/aravi/kernelwise-portfolio/02-embedded-linux-bringup/scripts/simulate_bringup.py)
* **What to tell them:**  
  > *"Notice how our bring-up harness validates the Device Tree Source (DTS), verifies the Linux kernel symbol binding, simulates the U-Boot to kernel handover, and binds the driver sysfs attributes under `/sys/class/hwmon0/`. We don't guess — we test every contract."*

#### Step 2: Show Firmware CI/CD Automation
Run:
```powershell
python run_portfolio.py --project 3
```
* **Script:** [03-embedded-firmware-cicd/scripts/run_pipeline_local.py](file:///C:/Users/aravi/kernelwise-portfolio/03-embedded-firmware-cicd/scripts/run_pipeline_local.py)
* **What to tell them:**  
  > *"This 5-stage pipeline cross-compiles ARM Cortex-M firmware, runs native Unity unit tests, boots the binary in a virtualized QEMU emulator, and outputs a cryptographic SHA256 manifest. It prevents regressions before code ever touches physical dev boards."*

#### Step 3: Show Live Web Dashboard (if they are IoT or Edge AI clients)
Run:
```powershell
python run_portfolio.py --project 9 --web
```
Open **`http://localhost:8086`** in your browser:
* **What to tell them:**  
  > *"Here is our live on-device Edge AI vision console. It's processing real-time object detection and 8x8 infrared thermal hotspot anomalies at 35+ FPS on ARM64 silicon while completely dropping raw video buffers to guarantee GDPR compliance."*

---

### 4. Transitioning to the Offer (Minutes 22:00 – 28:00)

Never pitch an open-ended, ambiguous hourly project. Pitch the **2-Week Fast-Track Sprint**:

> *"Based on what you've shared about your [Target Board/Problem], here is how we can solve this with zero risk for your team:*
>
> *We propose our **2-Week Fast-Track Bring-Up Sprint ($2,500 – $5,000)**:*
> *• **Week 1:** We review your Altium/KiCad schematics, map your Device Tree Source, write the custom C kernel driver, and verify virtual emulation.*
> *• **Week 2:** We bind on-board hardware peripherals, bench-test under stress, containerize your CI/CD pipeline, and hand off full source code and documentation.*
>
> *You get a dedicated senior embedded engineer, daily async video updates on Slack, and 100% intellectual property ownership. If we don't deliver the working driver milestone within 10 business days, you don't pay.*
>
> *Can I send over a 2-page Statement of Work (SOW) this afternoon for your review?"*

---

## 3. Objection Handling Guide

### Objection 1: "Why hire an agency instead of hiring a full-time engineer?"
> **Answer:** *"Hiring a senior embedded Linux or kernel engineer takes 3 to 6 months in recruiting, costs $140,000 – $180,000+ per year plus benefits, and carries high onboarding risk. With Kernelwise Labs, you get senior-level capability starting on Monday with a fixed-scope 2-week sprint. You only pay for the exact milestone you need de-risked."*

### Objection 2: "Can you work with our hardware if you are remote in India?"
> **Answer:** *"Absolutely. In embedded systems, 80% of bring-up risk can be solved virtually beforehand through device tree validation, mock registers, and QEMU virtual emulation. For physical testing, clients typically courier 2 development boards via DHL Express (takes 3 business days), or we remotely access your physical bench target over SSH/OpenVPN connected to a Raspberry Pi with a logic analyzer."*

### Objection 3: "Who owns the Intellectual Property (IP)?"
> **Answer:** *"You own 100% of the Intellectual Property. All source code, device tree overlays, driver sources, and CI/CD manifests created during the engagement are assigned directly to your company upon milestone completion. We provide clean MIT or proprietary licensing as requested."*

### Objection 4: "Can we start with a smaller test first?"
> **Answer:** *"That's exactly why we created the 2-Week Fast-Track Sprint. We don't ask for a 6-month contract. We pick your single highest-risk peripheral driver or test bottleneck and prove our code quality within 10 business days."*
