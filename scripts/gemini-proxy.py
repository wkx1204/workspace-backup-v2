#!/usr/bin/env python3
"""
gemini-proxy.py
本地代理：将 /v1/embeddings 请求转发到 Gemini API
OpenClaw memory search 走这个本地代理，不受 DNS/代理限制
"""
import http.server, json, os, urllib.request, urllib.error

PORT = 8080
GEMINI_KEY = "AIzaSyAaVuxUeVCMy3zEhx_viw8snLmfj8D92Cg"
PROXY = "http://127.0.0.1:10808"

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _proxy_gemini(self, text):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={GEMINI_KEY}"
        data = json.dumps({
            "model": "models/gemini-embedding-001",
            "content": {"parts": [{"text": text}]}
        }).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        proxy_handler = urllib.request.ProxyHandler({"https": PROXY, "http": PROXY})
        opener = urllib.request.build_opener(proxy_handler)
        with opener.open(req, timeout=30) as r:
            return json.loads(r.read())

    def do_POST(self):
        try:
            cl = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(cl)) if cl else {}

            if self.path == "/v1/embeddings":
                model = data.get("model", "gemini-embedding-001")
                texts = data.get("input", [])
                if isinstance(texts, str):
                    texts = [texts]
                results = []
                for i, text in enumerate(texts):
                    try:
                        d = self._proxy_gemini(text)
                        emb = d.get("embedding", {}).get("values", [])
                        results.append({"object": "embedding", "embedding": emb, "index": i})
                    except Exception as e:
                        results.append({"object": "embedding", "embedding": [], "index": i, "error": str(e)})
                resp_data = json.dumps({"object": "list", "data": results, "model": model}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp_data)
                return

            self.send_error(404, "unsupported path")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, *args): pass

server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
print(f"Gemini proxy ready on 127.0.0.1:{PORT}", flush=True)
server.serve_forever()
