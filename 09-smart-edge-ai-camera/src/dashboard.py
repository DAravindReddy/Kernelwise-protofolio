"""
Real-Time Web Visualization Console for Edge AI Vision Appliance
"""

import http.server
import json
import socketserver
import threading
from src.edge_infer import EdgeInferenceEngine
from src.privacy_filter import PrivacyFilter


HTML_EDGE_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Kernelwise Labs — Edge AI Smart Camera & Thermal Anomaly Engine</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0a0a0f; color: #f3f4f6; margin: 0; padding: 24px; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; padding-bottom: 16px; margin-bottom: 24px; }
        .brand { font-size: 20px; font-weight: bold; color: #a855f7; }
        .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
        .canvas-card { background: #111827; border-radius: 12px; padding: 20px; border: 1px solid #374151; }
        .stats-card { background: #111827; border-radius: 12px; padding: 20px; border: 1px solid #374151; display: flex; flex-direction: column; gap: 16px; }
        .stat-block { background: #1f2937; padding: 14px; border-radius: 8px; border: 1px solid #4b5563; }
        .stat-title { font-size: 12px; text-transform: uppercase; color: #9ca3af; letter-spacing: 0.05em; }
        .stat-val { font-size: 28px; font-weight: 700; color: #f9fafb; margin-top: 4px; }
        .alert-box { padding: 14px; border-radius: 8px; font-size: 14px; font-weight: 600; }
        .alert-nom { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }
        .alert-crit { background: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; }
        canvas { background: #030712; border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto; display: block; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="brand">KERNELWISE LABS // SMART EDGE AI VISION APPLIANCE</div>
            <div style="font-size: 13px; color: #9ca3af; margin-top: 4px;">On-Device INT8 Inference | Optical Bounding Boxes + AMG8833 Thermal Infrared</div>
        </div>
        <div style="color: #a855f7; font-size: 14px; font-weight: 600;">GDPR-Compliant Metadata Stream</div>
    </div>

    <div class="grid">
        <div class="canvas-card">
            <div style="display:flex; justify-content:space-between; margin-bottom: 12px;">
                <span style="font-size: 14px; font-weight: 600; color:#e5e7eb;">Live Edge Inference View (640x480)</span>
                <span id="fps-counter" style="color: #10b981; font-weight: 700;">-- FPS</span>
            </div>
            <canvas id="viewCanvas" width="640" height="480"></canvas>
        </div>

        <div class="stats-card">
            <div class="stat-block">
                <div class="stat-title">Inference Throughput</div>
                <div class="stat-val" id="fps-val">-- FPS</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;" id="latency-val">Latency: -- ms</div>
            </div>

            <div class="stat-block">
                <div class="stat-title">Thermal Sensor Peak</div>
                <div class="stat-val" id="temp-val">-- °C</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;" id="mean-temp-val">Mean: -- °C</div>
            </div>

            <div id="alert-indicator" class="alert-box alert-nom">
                ✔ Thermal status nominal. No hotspots detected.
            </div>

            <div class="stat-block">
                <div class="stat-title">Cloud Bandwidth Saved</div>
                <div class="stat-val" style="color: #10b981;">99.4%</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">Zero video streaming. Transmitting metadata only.</div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('viewCanvas');
        const ctx = canvas.getContext('2d');

        async function fetchInference() {
            try {
                const res = await fetch('/api/edge/telemetry');
                const data = await res.json();

                document.getElementById('fps-counter').textContent = data.fps + ' FPS';
                document.getElementById('fps-val').textContent = data.fps + ' FPS';
                document.getElementById('latency-val').textContent = 'Latency: ' + data.inference_latency_ms + ' ms';
                document.getElementById('temp-val').textContent = data.thermal_telemetry.peak_temperature_c + ' °C';
                document.getElementById('mean-temp-val').textContent = 'Mean Ambient: ' + data.thermal_telemetry.mean_temperature_c + ' °C';

                const alertEl = document.getElementById('alert-indicator');
                if (data.thermal_telemetry.hotspot_alert) {
                    alertEl.className = 'alert-box alert-crit';
                    alertEl.textContent = '🔥 DANGER: Equipment Hotspot Detected (' + data.thermal_telemetry.peak_temperature_c + '°C)!';
                } else {
                    alertEl.className = 'alert-box alert-nom';
                    alertEl.textContent = '✔ Thermal status nominal. No hotspots detected.';
                }

                // Render Canvas Frame
                ctx.fillStyle = '#030712';
                ctx.fillRect(0, 0, 640, 480);

                // Draw Grid Lines (Synthetic camera view)
                ctx.strokeStyle = '#1f2937';
                ctx.lineWidth = 1;
                for (let x = 0; x < 640; x += 40) {
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 480); ctx.stroke();
                }
                for (let y = 0; y < 480; y += 40) {
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(640, y); ctx.stroke();
                }

                // Render Bounding Boxes
                data.detections.forEach(d => {
                    const [bx, by, bw, bh] = d.bbox;
                    ctx.strokeStyle = d.class === 'person' ? '#38bdf8' : '#a855f7';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(bx, by, bw, bh);

                    ctx.fillStyle = d.class === 'person' ? 'rgba(56, 189, 248, 0.15)' : 'rgba(168, 85, 247, 0.15)';
                    ctx.fillRect(bx, by, bw, bh);

                    ctx.fillStyle = d.class === 'person' ? '#38bdf8' : '#a855f7';
                    ctx.font = '13px monospace';
                    ctx.fillText(`${d.class} (${Math.round(d.confidence*100)}%)`, bx, by - 6);
                });

                // Render Thermal Hotspot if active
                if (data.thermal_telemetry.hotspot_alert && data.thermal_telemetry.hotspot_coords) {
                    const [hx, hy] = data.thermal_telemetry.hotspot_coords;
                    ctx.beginPath();
                    ctx.arc(hx, hy, 45, 0, 2 * Math.PI);
                    ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
                    ctx.fill();
                    ctx.strokeStyle = '#ef4444';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.fillStyle = '#fca5a5';
                    ctx.font = 'bold 12px sans-serif';
                    ctx.fillText(`HOTSPOT: ${data.thermal_telemetry.peak_temperature_c}°C`, hx - 50, hy - 50);
                }

            } catch (err) {
                console.error(err);
            }
        }

        setInterval(fetchInference, 100);
        fetchInference();
    </script>
</body>
</html>
"""


class EdgeAIWebDashboard:
    def __init__(self, engine: EdgeInferenceEngine, port: int = 8086):
        self.engine = engine
        self.port = port
        self.filter = PrivacyFilter()
        self.latest_packet = {}
        self.server = None
        self.thread = None

    def start(self):
        engine_ref = self.engine
        filter_ref = self.filter
        dashboard_ref = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                return

            def do_GET(self):
                if self.path == "/api/edge/telemetry":
                    res = engine_ref.process_frame()
                    packet = filter_ref.format_telemetry_packet("kw-edge-vision-01", res)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(packet).encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(HTML_EDGE_DASHBOARD.encode("utf-8"))

        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[EDGE AI] Live Edge AI vision console active at: http://localhost:{self.port}")
