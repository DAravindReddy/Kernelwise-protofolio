"""
Privacy-Preserving Edge Metadata Filter
Ensures zero raw optical frames are transmitted or stored, emitting only anonymized vector coordinates.
"""

from typing import Dict
from src.edge_infer import InferenceResult


class PrivacyFilter:
    def format_telemetry_packet(self, device_id: str, result: InferenceResult) -> Dict:
        # Strict privacy filtering: purge all raw pixels, transmit bounding box metadata only
        return {
            "device_id": device_id,
            "privacy_compliance": "GDPR_ARTICLE_25_COMPLIANT_ZERO_RAW_PIXELS",
            "frame_id": result.frame_id,
            "fps": round(result.fps, 1),
            "inference_latency_ms": round(result.latency_ms, 1),
            "detected_entities_count": len(result.detections),
            "detections": [
                {
                    "class": d.class_name,
                    "confidence": d.confidence,
                    "bbox": d.bbox,
                }
                for d in result.detections
            ],
            "thermal_telemetry": {
                "peak_temperature_c": result.thermal.peak_temp_c,
                "mean_temperature_c": result.thermal.mean_temp_c,
                "hotspot_alert": result.thermal.hotspot_detected,
                "hotspot_coords": result.thermal.hotspot_location if result.thermal.hotspot_detected else None,
            },
        }
