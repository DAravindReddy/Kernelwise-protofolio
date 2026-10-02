# Kernelwise Labs — Smart Device Controller & Matter/Zigbee IoT Edge Gateway

[![Protocol](https://img.shields.io/badge/Standard-CSA%20Matter%201.2-blue)]()
[![Hardware](https://img.shields.io/badge/Gateway-ARM64%20Edge%20Gateway-red)]()
[![Mesh](https://img.shields.io/badge/Connectivity-Thread%20%7C%20BLE-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

An edge gateway daemon bridging proprietary smart appliances, BLE lighting, and Zigbee sensors into the unified Matter smart home ecosystem (Apple Home, Google Home, Alexa, and Home Assistant).

---

## 1. Executive Summary & Capabilities
Smart device OEMs are transitioning to Matter to avoid obsolescence and gain retail shelf placement.

This repository demonstrates Kernelwise Labs' Matter protocol and edge gateway bridging expertise:
- **Matter Data Model Engine (`src/matter_model.py`):** Models endpoints and standard clusters: OnOff (0x0006), LevelControl (0x0008), TemperatureMeasurement (0x0402), and DoorLock (0x0101).
- **Edge Gateway Daemon (`src/gateway_daemon.py`):** Sub-10ms local LAN execution, local state caching, and dynamic device pairing/commissioning.
- **Interactive Web Control Console (`src/dashboard.py`):** Live browser UI (`http://localhost:8084`) to toggle lights, adjust dimmers, actuate motorized locks, and commission new virtual endpoints.
- **REST & Local API:** Seamless bi-directional integration with Home Assistant and local home automation controllers.

---

## 2. Directory Structure
```
08-smart-device-matter-gateway/
├── ABSTRACT.md                 # Executive problem statement & OEM value
├── ARCHITECTURE.md             # Matter cluster mapping & system diagram
├── SDLC_PLAN.md                # 3–4 week OEM development SDLC plan
├── src/
│   ├── matter_model.py         # Endpoints, clusters, and attribute schemas
│   ├── gateway_daemon.py       # Core edge daemon & command dispatcher
│   └── dashboard.py            # Live interactive web control console
├── tests/
│   └── test_matter_gateway.py  # Unit tests
└── main.py                     # Gateway server launcher
```

---

## 3. Quickstart & Execution

### Run Gateway Simulation
```bash
python main.py
```

### Launch Interactive Web Control Console
```bash
python main.py --web --port 8084
```
*Open `http://localhost:8084` in your browser.*

### Run Unit Test Suite
```bash
python -m unittest discover tests
```
