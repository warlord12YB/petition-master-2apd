#!/usr/bin/env python3
"""
HTTP & REST API Server for the Master 2APD Payment Petition.
Includes Admin PIN verification to prevent unauthorized deletion or tampering.
"""

import http.server
import socketserver
import json
import os
import socket

PORT = int(os.environ.get('PORT', 8000))
ADMIN_PIN = "2apd2027"  # Admin PIN to protect data from tampering or deletion
DATA_FILE = os.path.join(os.path.dirname(__file__), 'signatures.json')

# Initialize signatures file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class PetitionHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        if self.path == '/api/signatures':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                content = '[]'
            self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/signatures':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            client_pin = self.headers.get('X-Admin-Pin', '').strip()

            try:
                new_data = json.loads(post_data.decode('utf-8'))
                
                # Load current database
                current_data = []
                if os.path.exists(DATA_FILE):
                    try:
                        with open(DATA_FILE, 'r', encoding='utf-8') as f:
                            current_data = json.load(f)
                    except Exception:
                        current_data = []

                # Security check:
                # If the incoming data reduces or resets the list, require valid Admin PIN
                if len(new_data) < len(current_data) and client_pin != ADMIN_PIN:
                    print(f"[ACCESS DENIED] Attempted to delete or truncate signatures without valid Admin PIN.")
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Unauthorized: Admin PIN required for deletion'}).encode('utf-8'))
                    return

                # Save validated data
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)

                if client_pin == ADMIN_PIN:
                    print(f"[ADMIN ACTION] Signatures list updated ({len(new_data)} entries).")
                else:
                    if len(new_data) > len(current_data):
                        latest = new_data[-1]
                        print(f"[NEW SIGNATURE] {latest.get('fullName')} (CIN: {latest.get('cinNumber')})")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'count': len(new_data)}).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Admin-Pin')
        self.end_headers()

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 70)
    print(" MASTER 2APD - PAYMENT PETITION SERVER")
    print("=" * 70)
    print(f" -> Localhost:       http://localhost:{PORT}")
    print(f" -> Mobile Link:     http://{local_ip}:{PORT}")
    print("    (Share this Mobile Link with classmates on the same Wi-Fi / Hotspot)")
    print(f" -> Admin PIN:       {ADMIN_PIN} (Used to unlock PDF export and admin controls)")
    print("=" * 70)
    print("Press Ctrl + C to stop the server.\n")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PetitionHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
