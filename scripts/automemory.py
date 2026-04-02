#!/usr/bin/env python3
"""
automemory runner — 定时调起 OpenClaw agent 执行记忆捕获

原理：
- OpenClaw 的 sessions_history 是 Tool，不是 HTTP API
- 所以改用 cron job → systemEvent → agent 自己调用工具执行
- 本脚本作为 stub，实际工作由 OpenClaw agent 完成

Usage:
    python3 automemory.py --dry-run   # 测试模式
    python3 automemory.py --hours 24  # 指定时间范围
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

VAULT_PATH = Path.home() / "Documents" / "Obsidian Vault"
MEMORY_DIR = VAULT_PATH / "memory"
MANIFEST_PATH = MEMORY_DIR / ".memory-manifest.json"
OPENCLAW_API_BASE = os.environ.get("OPENCLAW_API_BASE", "http://127.0.0.1:18789")
OPENCLAW_API_KEY = os.environ.get("OPENCLAW_API_KEY", "12345678")
TODAY = datetime.now().strftime("%Y-%m-%d")

def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def api_get(path: str) -> dict:
    url = f"{OPENCLAW_API_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {OPENCLAW_API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"API {path} -> {e}", "ERROR")
        return {}

def api_post(path: str, data: dict) -> dict:
    url = f"{OPENCLAW_API_BASE}{path}"
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {OPENCLAW_API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200]
        log(f"HTTP {e.code} on {path}: {body}", "ERROR")
        return {}
    except Exception as e:
        log(f"POST {path} -> {e}", "ERROR")
        return {}

def get_openclaw_routes():
    """探测 OpenClaw 可用的 HTTP API 端点"""
    # 尝试常见路径
    routes = [
        "/api/v1/status",
        "/api/status",
        "/api/v1/health",
        "/health",
    ]
    for r in routes:
        result = api_get(r)
        if result:
            log(f"Found: {r} -> {str(result)[:100]}")
    return {}

def find_sessions_api():
    """尝试找到 sessions API 的正确路径"""
    # OpenClaw gateway 通常有 RPC 或 REST 端点
    candidates = [
        "/api/v1/sessions",
        "/api/sessions/list",
        "/api/sessions",
        "/v1/sessions",
    ]
    for path in candidates:
        result = api_get(path)
        if result and result != {}:
            log(f"✓ sessions API: {path} -> {str(result)[:200]}")
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="automemory runner")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--probe", action="store_true", help="探测可用 API")
    args = parser.parse_args()

    if args.probe:
        log("探测 OpenClaw API 端点...")
        get_openclaw_routes()
        log("\n探测 sessions API...")
        sessions_path = find_sessions_api()
        if not sessions_path:
            log("未找到 sessions REST API（可能走 WebSocket RPC）", "WARN")
        return

    # 正常模式：创建 cron agentTurn 任务
    # 但实际上这个脚本现在没什么用了，因为 agent 逻辑不能写在这里
    # 保留 --dry-run --probe 功能用于调试
    log("automemory runner 已就绪", "INFO")
    log("提示：通过 cron job 创建 agentTurn 来执行 automemory", "INFO")
    log("实际执行由 OpenClaw agent 完成（sessions_history 是 Tool，非 HTTP API）")

if __name__ == "__main__":
    main()
