"""
Kernelwise Automation Toolkit Unified CLI Entrypoint
"""

import argparse
import os
import sys
from kw_tools.env_doctor import run_env_doctor
from kw_tools.log_triage import run_log_triage
from kw_tools.release_notes import generate_release_notes
from kw_tools.trace_analyzer import analyze_trace_data


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
    parser = argparse.ArgumentParser(
        prog="kw-tools",
        description="Kernelwise Labs — Developer Automation & Engineering Productivity Suite",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # env-doctor
    subparsers.add_parser("env-doctor", help="Audit local workstation developer tools")

    # log-triage
    triage_parser = subparsers.add_parser("log-triage", help="Scan logs for panics, OOMs, and bus errors")
    triage_parser.add_argument("--file", type=str, default=None, help="Path to log file")

    # release-notes
    rn_parser = subparsers.add_parser("release-notes", help="Generate SemVer changelog from git commits")
    rn_parser.add_argument("--current", type=str, default="v1.0.0", help="Current version tag (default: v1.0.0)")

    # trace-analyzer
    trace_parser = subparsers.add_parser("trace-analyzer", help="Profile execution trace bottlenecks")
    trace_parser.add_argument("--file", type=str, default=None, help="Path to trace file")

    args = parser.parse_args()

    if args.command == "env-doctor":
        run_env_doctor()
    elif args.command == "log-triage":
        log_text = ""
        if args.file:
            with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
                log_text = f.read()
        elif has_stdin_data():
            log_text = sys.stdin.read()
        else:
            log_text = (
                "[ 12.010] Kernel panic - not syncing: Fatal exception\n"
                "[ 12.015] LowMemoryKiller: Killing process com.pos.kiosk to free 512MB\n"
                "[ 14.500] i2c-bcm2835: transfer timed out"
            )
        run_log_triage(log_text)
    elif args.command == "release-notes":
        notes = generate_release_notes(args.current)
        print(notes)
    elif args.command == "trace-analyzer":
        sample_trace = [
            "[TRACE] init_device_tree took 12.4 ms",
            "[TRACE] probe_i2c_bus took 450.2 ms",
            "[TRACE] mount_rootfs took 820.5 ms",
            "[TRACE] start_telemetry_daemon took 22.1 ms",
        ]
        res = analyze_trace_data(sample_trace)
        print("====================================================================")
        print("   KERNELWISE LABS // TRACE BOTTLENECK PROFILER                    ")
        print("====================================================================")
        print(f" Total Events Profiled : {res['total_events']}")
        print(f" Total Cumulative Time : {res['total_duration_ms']} ms")
        print("\n Slowest Execution Bottlenecks:")
        for fn, dur in res["slowest"]:
            print(f"   * {fn:<26} -> {dur:>7.1f} ms")
        print("====================================================================\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
