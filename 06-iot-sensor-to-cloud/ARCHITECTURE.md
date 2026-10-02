# Project 06: Architecture Specification — IoT Sensor-to-Cloud

## 1. End-to-End System Block Diagram

```mermaid
flowchart TD
    subgraph Edge Hardware Node: STM32 / ESP32
        S1[BMP280 Temp & Humidity] -->|I2C 0x76| MCU[MCU Core ARM Cortex-M]
        S2[ADXL345 Vibration Sensor] -->|SPI Bus| MCU
        MCU --> BUFFER[Flash Offline Ring Buffer]
        BUFFER --> TLS[MbedTLS / X.509 Crypto Engine]
    end

    subgraph AWS IoT Cloud Infrastructure
        TLS -- MQTT / TLS 8883 --> IOT[AWS IoT Core Message Broker]
        IOT --> RULE[AWS IoT SQL Rules Engine]
        RULE --> DYNAMO[(DynamoDB Time-Series Table)]
        RULE --> LAMBDA[AWS Lambda Ingestion Processor]
    end

    subgraph User Presentation Layer
        LAMBDA --> WS[WebSocket Real-Time Dispatcher]
        WS --> UI[Kernelwise Web Telemetry Dashboard]
        DYNAMO --> BI[Power BI / Grafana Historical Analytics]
    end
```

---

## 2. Telemetry Packet Schema

```json
{
  "device_id": "kw-node-stm32-042",
  "timestamp": 1729004812,
  "telemetry": {
    "temperature_c": 26.85,
    "humidity_pct": 54.2,
    "vibration_g": 0.042,
    "battery_mv": 3280
  },
  "diagnostics": {
    "uptime_seconds": 86420,
    "rssi_dbm": -68,
    "queued_buffer_records": 0
  }
}
```
