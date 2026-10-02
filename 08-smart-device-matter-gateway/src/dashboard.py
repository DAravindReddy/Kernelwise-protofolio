"""
Interactive Web Control Console for Matter Smart Device Edge Gateway
"""

import http.server
import json
import socketserver
import threading
from urllib.parse import parse_qs, urlparse
from src.gateway_daemon import MatterGatewayDaemon


HTML_MATTER_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Kernelwise Labs — Matter Smart Device Edge Gateway</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #090d16; color: #f1f5f9; margin: 0; padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 24px; }
        .brand { font-size: 20px; font-weight: bold; color: #38bdf8; }
        .badge { background: #0284c7; color: white; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #131c2e; border-radius: 12px; padding: 20px; border: 1px solid #233554; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3); }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .card-title { font-size: 16px; font-weight: 600; color: #f8fafc; }
        .ep-id { font-size: 12px; color: #64748b; font-family: monospace; }
        .btn { background: #0284c7; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 14px; transition: background 0.2s; }
        .btn:hover { background: #0369a1; }
        .btn-off { background: #334155; }
        .btn-locked { background: #15803d; }
        .btn-unlocked { background: #b91c1c; }
        .slider-box { margin-top: 16px; }
        .slider { width: 100%; }
        .commission-box { margin-top: 28px; background: #131c2e; padding: 18px; border-radius: 12px; border: 1px dashed #38bdf8; display: flex; gap: 12px; align-items: center; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="brand">KERNELWISE LABS // MATTER SMART DEVICE EDGE GATEWAY</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 4px;">CSA Matter 1.2 Protocol Bridge | Thread / BLE Local Mesh</div>
        </div>
        <div class="badge">Local Gateway Active</div>
    </div>

    <div class="grid" id="devices-grid">
        <!-- Rendered dynamically -->
    </div>

    <div class="commission-box">
        <strong style="color:#38bdf8;">Commission New Smart Device:</strong>
        <select id="new-dev-type" style="padding: 8px; background: #0f172a; color: white; border: 1px solid #334155; border-radius: 6px;">
            <option value="light">Dimmable Smart Light (Cluster 0x0006 / 0x0008)</option>
            <option value="sensor">Environmental Temp Sensor (Cluster 0x0402)</option>
            <option value="lock">Motorized Door Lock (Cluster 0x0101)</option>
        </select>
        <button class="btn" onclick="commissionDevice()">+ Pair & Commission</button>
    </div>

    <script>
        async function fetchState() {
            try {
                const res = await fetch('/api/matter/endpoints');
                const endpoints = await res.json();
                renderEndpoints(endpoints);
            } catch (err) {
                console.error(err);
            }
        }

        function renderEndpoints(endpoints) {
            const grid = document.getElementById('devices-grid');
            grid.innerHTML = endpoints.map(ep => {
                let controlsHtml = '';
                const clusters = ep.clusters;

                if (clusters.OnOff) {
                    const isOn = clusters.OnOff.on_off;
                    const level = clusters.LevelControl ? clusters.LevelControl.current_level : 254;
                    controlsHtml += `
                        <div style="margin-bottom: 12px;">
                            <button class="btn ${isOn ? '' : 'btn-off'}" onclick="sendCommand(${ep.endpoint_id}, 'onoff', 'toggle')">
                                ${isOn ? '💡 LIGHT: ON' : '⚫ LIGHT: OFF'}
                            </button>
                        </div>
                        <div class="slider-box">
                            <label style="font-size: 12px; color: #94a3b8;">Level Control (Brightness): ${Math.round(level/254*100)}%</label>
                            <input type="range" min="0" max="254" value="${level}" class="slider" onchange="sendLevel(${ep.endpoint_id}, this.value)">
                        </div>
                    `;
                } else if (clusters.DoorLock) {
                    const isLocked = clusters.DoorLock.lock_state === 1;
                    controlsHtml += `
                        <div>
                            <button class="btn ${isLocked ? 'btn-locked' : 'btn-unlocked'}" onclick="sendCommand(${ep.endpoint_id}, 'doorlock', '${isLocked ? 'unlock' : 'lock'}')">
                                ${isLocked ? '🔒 LOCKED (Click to Unlock)' : '🔓 UNLOCKED (Click to Lock)'}
                            </button>
                        </div>
                    `;
                } else if (clusters.TemperatureMeasurement) {
                    const rawVal = clusters.TemperatureMeasurement.measured_value || 2400;
                    const tempC = (rawVal / 100).toFixed(1);
                    controlsHtml += `
                        <div style="font-size: 32px; font-weight: bold; color: #38bdf8; margin: 12px 0;">
                            ${tempC} °C
                        </div>
                        <div style="font-size: 13px; color: #64748b;">Indoor Ambient Sensor (Matter Cluster 0x0402)</div>
                    `;
                }

                return `
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">${ep.device_type}</div>
                            <div class="ep-id">Endpoint #${ep.endpoint_id}</div>
                        </div>
                        ${controlsHtml}
                    </div>
                `;
            }).join('');
        }

        async function sendCommand(epId, cluster, cmd) {
            await fetch(`/api/matter/command?endpoint=${epId}&cluster=${cluster}&cmd=${cmd}`, { method: 'POST' });
            fetchState();
        }

        async function sendLevel(epId, level) {
            await fetch(`/api/matter/command?endpoint=${epId}&cluster=levelcontrol&cmd=move&level=${level}`, { method: 'POST' });
            fetchState();
        }

        async function commissionDevice() {
            const devType = document.getElementById('new-dev-type').value;
            await fetch(`/api/matter/commission?type=${devType}`, { method: 'POST' });
            fetchState();
        }

        setInterval(fetchState, 1500);
        fetchState();
    </script>
</body>
</html>
"""


class MatterWebDashboard:
    def __init__(self, daemon: MatterGatewayDaemon, port: int = 8084):
        self.daemon = daemon
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        daemon_ref = self.daemon

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                return

            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path == "/api/matter/endpoints":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(daemon_ref.get_all_endpoints()).encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(HTML_MATTER_DASHBOARD.encode("utf-8"))

            def do_POST(self):
                parsed = urlparse(self.path)
                qs = parse_qs(parsed.query)

                if parsed.path == "/api/matter/command":
                    ep_id = int(qs.get("endpoint", [1])[0])
                    cluster = qs.get("cluster", ["onoff"])[0]
                    cmd = qs.get("cmd", ["toggle"])[0]
                    params = {}
                    if "level" in qs:
                        params["level"] = int(qs["level"][0])
                    res = daemon_ref.execute_command(ep_id, cluster, cmd, params)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(res).encode("utf-8"))

                elif parsed.path == "/api/matter/commission":
                    dev_type = qs.get("type", ["light"])[0]
                    res = daemon_ref.commission_new_device(dev_type, f"Virtual {dev_type.capitalize()}")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(res).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()

        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[MATTER GATEWAY] Live Matter gateway dashboard active at: http://localhost:{self.port}")
