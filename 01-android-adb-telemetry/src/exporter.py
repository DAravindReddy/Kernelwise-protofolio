"""
Telemetry Exporter for JSON and CSV Logs
"""

import csv
import json
import os
from typing import List
from src.collector import DeviceMetrics


class TelemetryExporter:
    def __init__(self, output_dir: str = "logs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.csv_path = os.path.join(self.output_dir, "telemetry_stream.csv")
        self.json_path = os.path.join(self.output_dir, "telemetry_stream.json")
        self._init_csv()

    def _init_csv(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "device_id", "cpu_total_pct", "cpu_user_pct",
                    "cpu_kernel_pct", "ram_used_mb", "ram_total_mb", "ram_pct",
                    "soc_temp_c", "battery_temp_c", "battery_pct"
                ])

    def export_point(self, m: DeviceMetrics):
        # Append CSV
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                m.timestamp, m.device_id, m.cpu_total_pct, m.cpu_user_pct,
                m.cpu_kernel_pct, m.ram_used_mb, m.ram_total_mb, m.ram_used_pct,
                m.soc_temp_c, m.battery_temp_c, m.battery_level
            ])

        # Write latest snapshot JSON
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(m.to_dict(), f, indent=2)
