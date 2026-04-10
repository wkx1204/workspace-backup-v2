#!/usr/bin/env python3
"""
Memory Dreaming - 记忆晋升脚本
每晚凌晨3点自动运行，把有价值的短期记忆晋升到 MEMORY.md
"""
import os, glob
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace-main")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
OBSIDIAN_MEMORY = os.path.join(os.path.expanduser("~/Documents/Obsidian Vault"), "memory")
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")
DREAMS_FILE = os.path.join(WORKSPACE, "DREAMS.md")

def get_memory_files():
    files = []
    for d in [MEMORY_DIR, OBSIDIAN_MEMORY]:
        if os.path.isdir(d):
            for f in glob.glob(os.path.join(d, "*.md")):
                files.append(f)
    return sorted(set(files))

def read_file(path):
    try:
        with open(path) as f: return f.read()
    except: return ""

def should_promote(line):
    if len(line) < 15: return False
    low = any(k in line for k in ["HEARTBEAT", "OK", "heartbeat", "DEBUG", "测试", "no_error"])
    if low: return False
    high = any(k in line for k in ["决策", "配置", "新项目", "生日", "重要", "偏好", "习惯", "住址", "工作", "财务", "晋升", "记住", "不要", "禁止"])
    return high

def analyze_memories():
    candidates = []
    seen = set()
    files = get_memory_files()
    for fpath in files:
        for line in read_file(fpath).split('\n'):
            line = line.strip()
            if not line or line in seen or len(line) < 15: continue
            if should_promote(line):
                seen.add(line)
                candidates.append(line)
    return list(seen)[:20]

def promote(candidates):
    if not candidates: return False
    existing = read_file(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else ""
    today = datetime.now().strftime("%Y-%m-%d")
    block = f"\n## 晋升记忆 — {today}\n"
    added = 0
    for c in candidates:
        if c not in existing:
            block += f"- {c}\n"
            added += 1
    if added > 0:
        with open(MEMORY_FILE, "a") as f:
            f.write(block)
    return added

def write_diary(candidates, added):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"## 梦境日记 — {today}\n"]
    if added:
        lines.append(f"✅ 晋升了 {added} 条记忆到 MEMORY.md\n")
        for c in candidates[:added]:
            lines.append(f"- {c}\n")
    else:
        lines.append("📝 今日无新记忆晋升\n")
    mode = "a" if os.path.exists(DREAMS_FILE) else "w"
    with open(DREAMS_FILE, mode) as f:
        f.write("\n".join(lines) + "\n")

def main():
    print(f"[Dreaming] 开始记忆整理 {datetime.now()}")
    candidates = analyze_memories()
    print(f"[Dreaming] 找到 {len(candidates)} 条候选记忆")
    added = promote(candidates)
    print(f"[Dreaming] 晋升了 {added} 条")
    write_diary(candidates, added)
    print(f"[Dreaming] 完成")

if __name__ == "__main__":
    main()
