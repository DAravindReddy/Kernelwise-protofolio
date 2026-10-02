# Project 06: SDLC Plan — IoT Sensor-to-Cloud System

## 1. Project Metadata & Team Allocation
- **Project Lead:** Embedded / Linux Engineer (STM32/ESP32 firmware, sensor drivers, MQTT/TLS)
- **Peer Reviewer:** Cloud / DevOps Engineer (AWS IoT Core, Terraform, DynamoDB, WebSocket API)
- **Estimated Duration:** 3 Weeks (Sprint Model)
- **Target Deliverable:** Embedded node firmware, hardware wiring diagram, Terraform cloud templates, and live web dashboard.

---

## 2. 6-Stage SDLC Lifecycle Breakdown

### Stage 1: Sensor & Cloud Specifications (Days 1–3)
- Define sensor telemetry schema (`IoTPayload`: device_uuid, timestamp, temp_c, humidity_pct, vibration_g, battery_mv, status_flags).
- Specify communication protocol: MQTT 3.1.1 over TLS 1.3 (Port 8883) with X.509 client certificate authentication.
- Establish hardware power profile (< 15mA sleep current target).

### Stage 2: Hardware Architecture & Wiring Specification (Days 4–6)
- Draft `WIRING_DIAGRAM.md` mapping STM32F4/ESP32 pinouts to I2C BMP280, SPI ADXL345, and status indicators.
- Define Bill of Materials (BOM) with commercial distributor part numbers (DigiKey / Mouser).

### Stage 3: Firmware & Cloud Implementation (Days 7–14)
- **Sprint 3A:** Sensor acquisition driver, offline ring buffer, and exponential backoff retry state machine.
- **Sprint 3B:** AWS IoT Core Terraform infrastructure-as-code (`terraform_iot_infra.tf`) and SQL routing rules (`aws_iot_rules.json`).
- **Sprint 3C:** Real-time WebSocket bridge and responsive web dashboard (`dashboard.py`).

### Stage 4: QA & Hardware-in-the-Loop Simulation (Days 15–17)
- Validate reconnect behavior under synthetic packet loss and network disconnections.
- Verify end-to-end latency from sensor read to browser dashboard display (< 250ms).
- Execute unit and integration tests.

### Stage 5: Cloud Deployment & Provisioning (Days 18–19)
- Run Terraform apply in client AWS account.
- Provision device certificates and attach restrictive AWS IoT policies.

### Stage 6: Client Handover & Video Walkthrough (Days 20–21)
- Record 2-minute video showing physical board sensor readings updating instantly on the cloud dashboard.
- Deliver README and client operator runbook.
