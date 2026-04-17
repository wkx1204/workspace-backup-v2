#!/bin/bash
# A股增量更新 - 新浪接口 + curl 并行 (绕过Python代理)
# 2026-04-17 02:00
# 速度预估: 5484只 / 30并行 ≈ 183秒 ≈ 3分钟

set -e
DEST="/Volumes/XB_Home/小兰/astock_data/daily/astock_full.csv"
TODAY="2026-04-16"

# 从现有CSV提取所有A股代码 (去重)
STOCKS=$(mktemp)
awk -F',' 'NR>1 && $2!~/^(sh|sz|bj)/ {code=$2; if(code~/^6/) code="sh"code; else code="sz"code} code {print code}' "$DEST" 2>/dev/null | sort -u > "$STOCKS"
TOTAL=$(wc -l < "$STOCKS")
echo "[$(date +%H:%M:%S)] 共 $TOTAL 只股票，开始抓取 $TODAY ..."

# 临时输出文件
OUT=$(mktemp)
echo "日期,股票代码,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率" > "$OUT"

# 计数器
DONE=0
FAIL=0

# 并行抓取函数 (单只)
do_fetch() {
    local sym=$1
    local url="https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=${sym}&scale=240&ma=no&datalen=5"
    local json=$(curl -s --max-time 8 -H "Referer: https://finance.sina.com.cn" "$url" 2>/dev/null)
    # 解析JSON，找目标日期
    echo "$json" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    for d in data:
        if d.get('day') == '$TODAY':
            o=d['open']; c=d['close']; h=d['high']; l=d['low']; v=d['volume']
            pct=round((float(c)-float(o))/float(o)*100,2) if float(o)!=0 else 0
            print(f\"{d['day']},{sym},{o},{c},{h},{l},{v},0,0,{pct},0,0\")
            break
except: pass
" 2>/dev/null
}
export -f do_fetch
export TODAY

# xargs 30 并行
cat "$STOCKS" | xargs -P30 -I{} bash -c "do_fetch {}" >> "$OUT" 2>/dev/null

DONE=$(tail -n +2 "$OUT" | wc -l)
echo "[$(date +%H:%M:%S)] 抓取完成: $DONE/$TOTAL"

# 追加到主文件 (去除同日期旧数据)
if [ $DONE -gt 0 ]; then
    # 删除目标日期的旧记录
    grep -v "^${TODAY}," "$DEST" > "${DEST}.bak"
    # 追加新数据
    tail -n +2 "$OUT" >> "${DEST}.bak"
    mv "${DEST}.bak" "$DEST"
    echo "[$(date +%H:%M:%S)] 已更新 $DEST (追加 $TODAY, $DONE 条)"
fi

# 清理
rm -f "$STOCKS" "$OUT"
echo "[$(date +%H:%M:%S)] 完成！"
