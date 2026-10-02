"""
Log Parser and Normalizer for Embedded Linux, Android, and Systems Telemetry
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ParsedLogEntry:
    raw_text: str
    timestamp: Optional[str] = None
    level: str = "INFO"
    subsystem: str = "system"
    message: str = ""
    is_stack_trace: bool = False


class LogParser:
    DMESG_PATTERN = re.compile(r"^\[\s*(\d+\.\d+)\]\s*(?:([a-zA-Z0-9_\-]+):\s*)?(.*)$")
    LOGCAT_PATTERN = re.compile(r"^(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+(\d+)\s+(\d+)\s+([VDIWEF])\s+([^:]+):\s*(.*)$")

    def parse_text(self, text: str) -> List[ParsedLogEntry]:
        entries = []
        for line in text.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            # Try Logcat
            m_logcat = self.LOGCAT_PATTERN.match(line_str)
            if m_logcat:
                level_map = {"V": "VERBOSE", "D": "DEBUG", "I": "INFO", "W": "WARN", "E": "ERROR", "F": "FATAL"}
                lvl = level_map.get(m_logcat.group(4), "INFO")
                entries.append(
                    ParsedLogEntry(
                        raw_text=line_str,
                        timestamp=m_logcat.group(1),
                        level=lvl,
                        subsystem=m_logcat.group(5).strip(),
                        message=m_logcat.group(6).strip(),
                        is_stack_trace="at " in line_str or "Exception" in line_str,
                    )
                )
                continue

            # Try Dmesg / Kernel
            m_dmesg = self.DMESG_PATTERN.match(line_str)
            if m_dmesg:
                msg = m_dmesg.group(3).strip()
                lvl = "ERROR" if any(w in msg.lower() for w in ["panic", "fault", "failed", "error", "timeout", "timed out"]) else "INFO"
                entries.append(
                    ParsedLogEntry(
                        raw_text=line_str,
                        timestamp=m_dmesg.group(1),
                        level=lvl,
                        subsystem=m_dmesg.group(2) or "kernel",
                        message=msg,
                        is_stack_trace="Call Trace:" in line_str or "[<" in line_str,
                    )
                )
                continue

            # Fallback Generic Entry
            lvl = "ERROR" if any(w in line_str.lower() for w in ["fatal", "critical", "error", "panic"]) else "INFO"
            entries.append(
                ParsedLogEntry(
                    raw_text=line_str,
                    timestamp=None,
                    level=lvl,
                    subsystem="generic",
                    message=line_str,
                    is_stack_trace="Call Trace:" in line_str or "backtrace" in line_str.lower(),
                )
            )

        return entries

    def extract_critical_signatures(self, entries: List[ParsedLogEntry]) -> List[str]:
        signatures = []
        for e in entries:
            if e.level in ["ERROR", "FATAL", "WARN"] or e.is_stack_trace:
                signatures.append(e.raw_text)
        return signatures or [e.raw_text for e in entries[:5]]
