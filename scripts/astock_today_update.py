#!/usr/bin/env python3
"""
A股今日增量更新脚本（并发版）
只下载今日收盘数据并追加到 astock_full.csv
使用 ThreadPoolExecutor 并发查询，压缩到1-2分钟内完成
"""
import baostock as bs
import time, os, sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_PATH = '/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv'
TODAY = datetime.now().strftime('%Y-%m-%d')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
THREADS = 1  # 并发线程数

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def query_stock(code):
    """单只股票查询，返回 (code, rows_list)"""
    try:
        # 每线程独立登录
        lg = bs.login()
        if lg.error_code != '0':
            return code, []
        
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount,adjustflag",
            start_date=TODAY, end_date=TODAY,
            frequency="d", adjustflag="3"
        )
        rows = []
        while rs.error_code == '0' and rs.next():
            row = rs.get_row_data()
            if row[0] == TODAY:
                rows.append(','.join(row) + '\n')
        
        bs.logout()
        return code, rows
    except Exception as e:
        return code, []

def main():
    log(f"增量更新（并发版）：下载 {TODAY} 数据，{THREADS} 线程")

    # 全局登录获取股票列表
    lg = bs.login()
    if lg.error_code != '0':
        log(f"登录失败: {lg.error_msg}")
        sys.exit(1)

    rs = bs.query_all_stock(day=YESTERDAY)
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

    # 并发查询
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(query_stock, code): code for code in ashare}
        for future in as_completed(futures):
            code, rows = future.result()
            done += 1
            if rows:
                all_rows.extend(rows)
            else:
                errors += 1
            if done % 1000 == 0 or done == len(ashare):
                log(f"  进度 {done}/{len(ashare)}, 累计 {len(all_rows)} 条")

    # 一次性写入
    if all_rows:
        with open(OUTPUT_PATH, 'a') as f:
            f.writelines(all_rows)

    log(f"完成！写入 {len(all_rows)} 条 {TODAY} 数据，查询异常 {errors} 次")
    if os.path.exists(OUTPUT_PATH):
        size = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
        log(f"文件: {size:.1f} MB")

if __name__ == '__main__':
    main()
