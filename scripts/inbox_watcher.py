#!/usr/bin/env python3
"""inbox 目录监控脚本 - FSEvents 实时监控，新图片立即通知小白
每张图片只通知一次（用 .watched 标记）
"""
import os, sys, time, json, urllib.request, urllib.error
from pathlib import Path

INBOX = Path.home() / ".openclaw/workspace-main/inbox"
MARKER_DIR = INBOX / ".watched"
GATEWAY_URL = "http://127.0.0.1:18789"
GATEWAY_TOKEN = "openclaw-local-relay-20260319"
# 通知到主会话（网页端），这样老板在网页端发图我立刻能看到
BOSS_SESSION_KEY = "agent:main:main"

IMAGE_EXTS = {".jpg",".jpeg",".png",".gif",".webp",".mp4",".mov"}

LOG_FILE = Path(__file__).parent.parent / "inbox" / ".watcher.log"

def log(msg):
    ts = time.strftime("%m-%d %H:%M:%S")
    line = f"[inbox_watcher {ts}] {msg}"
    print(line, flush=True)
    try:
        LOG_FILE.parent.mkdir(exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def notify_agent(filepath):
    """通知小白有新图片 - 用 sessions_send 注入到主会话"""
    payload = json.dumps({
        "tool": "sessions_send",
        "action": "send",
        "sessionKey": BOSS_SESSION_KEY,
        "args": {
            "message": f"📷 新图片到达 inbox：{filepath.name}\n\n路径：{filepath}"
        }
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{GATEWAY_URL}/tools/invoke",
        data=payload,
        headers={"Authorization": f"Bearer {GATEWAY_TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        log(f"通知发送结果: {result.get('ok')}")
    except Exception as e:
        log(f"通知失败: {e}")

def is_image(path):
    return path.suffix.lower() in IMAGE_EXTS

def scan_and_watch():
    """扫描当前所有未监控的图片，并开始监控"""
    MARKER_DIR.mkdir(exist_ok=True)
    log(f"启动 inbox 监控: {INBOX}")

    # 首次运行：监控所有现有图片（标记为已处理）
    for f in INBOX.iterdir():
        if f.is_file() and is_image(f):
            marker = MARKER_DIR / f.name
            if not marker.exists():
                marker.touch()
                log(f"首次运行，标记现有文件: {f.name}")

    log("开始监听 inbox 变化...")

    # 用简单轮询（macOS 无 inotify，用低间隔轮询代替）
    # 间隔 3 秒，够快且不影响性能
    last_mtime = {}
    while True:
        try:
            for f in INBOX.iterdir():
                if not f.is_file() or not is_image(f):
                    continue
                mtime = f.stat().st_mtime
                marker = MARKER_DIR / f.name
                if f.name not in last_mtime:
                    last_mtime[f.name] = mtime
                    if not marker.exists():
                        # 新文件（首次见到）
                        marker.touch()
                        log(f"🆕 新图片发现: {f.name}")
                        notify_agent(f)
                elif last_mtime[f.name] != mtime:
                    last_mtime[f.name] = mtime
                    if not marker.exists():
                        marker.touch()
                        log(f"🔄 图片更新: {f.name}")
                        notify_agent(f)
        except Exception as e:
            log(f"轮询异常: {e}")
        time.sleep(3)

if __name__ == "__main__":
    scan_and_watch()
