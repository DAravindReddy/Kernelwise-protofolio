"""
Microcontroller Sensor Node Firmware Simulator (STM32 / ESP32)
Simulates I2C BMP280, SPI ADXL345, battery ADC, and MQTT payload serialization.
"""

import math
import random
import time
from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class SensorTelemetryPayload:
    device_id: str
    seq_num: int
    timestamp: float
    temperature_c: float
    humidity_pct: float
    vibration_g: float
    battery_mv: int
    rssi_dbm: int
    firmware_version: str = "v1.2.4-prod"

    def to_dict(self):
        return asdict(self)


class SensorNodeSimulator:
    def __init__(self, device_id: str = "kw-stm32-node-01"):
        self.device_id = device_id
        self.seq_num = 0
        self._sim_step = 0

    def read_sensors(self) -> SensorTelemetryPayload:
        self.seq_num += 1
        self._sim_step += 1
        now = time.time()

        # Simulate environmental temperature wave with small noise
        temp = 24.0 + 4.0 * math.sin(self._sim_step / 12.0) + random.uniform(-0.3, 0.3)
        humidity = 55.0 + 8.0 * math.cos(self._sim_step / 15.0) + random.uniform(-1.0, 1.0)

        # Baseline machine vibration (0.02g - 0.05g) with periodic vibration spike
        base_vib = random.uniform(0.015, 0.045)
        if self._sim_step % 15 == 0:
            base_vib += random.uniform(0.18, 0.45)  # Motor bearing transient

        # Battery slow discharge from 3300mV
        battery = max(2700, 3300 - (self._sim_step % 200))
        rssi = -65 + random.randint(-5, 4)

        return SensorTelemetryPayload(
            device_id=self.device_id,
            seq_num=self.seq_num,
            timestamp=now,
            temperature_c=round(temp, 2),
            humidity_pct=round(humidity, 1),
            vibration_g=round(base_vib, 3),
            battery_mv=battery,
            rssi_dbm=rssi,
        )
