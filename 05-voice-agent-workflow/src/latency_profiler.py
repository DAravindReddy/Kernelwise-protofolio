"""
High-Precision Sub-Millisecond Latency Profiler for Real-Time Voice Pipelines
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TurnLatencyRecord:
    turn_id: int
    stt_latency_ms: float
    llm_decision_ms: float
    tool_exec_ms: float
    tts_ttft_ms: float
    total_latency_ms: float


class LatencyProfiler:
    def __init__(self):
        self.records: List[TurnLatencyRecord] = []

    def log_turn(self, turn_id: int, stt: float, llm: float, tool: float, tts: float) -> TurnLatencyRecord:
        rec = TurnLatencyRecord(
            turn_id=turn_id,
            stt_latency_ms=round(stt, 1),
            llm_decision_ms=round(llm, 1),
            tool_exec_ms=round(tool, 1),
            tts_ttft_ms=round(tts, 1),
            total_latency_ms=round(stt + llm + tool + tts, 1),
        )
        self.records.append(rec)
        return rec

    def compute_summary(self) -> Dict:
        if not self.records:
            return {"count": 0}
        totals = sorted(r.total_latency_ms for r in self.records)
        n = len(totals)
        p50 = totals[int(n * 0.50)]
        p95 = totals[min(n - 1, int(n * 0.95))]
        p99 = totals[min(n - 1, int(n * 0.99))]
        mean_val = sum(totals) / n
        return {
            "total_turns": n,
            "mean_ms": round(mean_val, 1),
            "p50_ms": round(p50, 1),
            "p95_ms": round(p95, 1),
            "p99_ms": round(p99, 1),
        }
