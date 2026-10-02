"""
Unit Tests for Matter Smart Device Edge Gateway
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gateway_daemon import MatterGatewayDaemon
from src.matter_model import ClusterId


class TestMatterGateway(unittest.TestCase):
    def setUp(self):
        self.daemon = MatterGatewayDaemon()

    def test_initial_endpoints(self):
        self.assertIn(1, self.daemon.endpoints)
        self.assertIn(2, self.daemon.endpoints)
        self.assertIn(3, self.daemon.endpoints)

    def test_onoff_toggle(self):
        init_state = self.daemon.endpoints[1].clusters[ClusterId.ON_OFF].get_attr("on_off")
        res = self.daemon.execute_command(endpoint_id=1, cluster_name="onoff", command="toggle")
        self.assertTrue(res["success"])
        self.assertEqual(res["state"], not init_state)

    def test_level_control(self):
        res = self.daemon.execute_command(endpoint_id=1, cluster_name="levelcontrol", command="move", params={"level": 75})
        self.assertTrue(res["success"])
        self.assertEqual(res["current_level"], 75)

    def test_door_lock(self):
        res = self.daemon.execute_command(endpoint_id=3, cluster_name="doorlock", command="unlock")
        self.assertTrue(res["success"])
        self.assertEqual(res["lock_state"], 2)  # 2 = Unlocked

    def test_device_commissioning(self):
        res = self.daemon.commission_new_device(device_type="sensor", name="Attic Temp")
        self.assertTrue(res["success"])
        new_ep_id = res["endpoint_id"]
        self.assertIn(new_ep_id, self.daemon.endpoints)


if __name__ == "__main__":
    unittest.main()
