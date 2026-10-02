# Project 06: Hardware Schematic, Pinout & Bill of Materials (BOM)

This document specifies the reference circuit connections between the STM32F401RE / ESP32-WROOM-32 microcontroller and the industrial sensor breakout boards.

---

## 1. Pin Connection Table

| Microcontroller Pin (STM32 / ESP32) | Sensor Module | Sensor Pin | Signal Description | Hardware Notes |
|---|---|---|---|---|
| **3V3 (Pin 16)** | BMP280 | VCC | 3.3V Power Rail | Decoupling cap: 100nF ceramic to GND |
| **GND (Pin 20)** | BMP280 | GND | Ground | Common system ground plane |
| **PB8 / GPIO21 (D15)** | BMP280 | SCL | I2C Clock | 4.7kΩ pull-up resistor to 3.3V |
| **PB9 / GPIO22 (D14)** | BMP280 | SDA | I2C Data | 4.7kΩ pull-up resistor to 3.3V |
| **PA5 / GPIO18 (SCK)** | ADXL345 | SCL/SCK | SPI Clock | Up to 5MHz SPI bus |
| **PA6 / GPIO19 (MISO)** | ADXL345 | SDO/MISO | SPI Master In | SPI full-duplex input |
| **PA7 / GPIO23 (MOSI)** | ADXL345 | SDA/MOSI | SPI Master Out | SPI full-duplex output |
| **PB6 / GPIO5 (CS)** | ADXL345 | CS | Chip Select | Active LOW, 10kΩ pull-up to 3.3V |
| **PA0 / GPIO4 (INT1)** | ADXL345 | INT1 | Vibration Alert IRQ | Configured as rising edge interrupt |
| **PA5 / GPIO2 (LED)** | On-board | ANODE | Status Heartbeat | 330Ω current limiting resistor |

---

## 2. Bill of Materials (BOM)

| Item # | Component | Manufacturer Part Number | Quantity | Est. Unit Cost ($) | Description |
|---|---|---|---|---|---|
| 1 | Microcontroller | ESP32-WROOM-32E / STM32F401RET6 | 1 | $3.80 | Dual-core Wi-Fi/BLE MCU or ARM Cortex-M4 |
| 2 | Environmental Sensor | Bosch Sensortec BMP280 | 1 | $1.95 | Temperature & Barometric Pressure (I2C/SPI) |
| 3 | 3-Axis Accelerometer | Analog Devices ADXL345BCCZ | 1 | $2.40 | High-resolution vibration sensor (SPI) |
| 4 | Resistors (Pull-up) | Yageo RC0603FR-074K7L | 2 | $0.02 | 4.7kΩ 0603 SMD Resistors |
| 5 | Decoupling Capacitors | Murata GRM188R71C104KA01D | 2 | $0.03 | 0.1uF 16V X7R 0603 SMD Capacitors |
| 6 | PCB Prototype Carrier | Custom 2-Layer FR4 (1.6mm) | 1 | $1.20 | Custom Kernelwise reference carrier |
