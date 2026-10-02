"""
Automated Log Triage Scanner
Parses logs and categorizes crashes, warnings, memory leaks, and bus timeouts.
"""

import re
from typing import Dict, List


CRITICAL_PATTERNS = {
    "KERNEL_PANIC": re.compile(r"(kernel panic|unable to handle kernel null|oops:|fatal exception)", re.IGNORECASE),
    "OUT_OF_MEMORY": re.compile(r"(lowmemorykiller|oom-killer|out of memory|alloc_pages failed)", re.IGNORECASE),
    "BUS_TIMEOUT": re.compile(r"(transfer timed out|arbitration lost|i2c_transfer failed|spi_sync failed)", re.IGNORECASE),
    "ANDROID_ANR_CRASH": re.compile(r"(ANR in|FATAL EXCEPTION|TransactionTooLargeException)", re.IGNORECASE),
    "THERMAL_ALERT": re.compile(r"(critical temperature|thermal throttle|emergency poweroff)", re.IGNORECASE),
}


def triage_log_text(text: str) -> Dict[str, List[str]]:
    results = {k: [] for k in CRITICAL_PATTERNS}
    lines = text.splitlines()

    for idx, line in enumerate(lines):
        line_clean = line.strip()
        for cat, pattern in CRITICAL_PATTERNS.items():
            if pattern.search(line_clean):
                results[cat].append(f"Line {idx+1}: {line_clean}")

    return {k: v for k, v in results.items() if v}


def run_log_triage(text: str):
    print("====================================================================")
    print("   KERNELWISE LABS // AUTOMATED CRASH & LOG TRIAGE SCANNER          ")
    print("====================================================================")
    findings = triage_log_text(text)

    if not findings:
        print(" [OK] No fatal kernel panics, OOM kills, or hardware timeouts detected.")
    else:
        for category, matched_lines in findings.items():
            print(f"\n [!] Category: {category} ({len(matched_lines)} occurrences):")
            for m in matched_lines[:4]:
                print(f"     * {m}")
            if len(matched_lines) > 4:
                print(f"     * ... and {len(matched_lines) - 4} more occurrences.")

    print("====================================================================\n")
    return findings
