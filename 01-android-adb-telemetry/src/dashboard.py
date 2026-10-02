"""
Terminal and Web Dashboard for Android ADB Telemetry
"""

import http.server
import json
import socketserver
import threading
from typing import List, Optional
from src.alert_engine import Alert, AlertSeverity
from src.collector import DeviceMetrics


HTML_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Kernelwise Labs — Android Device Health Monitor</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 16px; margin-bottom: 24px; }
        .brand { font-size: 20px; font-weight: bold; color: #38bdf8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .card { background: #1e293b; border-radius: 8px; padding: 20px; border: 1px solid #334155; }
        .card-title { font-size: 13px; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; margin-bottom: 8px; }
        .card-val { font-size: 32px; font-weight: 700; color: #f1f5f9; }
        .card-sub { font-size: 13px; color: #64748b; margin-top: 6px; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
        .badge-normal { background: #065f46; color: #6ee7b7; }
        .badge-warning { background: #854d0e; color: #fde047; }
        .badge-critical { background: #991b1b; color: #fca5a5; }
        .procs-table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }
        .procs-table th, .procs-table td { text-align: left; padding: 8px; border-bottom: 1px solid #334155; }
        .procs-table th { color: #94a3b8; }
        .alerts-box { background: #1e293b; border-radius: 8px; padding: 16px; border: 1px solid #334155; margin-top: 24px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">KERNELWISE LABS // ANDROID TELEMETRY FLEET ENGINE</div>
        <div id="device-id" style="color: #94a3b8; font-size: 14px;">Loading Device...</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Total CPU Load</div>
            <div class="card-val" id="cpu-total">--%</div>
            <div class="card-sub" id="cpu-breakdown">User: --% | Kernel: --%</div>
        </div>
        <div class="card">
            <div class="card-title">SoC Thermal Temp</div>
            <div class="card-val" id="soc-temp">--°C</div>
            <div class="card-sub" id="batt-temp">Battery: --°C</div>
        </div>
        <div class="card">
            <div class="card-title">RAM Utilization</div>
            <div class="card-val" id="ram-pct">--%</div>
            <div class="card-sub" id="ram-used">-- MB / -- MB</div>
        </div>
        <div class="card">
            <div class="card-title">Battery Status</div>
            <div class="card-val" id="batt-pct">--%</div>
            <div class="card-sub">Level Status: Active Monitoring</div>
        </div>
    </div>

    <div class="card">
        <div class="card-title">Top Active Device Processes</div>
        <table class="procs-table">
            <thead><tr><th>Process Name</th><th>PID</th><th>CPU Usage</th></tr></thead>
            <tbody id="procs-body"><tr><td colspan="3">Awaiting telemetry frames...</td></tr></tbody>
        </table>
    </div>

    <div class="alerts-box">
        <div class="card-title">Real-Time Threshold Alert Stream</div>
        <div id="alerts-stream" style="margin-top: 10px; font-size: 14px; color: #6ee7b7;">No critical alerts active. System nominal.</div>
    </div>

    <script>
        async function fetchMetrics() {
            try {
                const res = await fetch('/api/telemetry');
                const data = await res.json();
                document.getElementById('device-id').textContent = 'Target: ' + data.metrics.device_id;
                document.getElementById('cpu-total').textContent = data.metrics.cpu_total_pct + '%';
                document.getElementById('cpu-breakdown').textContent = `User: ${data.metrics.cpu_user_pct}% | Kernel: ${data.metrics.cpu_kernel_pct}%`;
                document.getElementById('soc-temp').textContent = data.metrics.soc_temp_c + '°C';
                document.getElementById('batt-temp').textContent = `Battery: ${data.metrics.battery_temp_c}°C`;
                document.getElementById('ram-pct').textContent = data.metrics.ram_used_pct + '%';
                document.getElementById('ram-used').textContent = `${data.metrics.ram_used_mb} MB / ${data.metrics.ram_total_mb} MB`;
                document.getElementById('batt-pct').textContent = data.metrics.battery_level + '%';

                const tbody = document.getElementById('procs-body');
                if (data.metrics.top_processes && data.metrics.top_processes.length > 0) {
                    tbody.innerHTML = data.metrics.top_processes.map(p => `
                        <tr>
                            <td style="font-family: monospace; color: #38bdf8;">${p.name}</td>
                            <td>${p.pid}</td>
                            <td><strong>${p.cpu_pct}%</strong></td>
                        </tr>
                    `).join('');
                }

                const alertBox = document.getElementById('alerts-stream');
                if (data.alerts && data.alerts.length > 0) {
                    alertBox.innerHTML = data.alerts.map(a => `
                        <div style="margin-bottom: 8px; padding: 8px; border-radius: 4px; background: ${a.severity === 'CRITICAL' ? '#450a0a' : '#422006'}; border-left: 4px solid ${a.severity === 'CRITICAL' ? '#ef4444' : '#f59e0b'};">
                            <strong>[${a.severity}] ${a.rule}:</strong> ${a.message}
                        </div>
                    `).join('');
                } else {
                    alertBox.innerHTML = '<span style="color: #6ee7b7;">✔ All operating parameters within safe tolerance limits.</span>';
                }
            } catch (err) {
                console.error(err);
            }
        }
        setInterval(fetchMetrics, 1000);
        fetchMetrics();
    </script>
</body>
</html>
"""


class TelemetryDashboard:
    def __init__(self, port: int = 8080):
        self.port = port
        self.latest_data = {"metrics": None, "alerts": []}
        self.server: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None

    def update(self, metrics: DeviceMetrics, alerts: List[Alert]):
        self.latest_data = {
            "metrics": metrics.to_dict(),
            "alerts": [
                {
                    "severity": a.severity.value,
                    "rule": a.rule,
                    "message": a.message,
                    "current": a.current_value,
                    "threshold": a.threshold_value,
                }
                for a in alerts
            ],
        }

    def print_terminal(self, metrics: DeviceMetrics, alerts: List[Alert]):
        print("\n" + "=" * 68)
        print(f" [KERNELWISE LABS] ANDROID HEALTH MONITOR | Target: {metrics.device_id}")
        print("=" * 68)
        print(f" CPU Total: {metrics.cpu_total_pct:>5.1f}%  [User: {metrics.cpu_user_pct:.1f}% | Kernel: {metrics.cpu_kernel_pct:.1f}%]")
        print(f" RAM Usage: {metrics.ram_used_pct:>5.1f}%  [{metrics.ram_used_mb:.0f} MB / {metrics.ram_total_mb:.0f} MB]")
        print(f" SoC Temp : {metrics.soc_temp_c:>5.1f}°C  | Battery: {metrics.battery_temp_c:.1f}°C ({metrics.battery_level}%)")
        print("-" * 68)
        print(" Top Processes:")
        for p in metrics.top_processes[:3]:
            print(f"   * {p['name']:<24} (PID: {p['pid']:<5}) -> {p['cpu_pct']:>5.1f}% CPU")
        if alerts:
            print("-" * 68)
            for a in alerts:
                prefix = "[CRITICAL ALERT]" if a.severity == AlertSeverity.CRITICAL else "[WARNING]"
                print(f" ! {prefix} {a.rule}: {a.message}")
        else:
            print("-" * 68)
            print(" Status: HEALTHY (All thermal and memory bounds nominal)")
        print("=" * 68)

    def start_web_server(self):
        dashboard_ref = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                return  # Suppress console logging

            def do_GET(self):
                if self.path == "/api/telemetry":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(dashboard_ref.latest_data).encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(HTML_DASHBOARD_TEMPLATE.encode("utf-8"))

        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[DASHBOARD] Live web dashboard active at: http://localhost:{self.port}")
