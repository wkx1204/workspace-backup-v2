#!/usr/bin/env python3
"""
A股增量更新脚本（串行版，逐只查询）
下载指定日期数据并追加到 astock_full.csv
"""
import baostock as bs
import time, os, sys
from datetime import datetime, timedelta

OUTPUT_PATH = '/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv'
TARGET_DATE = '2026-04-16'  # 指定日期

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def main():
    log(f"增量更新（串行版）：下载 {TARGET_DATE} 数据，逐只查询")

    # 登录获取股票列表
    lg = bs.login()
    if lg.error_code != '0':
        log(f"登录失败: {lg.error_msg}")
        sys.exit(1)

    rs = bs.query_all_stock(day=TARGET_DATE)
    data = []
    while rs.error_code == '0' and rs.next():
        data.append(rs.get_row_data())
    bs.logout()

    ashare = sorted([
        r[0] for r in data
        if (r[0].startswith('sh.6') or r[0].startswith('sz.0') or r[0].startswith('sz.3')) and len(r[0]) == 9
    ])
    log(f"A 股: {len(ashare)} 只")

    all_rows = []
    done = 0
    errors = 0

    for i, code in enumerate(ashare):
        try:
            lg = bs.login()
            if lg.error_code != '0':
                errors += 1
                continue

            rs = bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,volume,amount,adjustflag",
                start_date=TARGET_DATE, end_date=TARGET_DATE,
                frequency="d", adjustflag="3"
            )

            while rs.error_code == '0' and rs.next():
                row = rs.get_row_data()
                if row[0] == TARGET_DATE:
                    all_rows.append(','.join(row) + '\n')

            bs.logout()
        except Exception as e:
            bs.logout()
            errors += 1

        done += 1
        if done % 500 == 0 or done == len(ashare):
            log(f"  进度 {done}/{len(ashare)}, 累计 {len(all_rows)} 条")

    if all_rows:
        with open(OUTPUT_PATH, 'a') as f:
            f.writelines(all_rows)

    log(f"完成！写入 {len(all_rows)} 条 {TARGET_DATE} 数据，查询异常 {errors} 次")
    if os.path.exists(OUTPUT_PATH):
        size = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
        log(f"文件: {size:.1f} MB")

if __name__ == '__main__':
    main()
