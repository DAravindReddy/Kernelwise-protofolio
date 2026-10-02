"""
Android ADB Telemetry Collector
Handles both live ADB devices via subprocess and synthetic mock device emulation.
"""

import math
import random
import re
import subprocess
import time
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProcessMetric:
    name: str
    pid: int
    cpu_pct: float


@dataclass
class DeviceMetrics:
    timestamp: float
    device_id: str
    cpu_user_pct: float
    cpu_kernel_pct: float
    cpu_total_pct: float
    ram_used_mb: float
    ram_total_mb: float
    ram_used_pct: float
    battery_level: int
    battery_temp_c: float
    soc_temp_c: float
    top_processes: List[Dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


class ADBBridge:
    def __init__(self, device_id: Optional[str] = None, mock: bool = False):
        self.device_id = device_id
        self.mock = mock
        self._sim_step = 0
        if not self.mock and not self._is_adb_available():
            print("[WARN] ADB CLI not found or device offline. Falling back to synthetic telemetry simulator.")
            self.mock = True

    def _is_adb_available(self) -> bool:
        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=2)
            lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and not l.startswith("List")]
            if lines:
                if not self.device_id:
                    self.device_id = lines[0].split("\t")[0]
                return True
            return False
        except Exception:
            return False

    def get_device_info(self) -> str:
        if self.mock:
            return f"SIMULATED_DEVICE_ARM64_V8A (ID: sim-{self.device_id or 'kiosk-01'})"
        return f"PHYSICAL_ANDROID_DEVICE (ID: {self.device_id})"

    def sample_telemetry(self) -> DeviceMetrics:
        if self.mock:
            return self._sample_synthetic()
        return self._sample_adb()

    def _sample_synthetic(self) -> DeviceMetrics:
        self._sim_step += 1
        now = time.time()
        # Create realistic thermal and load wave
        wave = math.sin(self._sim_step / 10.0)
        cpu_total = max(10.0, min(98.0, 45.0 + (wave * 35.0) + random.uniform(-4, 6)))
        cpu_user = round(cpu_total * 0.72, 1)
        cpu_kernel = round(cpu_total - cpu_user, 1)

        total_ram = 4096.0  # 4 GB
        base_ram = 2300.0 + (wave * 800.0) + random.uniform(-50, 50)
        ram_used = round(max(1200.0, min(3950.0, base_ram)), 1)
        ram_pct = round((ram_used / total_ram) * 100.0, 1)

        # Thermal rises when CPU is sustained
        soc_temp = round(38.0 + (cpu_total * 0.28) + random.uniform(-0.5, 0.5), 1)
        batt_temp = round(32.0 + (soc_temp * 0.3) + random.uniform(-0.2, 0.2), 1)

        top_procs = [
            {"name": "com.kiosk.posapp", "pid": 1420, "cpu_pct": round(cpu_user * 0.6, 1)},
            {"name": "system_server", "pid": 650, "cpu_pct": round(cpu_kernel * 0.8, 1)},
            {"name": "surfaceflinger", "pid": 480, "cpu_pct": round(random.uniform(4.0, 12.0), 1)},
            {"name": "com.android.chrome", "pid": 2980, "cpu_pct": round(random.uniform(1.0, 5.0), 1)},
        ]

        return DeviceMetrics(
            timestamp=now,
            device_id=self.device_id or "sim-kiosk-arm64",
            cpu_user_pct=cpu_user,
            cpu_kernel_pct=cpu_kernel,
            cpu_total_pct=round(cpu_total, 1),
            ram_used_mb=ram_used,
            ram_total_mb=total_ram,
            ram_used_pct=ram_pct,
            battery_level=max(15, int(95 - (self._sim_step % 60) * 0.5)),
            battery_temp_c=batt_temp,
            soc_temp_c=soc_temp,
            top_processes=top_procs,
        )

    def _sample_adb(self) -> DeviceMetrics:
        now = time.time()
        # Query battery
        res_batt = subprocess.run(
            ["adb", "-s", self.device_id, "shell", "dumpsys", "battery"],
            capture_output=True, text=True, timeout=3
        )
        batt_level = 100
        batt_temp = 35.0
        for line in res_batt.stdout.splitlines():
            if "level:" in line:
                m = re.search(r"level:\s*(\d+)", line)
                if m: batt_level = int(m.group(1))
            if "temperature:" in line:
                m = re.search(r"temperature:\s*(\d+)", line)
                if m: batt_temp = float(m.group(1)) / 10.0

        # Query memory
        res_mem = subprocess.run(
            ["adb", "-s", self.device_id, "shell", "dumpsys", "meminfo"],
            capture_output=True, text=True, timeout=3
        )
        ram_total = 4096.0
        ram_used = 2048.0
        for line in res_mem.stdout.splitlines():
            if "Total RAM:" in line:
                m = re.findall(r"[\d,]+", line)
                if m: ram_total = float(m[0].replace(",", "")) / 1024.0
            if "Used RAM:" in line:
                m = re.findall(r"[\d,]+", line)
                if m: ram_used = float(m[0].replace(",", "")) / 1024.0

        ram_pct = round((ram_used / ram_total) * 100.0, 1)

        # Query CPU
        res_cpu = subprocess.run(
            ["adb", "-s", self.device_id, "shell", "dumpsys", "cpuinfo"],
            capture_output=True, text=True, timeout=3
        )
        cpu_total = 25.0
        cpu_user = 18.0
        cpu_kernel = 7.0
        top_procs = []
        for line in res_cpu.stdout.splitlines()[:6]:
            if "TOTAL:" in line:
                m = re.search(r"([\d.]+)%\s*TOTAL.*([\d.]+)%\s*user.*([\d.]+)%\s*kernel", line)
                if m:
                    cpu_total = float(m.group(1))
                    cpu_user = float(m.group(2))
                    cpu_kernel = float(m.group(3))
            elif "%" in line:
                parts = line.strip().split()
                if len(parts) >= 3 and "%" in parts[0]:
                    try:
                        pct = float(parts[0].replace("%", ""))
                        proc_name = parts[-1]
                        top_procs.append({"name": proc_name, "pid": 0, "cpu_pct": pct})
                    except ValueError:
                        pass

        # Query thermal sysfs
        soc_temp = batt_temp + 4.5
        try:
            res_th = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "cat /sys/class/thermal/thermal_zone0/temp"],
                capture_output=True, text=True, timeout=2
            )
            raw_t = res_th.stdout.strip()
            if raw_t.isdigit():
                val = float(raw_t)
                soc_temp = val / 1000.0 if val > 1000 else val
        except Exception:
            pass

        return DeviceMetrics(
            timestamp=now,
            device_id=self.device_id,
            cpu_user_pct=cpu_user,
            cpu_kernel_pct=cpu_kernel,
            cpu_total_pct=cpu_total,
            ram_used_mb=round(ram_used, 1),
            ram_total_mb=round(ram_total, 1),
            ram_used_pct=ram_pct,
            battery_level=batt_level,
            battery_temp_c=batt_temp,
            soc_temp_c=soc_temp,
            top_processes=top_procs[:5],
        )
