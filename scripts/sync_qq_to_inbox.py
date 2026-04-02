#!/usr/bin/env python3
"""QQ图片 → inbox 同步脚本
每分钟运行一次，把 qqbot/downloads 里的新图片复制到 inbox
"""
import os, shutil, time
from pathlib import Path

QQ_DOWNLOADS = Path.home() / ".openclaw/qqbot/downloads"
INBOX = Path.home() / ".openclaw/workspace-main/inbox"
MARKER = INBOX / ".qq_sync_marker"

def get_synced():
    if MARKER.exists():
        return set(MARKER.read_text().strip().splitlines())
    return set()

def save_synced(names):
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text("\n".join(names))

def sync():
    synced = get_synced()
    new_files = []
    for f in QQ_DOWNLOADS.iterdir():
        if f.name in synced:
            continue
        # 只同步图片
        if f.suffix.lower() in [".jpg",".jpeg",".png",".gif",".webp",".mp4",".mov"]:
            dest = INBOX / f.name
            shutil.copy2(f, dest)
            new_files.append(f.name)
            synced.add(f.name)
    if new_files:
        save_synced(synced)
        print(f"[qq→inbox] 同步了: {new_files}")
    else:
        print(f"[qq→inbox] 无新文件")

if __name__ == "__main__":
    sync()
