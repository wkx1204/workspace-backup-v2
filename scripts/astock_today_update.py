#!/usr/bin/env python3
"""
A股今日增量更新脚本
只下载今日收盘数据并追加到 astock_full.csv
优化版：去掉人为 sleep，网络延迟即是最快速度
baostock 全局 socket 不支持真并发，强行并发只会触发 Bad file descriptor
"""
import baostock as bs
import time, os, sys
from datetime import datetime, timedelta

OUTPUT_PATH = '/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv'
TODAY = datetime.now().strftime('%Y-%m-%d')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

log(f"增量更新：下载 {TODAY} 数据")

lg = bs.login()
if lg.error_code != '0':
    log(f"登录失败: {lg.error_msg}")
    sys.exit(1)

# 获取股票列表
rs = bs.query_all_stock(day=YESTERDAY)
data = []
while rs.error_code == '0' and rs.next():
    data.append(rs.get_row_data())
ashare = sorted([
    r[0] for r in data
    if (r[0].startswith('sh.6') or r[0].startswith('sz.0') or r[0].startswith('sz.3')) and len(r[0]) == 9
])
log(f"A 股: {len(ashare)} 只")

fields = "date,code,open,high,low,close,volume,amount,adjustflag"
today_count = 0
errors = 0
error_codes = []
today_rows = []

# 逐只查询，无额外 sleep（网络延迟即最快）
for i, code in enumerate(ashare):
    try:
        rs = bs.query_history_k_data_plus(
            code, fields,
            start_date=TODAY, end_date=TODAY,
            frequency="d", adjustflag="3"
        )
        while rs.error_code == '0' and rs.next():
            row = rs.get_row_data()
            if row[0] == TODAY:
                today_rows.append(','.join(row) + '\n')
                today_count += 1
    except Exception as e:
        errors += 1
        error_codes.append(code)
    
    if (i + 1) % 500 == 0 or i + 1 == len(ashare):
        log(f"  进度 {i+1}/{len(ashare)}, 累计写入 {today_count} 条今日数据")

# 一次性写入
if today_rows:
    with open(OUTPUT_PATH, 'a') as f:
        f.writelines(today_rows)

bs.logout()
log(f"完成！写入 {today_count} 条 {TODAY} 数据，错误 {errors} 次")
if error_codes[:5]:
    log(f"前几个出错: {error_codes[:5]}")

if os.path.exists(OUTPUT_PATH):
    size = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    log(f"文件: {size:.1f} MB")
