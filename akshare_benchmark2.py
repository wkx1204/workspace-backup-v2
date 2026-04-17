#!/usr/bin/env python3
"""
akshare (腾讯接口) vs baostock benchmark
Target: 2026-04-17 full market daily data
"""

import time
import csv
import json
import concurrent.futures

OUT_FILE = "/Volumes/XB_Home/小兰/astock_data/daily/astock_ak_20260417.csv"
LETTER_FILE = "/Volumes/XB_Home/小兰/小兰/letters/2026-04-17-akshare-benchmark.txt"

print("=" * 60)
print("akshare (腾讯接口) benchmark")
print("=" * 60)

# ── Step 1: 加载代码列表 ──────────────────────────────────────
with open('/tmp/tx_codes_20260417.json') as f:
    all_codes = json.load(f)
print(f"\n[1] 股票只数: {len(all_codes)}")
print(f"  前5只: {all_codes[:5]}")

# ── Step 2: 下载 ─────────────────────────────────────────────
import akshare as ak

print(f"\n[2] 开始下载 2026-04-17 数据 ({len(all_codes)} 只)...")
ak_start = time.time()

def fetch_one(tx_code):
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
MAX_WORKERS = 20

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(fetch_one, c): c for c in all_codes}
    done = 0
    for f in concurrent.futures.as_completed(futures):
        r = f.result()
        if r:
            all_rows.append(r)
        else:
            failed += 1
        done += 1
        if done % 500 == 0 or done == total:
            elapsed = time.time() - ak_start
            rate = done / elapsed if elapsed > 0 else 0
            eta_s = (total - done) / rate if rate > 0 else 0
            print(f"  {done}/{total} ({elapsed:.0f}s, {rate:.1f}/s, ETA {eta_s:.0f}s)")

ak_end = time.time()
ak_total = ak_end - ak_start
print(f"\n  总耗时: {ak_total:.1f}s ({ak_total/60:.2f}分钟)")
print(f"  成功: {len(all_rows)}, 失败: {failed}")

# ── Step 3: 保存 ─────────────────────────────────────────────
if all_rows:
    with open(OUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'code', 'open', 'high', 'low', 'volume'])
        writer.writeheader()
        writer.writerows(all_rows)

    with open(OUT_FILE) as f:
        lines = f.readlines()
    sample_row = lines[1].strip() if len(lines) > 1 else "N/A"
    print(f"\n[3] 已保存: {OUT_FILE}")
    print(f"  行数: {len(lines)} (含表头)")
    print(f"  表头: {lines[0].strip()}")
    print(f"  首行数据: {lines[1].strip()}")
else:
    sample_row = "N/A"

# ── Step 4: 前复权测试 ────────────────────────────────────────
print("\n[4] 前复权测试 (5 只抽样)...")
qfq_codes = ['sh600000', 'sz000001', 'sh600519', 'sz000858', 'sh600036']
qfq_ok = 0
qfq_detail = ""
for code in qfq_codes:
    try:
        df = ak.stock_zh_a_hist_tx(symbol=code, start_date='20260417', end_date='20260417', adjust='qfq')
        if df is not None and not df.empty:
            qfq_ok += 1
            if not qfq_detail:
                qfq_detail = f"qfq sample: open={df.iloc[0]['open']}, close={df.iloc[0]['close']}"
    except:
        pass
print(f"  前复权支持: {'是' if qfq_ok >= 4 else '部分' if qfq_ok > 0 else '否'} ({qfq_ok}/5)")

# ── Step 5: 报告 ────────────────────────────────────────────
baostock_time = 18 * 60  # 18分钟
ratio = baostock_time / ak_total if ak_total > 0 else 0
comparison = f"快 {ratio:.1f} 倍" if ratio > 1 else f"慢 {1/ratio:.1f} 倍"

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

前复权支持: {'是' if qfq_ok >= 4 else '部分' if qfq_ok > 0 else '否'} ({qfq_ok}/5)
{qfq_detail}

实现细节:
  - 并发线程: {MAX_WORKERS}
  - 接口: 腾讯证券历史数据 (非 eastmoney)
  - 注意: akshare 默认 eastmoney 接口在此环境中被代理拦截，腾讯接口可连通
"""

with open(LETTER_FILE, 'w') as f:
    f.write(report)
print(f"\n[5] 报告已保存: {LETTER_FILE}")
print()
print(report)
