"""
Web Dashboard for IoT Sensor-to-Cloud Telemetry
"""

import http.server
import json
import socketserver
import threading
from src.cloud_backend import CloudBackend


HTML_IOT_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Kernelwise Labs — IoT Sensor Cloud Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b132b; color: #f8fafc; margin: 0; padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1c2541; padding-bottom: 16px; margin-bottom: 24px; }
        .brand { font-size: 20px; font-weight: bold; color: #48bfe3; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .card { background: #1c2541; border-radius: 8px; padding: 20px; border: 1px solid #3a506b; }
        .card-title { font-size: 13px; text-transform: uppercase; color: #8d99ae; letter-spacing: 0.05em; margin-bottom: 8px; }
        .card-val { font-size: 32px; font-weight: 700; color: #ffffff; }
        .card-sub { font-size: 13px; color: #6fffe9; margin-top: 6px; }
        .device-card { background: #1c2541; border-radius: 8px; padding: 18px; border: 1px solid #3a506b; margin-bottom: 16px; }
        .alerts-box { background: #2b1b22; border-radius: 8px; padding: 16px; border: 1px solid #772b3a; margin-top: 24px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">KERNELWISE LABS // INDUSTRIAL IOT FLEET TELEMETRY</div>
        <div id="status-badge" style="color: #6fffe9; font-size: 14px;">AWS IoT Core: Connected</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Active Field Nodes</div>
            <div class="card-val" id="nodes-count">--</div>
            <div class="card-sub">Protocols: MQTT / TLS 1.3</div>
        </div>
        <div class="card">
            <div class="card-title">Total Ingested Frames</div>
            <div class="card-val" id="ingested-count">--</div>
            <div class="card-sub">DynamoDB Time-Series Table</div>
        </div>
        <div class="card">
            <div class="card-title">Peak Vibration Observed</div>
            <div class="card-val" id="peak-vib">-- g</div>
            <div class="card-sub">ADXL345 High-G Sensor</div>
        </div>
    </div>

    <h2>Connected Microcontroller Nodes</h2>
    <div id="devices-container">Awaiting node telemetry stream...</div>

    <div class="alerts-box">
        <div class="card-title" style="color: #ff758f;">Recent Anomaly Rules Triggered</div>
        <div id="alerts-container" style="margin-top: 10px; font-size: 14px; color: #ffb3c1;">No active alerts. All machines within tolerance.</div>
    </div>

    <script>
        async function updateDashboard() {
            try {
                const res = await fetch('/api/iot');
                const data = await res.json();
                document.getElementById('nodes-count').textContent = data.active_devices.length;
                document.getElementById('ingested-count').textContent = data.total_ingested;

                let maxVib = 0;
                let html = '';
                for (const d of data.active_devices) {
                    if (d.vibration_g > maxVib) maxVib = d.vibration_g;
                    html += `
                        <div class="device-card">
                            <div style="display:flex; justify-content:space-between; margin-bottom: 8px;">
                                <strong style="color:#6fffe9; font-size: 16px;">Node: ${d.device_id}</strong>
                                <span style="font-size:12px; color:#8d99ae;">Firmware: ${d.firmware_version} | RSSI: ${d.rssi_dbm} dBm</span>
                            </div>
                            <div style="display:flex; gap: 24px; font-size: 14px;">
                                <div>Temp: <strong>${d.temperature_c}°C</strong></div>
                                <div>Humidity: <strong>${d.humidity_pct}%</strong></div>
                                <div>Vibration: <strong style="color: ${d.vibration_g > 0.15 ? '#ff758f' : '#6fffe9'}">${d.vibration_g} g</strong></div>
                                <div>Battery: <strong>${d.battery_mv} mV</strong></div>
                                <div>Seq: #${d.seq_num}</div>
                            </div>
                        </div>
                    `;
                }
                document.getElementById('peak-vib').textContent = maxVib.toFixed(3) + ' g';
                document.getElementById('devices-container').innerHTML = html || 'No active nodes.';

                const alertsEl = document.getElementById('alerts-container');
                if (data.recent_alerts && data.recent_alerts.length > 0) {
                    alertsEl.innerHTML = data.recent_alerts.map(a => `<div style="margin-bottom:6px;">⚠️ ${a}</div>`).join('');
                } else {
                    alertsEl.innerHTML = '<span style="color:#6fffe9;">✔ All operating parameters nominal.</span>';
                }
            } catch (err) {
                console.error(err);
            }
        }
        setInterval(updateDashboard, 1000);
        updateDashboard();
    </script>
</body>
</html>
"""


class IoTWebDashboard:
    def __init__(self, backend: CloudBackend, port: int = 8082):
        self.backend = backend
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        backend_ref = self.backend

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                return

            def do_GET(self):
                if self.path == "/api/iot":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(backend_ref.get_fleet_status()).encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(HTML_IOT_DASHBOARD.encode("utf-8"))

        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[IOT DASHBOARD] Live IoT web dashboard active at: http://localhost:{self.port}")
