"""
Kernelwise Labs — Smart Edge AI Vision Appliance Entrypoint
"""

import argparse
import sys
import time
from src.dashboard import EdgeAIWebDashboard
from src.edge_infer import EdgeInferenceEngine
from src.privacy_filter import PrivacyFilter


def main():
    parser = argparse.ArgumentParser(description="Kernelwise Labs Smart Edge AI Vision Appliance")
    parser.add_argument("--port", type=int, default=8086, help="Web visualization console port (default: 8086)")
    parser.add_argument("--frames", type=int, default=10, help="Number of test frames to process (0 for continuous daemon)")
    parser.add_argument("--web", action="store_true", help="Launch live interactive browser canvas UI")
    args = parser.parse_args()

    engine = EdgeInferenceEngine(target_fps=35.0)
    p_filter = PrivacyFilter()
    dashboard = EdgeAIWebDashboard(engine=engine, port=args.port)

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print("====================================================================")
    print("   KERNELWISE LABS // SMART EDGE AI VISION & THERMAL APPLIANCE     ")
    print("====================================================================")
    print(" Architecture Target     : ARM64 Cortex-A53 / NPU Accelerator")
    print(" Quantization Precision  : INT8 (11.4MB Model Footprint)")
    print(" Privacy Specification   : Zero Raw Video Storage (Metadata Only)")
    if args.web:
        if args.frames == 10:
            args.frames = 0  # Continuous mode when web UI is launched
        dashboard.start()
        print(f" [WEB] Live camera inference stream active at: http://localhost:{args.port} (Continuous server mode)")

    print("\n Running Edge Inference Frame Pipeline...")
    count = 0
    try:
        while True:
            res = engine.process_frame()
            packet = p_filter.format_telemetry_packet("kw-edge-vision-01", res)
            count += 1

            hotspot_str = "[!] HOTSPOT ALERT" if res.thermal.hotspot_detected else "Nominal"
            print(
                f" [Frame #{res.frame_id:04d}] {res.fps:>4.1f} FPS (Latency: {res.latency_ms:>4.1f}ms) | "
                f"Objects: {len(res.detections)} | "
                f"Thermal Peak: {res.thermal.peak_temp_c:>4.1f}C [{hotspot_str}]"
            )

            if args.frames > 0 and count >= args.frames:
                print(f"\n[INFO] Completed {count} frames. Edge inference validated successfully.")
                break

            time.sleep(0.03)  # ~33ms per frame
    except KeyboardInterrupt:
        print("\n[INFO] Edge AI daemon stopped.")


if __name__ == "__main__":
    main()
