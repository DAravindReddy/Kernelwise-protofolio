"""
Unit Tests for IoT Sensor-to-Cloud Pipeline
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cloud_backend import CloudBackend
from src.sensor_node_sim import SensorNodeSimulator, SensorTelemetryPayload


class TestIoTPipeline(unittest.TestCase):
    def setUp(self):
        self.node = SensorNodeSimulator(device_id="test-node-01")
        self.backend = CloudBackend()

    def test_sensor_reading(self):
        payload = self.node.read_sensors()
        self.assertIsInstance(payload, SensorTelemetryPayload)
        self.assertEqual(payload.device_id, "test-node-01")
        self.assertGreater(payload.temperature_c, 10.0)
        self.assertLess(payload.temperature_c, 45.0)
        self.assertGreater(payload.battery_mv, 2500)

    def test_cloud_ingestion(self):
        payload = self.node.read_sensors()
        res = self.backend.ingest_payload(payload)
        self.assertEqual(res["status"], "INGESTED")
        status = self.backend.get_fleet_status()
        self.assertEqual(len(status["active_devices"]), 1)
        self.assertEqual(status["active_devices"][0]["device_id"], "test-node-01")

    def test_vibration_alert_trigger(self):
        # Force high vibration anomaly
        anom_payload = SensorTelemetryPayload(
            device_id="test-node-01",
            seq_num=99,
            timestamp=1000.0,
            temperature_c=25.0,
            humidity_pct=50.0,
            vibration_g=0.35,  # > 0.15 threshold
            battery_mv=3300,
            rssi_dbm=-60,
        )
        self.backend.ingest_payload(anom_payload)
        status = self.backend.get_fleet_status()
        self.assertTrue(any("CRITICAL VIBRATION" in a for a in status["recent_alerts"]))


if __name__ == "__main__":
    unittest.main()
