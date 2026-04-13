# Dream Diary

<!-- openclaw:dreaming:diary:start -->
---

*April 13, 2026*

<!-- openclaw:dreaming:backfill-entry day=2026-04-13 source=memory/2026-04-13.md -->

What Happened

1. **苏沪造价速算 V1.6→V1.9 迭代完成（00:01-01:56）**:
   - 老板发来 HTML 文件，要求核实数据并部署
   - V1.6 南京基准版数据全部对齐实测（住宅/厂房/办公楼/道路四个工程类型）
   - GitHub Pages 部署成功：https://wkx1204.github.io/cost-app/
   - 老板要求加版本号时 V1.8 把"项目年份"下拉弄丢了 → 被狠批（重要教训）
   - 之后每次改版都完整检查所有输入项完整性
   - V1.14-V1.16 装修说明初始空白 bug（依赖 JS 填充，window.onload 时机问题）
   - V1.9 正式版：修复装修说明初始内容 + 钢结构厂房装修标准锁死

2. **Cloudflare Pages 国内镜像部署（02:19-02:22）**:
   - GitHub Pages 国内打不开 → 需要国内可访问镜像
   - 尝试 cloudflared 临时隧道（成功但临时）、wrangler CLI（OAuth 认证问题）
   - 老板协助完成 wrangler OAuth 登录 → 部署成功
   - **永久 URL：https://cost-app.pages.dev/**（Cloudflare 全球 CDN，国内可访问）
   - 二维码发到 QQ，老板确认"牢牢记住"

3. **V1.9 正式版已推送 GitHub（01:56）**:
   - commit: b2dce4f，V1.9 = 基于 V1.16 修复版 + 版本号

4. **版本迭代回顾（V1.6→V1.9）**:
   - V1.10：材料波动步进器 + 三色装修卡片
   - V1.11：厂房楼层禁用 + H<12m 显示
   - V1.14：年份精简为4个 + 装修动态卡片
   - V1.15：年份扩充回7个（加回2020-2022）
   - V1.16：装修说明初始空白修复 + 材料波动按钮行高修复

Reflections
1. **"任何老板可见的改动，发出去之前自己先完整测试一遍"** — V1.8 翻车后建立的铁律，每次改版都有完整检查清单
2. **"默认状态必须在 HTML 里可见，不能全靠 JS 撑"** — V1.15 装修说明空白教训，避免依赖 JS 时机的默认值陷阱
3. **"网络不稳定时，先确认文件在本地，再用网络命令"** — git clone 超时教训，保留 /tmp 最新版本作为备用
4. **"用老板已有资源"** — Cloudflare 账号是现成的，直接用 wrangler 部署，不折腾新平台

---
