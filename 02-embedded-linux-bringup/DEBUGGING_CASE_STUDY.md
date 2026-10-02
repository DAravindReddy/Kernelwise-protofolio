# Project 02: Hardware Bring-Up Case Study — "Problems We Hit and Fixed"

This document serves as proof of real-world hardware triage expertise, demonstrating to clients that Kernelwise Labs solves deep, complex board bring-up hurdles.

---

## Case 1: Silent Kernel Hang During Early Boot (Clock Gate Deadlock)

### Symptom
After U-Boot relocated the kernel and jump-started execution at `0x80080000`, the serial console printed `Starting kernel ...` and immediately stopped outputting any characters. JTAG debugger showed CPU cores stuck in WFI (Wait For Interrupt) state.

### Root Cause Analysis
1. Enabled `CONFIG_EARLY_PRINTK=y` and `CONFIG_DEBUG_LL=y` with physical UART register base address `0xfe215040`.
2. Found execution halted inside `clk_core_enable()` when initializing the APB peripheral clock tree.
3. The board design used an external oscillator whose enable pin was wired to a GPIO that defaulted to High-Z (floating low) on power-up. Because the clock was physically gated, the SoC clock controller waited indefinitely for the clock lock bit.

### Remediation
- Modified U-Boot board initialization code (`board/kernelwise/board.c`) to pull the oscillator enable GPIO HIGH before jumping to Linux.
- Added explicit `assigned-clocks` and `assigned-clock-rates` in the device tree to ensure deterministic clock initialization.

---

## Case 2: I2C Bus Lockup (SDA Held Low by Slave Device)

### Symptom
During boot, the driver probe failed with `-ETIMEDOUT` (I2C transfer timed out). Subsequent calls to `i2cdetect -y 1` reported all addresses as active (`UU`), and the I2C bus became unresponsive until a full power cycle.

### Root Cause Analysis
1. Attached a digital logic analyzer to SDA and SCL pins.
2. SCL was idling high at 3.3V, but SDA was pulled down to 0V.
3. A warm reboot occurred during an active 9-bit I2C read cycle. The sensor was in the middle of sending an ACK or data byte and was holding SDA low waiting for clock pulses that never arrived.

### Remediation
- Implemented an I2C GPIO bus recovery routine in the device tree using `pinctrl` GPIO bit-banging:
```dts
&i2c1 {
    pinctrl-names = "default", "gpio";
    pinctrl-0 = <&i2c1_pins>;
    pinctrl-1 = <&i2c1_recovery_pins>;
    scl-gpios = <&gpio 3 (GPIO_ACTIVE_HIGH | GPIO_OPEN_DRAIN)>;
    sda-gpios = <&gpio 2 (GPIO_ACTIVE_HIGH | GPIO_OPEN_DRAIN)>;
};
```
- In the driver initialization sequence, if SDA is detected low, the controller triggers 9 consecutive dummy SCL clock pulses followed by a STOP condition, forcing the slave sensor out of its lockup state.

---

## Case 3: Memory Alignment Kernel Panic in SPI DMA Transfers

### Symptom
When reading 1024-byte packets from the high-speed SPI sensor, the kernel occasionally panicked with `Unhandled fault: alignment fault (0x92000021) at 0xffff800010abc001`.

### Root Cause Analysis
The driver allocated the rx buffer on the stack using a simple `u8 rx_buf[1024]`. On ARM64 with 64-byte cache lines, passing unaligned non-cacheline-aligned stack addresses to the SPI DMA controller triggered cache coherency corruption.

### Remediation
Replaced stack allocation with `dma_alloc_coherent()` and `kmalloc` with `GFP_DMA | GFP_KERNEL`, ensuring 64-byte alignment and DMA-safe memory descriptors:
```c
priv->rx_buf = kmalloc(BUF_SIZE, GFP_KERNEL | GFP_DMA);
if (!priv->rx_buf)
    return -ENOMEM;
```
Zero panics observed over 72 hours of continuous soak testing.
