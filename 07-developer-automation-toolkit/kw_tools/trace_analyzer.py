"""
Execution Trace and Bottleneck Profiler
"""

import re
from typing import Dict, List


def analyze_trace_data(trace_lines: List[str]) -> Dict:
    events = []
    # Pattern: function_name duration_ms or [TRACE] func took X ms
    pattern = re.compile(r"(?:\[TRACE\]\s+)?([a-zA-Z0-9_\-:]+)\s+(?:took\s+)?([\d.]+)\s*ms", re.IGNORECASE)

    for line in trace_lines:
        m = pattern.search(line)
        if m:
            func_name = m.group(1)
            dur = float(m.group(2))
            events.append((func_name, dur))

    if not events:
        return {"total_events": 0, "slowest": []}

    events.sort(key=lambda x: x[1], reverse=True)
    total_time = sum(d for _, d in events)

    return {
        "total_events": len(events),
        "total_duration_ms": round(total_time, 2),
        "slowest": events[:5],
    }
