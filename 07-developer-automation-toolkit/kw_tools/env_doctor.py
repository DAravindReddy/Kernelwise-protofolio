"""
Workstation Environment Diagnostic Tool
Verifies existence and versions of embedded engineering tools.
"""

import os
import shutil
import subprocess
from typing import Dict, List


TOOLS_TO_CHECK = [
    {"name": "Git", "binary": "git", "cmd": ["git", "--version"], "category": "VCS"},
    {"name": "Python 3", "binary": "python", "cmd": ["python", "--version"], "category": "Runtime"},
    {"name": "Android ADB", "binary": "adb", "cmd": ["adb", "version"], "category": "Mobile/Device"},
    {"name": "GCC / Clang", "binary": "gcc", "cmd": ["gcc", "--version"], "category": "Compiler"},
    {"name": "Docker", "binary": "docker", "cmd": ["docker", "--version"], "category": "Containers"},
    {"name": "ARM GCC", "binary": "arm-none-eabi-gcc", "cmd": ["arm-none-eabi-gcc", "--version"], "category": "Embedded Toolchain"},
    {"name": "QEMU ARM", "binary": "qemu-system-arm", "cmd": ["qemu-system-arm", "--version"], "category": "Emulator"},
]


def run_env_doctor():
    print("====================================================================")
    print("   KERNELWISE LABS // DEVELOPER WORKSTATION ENVIRONMENT DOCTOR     ")
    print("====================================================================")
    print(f" {'Category':<18} | {'Tool':<15} | {'Status':<10} | {'Details'}")
    print("-" * 68)

    passed = 0
    for item in TOOLS_TO_CHECK:
        path = shutil.which(item["binary"])
        status = "MISSING"
        details = "Not found in system PATH"
        if path:
            try:
                res = subprocess.run(item["cmd"], capture_output=True, text=True, timeout=2)
                first_line = (res.stdout or res.stderr).splitlines()
                ver = first_line[0] if first_line else "Available"
                status = "INSTALLED"
                details = ver[:32]
                passed += 1
            except Exception as e:
                status = "ERROR"
                details = str(e)[:30]

        tag = "[OK]      " if status == "INSTALLED" else "[OPTIONAL]"
        print(f" {item['category']:<18} | {item['name']:<15} | {tag} | {details}")

    print("--------------------------------------------------------------------")
    print(f" Audit Summary: {passed}/{len(TOOLS_TO_CHECK)} core engineering tools detected.")
    print("====================================================================\n")
    return passed
