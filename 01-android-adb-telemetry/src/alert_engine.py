"""
Threshold and Anomaly Alert Engine for Android Device Health
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from src.collector import DeviceMetrics


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class Alert:
    severity: AlertSeverity
    rule: str
    message: str
    current_value: float
    threshold_value: float
    timestamp: float


class AlertEngine:
    def __init__(
        self,
        cpu_warn: float = 80.0,
        cpu_crit: float = 92.0,
        temp_warn: float = 48.0,
        temp_crit: float = 58.0,
        ram_warn_pct: float = 85.0,
        ram_crit_pct: float = 95.0,
    ):
        self.cpu_warn = cpu_warn
        self.cpu_crit = cpu_crit
        self.temp_warn = temp_warn
        self.temp_crit = temp_crit
        self.ram_warn_pct = ram_warn_pct
        self.ram_crit_pct = ram_crit_pct
        self._consecutive_cpu_spikes = 0

    def evaluate(self, metrics: DeviceMetrics) -> List[Alert]:
        alerts = []

        # 1. Thermal Throttling Alert
        if metrics.soc_temp_c >= self.temp_crit:
            alerts.append(
                Alert(
                    severity=AlertSeverity.CRITICAL,
                    rule="THERMAL_THROTTLE_DANGER",
                    message=f"SoC Temperature {metrics.soc_temp_c}°C exceeds critical threshold ({self.temp_crit}°C). Imminent hardware throttling or shutdown!",
                    current_value=metrics.soc_temp_c,
                    threshold_value=self.temp_crit,
                    timestamp=metrics.timestamp,
                )
            )
        elif metrics.soc_temp_c >= self.temp_warn:
            alerts.append(
                Alert(
                    severity=AlertSeverity.WARNING,
                    rule="THERMAL_ELEVATED",
                    message=f"SoC Temperature {metrics.soc_temp_c}°C is elevated. Check device airflow or ambient kiosk temp.",
                    current_value=metrics.soc_temp_c,
                    threshold_value=self.temp_warn,
                    timestamp=metrics.timestamp,
                )
            )

        # 2. CPU Saturation Alert
        if metrics.cpu_total_pct >= self.cpu_crit:
            self._consecutive_cpu_spikes += 1
            if self._consecutive_cpu_spikes >= 2:
                alerts.append(
                    Alert(
                        severity=AlertSeverity.CRITICAL,
                        rule="CPU_SATURATION_CRITICAL",
                        message=f"Sustained CPU usage {metrics.cpu_total_pct}% across {self._consecutive_cpu_spikes} cycles.",
                        current_value=metrics.cpu_total_pct,
                        threshold_value=self.cpu_crit,
                        timestamp=metrics.timestamp,
                    )
                )
        else:
            self._consecutive_cpu_spikes = 0

        # 3. RAM Pressure Alert
        if metrics.ram_used_pct >= self.ram_crit_pct:
            alerts.append(
                Alert(
                    severity=AlertSeverity.CRITICAL,
                    rule="LOW_MEMORY_KILLER_RISK",
                    message=f"RAM usage {metrics.ram_used_pct}% ({metrics.ram_used_mb}MB / {metrics.ram_total_mb}MB). High risk of Android LMK killing kiosk apps!",
                    current_value=metrics.ram_used_pct,
                    threshold_value=self.ram_crit_pct,
                    timestamp=metrics.timestamp,
                )
            )
        elif metrics.ram_used_pct >= self.ram_warn_pct:
            alerts.append(
                Alert(
                    severity=AlertSeverity.WARNING,
                    rule="RAM_ELEVATED",
                    message=f"RAM usage {metrics.ram_used_pct}% indicates potential background memory leak.",
                    current_value=metrics.ram_used_pct,
                    threshold_value=self.ram_warn_pct,
                    timestamp=metrics.timestamp,
                )
            )

        return alerts
