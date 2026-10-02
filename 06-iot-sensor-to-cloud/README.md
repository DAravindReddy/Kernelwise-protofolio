# Kernelwise Labs — IoT Sensor-to-Cloud System (STM32 / ESP32 to AWS IoT)

[![IoT Hardware](https://img.shields.io/badge/Hardware-STM32%20%7C%20ESP32-blue)]()
[![Cloud](https://img.shields.io/badge/Cloud-AWS%20IoT%20Core%20%7C%20DynamoDB-orange)]()
[![Security](https://img.shields.io/badge/Security-mTLS%20X.509-green)]()
[![IaC](https://img.shields.io/badge/IaC-Terraform-purple)]()

End-to-end industrial IoT telemetry pipeline bridging microcontroller sensor acquisition to AWS IoT Core and live web dashboards.

---

## 1. Executive Summary & Capabilities
Hardware OEMs often struggle to connect physical sensor prototypes to cloud dashboards with production-grade security and reliability.

This repository demonstrates Kernelwise Labs' end-to-end IoT engineering:
- **Microcontroller Sensor Node Simulator (`src/sensor_node_sim.py`):** Simulates I2C environmental and SPI 3-axis vibration sensors with battery voltage monitoring.
- **Hardware Schematic & Wiring Guide (`WIRING_DIAGRAM.md`):** Complete pinout specifications, decoupling capacitors, and commercial Bill of Materials (BOM).
- **Terraform Infrastructure as Code (`cloud/terraform_iot_infra.tf`):** Automated provisioning of AWS IoT Core message brokers, DynamoDB time-series storage, and IAM policies.
- **Real-Time Web Dashboard (`src/dashboard.py`):** Responsive browser dashboard (`http://localhost:8082`) tracking live multi-node telemetry and machine vibration threshold alerts.

---

## 2. Directory Structure
```
06-iot-sensor-to-cloud/
├── ABSTRACT.md                 # Executive problem statement & customer ROI
├── ARCHITECTURE.md             # End-to-end system block diagram
├── SDLC_PLAN.md                # 3-week turnkey SDLC engineering plan
├── WIRING_DIAGRAM.md           # Hardware pinout & Bill of Materials (BOM)
├── cloud/
│   ├── aws_iot_rules.json      # AWS IoT SQL routing rule
│   └── terraform_iot_infra.tf  # AWS IoT Core & DynamoDB Terraform spec
├── src/
│   ├── sensor_node_sim.py      # Microcontroller firmware simulator
│   ├── cloud_backend.py        # Cloud ingestion & anomaly engine
│   └── dashboard.py            # Live browser telemetry dashboard
├── tests/
│   └── test_iot_pipeline.py    # Unit tests
└── main.py                     # Unified multi-node launcher
```

---

## 3. Quickstart & Execution

### Run Multi-Node Telemetry Simulation
```bash
python main.py --nodes 2 --cycles 5
```

### Launch with Real-Time Web Dashboard
```bash
python main.py --nodes 3 --web --port 8082
```
*Open `http://localhost:8082` in your browser to view the live dashboard.*

### Run Unit Test Suite
```bash
python -m unittest discover tests
```
