#!/usr/bin/env python3
"""
A股增量更新脚本（断点续传版）
- 支持 --date 指定日期，默认昨天
- 每下载 200 只股票自动写入检查点快照
- 被 kill 后重跑会自动从检查点恢复，跳过已完成的
- 检查点文件：~/.openclaw/astock_checkpoint_<date>.json
"""
import baostock as bs
import time, os, sys, json
from datetime import datetime, timedelta

OUTPUT_PATH = '/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv'
CHECKPOINT_DIR = os.path.expanduser('~/.openclaw')
THREADS = 1
BATCH_SIZE = 200  # 每200只写一次检查点

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_date():
    if len(sys.argv) >= 2 and sys.argv[1] == '--date':
        return sys.argv[2]
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

TODAY = get_date()
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_stock_list():
    lg = bs.login()
    rs = bs.query_all_stock(day=YESTERDAY)
    data = []
    while rs.error_code == '0' and rs.next():
        data.append(rs.get_row_data())
    bs.logout()
    return sorted([
        r[0] for r in data
        if (r[0].startswith('sh.6') or r[0].startswith('sz.0') or r[0].startswith('sz.3')) and len(r[0]) == 9
    ])

def load_checkpoint(date):
    ckpt_file = os.path.join(CHECKPOINT_DIR, f'astock_checkpoint_{date}.json')
    if os.path.exists(ckpt_file):
        with open(ckpt_file) as f:
            d = json.load(f)
        log(f"检查点恢复：跳过前 {len(d['done'])} 只已完成的股票")
        return d['done'], set(d['done'])
    return [], set()

def save_checkpoint(date, done, all_rows):
    ckpt_file = os.path.join(CHECKPOINT_DIR, f'astock_checkpoint_{date}.json')
    with open(ckpt_file, 'w') as f:
        json.dump({'done': done, 'count': len(all_rows)}, f)
    log(f"  检查点已保存 ({len(done)} 只)")

def query_stock(code, date):
    try:
        lg = bs.login()
        if lg.error_code != '0':
            return code, []
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount,adjustflag",
            start_date=date, end_date=date,
            frequency="d", adjustflag="3"
        )
        rows = []
        while rs.error_code == '0' and rs.next():
            row = rs.get_row_data()
            if row[0] == date:
                rows.append(','.join(row) + '\n')
        bs.logout()
        return code, rows
    except:
        return code, []

def main():
    log(f"增量更新（断点续传）：下载 {TODAY} 数据，{THREADS} 线程")

    # 获取股票列表
    ashare = get_stock_list()
    log(f"A 股: {len(ashare)} 只")

    # 加载检查点
    done_list, done_set = load_checkpoint(TODAY)
    remaining = [c for c in ashare if c not in done_set]
    log(f"待下载: {len(remaining)} 只")

    all_rows = []
    done = 0
    errors = 0

    for code in remaining:
        code, rows = query_stock(code, TODAY)
        done_list.append(code)
        done += 1
        if rows:
            all_rows.extend(rows)
        else:
            errors += 1

        if done % BATCH_SIZE == 0:
            save_checkpoint(TODAY, done_list, all_rows)
            log(f"  进度 {done}/{len(remaining)}, 累计 {len(all_rows)} 条，误差 {errors}")

    # 最终写入
    if all_rows:
        with open(OUTPUT_PATH, 'a') as f:
            f.writelines(all_rows)

    # 删除检查点（完成）
    ckpt_file = os.path.join(CHECKPOINT_DIR, f'astock_checkpoint_{TODAY}.json')
    if os.path.exists(ckpt_file):
        os.remove(ckpt_file)

    log(f"完成！写入 {len(all_rows)} 条 {TODAY} 数据，查询异常 {errors} 次")
    if os.path.exists(OUTPUT_PATH):
        size = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
        log(f"文件: {size:.1f} MB")

if __name__ == '__main__':
    main()