"""
Unit Tests for Developer Automation Toolkit
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kw_tools.log_triage import triage_log_text
from kw_tools.release_notes import parse_commits
from kw_tools.trace_analyzer import analyze_trace_data


class TestDeveloperToolkit(unittest.TestCase):
    def test_log_triage_patterns(self):
        log = "Kernel panic - not syncing: Fatal exception\ni2c-bcm2835: transfer timed out"
        res = triage_log_text(log)
        self.assertIn("KERNEL_PANIC", res)
        self.assertIn("BUS_TIMEOUT", res)

    def test_release_notes_parser(self):
        commits = [
            "1234567 feat: add telemetry dashboard",
            "89abcde fix: resolve memory leak in buffer",
            "fedcba0 docs: add wiring guide",
        ]
        cats, bump = parse_commits(commits)
        self.assertEqual(bump, "MINOR")
        self.assertEqual(len(cats["Features"]), 1)
        self.assertEqual(len(cats["Bug Fixes"]), 1)

    def test_trace_analyzer(self):
        trace = [
            "[TRACE] init_task took 10.5 ms",
            "[TRACE] slow_task took 350.0 ms",
        ]
        res = analyze_trace_data(trace)
        self.assertEqual(res["total_events"], 2)
        self.assertEqual(res["slowest"][0][0], "slow_task")


if __name__ == "__main__":
    unittest.main()
