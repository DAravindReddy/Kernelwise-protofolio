# STATEMENT OF WORK (SOW) — 2-WEEK FAST-TRACK ENGINEERING SPRINT

**Agreement Ref:** SOW-KWL-2026-[CLIENT_ID]  
**Effective Date:** [Date, e.g., October 15, 2026]  
**Client Organization:** [Client Company Name, e.g., Apex Hardware Inc.]  
**Service Provider:** Kernelwise Labs Engineering (Represented by Aravind Reddy)  
**Provider Contact:** engineering@kernelwiselabs.com | https://daravindreddy.github.io/Kernelwise-protofolio/

---

## 1. Executive Summary & Purpose

Client engages Kernelwise Labs to execute a dedicated, fixed-price **2-Week Fast-Track Engineering Sprint** focused on de-risking [e.g., custom ARM64 Linux board bring-up / firmware CI/CD automation / IoT sensor-to-cloud integration].

The engagement is structured into clear milestone gates to ensure zero ambiguity, rapid feedback cycles, and complete technical delivery.

---

## 2. Technical Scope of Work & Deliverables

| Milestone | Delivery Phase | Key Deliverables & Acceptance Criteria | Timeline |
|---|---|---|---|
| **M1** | **Architecture & Hardware Audit** | • Review client schematics (Altium/KiCad) and pin multiplexing contracts.<br>• Define Device Tree Source (`.dts`) hierarchy and interrupt allocations.<br>• Deliver written Architectural Alignment Spec and register map. | **Days 1 – 3** |
| **M2** | **Driver Implementation & Emulation** | • Author production C Linux kernel driver or microcontroller firmware module.<br>• Implement `probe/remove` lifecycle, mutex locking, and sysfs hardware monitoring attributes (`/sys/class/hwmon`).<br>• Verify virtualized driver contracts and mock sensor loopbacks. | **Days 4 – 7** |
| **M3** | **Hardware Bench Test & CI/CD Gating** | • Physical hardware verification on bench target (I2C/SPI bus stability, 400kHz clock testing).<br>• Dockerized CI/CD pipeline script cross-compiling binary with Unity C99 unit tests and virtualized QEMU smoke test.<br>• Comprehensive SDLC documentation, README, and cryptographic SHA256 build manifest. | **Days 8 – 10** |

---

## 3. Commercial Investment & Payment Terms

The total fixed investment for the 2-Week Fast-Track Sprint is **$3,500 USD** (or agreed sprint price between $2,500 – $5,000):

* **Initial Deposit (50% — $1,750 USD):** Due upon signing of this SOW prior to work commencement.
* **Final Milestone Release (50% — $1,750 USD):** Due upon delivery and client acceptance of Milestone M3 deliverables.
* **Payment Methods:** Wire Transfer (Wise / Stripe / International Wire) or Upwork Direct Contract escrow.
* **Invoicing:** Invoices issued by Kernelwise Labs with GST/tax compliance numbers.

---

## 4. Client Responsibilities

To ensure completion within the 10 business day timeline, Client agrees to:
1. Provide access to schematic PDFs, component datasheets, and pinmux allocations on Day 1.
2. Provide remote target bench access (SSH/VPN) or dispatch 2 physical dev boards to Provider's test bench via DHL/FedEx.
3. Appoint a technical point-of-contact for asynchronous daily Slack/video review.

---

## 5. Intellectual Property (IP) & Code Ownership

* **100% Client Ownership:** All custom source code, Device Tree overlays, kernel drivers, firmware scripts, and documentation authored under this SOW shall become the exclusive intellectual property of Client upon receipt of final milestone payment.
* **Clean Open-Source Compliance:** Provider guarantees all third-party libraries (e.g. Linux Kernel GPL-2.0, FreeRTOS MIT) comply with license requirements with zero proprietary infringement.

---

## 6. Post-Sprint Warranty & Support

* Kernelwise Labs provides a **14-day warranty period** following milestone completion to resolve any direct bug regressions within the defined scope at no additional charge.
* Client has the option to transition the project into an ongoing **Dedicated Fleet SLA Retainer ($1,500 – $4,000/mo)** or a broader **Turnkey System Delivery** contract.

---

## 7. Execution Signatures

**For Client:**  
Name: ____________________________  
Title: _____________________________  
Signature: _________________________ Date: ______________  

**For Kernelwise Labs:**  
Name: **Aravind Reddy**  
Title: Principal Systems Engineer  
Signature: _________________________ Date: ______________  
