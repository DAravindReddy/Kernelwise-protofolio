"""
Intelligent Diagnostic Agent for Systems Failures
Combines log parsing, vector retrieval, and deterministic reasoning.
"""

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional
from src.log_parser import LogParser, ParsedLogEntry
from src.rag_engine import RAGEngine


@dataclass
class DiagnosticReport:
    incident_id: str
    subsystem: str
    failure_type: str
    root_cause: str
    confidence_score: float
    evidence: List[str]
    matched_kb_id: str
    remediation_steps: List[str]

    def to_dict(self):
        return asdict(self)


class DiagnosticAgent:
    def __init__(self, kb_path: str):
        self.parser = LogParser()
        self.rag = RAGEngine(kb_path)
        self._incident_seq = 100

    def analyze_log(self, raw_log_text: str) -> DiagnosticReport:
        self._incident_seq += 1
        incident_id = f"INC-2026-{self._incident_seq:04d}"

        entries = self.parser.parse_text(raw_log_text)
        signatures = self.parser.extract_critical_signatures(entries)
        combined_query = " ".join(signatures)

        # Query RAG Vector Index
        results = self.rag.query(combined_query, top_k=1)

        if not results or results[0][1] < 0.10:
            return DiagnosticReport(
                incident_id=incident_id,
                subsystem="Unknown",
                failure_type="GENERIC_UNCLASSIFIED",
                root_cause="Log signatures do not match known critical kernel or hardware failure patterns.",
                confidence_score=0.20,
                evidence=signatures[:3],
                matched_kb_id="NONE",
                remediation_steps=[
                    "Check device dmesg and syslog with verbose debug flags enabled",
                    "Verify power supply stability and hardware peripheral connections"
                ],
            )

        best_match, raw_score = results[0]
        # Calibrate confidence score
        confidence = min(0.99, max(0.65, raw_score * 1.35))

        return DiagnosticReport(
            incident_id=incident_id,
            subsystem=best_match["subsystem"],
            failure_type=best_match["failure_type"],
            root_cause=best_match["root_cause"],
            confidence_score=round(confidence, 3),
            evidence=signatures[:4],
            matched_kb_id=best_match["id"],
            remediation_steps=best_match["remediation"],
        )
