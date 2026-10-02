"""
Unit Tests for Project 02: Embedded Linux Bringup Contracts
"""

import os
import re
import unittest


class TestBringupContracts(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dts_path = os.path.join(self.base_dir, "dts", "bcm2711-kernelwise-sensor.dts")
        self.drv_path = os.path.join(self.base_dir, "drivers", "kernelwise_sensor.c")
        self.case_study_path = os.path.join(self.base_dir, "DEBUGGING_CASE_STUDY.md")

    def test_dts_file_exists_and_contains_valid_nodes(self):
        self.assertTrue(os.path.exists(self.dts_path))
        with open(self.dts_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("kernelwise,env-sensor-v1", content)
        self.assertIn("0x76", content)
        self.assertIn("interrupts", content)

    def test_c_driver_syntax_and_sysfs_attributes(self):
        self.assertTrue(os.path.exists(self.drv_path))
        with open(self.drv_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("kernelwise,env-sensor-v1", content)
        self.assertIn("DEVICE_ATTR_RO(temperature)", content)
        self.assertIn("DEVICE_ATTR_RO(pressure)", content)
        self.assertIn("DEVICE_ATTR_RW(sample_rate)", content)
        self.assertIn("module_i2c_driver", content)

    def test_case_study_documents_core_failures(self):
        self.assertTrue(os.path.exists(self.case_study_path))
        with open(self.case_study_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Clock Gate Deadlock", content)
        self.assertIn("I2C Bus Lockup", content)
        self.assertIn("Kernel Panic", content)


if __name__ == "__main__":
    unittest.main()
