#!/usr/bin/env python3
"""inbox 图片通知脚本
每分钟运行一次，检查 inbox 中的新图片并通知小白（通过 cron announce）
新方案：qqbot 1.6.4 直接把图存 inbox，跳过 qqbot/downloads
"""
import os, time
from pathlib import Path

INBOX = Path.home() / ".openclaw/workspace-main/inbox"
MARKER = INBOX / ".inbox_check_marker"

IMAGE_EXTS = {".jpg",".jpeg",".png",".gif",".webp",".mp4",".mov"}

def get_checked():
    if MARKER.exists():
        return set(MARKER.read_text().strip().splitlines())
    return set()

def save_checked(names):
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text("\n".join(names))

def check():
    checked = get_checked()
    new_files = []
    for f in INBOX.iterdir():
        if not f.is_file() or f.name in checked:
            continue
        if f.suffix.lower() in IMAGE_EXTS:
            new_files.append(f.name)
            checked.add(f.name)
    if new_files:
        save_checked(checked)
        print(f"[inbox check] 发现新图片: {new_files}")
        # 输出供 cron 读取
        print("NEW_IMAGES:" + ",".join(new_files))
    else:
        print(f"[inbox check] 无新图片")

if __name__ == "__main__":
    check()
