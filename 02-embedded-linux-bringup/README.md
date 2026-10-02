# Kernelwise Labs — Embedded Linux Board Bring-Up on ARM

[![Target](https://img.shields.io/badge/SoC-ARM64%20Cortex--A72%2FA53-red)]()
[![Kernel](https://img.shields.io/badge/Kernel-Linux%206.6%20LTS-blue)]()
[![Build](https://img.shields.io/badge/Yocto-Kirkstone%20%7C%20Scarthgap-brightgreen)]()
[![License](https://img.shields.io/badge/License-GPL--2.0-yellow)]()

Production Board Bring-Up, Custom Device Tree Sources, and Linux Kernel I2C Driver for ARM64 platforms.

---

## 1. Executive Summary & Capabilities
When new custom PCB hardware arrives from manufacturing, getting the first kernel to boot and communicating with on-board sensors is the highest-risk phase for hardware startups.

This repository demonstrates Kernelwise Labs' end-to-end bring-up capability:
- **ARM64 Device Tree (`bcm2711-kernelwise-sensor.dts`):** Complete peripheral mapping, I2C fast mode (400kHz), pin multiplexing (`pinctrl`), and edge-triggered GPIO interrupts.
- **Production C Kernel Driver (`kernelwise_sensor.c`):** Implements `i2c_driver`, probe/remove lifecycle, mutex locking, threaded IRQ handler, and standard sysfs class attributes (`/sys/class/kernelwise_sensor/hwmon0/`).
- **Yocto BitBake Meta-Layer (`meta-kernelwise`):** Automated recipe compiling the out-of-tree kernel module and bundling it into the rootfs.
- **Real-World Case Study (`DEBUGGING_CASE_STUDY.md`):** Deep technical write-up detailing resolution of clock gating deadlocks, I2C bus lockup recovery, and 64-byte DMA alignment faults.

---

## 2. Directory Structure
```
02-embedded-linux-bringup/
├── ABSTRACT.md                 # Executive problem statement & client value
├── ARCHITECTURE.md             # Subsystem block diagrams & sysfs contracts
├── SDLC_PLAN.md                # 6-Stage SDLC engineering lifecycle
├── DEBUGGING_CASE_STUDY.md     # Real-world bring-up triage & fixes
├── dts/
│   └── bcm2711-kernelwise-sensor.dts   # ARM64 device tree overlay
├── drivers/
│   └── kernelwise_sensor.c             # C Linux kernel I2C driver
├── yocto/
│   ├── conf/layer.conf                 # meta-kernelwise configuration
│   └── recipes-kernel/kernelwise-sensor/kernelwise-sensor_1.0.bb
├── scripts/
│   └── simulate_bringup.py             # Emulation & contract verification
└── tests/
    └── test_bringup_validation.py      # Contract unit test suite
```

---

## 3. Quickstart & Verification

### Run the Bring-up Emulation Harness
```bash
python scripts/simulate_bringup.py
```

### Run Automated Contract Tests
```bash
python -m unittest discover tests
```
