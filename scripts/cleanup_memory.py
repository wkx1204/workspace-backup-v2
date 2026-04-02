#!/usr/bin/env python3
"""
cleanup_memory.py
功能：
1. 删除 7 天前的每日记忆文件（memory/YYYY-MM-DD.md）
2. 删除 15 天前的会话历史（sessions/）
3. 自动备份（删除前打包 zip）
4. 自动重建记忆索引
每周日 凌晨 3:00 自动执行
手动：python3 cleanup_memory.py [--dry-run]
"""
import os, sys, glob, shutil, zipfile, datetime
from pathlib import Path

WORKSPACE  = "/Users/wf/.openclaw/workspace-main"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
BACKUP_DIR = os.path.join(WORKSPACE, "backups")
SESSION_DIR = os.path.join(WORKSPACE, ".sessions")

MEMORY_DAYS = 7
SESSION_DAYS = 15

dry_run = "--dry-run" in sys.argv

today = datetime.datetime.now()
mem_threshold = today - datetime.timedelta(days=MEMORY_DAYS)
sess_threshold = today - datetime.timedelta(days=SESSION_DAYS)

print(f"=== 记忆清理 {today.strftime('%Y-%m-%d %H:%M')} ===")
print(f"模式：{'预览（不实际删除）' if dry_run else '执行'}")
print(f"  记忆文件：删除 {MEMORY_DAYS} 天前（< {mem_threshold.strftime('%Y-%m-%d')}）")
print(f"  会话历史：删除 {SESSION_DAYS} 天前（< {sess_threshold.strftime('%Y-%m-%d')}）")
print()

# ========== 1. 备份 ==========
if dry_run:
    print(f"[预览] 备份：将删除的文件打包为 backup_YYYYMMDD.zip")
else:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = f"cleanup_{today.strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    files_to_backup = []
    for f in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
        st = os.stat(f)
        if datetime.datetime.fromtimestamp(st.st_mtime) < mem_threshold:
            files_to_backup.append(f)
    for f in glob.glob(os.path.join(SESSION_DIR, "*.json")):
        st = os.stat(f)
        if datetime.datetime.fromtimestamp(st.st_mtime) < sess_threshold:
            files_to_backup.append(f)
    if files_to_backup:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in files_to_backup:
                zf.write(f, os.path.relpath(f, WORKSPACE))
        print(f"[备份] 已打包 {len(files_to_backup)} 个文件 → {backup_path}")
    else:
        print(f"[备份] 没有文件需要备份，跳过")

print()

# ========== 2. 删除 7 天前的记忆文件 ==========
deleted_mem = []
total_size = 0
if os.path.exists(MEMORY_DIR):
    for f in glob.glob(os.path.join(MEMORY_DIR, "*.md")):
        st = os.stat(f)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        if mtime < mem_threshold:
            size = st.st_size
            if dry_run:
                print(f"[预览删除] memory  {mtime.strftime('%Y-%m-%d')}  {os.path.basename(f)}")
            else:
                os.remove(f)
                print(f"[已删除] memory  {mtime.strftime('%Y-%m-%d')}  {os.path.basename(f)}")
            deleted_mem.append(f)
            total_size += size

# ========== 3. 删除 15 天前的会话历史 ==========
deleted_sess = []
if os.path.exists(SESSION_DIR):
    for f in glob.glob(os.path.join(SESSION_DIR, "*.json")):
        st = os.stat(f)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        if mtime < sess_threshold:
            size = st.st_size
            basename = os.path.basename(f)
            if dry_run:
                print(f"[预览删除] session {mtime.strftime('%Y-%m-%d')}  {basename[:40]}...")
            else:
                os.remove(f)
                print(f"[已删除] session {mtime.strftime('%Y-%m-%d')}  {basename[:40]}")
            deleted_sess.append(f)
            total_size += size

# ========== 4. 统计 ==========
print()
count = len(deleted_mem) + len(deleted_sess)
print(f"结果：{'预览' if dry_run else '清理'} {count} 个文件（{total_size/1024:.1f} KB）")
print(f"  memory 文件：{len(deleted_mem)} 个")
print(f"  会话历史：{len(deleted_sess)} 个")
if dry_run:
    print(f"（以上为预览，实际不会删除）")
else:
    # ========== 5. 重建记忆索引 ==========
    import subprocess
    print()
    print("[索引] 正在重建记忆索引...")
    result = subprocess.run(
        ["openclaw", "memory", "index", "--force"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print("[索引] ✓ 记忆索引重建完成")
    else:
        print(f"[索引] ⚠ 索引重建异常: {result.stderr[:200]}")

    print()
    print(f"✓ 全部完成，备份已保存至 backups/ 目录")
