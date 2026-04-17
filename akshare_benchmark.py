#!/usr/bin/env python3
"""
Ashare benchmark: akshare (腾讯接口) vs baostock
目标: 2026-04-17 全市场日线数据
"""

import time
import csv
import os
import sys
import concurrent.futures
from datetime import datetime

OUT_FILE = "/Volumes/XB_Home/小兰/astock_data/daily/astock_ak_20260417.csv"
LETTER_FILE = "/Volumes/XB_Home/小兰/小兰/letters/2026-04-17-akshare-benchmark.txt"

print("=" * 60)
print("akshare (腾讯接口) benchmark")
print("=" * 60)

# ── Step 1: 获取全市场 A 股代码列表 ────────────────────────────
import akshare as ak

print("\n[1] 获取全市场 A 股列表...")
list_start = time.time()

# 使用 baostock 获取股票列表（它能连通）
import baostock as bs
lg = bs.login()
rs = bs.query_stock_basic(code_name="")
data_list = []
while rs.next():
    data_list.append(rs.get_row_data())
bs.logout()

# 过滤 A 股（去掉 B 股、指数等）
# code: sh.600000 / sz.000001 格式
code_map = {}  # baostock_code -> tx_code
for row in data_list:
    code, name, type_ = row[0], row[1], row[2]
    if type_ == '1':
        # A 股
        if code.startswith('sh.6'):
            tx_code = 'sh' + code[3:]  # sh600000
        elif code.startswith('sz.0') or code.startswith('sz.3'):
            tx_code = 'sz' + code[3:]  # sz000001
        else:
            continue
        code_map[tx_code] = code  # tx_code -> baostock_code

all_codes = list(code_map.keys())
list_time = time.time() - list_start
print(f"  股票列表获取成功: {len(all_codes)} 只, 耗时 {list_time:.1f}s")
print(f"  前10只: {all_codes[:10]}")

# ── Step 2: 腾讯接口下载 ─────────────────────────────────────
print(f"\n[2] 开始下载 2026-04-17 数据 ({len(all_codes)} 只)...")
ak_start = time.time()

def fetch_one(tx_code):
    """下载单只股票日线数据"""
    try:
        df = ak.stock_zh_a_hist_tx(
            symbol=tx_code,
            start_date='20260417',
            end_date='20260417',
            adjust=''  # 不复权
        )
        if df is not None and not df.empty:
            row = df.iloc[0]
            return {
                'date': str(row['date']),
                'code': tx_code,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'volume': row['amount']
            }
    except Exception:
        pass
    return None

all_rows = []
failed = 0
total = len(all_codes)

# 使用 20 线程并发（腾讯接口支持较好的并发）
MAX_WORKERS = 20

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(fetch_one, c): c for c in all_codes}
    done_count = 0
    for f in concurrent.futures.as_completed(futures):
        result = f.result()
        if result:
            all_rows.append(result)
        else:
            failed += 1
        done_count += 1
        if done_count % 500 == 0:
            elapsed = time.time() - ak_start
            rate = done_count / elapsed
            eta = (total - done_count) / rate if rate > 0 else 0
            print(f"  进度: {done_count}/{total} ({elapsed:.1f}s, {rate:.1f}只/s, ETA {eta:.0f}s)")

ak_end = time.time()
ak_total = ak_end - ak_start
print(f"\n  akshare(腾讯) 总耗时: {ak_total:.1f}s ({ak_total/60:.2f}分钟)")
print(f"  成功: {len(all_rows)}, 失败: {failed}")

# ── Step 3: 保存 CSV ─────────────────────────────────────────
if all_rows:
    with open(OUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'code', 'open', 'high', 'low', 'volume'])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\n[3] 数据已保存: {OUT_FILE}")

    # 验证文件
    with open(OUT_FILE, 'r') as f:
        lines = f.readlines()
    print(f"  文件行数: {len(lines)} (含表头)")
    print(f"  首行(表头): {lines[0].strip()}")
    print(f"  第二行(数据): {lines[1].strip()}")
    sample_row = lines[1].strip()
else:
    sample_row = "N/A"
    print("  没有数据！")

# ── Step 4: 对比 ──────────────────────────────────────────────
# baostock 基准: 18 分钟 = 1080 秒 (THREADS=1)
baostock_time = 18 * 60

if ak_total > 0:
    ratio = baostock_time / ak_total
    if ratio > 1:
        comparison = f"快 {ratio:.1f} 倍"
    else:
        comparison = f"慢 {1/ratio:.1f} 倍"
    comp_detail = f"baostock: {baostock_time:.0f}s (18分钟) / akshare: {ak_total:.1f}s → {ratio:.2f}x"
else:
    comparison = "无法计算"
    comp_detail = ""

# 前复权测试（抽样 5 只）
print("\n[5] 前复权 (adjust='qfq') 测试...")
qfq_test_codes = ['sh600000', 'sz000001', 'sh600519', 'sz000858', 'sh600036']
qfq_ok = 0
qfq_sample = ""
for code in qfq_test_codes:
    try:
        df = ak.stock_zh_a_hist_tx(symbol=code, start_date='20260417', end_date='20260417', adjust='qfq')
        if df is not None and not df.empty:
            qfq_ok += 1
            if not qfq_sample:
                qfq_sample = f"qfq: date={df.iloc[0]['date']}, open={df.iloc[0]['open']}, close={df.iloc[0]['close']}"
    except:
        pass
print(f"  前复权测试: {qfq_ok}/5 支持")

# ── Step 5: 生成报告 ─────────────────────────────────────────
report = f"""akshare benchmark 结果
=======================
日期: 2026-04-17
股票只数: {len(all_codes)}
下载接口: akshare.stock_zh_a_hist_tx (腾讯证券)

akshare 耗时: {ak_total:.1f}秒 ({ak_total/60:.2f}分钟)
akshare 数据条数: {len(all_rows)}
akshare 失败只数: {failed}
akshare 数据样例: {sample_row}

对比 baostock: {comparison}
  - baostock 基准: {baostock_time:.0f}s (18分钟, THREADS=1)
  - akshare 耗时:  {ak_total:.1f}s
  - 比率: {ratio:.2f}x

前复权支持: {'是' if qfq_ok > 0 else '否'} ({qfq_ok}/5 测试通过)
{qfq_sample}

实现细节:
  - 并发线程: {MAX_WORKERS}
  - 单只耗时(10线程测试): ~0.3s
  - 接口: 腾讯证券历史数据
"""

with open(LETTER_FILE, 'w') as f:
    f.write(report)

print(f"\n[6] 报告已保存: {LETTER_FILE}")
print()
print("=" * 60)
print(report)
