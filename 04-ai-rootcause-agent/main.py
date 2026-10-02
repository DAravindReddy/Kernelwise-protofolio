"""
AI Root-Cause Diagnostic Agent CLI Entrypoint
"""

import argparse
import os
import sys
from src.diagnostic_agent import DiagnosticAgent


def has_stdin_data() -> bool:
    if sys.stdin.isatty():
        return False
    if os.name == "nt":
        try:
            import msvcrt
            import ctypes
            handle = msvcrt.get_osfhandle(sys.stdin.fileno())
            avail = ctypes.c_ulong()
            res = ctypes.windll.kernel32.PeekNamedPipe(handle, None, 0, None, ctypes.byref(avail), None)
            return res != 0 and avail.value > 0
        except Exception:
            return False
    else:
        import select
        r, _, _ = select.select([sys.stdin], [], [], 0.0)
        return bool(r)


def main():
    parser = argparse.ArgumentParser(description="Kernelwise Labs AI Root-Cause Diagnostic Agent")
    parser.add_argument("--file", type=str, default=None, help="Path to log file (dmesg, logcat, syslog)")
    parser.add_argument("--log", type=str, default=None, help="Direct inline log string to diagnose")
    parser.add_argument("--benchmark", action="store_true", help="Run automated benchmark suite on canonical test cases")
    args = parser.parse_args()

    kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base", "failure_patterns.json")
    if not os.path.exists(kb_path):
        print(f"[FAIL] Knowledge base not found at: {kb_path}")
        sys.exit(1)

    if args.benchmark:
        from src.benchmark_runner import run_benchmark
        run_benchmark()
        return

    agent = DiagnosticAgent(kb_path)

    log_input = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            log_input = f.read()
    elif args.log:
        log_input = args.log
    elif has_stdin_data():
        log_input = sys.stdin.read()
    else:
        # Default sample incident for demonstration
        print("[INFO] No input provided. Analyzing simulated production Linux I2C lockup incident...\n")
        log_input = (
            "[  42.108] i2c-bcm2835 fe804000.i2c: transfer timed out\n"
            "[  42.112] kernelwise_sensor: probe failed with error -110\n"
            "[  42.115] i2c_transfer failed: arbitration lost or SDA held low by slave 0x76"
        )

    report = agent.analyze_log(log_input)

    print("====================================================================")
    print(f"   KERNELWISE LABS // AI DIAGNOSTIC REPORT [{report.incident_id}]")
    print("====================================================================")
    print(f" Subsystem        : {report.subsystem}")
    print(f" Failure Type     : {report.failure_type}")
    print(f" Confidence Score : {report.confidence_score*100:.1f}%")
    print(f" Knowledge Ref    : {report.matched_kb_id}")
    print("-" * 68)
    print(f" Root Cause Hypothesis:\n   {report.root_cause}")
    print("-" * 68)
    print(" Offending Log Evidence:")
    for line in report.evidence:
        print(f"   * {line}")
    print("-" * 68)
    print(" Actionable Remediation Runbook:")
    for idx, step in enumerate(report.remediation_steps):
        print(f"   {idx+1}. {step}")
    print("====================================================================\n")


if __name__ == "__main__":
    main()
