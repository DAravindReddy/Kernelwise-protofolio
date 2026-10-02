"""
Kernelwise Labs — IoT Sensor-to-Cloud System Entrypoint
Runs both simulated hardware nodes and the cloud ingestion backend.
"""

import argparse
import sys
import time
from src.cloud_backend import CloudBackend
from src.dashboard import IoTWebDashboard
from src.sensor_node_sim import SensorNodeSimulator


def main():
    parser = argparse.ArgumentParser(description="Kernelwise Labs IoT Sensor-to-Cloud System")
    parser.add_argument("--nodes", type=int, default=2, help="Number of simulated STM32/ESP32 sensor nodes (default: 2)")
    parser.add_argument("--web", action="store_true", help="Launch live web dashboard on port 8082")
    parser.add_argument("--port", type=int, default=8082, help="Web dashboard port (default: 8082)")
    parser.add_argument("--cycles", type=int, default=8, help="Number of cycles to execute (0 for infinite)")
    parser.add_argument("--interval", type=float, default=1.0, help="Sampling interval in seconds (default: 1.0)")
    args = parser.parse_args()

    backend = CloudBackend()
    nodes = [SensorNodeSimulator(device_id=f"kw-stm32-node-{i+1:02d}") for i in range(args.nodes)]
    dashboard = IoTWebDashboard(backend=backend, port=args.port)

    print("====================================================================")
    print("   KERNELWISE LABS // IOT SENSOR-TO-CLOUD TELEMETRY ENGINE         ")
    print("====================================================================")
    print(f" Microcontroller Nodes : {args.nodes} active")
    print(f" Cloud Message Broker  : AWS IoT Core Emulated (MQTT/TLS)")
    print(f" Sampling Rate         : {args.interval}s")
    if args.web:
        if args.cycles == 8:
            args.cycles = 0  # Continuous mode when web UI is launched
        dashboard.start()
        print(f" [WEB] Dashboard active at http://localhost:{args.port} (Continuous server mode)")
    print(" Press Ctrl+C to terminate telemetry.\n")

    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            print(f"--- Telemetry Cycle #{cycle_count} ---")
            for node in nodes:
                payload = node.read_sensors()
                backend.ingest_payload(payload)
                print(
                    f" [{payload.device_id}] Temp: {payload.temperature_c:>5.2f}°C | "
                    f"Humidity: {payload.humidity_pct:>4.1f}% | "
                    f"Vibration: {payload.vibration_g:>5.3f}g | "
                    f"Battery: {payload.battery_mv}mV"
                )

            if args.cycles > 0 and cycle_count >= args.cycles:
                print(f"\n[INFO] Reached {args.cycles} cycles. Ingested total {len(backend.records)} telemetry frames.")
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[INFO] Telemetry stopped by user.")


if __name__ == "__main__":
    main()
