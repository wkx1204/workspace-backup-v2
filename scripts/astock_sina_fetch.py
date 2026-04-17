#!/usr/bin/env python3
"""
A股增量更新 - 新浪接口 + curl 并行 (绕过Python代理问题)
2026-04-17 02:00
速度: 5484只 / 50并行 ≈ 3-5分钟
"""
import subprocess, json, time, csv, sys, os, re
from concurrent.futures import ThreadPoolExecutor, as_completed

DEST = "/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv"
TODAY = "2026-04-16"

def get_stock_codes():
    """从CSV提取所有A股代码（格式 sh.600000 -> sh600000）"""
    codes = set()
    try:
        with open(DEST, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) < 2: continue
                raw = row[1].strip()
                # sh.600000 -> sh600000
                code = raw.replace("sh.", "sh").replace("sz.", "sz").replace("bj.", "bj")
                if len(code) >= 7 and code[:2] in ("sh", "sz", "bj") and code[2:].isdigit():
                    codes.add(code)
    except Exception as e:
        print(f"读代码失败: {e}", file=sys.stderr)
    return sorted(codes)

def fetch_one(sym):
    """curl单只股票，返回Apr16数据行或None"""
    url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sym}&scale=240&ma=no&datalen=5"
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "10",
             "-H", "Referer: https://finance.sina.com.cn",
             url],
            capture_output=True, text=True, timeout=12
        )
        if not r.stdout.strip().startswith('['): return None
        data = json.loads(r.stdout)
        for d in data:
            if d.get("day") == TODAY:
                o, c, h, l, v = float(d['open']), float(d['close']), float(d['high']), float(d['low']), d['volume']
                pct = round((c - o) / o * 100, 2) if o != 0 else 0
                return f"{d['day']},{sym},{o},{c},{h},{l},{v},0,0,{pct},0,0"
    except:
        pass
    return None

def main():
    print(f"[{time.strftime('%H:%M:%S')}] 读取股票列表...")
    codes = get_stock_codes()
    total = len(codes)
    print(f"[{time.strftime('%H:%M:%S')}] 共 {total} 只，开始抓取 {TODAY} ...")

    results = []
    done = 0
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=50) as ex:
        futures = {ex.submit(fetch_one, c): c for c in codes}
        for fut in as_completed(futures):
            done += 1
            row = fut.result()
            if row:
                results.append(row)
            if done % 500 == 0 or done == total:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                remain = (total - done) / rate if rate > 0 else 0
                print(f"[{time.strftime('%H:%M:%S')}] {done}/{total} ({done*100//total}%) 成功{len(results)} 剩余~{remain:.0f}秒")

    print(f"[{time.strftime('%H:%M:%S')}] 抓取完成: {len(results)}/{total} 耗时{time.time()-t0:.0f}秒")

    if results:
        # 备份+去重合并
        bak = DEST + ".bak"
        written = 0
        if os.path.exists(DEST):
            with open(DEST, 'r', encoding='utf-8') as f:
                existing = set(line.strip() for line in f if line.startswith(TODAY + ","))
            with open(bak, 'w', encoding='utf-8') as f:
                for line in open(DEST, 'r', encoding='utf-8'):
                    if not line.strip().startswith(TODAY + ","):
                        f.write(line)
        else:
            existing = set()
            with open(bak, 'w', encoding='utf-8') as f:
                f.write("日期,股票代码,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率\n")
        
        new_lines = [r for r in results if r not in existing]
        with open(bak, 'a', encoding='utf-8') as f:
            for r in new_lines:
                f.write(r + "\n")
        
        os.replace(bak, DEST)
        print(f"[{time.strftime('%H:%M:%S')}] 已更新 {DEST} (新增 {len(new_lines)} 条 {TODAY} 数据)")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] 没有抓到任何数据！")

if __name__ == "__main__":
    main()
