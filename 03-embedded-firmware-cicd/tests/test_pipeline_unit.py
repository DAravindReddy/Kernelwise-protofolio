"""
Python Unit Tests for Embedded CI/CD Pipeline Components
"""

import os
import unittest


class TestFirmwareCIStructure(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.gh_workflow = os.path.join(self.base_dir, ".github", "workflows", "firmware_ci.yml")
        self.gitlab_ci = os.path.join(self.base_dir, ".gitlab-ci.yml")
        self.dockerfile = os.path.join(self.base_dir, "docker", "Dockerfile.embedded")
        self.benchmark = os.path.join(self.base_dir, "BENCHMARK_REPORT.md")

    def test_pipeline_files_exist(self):
        self.assertTrue(os.path.exists(self.gh_workflow))
        self.assertTrue(os.path.exists(self.gitlab_ci))
        self.assertTrue(os.path.exists(self.dockerfile))
        self.assertTrue(os.path.exists(self.benchmark))

    def test_workflow_has_required_stages(self):
        with open(self.gh_workflow, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("cppcheck", content)
        self.assertIn("arm-none-eabi", content)
        self.assertIn("qemu", content)
        self.assertIn("checksums.sha256", content)


if __name__ == "__main__":
    unittest.main()
