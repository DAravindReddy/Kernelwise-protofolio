"""
Kernelwise Labs — Android Device Health Monitor Entrypoint
"""

import argparse
import sys
import time
from src.alert_engine import AlertEngine
from src.collector import ADBBridge
from src.dashboard import TelemetryDashboard
from src.exporter import TelemetryExporter


def main():
    parser = argparse.ArgumentParser(description="Android ADB Health & Telemetry Monitor (Kernelwise Labs)")
    parser.add_argument("--device", type=str, default=None, help="Specific ADB device serial ID")
    parser.add_argument("--mock", action="store_true", help="Force synthetic device telemetry emulator")
    parser.add_argument("--web", action="store_true", help="Enable browser web dashboard on port 8080")
    parser.add_argument("--port", type=int, default=8080, help="Web dashboard port (default: 8080)")
    parser.add_argument("--interval", type=float, default=1.5, help="Sampling interval in seconds (default: 1.5)")
    parser.add_argument("--cycles", type=int, default=10, help="Number of telemetry cycles to run (0 for infinite)")
    args = parser.parse_args()

    bridge = ADBBridge(device_id=args.device, mock=args.mock)
    alert_engine = AlertEngine()
    exporter = TelemetryExporter(output_dir="logs")
    dashboard = TelemetryDashboard(port=args.port)

    print("\n" + "=" * 60)
    print("   KERNELWISE LABS — ANDROID ADB TELEMETRY ENGINE")
    print("=" * 60)
    print(f" Target  : {bridge.get_device_info()}")
    print(f" Interval: {args.interval}s")
    if args.web:
        if args.cycles == 10:
            args.cycles = 0  # Continuous mode when web UI is launched
        dashboard.start_web_server()
        print(f" [WEB] Dashboard active at http://localhost:{args.port} (Continuous server mode)")
    print(" Press Ctrl+C to terminate monitor.\n")

    cycle_count = 0
    try:
        while True:
            metrics = bridge.sample_telemetry()
            alerts = alert_engine.evaluate(metrics)
            exporter.export_point(metrics)
            dashboard.update(metrics, alerts)
            dashboard.print_terminal(metrics, alerts)

            cycle_count += 1
            if args.cycles > 0 and cycle_count >= args.cycles:
                print(f"\n[INFO] Completed {cycle_count} sample cycles. Exporter logs saved to logs/.")
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[INFO] Monitor stopped by user.")


if __name__ == "__main__":
    main()
