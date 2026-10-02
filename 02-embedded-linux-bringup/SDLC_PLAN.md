# Project 02: SDLC Plan — Embedded Linux Board Bring-Up

## 1. Project Metadata & Team Allocation
- **Project Lead:** Embedded & Linux Engineer (Kernel driver, Device Tree, Yocto BSP)
- **Peer Reviewer:** Technical Lead (Hardware schematic audit, bootloader bring-up)
- **Estimated Duration:** 3–4 Weeks (Milestone Model)
- **Target Deliverable:** Bootable ARM64 Yocto image, verified DTS, production C kernel driver, QEMU runner, and debugging case study.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Schematics Audit & Power Sequencing (Days 1–4)
- **Schematic & Pinout Review:** Cross-reference SoC datasheet (e.g. BCM2711 / NXP i.MX8M) against custom board schematics.
- **Power & Clock Tree Verification:** Verify 3.3V, 1.8V, and core rails with oscilloscope/multimeter. Confirm 25MHz/32.768kHz crystal oscillators.
- **UART Early Console:** Ensure UART TX/RX lines are mapped to early printk pins.

### Stage 2: Bootloader & Device Tree Construction (Days 5–9)
- **U-Boot Customization:** Set up DDR training parameters, eMMC partition table, and boot environment variables.
- **Device Tree Authoring:** Draft `.dts` declaring I2C bus controllers, pin multiplexing (`pinctrl`), SPI channels, and interrupt controller IRQ mapping.

### Stage 3: Linux Kernel Driver Development (Days 10–16)
- Implement `drivers/kernelwise_sensor.c`:
  - `i2c_driver` registration and `of_match_table` device tree binding.
  - Hardware probing, ID register verification, and mutex-protected register read/write.
  - Sysfs attribute group (`/sys/class/kernelwise_sensor/hwmon0/`) exposing temperature and pressure values.
  - Non-blocking threaded interrupt handler for alert/threshold pins.

### Stage 4: Yocto Integration & Image Generation (Days 17–21)
- Create `meta-kernelwise` layer:
  - BitBake recipe `kernelwise-sensor_1.0.bb` compiling out-of-tree kernel module.
  - Image recipe packaging minimal BusyBox/systemd rootfs with test utilities.
  - Build validation in clean Docker container.

### Stage 5: Emulation & Hardware-in-the-Loop QA (Days 22–24)
- Automated verification script (`scripts/simulate_bringup.py`) checking DTS node integrity and driver sysfs ABI contracts.
- QEMU ARM64 boot validation testing kernel initialization and driver probe sequence.

### Stage 6: Handover Package & Case Study (Days 25–26)
- Compile `DEBUGGING_CASE_STUDY.md` detailing real hardware troubleshooting (clock gating, I2C bus hang recovery).
- Publish customer-facing README and video walkthrough of the booted Linux prompt.
