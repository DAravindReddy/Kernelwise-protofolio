"""
Kernelwise Portfolio Unified Runner
Enables interactive or batch execution of all portfolio projects one by one.
"""

import os
import subprocess
import sys

PROJECTS = [
    {
        "id": "1",
        "name": "01-android-adb-telemetry",
        "title": "Android Device Health & ADB Telemetry Monitor",
        "command": [sys.executable, "main.py", "--mock", "--cycles", "3"],
        "web_command": [sys.executable, "main.py", "--mock", "--web", "--port", "8080", "--cycles", "0"],
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "Non-invasive thermal, CPU, RAM, and process telemetry daemon for Android fleets.",
    },
    {
        "id": "2",
        "name": "02-embedded-linux-bringup",
        "title": "Embedded Linux Board Bring-Up on ARM64",
        "command": [sys.executable, os.path.join("scripts", "simulate_bringup.py")],
        "web_command": None,
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "ARM64 DTS peripheral mapping, I2C kernel driver probe, and sysfs contract simulation.",
    },
    {
        "id": "3",
        "name": "03-embedded-firmware-cicd",
        "title": "Embedded Firmware CI/CD & QEMU Automation Pipeline",
        "command": [sys.executable, os.path.join("scripts", "run_pipeline_local.py")],
        "web_command": None,
        "test_command": [sys.executable, "-m", "unittest", os.path.join("tests", "test_pipeline_unit.py")],
        "description": "5-stage CI/CD pipeline: static analysis, unit tests, ARM build, QEMU boot, checksums.",
    },
    {
        "id": "4",
        "name": "04-ai-rootcause-agent",
        "title": "AI Root-Cause Diagnostic Agent",
        "command": [sys.executable, "main.py"],
        "benchmark_command": [sys.executable, "main.py", "--benchmark"],
        "web_command": None,
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "RAG semantic reasoning engine diagnosing Linux kernel panics and bus lockups in <50ms.",
    },
    {
        "id": "5",
        "name": "05-voice-agent-workflow",
        "title": "Low-Latency Voice Agent Workflow Engine",
        "command": [sys.executable, "main.py"],
        "web_command": None,
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "Sub-500ms voice pipeline for hardware diagnostics and automated RMA booking.",
    },
    {
        "id": "6",
        "name": "06-iot-sensor-to-cloud",
        "title": "IoT Sensor-to-Cloud System (STM32/ESP32 to AWS IoT)",
        "command": [sys.executable, "main.py", "--nodes", "2", "--cycles", "3"],
        "web_command": [sys.executable, "main.py", "--nodes", "2", "--web", "--port", "8082", "--cycles", "0"],
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "Multi-node microcontroller sensor telemetry ingestion with live anomaly detection.",
    },
    {
        "id": "7",
        "name": "07-developer-automation-toolkit",
        "title": "Developer Automation Toolkit (kw-tools)",
        "command": [sys.executable, "-m", "kw_tools.cli", "env-doctor"],
        "web_command": None,
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "CLI automation suite: workstation doctor, log triage scanner, and release notes generator.",
    },
    {
        "id": "8",
        "name": "08-smart-device-matter-gateway",
        "title": "Matter Smart Device Edge Gateway",
        "command": [sys.executable, "main.py"],
        "web_command": [sys.executable, "main.py", "--web", "--port", "8084"],
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "CSA Matter 1.2 edge bridge for lights, locks, sensors with cluster command dispatcher.",
    },
    {
        "id": "9",
        "name": "09-smart-edge-ai-camera",
        "title": "Smart Edge AI Vision & Thermal Anomaly Appliance",
        "command": [sys.executable, "main.py", "--frames", "5"],
        "web_command": [sys.executable, "main.py", "--web", "--port", "8086", "--frames", "0"],
        "test_command": [sys.executable, "-m", "unittest", "discover", "tests"],
        "description": "35+ FPS on-device INT8 computer vision and AMG8833 thermal grid analysis.",
    },
]


def print_banner():
    print("=" * 70)
    print("      KERNELWISE LABS // PORTFOLIO UNIFIED EXECUTION ENGINE      ")
    print("=" * 70)


def list_projects():
    print_banner()
    print("Available Projects to Execute:\n")
    for p in PROJECTS:
        print(f" [{p['id']}] {p['title']}")
        print(f"     Directory   : {p['name']}")
        print(f"     Description : {p['description']}\n")
    print("=" * 70)


def execute_project(proj: dict, mode: str = "run") -> bool:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.join(root_dir, proj["name"])

    if mode == "web":
        if not proj.get("web_command"):
            print(f"\n[INFO] {proj['name']} does not have a dedicated web dashboard.")
            return True
        cmd = proj["web_command"]
    elif mode == "test":
        cmd = proj["test_command"]
    elif mode == "benchmark" and proj.get("benchmark_command"):
        cmd = proj["benchmark_command"]
    else:
        cmd = proj["command"]

    print("\n" + "=" * 70)
    print(f" >> EXECUTING [{proj['id']}/9]: {proj['title']}")
    print(f" >> Working Dir : {proj['name']}")
    print(f" >> Command     : {' '.join(cmd)}")
    print("=" * 70 + "\n")

    try:
        ret = subprocess.run(cmd, cwd=proj_dir)
        success = (ret.returncode == 0)
    except Exception as e:
        print(f"\n[ERROR] Execution failed with exception: {e}")
        success = False

    if success:
        print(f"\n [PASS] {proj['name']} finished successfully.")
    else:
        print(f"\n [FAIL] {proj['name']} exited with non-zero status.")
    return success


def run_all_sequentially(mode: str = "run"):
    print_banner()
    print(f"Starting sequential one-by-one execution of all 9 projects (mode: {mode})...\n")

    results = []
    for proj in PROJECTS:
        success = execute_project(proj, mode=mode)
        results.append((proj["title"], success))
        print("\n" + "-" * 70)

    print("\n" + "=" * 70)
    print("                     EXECUTION SUMMARY")
    print("=" * 70)
    all_ok = True
    for title, success in results:
        status_str = "[PASS]" if success else "[FAIL]"
        if not success:
            all_ok = False
        print(f" {status_str} {title}")
    print("=" * 70)
    if all_ok:
        print(" [ALL PASSED] All portfolio projects executed successfully!")
    else:
        print(" [ATTENTION] One or more projects reported failures.")
    print("=" * 70 + "\n")


def launch_website(port: int = 3000):
    import http.server
    import socketserver
    socketserver.TCPServer.allow_reuse_address = True
    print("\n" + "=" * 70)
    print("   KERNELWISE LABS // CLIENT-FACING ORGANIZATION WEBSITE")
    print("=" * 70)
    print(f" [WEBSITE] Live at: http://localhost:{port}")
    print(" [WEBSITE] Press Ctrl+C in this terminal when finished to return.\n")
    try:
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Website server stopped.")


def interactive_menu():
    while True:
        print_banner()
        print("Select an option to execute:")
        for p in PROJECTS:
            web_tag = " (+Web UI)" if p.get("web_command") else ""
            print(f"  {p['id']}) {p['title']}{web_tag}")
        print("  -------------------------------------------------------------")
        print("  W) Launch Client Organization Website (http://localhost:3000)")
        print("  A) Run ALL projects one by one (Sequential Run)")
        print("  T) Run ALL project unit test suites")
        print("  L) List project details")
        print("  Q) Quit")
        print("=" * 70)

        choice = input("Enter your choice (1-9, W, A, T, L, Q): ").strip().upper()

        if choice == "Q":
            print("\nExiting. Happy engineering!")
            break
        elif choice == "W":
            launch_website()
            input("\nPress Enter to return to menu...")
        elif choice == "A":
            run_all_sequentially(mode="run")
            input("\nPress Enter to return to menu...")
        elif choice == "T":
            run_all_sequentially(mode="test")
            input("\nPress Enter to return to menu...")
        elif choice == "L":
            list_projects()
            input("\nPress Enter to return to menu...")
        else:
            match = next((p for p in PROJECTS if p["id"] == choice), None)
            if match:
                if match.get("web_command"):
                    sub = input(f"Run mode for {match['title']} - [1] Standard CLI demo (default), [2] Web Dashboard, [3] Tests: ").strip()
                    if sub == "2":
                        execute_project(match, mode="web")
                    elif sub == "3":
                        execute_project(match, mode="test")
                    else:
                        execute_project(match, mode="run")
                else:
                    sub = input(f"Run mode for {match['title']} - [1] Standard CLI demo (default), [2] Tests: ").strip()
                    if sub == "2":
                        execute_project(match, mode="test")
                    else:
                        execute_project(match, mode="run")
                input("\nPress Enter to return to menu...")
            else:
                print(f"\n[!] Invalid selection '{choice}'. Please try again.\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Kernelwise Labs Portfolio Master Runner")
    parser.add_argument("--project", "-p", type=str, help="Project number (1-9) or directory name to execute")
    parser.add_argument("--all", "-a", action="store_true", help="Execute all 9 projects sequentially one by one")
    parser.add_argument("--test-all", "-t", action="store_true", help="Run test suites for all 9 projects")
    parser.add_argument("--web", "-w", action="store_true", help="Launch web dashboard for the specified project")
    parser.add_argument("--website", action="store_true", help="Launch the client-facing organization website on port 3000")
    parser.add_argument("--list", "-l", action="store_true", help="List all portfolio projects")
    args = parser.parse_args()

    if args.website:
        launch_website()
        return

    if args.list:
        list_projects()
        return

    if args.all:
        run_all_sequentially(mode="run")
        return

    if args.test_all:
        run_all_sequentially(mode="test")
        return

    if args.project:
        query = args.project.strip().lower()
        match = next((p for p in PROJECTS if p["id"] == query or query in p["name"].lower()), None)
        if match:
            mode = "web" if args.web else "run"
            execute_project(match, mode=mode)
        else:
            print(f"[ERROR] Could not find project matching '{args.project}'. Use --list to see available projects.")
        return

    # If no CLI arguments provided and running interactively, show interactive menu
    if sys.stdin.isatty():
        interactive_menu()
    else:
        # Default non-interactive behavior: list available options
        list_projects()
        print("\nTip: Run 'python run_portfolio.py --all' to execute all projects sequentially,")
        print("     or 'python run_portfolio.py --project <1-9>' to run an individual project.")


if __name__ == "__main__":
    main()
