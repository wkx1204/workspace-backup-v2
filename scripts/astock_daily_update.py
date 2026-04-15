#!/usr/bin/env python3
"""
A股日线数据每日更新脚本
覆盖沪深A股全量股票 (sh.6 / sz.0 / sz.3)
输出: /Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv
"""
import baostock as bs
import time
import os
from datetime import datetime, timedelta

OUTPUT_PATH = '/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv'
TEMP_PATH = '/tmp/astock_new.csv'
START_DATE = '2021-04-01'
TODAY = datetime.now().strftime('%Y-%m-%d')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

log(f"开始下载 A 股数据 {START_DATE} ~ {TODAY}")

lg = bs.login()
if lg.error_code != '0':
    log(f"登录失败: {lg.error_msg}")
    exit(1)

# 用昨日获取股票列表（盘中用今日可能数据不完整）
rs = bs.query_all_stock(day=YESTERDAY)
all_stocks_raw = []
while rs.error_code == '0' and rs.next():
    all_stocks_raw.append(rs.get_row_data())

ashare_codes = sorted([
    r[0] for r in all_stocks_raw
    if (r[0].startswith('sh.6') or r[0].startswith('sz.0') or r[0].startswith('sz.3')) and len(r[0]) == 9
])
log(f"A 股股票数: {len(ashare_codes)}")

if os.path.exists(TEMP_PATH):
    os.remove(TEMP_PATH)

fields = "date,code,open,high,low,close,volume,amount,adjustflag"
total_rows = 0
errors = 0

for i, code in enumerate(ashare_codes):
    try:
        rs = bs.query_history_k_data_plus(
            code, fields,
            start_date=START_DATE, end_date=TODAY,
            frequency="d", adjustflag="3"
        )
        rows = []
        while rs.error_code == '0' and rs.next():
            rows.append(rs.get_row_data())
        if rows:
            with open(TEMP_PATH, 'a') as f:
                for row in rows:
                    f.write(','.join(row) + '\n')
            total_rows += len(rows)
        if rs.error_code != '0':
            errors += 1
    except Exception as e:
        errors += 1

    if (i + 1) % 200 == 0:
        log(f"  进度 {i+1}/{len(ashare_codes)}, 累计 {total_rows} 条, 错误 {errors}")

    time.sleep(0.05)

bs.logout()

if os.path.exists(TEMP_PATH):
    os.replace(TEMP_PATH, OUTPUT_PATH)
    size_mb = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    log(f"完成！{total_rows} 条写入 {OUTPUT_PATH} ({size_mb:.1f} MB), 错误 {errors} 次")
else:
    log("错误：未生成文件")
    exit(1)
