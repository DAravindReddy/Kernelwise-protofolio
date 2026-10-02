"""
Unit Tests for Android ADB Telemetry and Alert Engine
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.alert_engine import AlertEngine, AlertSeverity
from src.collector import ADBBridge, DeviceMetrics


class TestTelemetryEngine(unittest.TestCase):
    def setUp(self):
        self.bridge = ADBBridge(mock=True)
        self.alert_engine = AlertEngine(temp_warn=45.0, temp_crit=55.0, ram_crit_pct=90.0)

    def test_mock_sampling(self):
        sample = self.bridge.sample_telemetry()
        self.assertIsInstance(sample, DeviceMetrics)
        self.assertGreater(sample.cpu_total_pct, 0.0)
        self.assertLessEqual(sample.cpu_total_pct, 100.0)
        self.assertGreater(sample.ram_used_mb, 500.0)
        self.assertGreater(sample.soc_temp_c, 20.0)

    def test_thermal_alert_critical(self):
        m = DeviceMetrics(
            timestamp=1000.0,
            device_id="test-phone",
            cpu_user_pct=40.0,
            cpu_kernel_pct=10.0,
            cpu_total_pct=50.0,
            ram_used_mb=2000.0,
            ram_total_mb=4096.0,
            ram_used_pct=48.8,
            battery_level=80,
            battery_temp_c=50.0,
            soc_temp_c=62.0,  # > 55.0 crit
        )
        alerts = self.alert_engine.evaluate(m)
        self.assertTrue(any(a.rule == "THERMAL_THROTTLE_DANGER" for a in alerts))
        crit = [a for a in alerts if a.rule == "THERMAL_THROTTLE_DANGER"][0]
        self.assertEqual(crit.severity, AlertSeverity.CRITICAL)

    def test_ram_pressure_alert(self):
        m = DeviceMetrics(
            timestamp=1000.0,
            device_id="test-phone",
            cpu_user_pct=20.0,
            cpu_kernel_pct=5.0,
            cpu_total_pct=25.0,
            ram_used_mb=3900.0,
            ram_total_mb=4096.0,
            ram_used_pct=95.2,  # > 90.0 crit
            battery_level=80,
            battery_temp_c=35.0,
            soc_temp_c=40.0,
        )
        alerts = self.alert_engine.evaluate(m)
        self.assertTrue(any(a.rule == "LOW_MEMORY_KILLER_RISK" for a in alerts))


if __name__ == "__main__":
    unittest.main()
