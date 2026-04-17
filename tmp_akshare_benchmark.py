#!/usr/bin/env python3
"""
Ashare data download benchmark: akshare vs baostock
Target: 2026-04-17 full market data
"""

import time
import csv
import os
import sys

# Output file
OUT_FILE = "/Volumes/XB_Home/小兰/astock_data/daily/astock_ak_20260417.csv"
LETTER_FILE = "/Volumes/XB_Home/小兰/小兰/letters/2026-04-17-akshare-benchmark.txt"

print("=" * 60)
print("akshare benchmark 启动")
print("=" * 60)

# ── Step 1: 获取全市场股票列表 ──────────────────────────────────
import akshare as ak

print("\n[1] 获取全市场 A 股列表...")
list_start = time.time()
try:
    # 获取所有 A 股列表
    stock_info = ak.stock_zh_a_spot_em()
    codes = stock_info['代码'].tolist()
    # 过滤：去除 ST、ETF 等，只保留 6 位数字纯股票代码
    codes = [c for c in codes if c.isdigit() and len(c) == 6]
    # 补全前缀
    code_list = [f"sh.{c}" if c.startswith(('6', '5')) else f"sz.{c}" for c in codes]
    list_time = time.time() - list_start
    print(f"  股票列表获取成功: {len(code_list)} 只, 耗时 {list_time:.1f}s")
    print(f"  前10只: {code_list[:10]}")
except Exception as e:
    print(f"  获取失败: {e}")
    sys.exit(1)

# ── Step 2: akshare 下载测试 ──────────────────────────────────
print(f"\n[2] 开始下载 2026-04-17 数据 ({len(code_list)} 只)...")
ak_start = time.time()

all_rows = []
failed = []

# 批量下载（akshare 支持单次多只）
# stock_zh_a_hist 支持指定股票代码列表和日期范围
chunk_size = 50  # 每批50只

for i in range(0, len(code_list), chunk_size):
    chunk = code_list[i:i+chunk_size]
    chunk_str = ",".join(chunk)
    try:
        df = ak.stock_zh_a_hist(
            symbol="ALL",
            start_date="20260417",
            end_date="20260417",
            adjustflag="2"  # 不复权
        )
        # 过滤 2026-04-17 的数据
        if df is not None and not df.empty:
            df_017 = df[df['日期'] == '2026-04-17']
            for _, row in df_017.iterrows():
                all_rows.append({
                    'date': row['日期'],
                    'code': row['代码'],
                    'open': row['开盘'],
                    'high': row['最高'],
                    'low': row['最低'],
                    'volume': row['成交量']
                })
    except Exception as e:
        pass
    
    if (i // chunk_size) % 10 == 0:
        elapsed = time.time() - ak_start
        print(f"  进度: {i}/{len(code_list)} ({elapsed:.1f}s)")

ak_end = time.time()
ak_total = ak_end - ak_start
print(f"\n  akshare 总耗时: {ak_total:.1f}s ({ak_total/60:.2f}分钟)")
print(f"  成功获取: {len(all_rows)} 条")

# ── Step 3: 保存 CSV ──────────────────────────────────────────
if all_rows:
    with open(OUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'code', 'open', 'high', 'low', 'volume'])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\n[3] 数据已保存: {OUT_FILE}")

    with open(OUT_FILE, 'r') as f:
        lines = f.readlines()
    print(f"  文件行数: {len(lines)}")
    print(f"  首行:\n    {lines[0].strip()}")
    print(f"  第二行:\n    {lines[1].strip()}")
else:
    print("  没有数据！")

# ── Step 4: 生成报告 ──────────────────────────────────────────
# baostock 基准: 18 分钟 = 1080 秒
baostock_time = 18 * 60  # 18分钟

if ak_total > 0:
    ratio = baostock_time / ak_total
    if ratio > 1:
        comparison = f"快 {ratio:.1f} 倍"
    else:
        comparison = f"慢 {1/ratio:.1f} 倍"
else:
    comparison = "无法计算"

report = f"""akshare benchmark 结果
=======================
日期: 2026-04-17
股票只数: {len(code_list)}

akshare 耗时: {ak_total:.1f}秒 ({ak_total/60:.2f}分钟)
akshare 数据条数: {len(all_rows)}
akshare 数据样例: {lines[1].strip() if all_rows else 'N/A'}

对比 baostock: {comparison}
  - baostock 基准: {baostock_time}s (18分钟, THREADS=1)
  - akshare 耗时:  {ak_total:.1f}s
  - 比率: {ratio:.2f}x
"""

with open(LETTER_FILE, 'w') as f:
    f.write(report)
print(f"\n[4] 报告已保存: {LETTER_FILE}")

print(report)
