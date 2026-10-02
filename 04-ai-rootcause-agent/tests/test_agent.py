"""
Unit Tests for AI Root-Cause Diagnostic Agent
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.diagnostic_agent import DiagnosticAgent
from src.log_parser import LogParser


class TestDiagnosticAgent(unittest.TestCase):
    def setUp(self):
        self.kb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base", "failure_patterns.json")
        self.agent = DiagnosticAgent(self.kb_path)
        self.parser = LogParser()

    def test_log_parser_dmesg(self):
        raw = "[ 12.345] test_driver: error initializing hardware device"
        entries = self.parser.parse_text(raw)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].subsystem, "test_driver")
        self.assertEqual(entries[0].level, "ERROR")

    def test_null_pointer_diagnosis(self):
        log = "[ 10.001] Unable to handle kernel NULL pointer dereference at 00000000\n[ 10.002] Call Trace: [<ffff8000>] probe+0x10"
        report = self.agent.analyze_log(log)
        self.assertEqual(report.failure_type, "NULL_POINTER_DEREFERENCE")
        self.assertGreaterEqual(report.confidence_score, 0.65)
        self.assertGreater(len(report.remediation_steps), 0)

    def test_i2c_timeout_diagnosis(self):
        log = "[ 142.108] i2c-bcm2835 fe804000.i2c: transfer timed out\n[ 142.112] probe failed with error -110"
        report = self.agent.analyze_log(log)
        self.assertEqual(report.failure_type, "I2C_TRANSFER_TIMEOUT")
        self.assertIn("pull-up", " ".join(report.remediation_steps).lower())


if __name__ == "__main__":
    unittest.main()
