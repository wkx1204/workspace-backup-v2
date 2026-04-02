#!/usr/bin/env python3
"""图片上传服务器 - 18790端口（加固版）"""
import http.server, json, os, socketserver, sys, time, cgi, signal
from pathlib import Path
import urllib.request
import urllib.error

PORT = 18790
INBOX = Path.home() / ".openclaw/workspace-main/inbox"
HTML = INBOX / "upload.html"
PIDFILE = Path.home() / ".openclaw/workspace-main/scripts/upload_server.pid"
LOGFILE = Path.home() / ".openclaw/workspace-main/inbox/upload_server.log"

GATEWAY_URL = "http://127.0.0.1:18789"
GATEWAY_TOKEN = "openclaw-local-relay-20260319"
BOSS_SESSION_KEY = "agent:main:main"


def log(msg):
    ts = time.strftime("%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOGFILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/upload.html":
            try:
                with open(HTML, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "upload.html not found")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/upload/send" or self.path == "/send":
            self.handle_send()
        elif self.path == "/":
            self.handle_upload()
        else:
            self.send_error(404)

    def handle_upload(self):
        try:
            content_type = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in content_type:
                self.send_json({"ok": False, "error": "Only multipart/form-data accepted"})
                return
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type}
            )
            if "file" not in form:
                self.send_json({"ok": False, "error": "No file field"})
                return
            file_item = form["file"]
            if not file_item.filename:
                self.send_json({"ok": False, "error": "Empty filename"})
                return
            filename = os.path.basename(file_item.filename)
            safe_name = f"upload_{int(time.time())}_{filename}"
            out_path = INBOX / safe_name
            with open(out_path, "wb") as f:
                f.write(file_item.file.read())
            self.send_json({"ok": True, "path": str(out_path), "name": safe_name})
        except Exception as e:
            log(f"handle_upload error: {e}")
            self.send_json({"ok": False, "error": str(e)})

    def handle_send(self):
        """上传图片并发送给小白"""
        try:
            content_type = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in content_type:
                self.send_json({"ok": False, "error": "Only multipart/form-data accepted"})
                return
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type}
            )
            if "file" not in form:
                self.send_json({"ok": False, "error": "No file field"})
                return
            file_item = form["file"]
            if not file_item.filename:
                self.send_json({"ok": False, "error": "Empty filename"})
                return

            filename = os.path.basename(file_item.filename)
            safe_name = f"upload_{int(time.time())}_{filename}"
            out_path = INBOX / safe_name
            file_data = file_item.file.read()
            with open(out_path, "wb") as f:
                f.write(file_data)
            log(f"文件已保存: {safe_name}")

            # 通过 Gateway API 发送图片给小白（加超时保护）
            payload = json.dumps({
                "tool": "message",
                "action": "send",
                "sessionKey": BOSS_SESSION_KEY,
                "args": {
                    "channel": "qqbot",
                    "target": "qqbot:c2c:7E2E8699372FE33EC4E2DA736D020639",
                    "media": str(out_path),
                    "message": "📷 收到图片"
                }
            }).encode("utf-8")

            req = urllib.request.Request(
                f"{GATEWAY_URL}/tools/invoke",
                data=payload,
                headers={
                    "Authorization": f"Bearer {GATEWAY_TOKEN}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    result = json.loads(resp.read())
                log(f"Gateway 响应: {result.get('ok')}")
            except urllib.error.URLError as e:
                log(f"Gateway 超时/错误（图片已保存）: {e}")
                self.send_json({"ok": True, "path": str(out_path), "name": safe_name, "sent": False, "reason": "gateway_timeout"})
                return

            if result.get("ok"):
                self.send_json({"ok": True, "path": str(out_path), "name": safe_name, "sent": True})
            else:
                self.send_json({"ok": True, "path": str(out_path), "name": safe_name, "sent": False, "send_error": str(result)})
        except Exception as e:
            log(f"handle_send error: {e}")
            self.send_json({"ok": False, "error": str(e)})

    def send_json(self, data):
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception:
            pass

    def log_message(self, fmt, *args):
        log(f"{fmt % args}")


def write_pid(pid):
    with open(PIDFILE, "w") as f:
        f.write(str(pid))


def serve():
    INBOX.mkdir(parents=True, exist_ok=True)
    HTML.touch(exist_ok=True)
    write_pid(os.getpid())

    socketserver.TCPServer.allow_reuse_address = True
    # 禁用 URL timeout（不影响 Gateway 请求超时）
    socketserver.TCPServer.timeout = None

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            log(f"Upload server 运行中，端口 {PORT}，inbox={INBOX}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        log("收到 KeyboardInterrupt，退出")
        sys.exit(0)


if __name__ == "__main__":
    serve()
