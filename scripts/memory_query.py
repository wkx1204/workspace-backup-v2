#!/usr/bin/env python3
"""
memory_query.py — Obsidian 记忆查询工具

用法:
    python3 memory_query.py --list              # 列出所有记忆
    python3 memory_query.py --tag 老板偏好      # 按标签查
    python3 memory_query.py --type decision     # 按类型查
    python3 memory_query.py --importance high  # 按重要度查
    python3 memory_query.py --keyword automemory  # 全文搜索
    python3 memory_query.py --boot             # 只看启动记忆
    python3 memory_query.py --recent 7         # 最近7天
    python3 memory_query.py --cleanup --dry-run # 预览要清理的记忆
    python3 memory_query.py --cleanup --confirm # 确认后执行清理

示例:
    python3 memory_query.py --tag 配置变更
    python3 memory_query.py --type learned --importance medium
    python3 memory_query.py --keyword openclaw
    python3 memory_query.py --recent 30 --importance low

标签规范（Obsidian原生）:
    #老板偏好  #配置变更  #教训  #系统  #项目
    #技术  #skill  #修复  #obsidian  #创作  #小说
    #memory/automemory  #memory/决策  #memory/教训

类型（memory type）:
    decision  |  project  |  setup  |  learned
    identity  |  insight  |  any

重要度:
    high  |  medium  |  low
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent
MEMORY_DIR = Path.home() / "Documents/Obsidian Vault/memory"
MANIFEST_PATH = MEMORY_DIR / ".memory-manifest.json"


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", file=sys.stderr)


def load_manifest() -> dict:
    """加载 manifest"""
    if not MANIFEST_PATH.exists():
        log(f"manifest 不存在: {MANIFEST_PATH}", "WARN")
        return {}
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(data: dict) -> None:
    """保存 manifest"""
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def list_memories(manifest: dict, filters: dict) -> list:
    """根据过滤条件从 manifest 筛选记忆"""
    memories = manifest.get("memories", [])
    
    results = []
    for m in memories:
        # 按标签过滤
        if filters.get("tag"):
            tags = m.get("tags", [])
            if filters["tag"] not in tags:
                continue
        
        # 按类型过滤
        if filters.get("type") and filters["type"] != "any":
            if m.get("type") != filters["type"]:
                continue
        
        # 按重要度过滤
        if filters.get("importance"):
            if m.get("importance") != filters["importance"]:
                continue
        
        # 按关键词过滤（preview + uri）
        if filters.get("keyword"):
            kw = filters["keyword"].lower()
            preview = m.get("preview", "").lower()
            uri = m.get("uri", "").lower()
            if kw not in preview and kw not in uri:
                continue
        
        # 按日期过滤
        if filters.get("days"):
            mem_date_str = m.get("date", "")
            if mem_date_str:
                try:
                    mem_date = datetime.strptime(mem_date_str, "%Y-%m-%d")
                    cutoff = datetime.now() - timedelta(days=filters["days"])
                    if mem_date < cutoff:
                        continue
                except ValueError:
                    pass
        
        results.append(m)
    
    return results


def search_fulltext(query: str) -> list:
    """全文搜索 Obsidian 记忆文件"""
    results = []
    if not MEMORY_DIR.exists():
        return results
    
    try:
        # 在 memory/ 目录下 grep
        result = subprocess.run(
            ["grep", "-r", "-l", query, str(MEMORY_DIR)],
            capture_output=True, text=True, timeout=10
        )
        for filepath in result.stdout.strip().split("\n"):
            if filepath and filepath != MANIFEST_PATH:
                results.append(filepath)
    except Exception as e:
        log(f"全文搜索失败: {e}", "WARN")
    
    return results


def display_memory(m: dict, idx: int = None) -> None:
    """格式化打印一条记忆"""
    prefix = f"[{idx}] " if idx is not None else ""
    uri = m.get("uri", "unknown")
    mem_type = m.get("type", "-")
    importance = m.get("importance", "-")
    date = m.get("date", "-")
    preview = m.get("preview", "")
    tags = ", ".join(f"#{t}" for t in m.get("tags", []))
    boot = " ⭐" if m.get("boot") else ""
    
    print(f"{prefix}📌 {uri}{boot}")
    print(f"    类型: {mem_type} | 重要度: {importance} | 日期: {date}")
    if tags:
        print(f"    标签: {tags}")
    print(f"    {preview}")
    print()


def list_boot_memories(manifest: dict) -> None:
    """列出所有启动记忆"""
    boot = [m for m in manifest.get("memories", []) if m.get("boot")]
    if not boot:
        print("暂无启动记忆")
        return
    
    print(f"⭐ 启动记忆（共 {len(boot)} 条）\n")
    for i, m in enumerate(boot, 1):
        display_memory(m, i)


def cleanup_memories(dry_run: bool = True, confirm: bool = False) -> dict:
    """
    清理 manifest 中的过期记忆条目
    - high: 永久保留
    - medium: 90天
    - low: 30天
    - 超180天自动从 manifest 移除（文件由周日清理脚本处理）
    """
    manifest = load_manifest()
    memories = manifest.get("memories", [])
    now = datetime.now()
    
    to_remove = []
    to_keep = []
    
    for m in memories:
        # boot=true 的永久保留
        if m.get("boot") or m.get("importance") == "high":
            to_keep.append(m)
            continue
        
        date_str = m.get("date", "")
        if not date_str:
            to_keep.append(m)
            continue
        
        try:
            mem_date = datetime.strptime(date_str, "%Y-%m-%d")
            age_days = (now - mem_date).days
        except ValueError:
            to_keep.append(m)
            continue
        
        importance = m.get("importance", "medium")
        if importance == "low" and age_days > 30:
            to_remove.append((m, age_days, "low > 30d"))
        elif importance == "medium" and age_days > 90:
            to_remove.append((m, age_days, "medium > 90d"))
        elif age_days > 180:
            to_remove.append((m, age_days, "age > 180d"))
        else:
            to_keep.append(m)
    
    if dry_run:
        print(f"🔍 清理预览（dry-run，不实际删除）")
        print(f"   当前: {len(memories)} 条 → 清理后: {len(to_keep)} 条")
        print(f"   将移除: {len(to_remove)} 条:\n")
        for m, age, reason in to_remove:
            print(f"   - {m.get('uri')} ({age}天, {reason})")
        return {"to_remove": len(to_remove), "to_keep": len(to_keep)}
    
    if not confirm:
        log("需要 --confirm 参数才会实际执行清理", "WARN")
        return {}
    
    # 执行清理
    manifest["memories"] = to_keep
    manifest["total_memories"] = len(to_keep)
    manifest["last_updated"] = datetime.now().isoformat() + "Z"
    save_manifest(manifest)
    
    log(f"✅ 清理完成: {len(memories)} → {len(to_keep)} 条（移除 {len(to_remove)} 条）", "INFO")
    return {"removed": len(to_remove), "kept": len(to_keep)}


def main():
    parser = argparse.ArgumentParser(
        description="Obsidian 记忆查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("--list", action="store_true", help="列出所有记忆")
    parser.add_argument("--tag", type=str, help="按标签筛选（不含#）")
    parser.add_argument("--type", type=str, default="any", help=f"记忆类型: decision/project/setup/learned/identity/insight/any")
    parser.add_argument("--importance", type=str, choices=["high", "medium", "low"], help="按重要度筛选")
    parser.add_argument("--keyword", type=str, help="在 preview/uri 中搜索关键词")
    parser.add_argument("--boot", action="store_true", help="只显示启动记忆（boot=true）")
    parser.add_argument("--recent", type=int, metavar="N", help=f"只显示最近 N 天")
    parser.add_argument("--cleanup", action="store_true", help="执行 manifest 清理")
    parser.add_argument("--dry-run", action="store_true", help="dry-run 模式（预览清理）")
    parser.add_argument("--confirm", action="store_true", help="确认执行清理（需配合 --cleanup）")
    parser.add_argument("--manifest", action="store_true", help="显示 manifest 统计信息")
    
    args = parser.parse_args()
    
    # 无参数时显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n💡 示例:")
        print("   python3 memory_query.py --list")
        print("   python3 memory_query.py --tag 配置变更")
        print("   python3 memory_query.py --boot")
        print("   python3 memory_query.py --cleanup --dry-run")
        return
    
    # manifest 信息
    if args.manifest:
        manifest = load_manifest()
        print(f"📊 Manifest 统计")
        print(f"   总记忆: {manifest.get('total_memories', 0)} 条")
        print(f"   最后更新: {manifest.get('last_updated', '-')}")
        print(f"   启动记忆: {len([m for m in manifest.get('memories', []) if m.get('boot')])} 条")
        print(f"   格式版本: {manifest.get('format', 'v1')}")
        policy = manifest.get("retention_policy", {})
        print(f"   保留策略: high={policy.get('high')}, medium={policy.get('medium')}, low={policy.get('low')}")
        return
    
    # 清理模式
    if args.cleanup:
        cleanup_memories(dry_run=args.dry_run or not args.confirm, confirm=args.confirm)
        return
    
    # 加载数据
    manifest = load_manifest()
    if not manifest:
        log("manifest 为空或不存在", "WARN")
        return
    
    # 构建过滤条件
    filters = {}
    if args.tag:
        filters["tag"] = args.tag
    if args.type:
        filters["type"] = args.type
    if args.importance:
        filters["importance"] = args.importance
    if args.keyword:
        filters["keyword"] = args.keyword
    if args.recent:
        filters["days"] = args.recent
    
    # 启动记忆模式
    if args.boot:
        list_boot_memories(manifest)
        return
    
    # 查询
    results = list_memories(manifest, filters)
    
    # 如果有关键词，再做一下全文搜索补充
    if args.keyword and not results:
        files = search_fulltext(args.keyword)
        if files:
            print(f"🔍 manifest 中未找到，补充搜索文件内容:")
            for f in files[:5]:
                print(f"   {f}")
            print()
    
    # 输出
    if not results:
        print("未找到匹配的记忆")
        return
    
    print(f"🔍 找到 {len(results)} 条记忆:\n")
    for i, m in enumerate(results, 1):
        display_memory(m, i)
    
    # 如果有 --tag 或 --type，再显示 PARA 中的相关文件
    if args.tag or args.keyword:
        relevant_folders = []
        if args.tag == "obsidian" or args.tag == "organization":
            relevant_folders = ["~/Documents/Obsidian Vault/0-project/", "~/Documents/Obsidian Vault/1-area/"]
        
        if relevant_folders:
            print("💡 PARA 中可能相关的文件夹:")
            for folder in relevant_folders:
                print(f"   {folder}")

if __name__ == "__main__":
    main()
