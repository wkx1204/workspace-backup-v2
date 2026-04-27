#!/usr/bin/env python3
"""
早报脚本 - 每天8:45通过小兰QQ发送
内容：隔夜美股三大指数 + 中概股 + 重大新闻
"""
import urllib.request, json, os, sys
from datetime import datetime, timezone, timedelta
from urllib.request import ProxyHandler, build_opener, Request

EASTMONEY_URL = "https://push2.eastmoney.com/api/qt/ulist.np/get"

# 美股指数  secid -> 显示名
US_INDICES = {
    "100.DJIA": "道琼斯",
    "100.SPX": "标普500",
    "100.NDX": "纳斯达克",
}

# 主要中概股
CHINA_STOCKS = {
    "105.BABA": "阿里巴巴",
    "105.TCEHY": "腾讯(ADR)",
    "105.JD": "京东",
    "105.BIDU": "百度",
    "105.NTES": "网易",
    "105.XPEV": "小鹏汽车",
    "105.NIO": "蔚来",
    "105.LI": "理想汽车",
}

def _no_proxy_open(url, timeout=15):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    opener = build_opener(ProxyHandler({}))
    return opener.open(req, timeout=timeout)

def fetch_quotes(secid_list):
    url = f"{EASTMONEY_URL}?fltt=2&secids={','.join(secid_list)}&fields=f2,f3,f12"
    resp = _no_proxy_open(url)
    data = json.loads(resp.read())
    results = {}
    for item in data.get("data", {}).get("diff", []):
        results[item["f12"]] = {
            "price": item.get("f2"),
            "change_pct": item.get("f3"),
        }
    return results

def get_weekday_cn():
    now = datetime.now(timezone(timedelta(hours=8)))
    days = ["一", "二", "三", "四", "五", "六", "日"]
    return days[now.weekday()]

QQ_TARGET = "CADF977D8F6C11C1C68D5271F6966428"


def build_briefing():
    now = datetime.now(timezone(timedelta(hours=8)))
    if now.weekday() >= 5:
        return (f"📅 {now.strftime('%Y-%m-%d')} 周{get_weekday_cn()}\n"
                "━━━━━━━━━━━\n"
                "周末休市，美股已收盘。\n☕ 祝老板周末愉快！")

    wd = get_weekday_cn()
    lines = [
        f"📊 小兰早报 | {now.strftime('%Y-%m-%d')} 周{wd}",
        "━━━━━━━━━━━",
        "",
        "🇺🇸【隔夜美股】",
    ]

    us_data = fetch_quotes(list(US_INDICES.keys()))
    for sid, name in US_INDICES.items():
        short = sid.split(".")[-1]
        d = us_data.get(sid) or us_data.get(short)
        if d and d["price"] is not None:
            arrow = "🔴" if d["change_pct"] and d["change_pct"] < 0 else "🟢"
            lines.append(f"  {arrow} {name}: {d['price']} ({d['change_pct']:+.2f}%)")
        else:
            lines.append(f"  ⚪ {name}: 数据暂缺")

    lines += ["", "🇨🇳【热门中概】"]
    cn_data = fetch_quotes(list(CHINA_STOCKS.keys()))
    for sid, name in CHINA_STOCKS.items():
        short = sid.split(".")[-1]
        d = cn_data.get(sid) or cn_data.get(short)
        if d and d["price"] is not None:
            arrow = "🔴" if d["change_pct"] and d["change_pct"] < 0 else "🟢"
            lines.append(f"  {arrow} {name}: ${d['price']} ({d['change_pct']:+.2f}%)")
        else:
            lines.append(f"  ⚪ {name}: 暂无数据")

    lines += [
        "",
        "━━━━━━━━━━━",
        f"💡 数据: 东方财富 | {now.strftime('%H:%M')}",
    ]
    return "\n".join(lines)

def send_via_openclaw(msg):
    """通过 OpenClaw message send 直发QQ"""
    import subprocess
    cmd = [
        "/opt/homebrew/bin/openclaw", "message", "send",
        "--channel", "qqbot",
        "--account", "xl",
        "--target", QQ_TARGET,
        "--message", msg,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("✅ 早报已通过小兰发送")
        return True
    else:
        print(f"❌ 发送失败: {result.stderr}")
        print("早报内容:")
        print(msg)
        return False

if __name__ == "__main__":
    msg = build_briefing()
    print(msg)
    print()
    send_via_openclaw(msg)