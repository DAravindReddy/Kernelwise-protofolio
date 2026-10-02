"""
Edge Vision & Thermal Anomaly Inference Engine
Simulates low-latency INT8 quantized computer vision on ARM64 Cortex-A53 / NPU.
"""

import math
import random
import time
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple


@dataclass
class DetectedObject:
    class_name: str
    confidence: float
    bbox: List[int]  # [x, y, width, height]


@dataclass
class ThermalAnalysis:
    peak_temp_c: float
    mean_temp_c: float
    hotspot_detected: bool
    hotspot_location: List[int]


@dataclass
class InferenceResult:
    frame_id: int
    timestamp: float
    fps: float
    latency_ms: float
    detections: List[DetectedObject]
    thermal: ThermalAnalysis

    def to_dict(self):
        return {
            "frame_id": self.frame_id,
            "timestamp": self.timestamp,
            "fps": round(self.fps, 1),
            "latency_ms": round(self.latency_ms, 1),
            "detections": [asdict(d) for d in self.detections],
            "thermal": asdict(self.thermal),
        }


class EdgeInferenceEngine:
    def __init__(self, target_fps: float = 35.0):
        self.target_fps = target_fps
        self.frame_counter = 0
        self._sim_time = 0

    def process_frame(self) -> InferenceResult:
        self.frame_counter += 1
        self._sim_time += 1
        t_start = time.time()

        # Simulate hardware NPU / NEON INT8 inference execution (25-30ms)
        latency_ms = random.uniform(26.5, 30.2)
        # Compute realistic FPS
        fps = 1000.0 / latency_ms

        # Generate realistic moving objects
        # Object 1: Person moving in front of camera
        x_pos = int(120 + 80 * math.sin(self._sim_time / 10.0))
        person = DetectedObject(
            class_name="person",
            confidence=round(random.uniform(0.91, 0.97), 2),
            bbox=[x_pos, 80, 140, 320],
        )

        # Object 2: Stationary Appliance / Machinery
        machinery = DetectedObject(
            class_name="commercial_appliance",
            confidence=round(random.uniform(0.88, 0.94), 2),
            bbox=[340, 100, 260, 340],
        )

        detections = [person, machinery]

        # Thermal Infrared Grid Simulation (8x8 Sensor interpolated)
        # Periodic thermal spike simulating overheating
        is_spike = (self._sim_time % 12 >= 8)
        base_temp = 32.5 + random.uniform(-0.5, 0.5)
        peak_temp = base_temp + (42.0 if is_spike else random.uniform(2.0, 5.0))
        hotspot_loc = [420, 220] if is_spike else [0, 0]

        thermal = ThermalAnalysis(
            peak_temp_c=round(peak_temp, 1),
            mean_temp_c=round(base_temp + 4.2, 1),
            hotspot_detected=is_spike,
            hotspot_location=hotspot_loc,
        )

        return InferenceResult(
            frame_id=self.frame_counter,
            timestamp=t_start,
            fps=fps,
            latency_ms=latency_ms,
            detections=detections,
            thermal=thermal,
        )
