"""
Unit Tests for Smart Edge AI Vision Appliance
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.edge_infer import EdgeInferenceEngine, InferenceResult
from src.privacy_filter import PrivacyFilter


class TestEdgeAI(unittest.TestCase):
    def setUp(self):
        self.engine = EdgeInferenceEngine()
        self.filter = PrivacyFilter()

    def test_inference_frame_processing(self):
        res = self.engine.process_frame()
        self.assertIsInstance(res, InferenceResult)
        self.assertGreater(res.fps, 20.0)
        self.assertLess(res.latency_ms, 50.0)
        self.assertEqual(len(res.detections), 2)
        self.assertGreater(res.thermal.peak_temp_c, 20.0)

    def test_privacy_filter_compliance(self):
        res = self.engine.process_frame()
        packet = self.filter.format_telemetry_packet("test-cam-01", res)
        self.assertEqual(packet["device_id"], "test-cam-01")
        self.assertIn("GDPR", packet["privacy_compliance"])
        # Ensure no raw pixel buffers or image bytes exist
        self.assertNotIn("raw_image", packet)
        self.assertNotIn("pixels", packet)
        self.assertIn("detections", packet)
        self.assertIn("thermal_telemetry", packet)


if __name__ == "__main__":
    unittest.main()
