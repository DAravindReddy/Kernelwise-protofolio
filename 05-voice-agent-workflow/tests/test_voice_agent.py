"""
Unit Tests for Voice Agent Workflow and Tool Execution
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.device_tools import check_warranty, schedule_rma_repair, trigger_remote_diagnostics
from src.voice_pipeline import VoiceAgentPipeline


class TestVoiceAgent(unittest.TestCase):
    def setUp(self):
        self.pipeline = VoiceAgentPipeline()

    def test_check_warranty(self):
        res = check_warranty("SN-88210")
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "ACTIVE")
        self.assertEqual(res["tier"], "Platinum Enterprise")

    def test_remote_diagnostics(self):
        res = trigger_remote_diagnostics("SN-88210")
        self.assertTrue(res["success"])
        self.assertGreater(res["temperature_c"], 40.0)
        self.assertIn("ERR_THERMAL_THROTTLE_ZONE2", res["errors"])

    def test_schedule_rma(self):
        res = schedule_rma_repair("SN-88210", "Overheating", "Friday at 10am")
        self.assertTrue(res["success"])
        self.assertIn("RMA-", res["ticket_id"])

    def test_end_to_end_voice_turn(self):
        reply, rec, tool_res = self.pipeline.process_utterance("Can you check the warranty on SN-88210?")
        self.assertIn("Platinum Enterprise", reply)
        self.assertLess(rec.total_latency_ms, 700.0)  # Sub-700ms verification


if __name__ == "__main__":
    unittest.main()
