#!/usr/bin/env python3
"""
清理 inbox 中的图片文件（每日定时执行）
保留非图片文件（log、json 等）
"""
import os
import glob
from datetime import datetime

INBOX = os.path.expanduser("~/.openclaw/workspace-main/inbox")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".mp4", ".mov", ".avi"}

deleted = []
kept = []

for fname in os.listdir(INBOX):
    fpath = os.path.join(INBOX, fname)
    if not os.path.isfile(fpath):
        continue
    ext = os.path.splitext(fname.lower())[1]
    if ext in IMAGE_EXTS:
        try:
            os.remove(fpath)
            deleted.append(fname)
        except Exception as e:
            kept.append(f"{fname} (失败: {e})")
    else:
        kept.append(fname)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"[{now}] inbox 清理完成：删除 {len(deleted)} 个图片文件，保留 {len(kept)} 个非图片文件")
if deleted:
    print(f"  已删除: {', '.join(deleted[:10])}{' ...' if len(deleted) > 10 else ''}")
if kept:
    print(f"  保留: {', '.join(kept)}")
