# api/server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, base64, re
from urllib.parse import urlparse
from pathlib import Path

DATA_FILE = Path("../data/transactions.json").resolve()  # relative to api/; adjust if needed
# Simple credentials for Basic Auth (for assignment use)
AUTH_USERS = {"admin": "password123"}  # change before final push to non-sensitive value

HOST = "127.0.0.1"
PORT = 8000

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    return []

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

TRANSACTIONS = load_data()

def check_auth_header(header):
    if not header:
        return False
    try:
        scheme, b64 = header.split(" ", 1)
        if scheme != "Basic":
            return False
        decoded = base64.b64decode(b64).decode()
        username, password = decoded.split(":", 1)
        return AUTH_USERS.get(username) == password
    except Exception:
        return False

class SimpleHandler(BaseHTTPRequestHandler):
    def _require_auth(self):
        h = self.headers.get("Authorization")
        if not check_auth_header(h):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return False
        return True

    def _send_json(self, status, obj):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj, indent=2, ensure_ascii=False).encode())

    def do_GET(self):
        if not self._require_auth():
            return
        parsed = urlparse(self.path)
        m = re.match(r"^/transactions/?$", parsed.path)
        m_id = re.match(r"^/transactions/([^/]+)/?$", parsed.path)
        if m:
            # list all
            self._send_json(200, TRANSACTIONS)
        elif m_id:
            tid = m_id.group(1)
            for tx in TRANSACTIONS:
                if tx.get("txn_external_id") == tid:
                    self._send_json(200, tx)
                    return
            self._send_json(404, {"error": "Not found"})
        else:
            self._send_json(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        if not self._require_auth():
            return
        parsed = urlparse(self.path)
        if parsed.path != "/transactions":
            self._send_json(404, {"error": "Unknown endpoint"})
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        try:
            obj = json.loads(body)
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return
        # require txn_external_id unique
        if any(tx.get("txn_external_id") == obj.get("txn_external_id") for tx in TRANSACTIONS):
            self._send_json(409, {"error": "Transaction ID already exists"})
            return
        TRANSACTIONS.append(obj)
        save_data(TRANSACTIONS)
        self._send_json(201, obj)

    def do_PUT(self):
        if not self._require_auth():
            return
        m_id = re.match(r"^/transactions/([^/]+)/?$", self.path)
        if not m_id:
            self._send_json(404, {"error": "Unknown endpoint"})
            return
        tid = m_id.group(1)
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        try:
            obj = json.loads(body)
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return
        for i, tx in enumerate(TRANSACTIONS):
            if tx.get("txn_external_id") == tid:
                # update fields (overwrite)
                TRANSACTIONS[i].update(obj)
                save_data(TRANSACTIONS)
                self._send_json(200, TRANSACTIONS[i])
                return
        self._send_json(404, {"error": "Not found"})

    def do_DELETE(self):
        if not self._require_auth():
            return
        m_id = re.match(r"^/transactions/([^/]+)/?$", self.path)
        if not m_id:
            self._send_json(404, {"error": "Unknown endpoint"})
            return
        tid = m_id.group(1)
        for i, tx in enumerate(TRANSACTIONS):
            if tx.get("txn_external_id") == tid:
                removed = TRANSACTIONS.pop(i)
                save_data(TRANSACTIONS)
                self._send_json(200, {"deleted": removed})
                return
        self._send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        # quiet stdout; or use print if debugging
        return

if __name__ == "__main__":
    # Ensure data file is in a known location relative to repo root
    print(f"Using data file: {DATA_FILE}")
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f"Server running at http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()