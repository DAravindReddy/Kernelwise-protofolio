"""
Cloud Ingestion Backend & Telemetry Dispatcher
Emulates AWS IoT Core ingestion, validation, and historical time-series storage.
"""

from typing import Dict, List, Optional
from src.sensor_node_sim import SensorTelemetryPayload


class CloudBackend:
    def __init__(self, history_limit: int = 100):
        self.history_limit = history_limit
        self.records: List[Dict] = []
        self.latest_per_device: Dict[str, Dict] = {}
        self.alerts: List[str] = []

    def ingest_payload(self, payload: SensorTelemetryPayload) -> Dict:
        data = payload.to_dict()
        self.latest_per_device[payload.device_id] = data
        self.records.append(data)
        if len(self.records) > self.history_limit:
            self.records.pop(0)

        # Rule Engine: Anomaly detection
        if payload.vibration_g > 0.15:
            alert_msg = f"[CRITICAL VIBRATION] Node {payload.device_id} detected {payload.vibration_g}g abnormal peak!"
            self.alerts.append(alert_msg)
            if len(self.alerts) > 10:
                self.alerts.pop(0)

        if payload.temperature_c > 35.0:
            alert_msg = f"[HIGH TEMP ALERT] Node {payload.device_id} ambient temp {payload.temperature_c}°C elevated!"
            self.alerts.append(alert_msg)
            if len(self.alerts) > 10:
                self.alerts.pop(0)

        return {"status": "INGESTED", "records_stored": len(self.records)}

    def get_fleet_status(self) -> Dict:
        return {
            "active_devices": list(self.latest_per_device.values()),
            "total_ingested": len(self.records),
            "recent_alerts": self.alerts,
        }
