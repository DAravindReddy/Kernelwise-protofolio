# Kernelwise Labs — Direct Outbound Client Prospecting Playbook

This playbook outlines the exact outbound prospecting system to win high-ticket contracts ($5,000 – $25,000+) from funded hardware startups, IoT OEMs, and smart device manufacturers.

---

## 1. The 100-20-5-1 Outbound Sales Funnel

According to our master business strategy:

* **100 Targeted Prospects** (identified via LinkedIn, Crunchbase, Kickstarter)
* **20 Discovery Calls** (15-30 min screen-share walking through working code)
* **5 Formal SOW Proposals** (Fixed-Scope 2-Week Sprint or Turnkey Delivery)
* **1 to 2 Paying Clients** ($2,500 – $15,000 initial contract size)

---

## 2. Target Persona & Prospect Sourcing

### Target Persona 1: Hardware Startup Founder / CTO
* **Companies:** Seed or Series A funded IoT, robotics, drone, or smart appliance startups (5–30 employees).
* **Pain Point:** PCB design is complete, but firmware bring-up is delayed; lack an in-house senior embedded Linux/kernel specialist.
* **Search Query on LinkedIn / Crunchbase:**
  `("Founder" OR "CTO" OR "Head of Hardware") AND ("IoT" OR "Embedded" OR "Robotics" OR "Connected Device")`

### Target Persona 2: VP / Director of Embedded Engineering
* **Companies:** Mid-market OEMs producing smart retail kiosks, POS terminals, medical devices, or smart home gateways (50–500 employees).
* **Pain Point:** Field crash logs are overwhelming support; builds take hours with manual flashing regressions.
* **Search Query:**
  `("VP of Engineering" OR "Director of Firmware" OR "Lead Embedded Engineer") AND ("Linux" OR "STM32" OR "Android")`

### Target Persona 3: Boutique Hardware & PCB Design Agencies
* **Companies:** Hardware engineering consultancies that design schematics and layout in Altium/KiCad.
* **Pain Point:** They design physical PCBs for clients, but don't have enough firmware/driver engineers to write production Linux drivers or cloud pipelines.
* **Opportunity:** Become their white-label software engineering partner.

---

## 3. High-Converting 5-Touch Outreach Sequence

### Touch 1: Day 1 — The Hyper-Relevant Code Hook (LinkedIn Connection or Email)
**Subject:** Hardware bring-up & firmware CI/CD for [Company Name]

> Hi [First Name],
>
> Saw your recent update on [Product Name / Silicon Target / Funding announcement] — exciting milestone with the new revision.
>
> When new prototype PCBs arrive from manufacturing, getting the first Linux kernel booting and binding on-board sensor drivers without clock stretching lockups is usually the highest-risk phase.
>
> We recently open-sourced our complete ARM64 board bring-up and firmware CI/CD framework at Kernelwise Labs:
> 🔹 **ARM64 Board Bring-Up & DTS:** https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/02-embedded-linux-bringup  
> 🔹 **Firmware CI/CD & QEMU Automation (93% faster builds):** https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/03-embedded-firmware-cicd  
>
> We help hardware startups de-risk bring-up through a fixed-scope **2-Week Fast-Track Sprint ($2,500 – $5,000)** with guaranteed deliverables.
>
> Open to a brief 15-minute technical discovery call this Thursday at 2 PM or 4 PM?
>
> Best regards,  
> **Aravind Reddy**  
> Principal Engineer, Kernelwise Labs  
> Portfolio: https://daravindreddy.github.io/Kernelwise-protofolio/

---

### Touch 2: Day 3 — The Specific Debugging Case Study (Value Drop)
**Subject:** Re: Hardware bring-up & firmware CI/CD for [Company Name]

> Hi [First Name],
>
> Following up on my previous note. Thought you or your firmware team might appreciate this technical post-mortem:
>
> 👉 **Real-World Bring-Up Triage Case Study:** https://github.com/DAravindReddy/Kernelwise-protofolio/blob/main/02-embedded-linux-bringup/DEBUGGING_CASE_STUDY.md
>
> It details how we resolved an edge-triggered I2C clock gating deadlock and 64-byte SPI DMA alignment faults on an ARM64 Cortex-A72 target.
>
> If your team is currently facing any driver crashes or manual test bottlenecks on your current revision, happy to review your block diagram and share insights.
>
> Are you free for 10 minutes this Friday?
>
> Best,  
> Aravind

---

### Touch 3: Day 7 — The Video / Interactive Web Console Demonstration
**Subject:** Live edge telemetry & sensor dashboard demo

> Hi [First Name],
>
> Quick demonstration of how we connect physical sensor prototypes to live web consoles and AWS IoT Core without proprietary cloud lock-in:
>
> We built a live interactive multi-node telemetry system:
> 🔹 **IoT Sensor-to-Cloud System:** https://github.com/DAravindReddy/Kernelwise-protofolio/tree/main/06-iot-sensor-to-cloud
>
> It features automated mTLS encryption, DynamoDB time-series storage, and machine vibration alert thresholds.
>
> Would you like to see how we could apply this pipeline to your [Product Name]?
>
> Best,  
> Aravind

---

### Touch 4: Day 12 — The Low-Risk Trial Offer
**Subject:** De-risking your next hardware sprint

> Hi [First Name],
>
> I know hardware engineering cycles move fast. If you're hesitant about bringing on a new software agency, we structure our client engagements with zero long-term lock-in:
>
> **The 2-Week Fast-Track Trial Sprint:**
> • Dedicated focus on 1 target board / peripheral bus.
> • Complete Device Tree mapping and custom C driver.
> • Bench stress testing + automated CI/CD smoke test.
> • 100% full IP ownership and cryptographic build manifests transferred to your team.
>
> If we don't hit the agreed technical milestone within 10 business days, you don't pay.
>
> Let me know if you have 15 minutes next Tuesday to discuss.
>
> Best,  
> Aravind

---

### Touch 5: Day 18 — The Break-Up Note
**Subject:** Permission to close your file?

> Hi [First Name],
>
> I haven't heard back, which usually means one of two things:
> 1. You've already solved your firmware bring-up and CI/CD pipelines in-house.
> 2. This isn't a priority right now.
>
> If it's the latter, no problem at all — I won't follow up further.
>
> If you ever need specialized ARM Linux bring-up, sub-second voice AI, or Edge AI computer vision in the future, you can always explore our open-source codebase here:
> 👉 https://daravindreddy.github.io/Kernelwise-protofolio/
>
> Wishing you and the [Company Name] team massive success on the hardware launch.
>
> Best regards,  
> Aravind Reddy

---

## 4. White-Label Partnership Pitch for Boutique PCB Design Agencies

Send this to Founders or Directors of PCB Design / Hardware Engineering Agencies:

> **Subject:** Software & Linux bring-up partner for your PCB design clients
>
> Hi [Agency Founder Name],
>
> I've been following [Agency Name]'s impressive custom hardware and Altium layout work for clients.
>
> Many boutique PCB design firms face a recurring dilemma: once the prototype boards are manufactured and delivered, clients need custom Linux device trees, kernel drivers, and cloud IoT connectivity that your hardware team may not have the capacity or interest to develop in-house.
>
> At **Kernelwise Labs**, we act as the dedicated software & firmware partner for hardware design firms:
> • When your client's PCB arrives from the fab, we handle the Linux board bring-up, write C drivers for on-board sensors, and set up automated QEMU CI/CD testing.
> • We can operate either as a trusted referral partner (with a referral fee) or white-labeled under [Agency Name]'s umbrella.
>
> You can inspect our public code and engineering contracts here:
> 👉 https://daravindreddy.github.io/Kernelwise-protofolio/
>
> Would you be open to a 15-minute introductory call to explore how we can provide end-to-end software delivery for your upcoming client boards?
>
> Best regards,  
> **Aravind Reddy**  
> Principal Engineer, Kernelwise Labs  
> Email: engineering@kernelwiselabs.com
