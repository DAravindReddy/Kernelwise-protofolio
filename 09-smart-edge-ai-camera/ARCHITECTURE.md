# Project 09: Architecture Specification — Smart Edge AI Vision Appliance

## 1. Edge Inference Pipeline Block Diagram

```mermaid
flowchart TD
    subgraph Multi-Modal Edge Sensors
        CAM[CMOS Image Sensor: 640x480 @ 30FPS] --> ISP[Hardware Video Processing]
        TH[AMG8833 8x8 IR Thermal Sensor] --> I2C[I2C Bus Controller]
    end

    subgraph On-Device Edge AI Runtime: ARM Cortex-A53 / NPU
        ISP --> FRAME_BUF[Volatile Frame Buffer]
        FRAME_BUF --> NPU[INT8 Quantized Neural Engine: MobileNet/YOLO]
        I2C --> THERMAL_ENG[Thermal Grid Correlator]
        
        NPU --> ANOMALY{Thermal / Object Anomaly?}
        THERMAL_ENG --> ANOMALY
        
        FRAME_BUF -->|IMMEDIATELY ZEROED / PURGED| PURGE[(No Video Stored or Sent)]
    end

    subgraph Privacy-Preserving Metadata Broadcaster
        ANOMALY --> PRIV[Privacy Filter: Bounding Boxes & Hotspots]
        PRIV --> MQTT[MQTT / WebSocket Metadata Stream]
    end

    subgraph Presentation & Fleet Alerting
        MQTT --> UI[Interactive Edge Dashboard: Port 8086]
        MQTT --> SMS[SMS / Email Factory Overheat Alert]
    end
```

---

## 2. Privacy-Preserving Metadata Schema

```json
{
  "device_id": "kw-edge-vision-01",
  "timestamp": 1729008920.45,
  "inference_fps": 35.2,
  "inference_latency_ms": 28.4,
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.94,
      "bbox": [120, 45, 280, 410]
    },
    {
      "class_name": "industrial_oven",
      "confidence": 0.89,
      "bbox": [320, 110, 600, 460]
    }
  ],
  "thermal_analysis": {
    "peak_temp_c": 78.4,
    "mean_temp_c": 32.1,
    "hotspot_detected": true,
    "hotspot_location": [450, 210]
  }
}
```
