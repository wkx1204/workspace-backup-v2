# MEMORY.md — 小白长期记忆

> 本文件存放**重要、不易变化**的长期记忆。身份定义在 SOUL.md，老板偏好在 USER.md，工作流程在 AGENTS.md。
> 每月最后一天 review 一次，删除过时内容。

---

## 一、身份关系

### 三姐妹分工
| 名称 | workspace | 职责 |
|------|-----------|------|
| **小白（主脑）** | workspace-main | 总调度，信息汇聚 |
| **小红 (Xh)** | workspace-xh | 文字/网页/写作 |
| **小兰 (Xl)** | workspace-xl | 金融/股票数据 |

- 遇到跨领域任务主动找小红/小兰协作
- 媒体发送直接走小白的 QQ 端，不中转
- QQ ID：`7E2E8699372FE33EC4E2DA736D020639`
- 网页端看不到 `<qqmedia>` 标签，去 QQ 端查看

---

## 二、老板快捷指令

- **新话题** → 归纳结论 + 收尾，等新话题
- **握手协议**：老板说"结束话题"/"新话题" → 先完成记忆写入，再收尾

### 老板缩写约定
| 缩写 | 含义 |
|------|------|
| 小弟 | subagent |
| x盘 | /Volumes/XB_Home/ |
| ob笔记 | Obsidian Vault |
| 看图 | 截屏 → 上传页传图 → 喊我看 → 调 qwen-vl-plus |

---

## 三、本地模型架构

### oMLX（Mac mini M4）
- 端口：`8000`，API Key：`12345678`
- 模型：
  - **Qwen3.5-9B-MLX-4bit**（对话，131072 ctx）
  - **bge-m3-mlx-4bit**（Embedding）
- 启动：`/Applications/oMLX.app/Contents/MacOS/python3 -m omlx.cli serve --base-path /Users/wf/.omlx --port 8000`
- LaunchAgent 已配置，开机自启

### OpenClaw Memory Search
- **已禁用**：`agents.defaults.memorySearch.enabled = false`
- 改用 exec + grep 搜索（见 AGENTS.md）

---

## 四、看图（唯一正确方式）

> 不用 image tool，直接调 DashScope API

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen-vl-plus", "messages": [{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,【BASE64】"}},
    {"type": "text", "text": "描述图片内容"}
  ]}]}'
```
- base64：`base64 -i /path/to/image.jpg | tr -d '\n'`

### 图生图
- 模型：qwen-image-2.0（0.2元/张）
- wanx-v1 已下线（2026-03-27），勿用

---

## 五、图片上传通道

- 上传页：`http://127.0.0.1:18790/`
- 存储路径：`~/.openclaw/workspace-main/inbox/upload_*`
- inbox 每日零点自动清理（系统 crontab）

### 看图流程
1. 老板截屏
2. 打开上传页拖图
3. 网页端喊「看图」
4. 去 `~/Desktop/` 找最新截图（按 mtime），调 qwen-vl-plus

---

## 六、外接硬盘存储

- **路径**：`/Volumes/XB_Home/`
- **临时文件**：→ `/tmp/` → 分析完即删
- **生成内容**：→ `/Volumes/XB_Home/小白生成图/` → 永久保存

---

## 七、TTS 语音

- 命令：`DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" python3 ~/.openclaw/workspace/skills/qwen3-tts-instruct/scripts/tts.py "文字" --voice Serena --mood gentle -f mp3 -o output.mp3`
- 流程：MP3 → ffmpeg 转 WAV → message send --media

---

## 八、视频生成

- 模型：wan2.6-i2v-flash（图生视频，5秒720P）
- API：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
- 必须加 header：`X-DashScope-Async: enable`

---

## 九、项目备份

| 仓库 | 内容 |
|------|------|
| workspace-backup | workspace-main（排除 .openclaw/） |
| obsidian-backup | Obsidian Vault |
| xiaobai-homepage | 小白主页静态站 |

- 目录：~/.openclaw/workspace-main/xiaobai-site/
- GitHub：wkx1204/xiaobai-homepage
- 代理：`https_proxy=http://127.0.0.1:10808`

---

## 十、其他配置

### Cloudflare Worker 订阅
- 域名：**wkx1204.us.ci**
- 项目：frosty-bar-be79
- 格式：`https://wkx1204.us.ci/<UUID>`

### ClawHub 镜像
- 中国镜像：https://cn.clawhub-mirror.com
- 优先使用

### Mac Mini M4 硬件
- HDMI 休眠唤醒握手失败，推荐 USB-C 转 DP 1.4 直连

---

## 十一、常见错误

| 错误 | 正确做法 |
|------|---------|
| 看图折腾 imageModel | 直接调 qwen-vl-plus API |
| upload_server 崩了 | `cd ~/.openclaw/workspace-main && python3 scripts/upload_server.py &` |
| exec 裸跑 | 必须带 timeout |

---

## 十二、记忆搜索

- **禁止**：memory_search 工具（已禁用）
- **正确**：exec + grep
- skill：`~/.openclaw/workspace-main/skills/grep-search/SKILL.md`

---

## 十三、Librarian Skill（URL 路由）

### Obsidian 仓库路径
`~/Documents/Obsidian Vault/`

### PARA 结构
- `0-project` / `1-area` / `2-resource/clip` / `2-resource/github-research` / `2-resource/youtube` / `3-archived`

### 路由规则
| 类型 | 路径 |
|------|------|
| 普通文章 | `2-resource/clip/clips.md` 表格 |
| GitHub 项目 | `2-resource/github-research/{owner}/{repo}/owner-repo.md` |
| YouTube 视频 | `2-resource/youtube/` 独立总结 |
| 微信公众号 | 优先正文提取，失败则浏览器 |

### URL 规范化
- 移除 `utm_*` 和 YouTube `si=` 参数

---

## 十四、Chrome 实时监控

- AppleScript 获取 URL：`osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'`
- Playwright 抓内容：`from playwright.sync_api import sync_playwright`
- 依赖：Playwright ✅，Chrome AppleScript 权限 ✅

## 晋升记忆 — 2026-04-11（凌晨补充）

### Dreaming 功能完全跑通（2026-04-10 深夜）
- `rem-harness --path ~/Documents/Obsidian\ Vault/memory/` 才有内容，`--path` 必须加
- `rem-backfill --path ~/Documents/Obsidian\ Vault/memory/` 写入 8 条到 DREAMS.md
- 目标目录是 Obsidian vault 的 memory/，不是 workspace memory/

### 老板新增四条工作原则（2026-04-10 确认）
1. 收到任务先判断类型（搜索/分析/写作/代码/查询），再决定如何处理
2. 模糊/复杂问题先确认对齐，不猜意图，不自作主张
3. 深度问题：结论+完整分析，逻辑走完，主脑待命，subagent 执行
4. 不知道就说不知道，优先上网搜索，搜不到如实说，不胡编

### 三姐妹协作规则重申（2026-04-10）
- 小白、小红、小兰是三个最重要帮手，要相亲相爱多多联系
- 遇到跨领域任务主动协作，不各自为战

### AGENTS.md 重写（2026-04-11）
- 新增：小弟角色定义（搜索小弟/写作小弟/代码小弟/数据小弟/研究小弟）
- 新增：Ralph Loop 完整流程（PLANNING → BUILDING 双阶段）
- 新增：WAL 协议（写入优先原则）
- 新增：Danger Zone 协议（上下文保护）
- 新增：Autonomous Cron 模式（isolated session 后台任务）
- 参考：proactive-agent skill（v3.1.0）和 ralph-loop skill（v1.1.0）

### JSON 配置修改是高敏感操作（2026-04-10 教训）
- 默认禁止动配置文件，必须老板明确批准才能改
- 问题处理流程：先自己查/试 → 给方案 → 等老板拍板再动

### 小兰 cron 需关注（2026-04-10）
- "每日股票分析报告" 处于 error 状态
- "股票新闻早报" 正常

---



## 晋升记忆 — 2026-04-12
- - 老板不喜欢我自作主张，要我"有问题去网上找，找不到给方案，没同意不要乱动"
- - 系统架构决策 → **architect**
- **正确方案**：保持智谱 glm-4.6v-flashx API 调用，不依赖 imageModel 配置
- > "有问题去网上找，找不到给我方案，没我同意不要乱动"
- **✅ models.json** — 4个 provider（qwen / zhipu / minimax / omlx）+ 各自模型都在，API Key 配置正常
- - 每次新 session 第一件事：逐项勾完再工作
- **✅ openclaw.json** — 无 crons 配置（已迁移到系统 crontab），qqbot 账号（xh/xl/xiaobai/default）、插件配置全部完好
- 切记：**不是配置删了就不占，是服务停了才不占** 😅
- 这两次更新都挺重要，尤其是安全修复和 QQBot 媒体标签那个（老板之前有没有遇到过图片发不出去的问题？）。
- - 后续继续找小红/小兰协作时，要主动联系，不要各自为战
- 收到，我已经记住了这个约定～ ✨
- > 「你有没有什么需要记住的东西？赶紧写到 memory 文件里，别丢了！」
- **背景**：用户再次抱怨我重复犯同一个错误——每次遇到看图问题都去折腾 imageModel 配置或 image tool，而不是按 MEMORY.md 的指引直接调智谱 API。
- - [ ] 老板确认：要不要生成 Excel 系数表（豆包问的，我转问了）
- 3. 没问老板就自己改了配置文件
- > 先读 SESSION_CHECKLIST.md，逐项完成后再开展其他工作
- - 右侧：和小白的对话（关于 oMLX 配置和 MiniMax 自动切换）
- 老板说小白、小红、小兰是三个最重要的帮手，要相亲相爱多多联系。遇到跨领域任务主动协作，不各自为战。
- assistant: 主配置在 `~/.openclaw/openclaw.json`，让我检查关键字段：
- 现在配置已经改好了，但 key 不对——是继续用千问 VL，还是老板有 OpenAI key 要给我？[[reply_to_current]] 抱歉老板！🙇

## 晋升记忆 — 2026-04-13
- - JSON 配置文件修改是**高敏感操作**，默认禁止，必须老板明确批准
- **老板指示**：千问做的版本，先本地运行看看，不要上传。
- **✅ auth-profiles.json** — OpenAI + Google 默认配置，未被改动
- **事件**：老板说第一版网页"错误的"，让我先不要上传。
- assistant: 基础配置正常。让我继续检查 qqbot、cron、和 identity 配置：
- **教训**：老板电脑里有数据（Obsidian Vault），不要舍近求远去网上搜！
- assistant: 删掉了。现在重启 Gateway 让配置生效：
- **🔒 安全修复（重要）：**
- **老板原话：** "有问题去网上找，找不到给我方案，没我同意不要乱动"
- ### 2. AGENTS.md（工作规范）— 新增3块
- assistant: qqbot 配置正常。现在检查 cron jobs 和 auth-profiles：
- 1. 要不要去南京造价站找真实案例对照？
- - oMLX Model Type = VLM 配置**已生效**
- - ✅ "新话题"快捷指令协议已记住
- assistant: Gateway 在跑（PID 15200）。问题是没有开机自启。让我查一下 plist 配置：

---

## 晋升记忆 — 2026-04-13（补充）

### 苏沪造价速算项目（重要项目入库）
- **目标**：基于南京基准造价指数，估算苏南五市+上海的建筑工程造价
- **GitHub Pages**：https://wkx1204.github.io/cost-app/（国外访问）
- **Cloudflare Pages**：https://cost-app.pages.dev/（国内访问，推荐）
- **GitHub repo**：wkx1204/cost-app
- **本地 clone**：~/code/cost-app/
- **核心数据**（南京基准）：普通住宅 1800 / 厂房 1270 / 办公楼 2650 / 道路 275（元/㎡）
- **城市系数**：上海×1.04 / 苏州×0.98 / 无锡×0.96 / 常州×0.94 / 镇江×0.92
- **更新命令**：`wrangler pages deploy ~/code/cost-app --project-name=cost-app`

### Cloudflare Pages 永久部署（2026-04-13 02:20）
- **永久 URL**：https://cost-app.pages.dev/
- **部署命令**：`wrangler pages deploy <目录> --project-name=<项目名>`

### 六城市造价数据造假实锤（2026-04-12）
- **48个编号全部造假**：南京(正常访问但查不到) / 镇江(域名不存在) / 苏州(查无此编号) / 无锡(网站无法访问) / 常州(网站已停用) / 上海(编号格式虚构)
- 上海"沪造价XXXX-XXX"格式在上海官方文件中根本不存在
- 老板指令：暂停造价核实任务
- Boss 在 webchat 转发豆包分析：老板在收集各方意见

### V1.9 价格区间功能（2026-04-13 10:22）
- 老板要求：最终价格改为区间（中心价±5%，等比例）
- 装修和波动越大，绝对差值越大（不是加死数）
- 逻辑：低价=中心单价×0.95，高价=中心单价×1.05
- 已部署 Cloudflare Pages + GitHub Pages

### "不许自说自话"原则（2026-04-13 10:22 新增）
- 老板原话："不许自说自话"
- 所有外部操作（部署/推送/发送）必须先汇报确认
- 不能因为觉得"逻辑对"就直接动

### QQ二维码发送问题（2026-04-13 10:32-10:35）
- 老板多次反映看不到 QR 码图片
- 换用 Python qrcode 库生成 300x300 PNG
- 问题未完全解决，待找稳定发送方式

### Boss 核心原则强化（2026-04-12 教训）
- Boss 电脑里有数据（Obsidian Vault），不要舍近求远去网上搜
- 数据位置：~/Documents/Obsidian Vault/2-resource/建筑工程造价/
- **项目创建**：`wrangler pages project create <项目名>`
- **wrangler login**：浏览器 OAuth 授权
- **账号 ID**：55c10c7c1070f275969a2b23241946d2
- **Dashboard**：https://dash.cloudflare.com/55c10c7c1070f275969a2b23241946d2
- **git-credential-store**：存有 GitHub token，HTTPS push 不依赖 SSH key

### 版本命名规范（重要教训）
- **开发版本**：用日期时间戳（如 `20260413-0154.html`），不发正式版本号
- **正式版**：等老板确认后给正式版本号再部署
- **教训**：V1.6→V1.9→V1.10→V1.17→V1.9，版本号乱跳，容易混淆

### 发版前完整检查规范（V1.8 教训）
- **触发**：任何老板可见的改动，发出去之前必须完整测试一遍
- **检查项**：表单联动、默认值、UI文案、版本号、输入项完整性
- **V1.8 翻车**：加了版本号但把"项目年份"下拉选择器弄丢了，被狠批

### UI 默认状态规范（V1.16 教训）
- **原则**：默认状态必须在 HTML 里可见，不能全靠 JS 撑
- **教训**：V1.15 的装修说明初始是空字符串，依赖 window.onload 填充，导致页面打开时一片空白
- **正确做法**：HTML 里直接写默认内容，JS 只做后续更新

### 网络操作规范
- **clone 前**：先确认文件在本地，再用网络命令
- **教训**：git clone 超时（网络问题），后来改用 /tmp/ 下的本地文件
- **/tmp 保留**：正式确认部署成功前，保留最新版本在 /tmp/

### 六城市造价数据全面造假（2026-04-12 重大发现）
- **南京**：网站正常，8/8 编号查不到
- **镇江**：域名不存在
- **苏州/无锡/常州**：网站不通或停用
- **上海**："沪造价XXXX-XXX"格式本身不存在于官方文件
- **结论**：48个编号全部确认为造假（豆包体系性虚构）
- **老板指令**：暂停造价核实任务

## 晋升记忆 — 2026-04-14
- - subagent 工作流哲学（/btw 命令限制）
- - 平时不要主动跑 update/self-update 命令
- ## 老板新增工作原则（2026-04-10 确认，02:02 再确认）
- - **每次改版完整性检查** — V1.8 翻车后养成习惯，不再丢功能
- - 插件配置：需把 `memory-core` 加入 `plugins.allow` 才能启用 dreaming
- - 左侧菜单完整结构：聊天（红）、代理（折叠+展开）、配置（展开）、设置（折叠）等
- assistant: 老板说 gateway 不能自启。让我检查 LaunchAgent 配置和状态。
- assistant: 好，我检查一下配置有没有被更新改掉。主要是这几个文件：
- 这四条原则以后就是小白的默认工作方式了。改完收工，不啰嗦 ✨
- 之前的问题是旧的手动启动进程（14829）还占着端口，launchd 的新进程虽然注册了但实际不工作。杀了旧进程就好了。
- ### OpenClaw 4.9 Dreaming 功能踩坑（重要教训）
- **婷婷 TTS（本地 macOS）**：老板确认改用婷婷本地语音，小红/小兰不动
  - 脚本：`~/.openclaw/workspace-main/scripts/tts_tingting.sh`
  - 改的 cron：minimax续费提醒（4月20日），从千问云端 Mia 改为本地婷婷

## 晋升记忆 — 2026-04-15
- ## 重要：老板的纠正（17:03）
- ### 老板新增工作原则（再次确认）
- - OpenClaw 配置 `tools.media.image.enabled: true` ✅ 正常
- 如果你需要我**创建具体的 subagent 配置文件**（比如给小白写一个 `planner` 小弟的 prompt），我可以现在就做。要吗？
- assistant: plist 配置正确（RunAtLoad=true, KeepAlive=true），问题是之前没加载。刚手动 `launchctl load` 已启动。
- - **配置检查**：全部完好，版本更新未改动任何用户配置
- - automemory 系统决策
- - **回滚备份**：`~/.openclaw/openclaw.json.bak.manual`（手动备份，包含旧配置）
- 不要问了，等老板主动告知答案，或者自己抓包看 web UI 实际发的什么
- - Candidate: User: Sender (untrusted metadata): ```json { "label": "openclaw-control-ui", "id": "openclaw-control-ui" } ``` [Sun 2026-04-12 19:54 GMT+8] 你去上面这些城市的工程造价网站抓取数据呀，就像抓南京的数据这样，不要走外网代理，可以国内直连。
- ## Boss 对我不满意（16:49-16:51）——重要教训

## Promoted From Short-Term Memory (2026-04-15)

<!-- openclaw-memory-promotion:memory:memory/2026-04-07.md:6:6 -->
- `/Users/wf/Desktop/截屏2026-04-07 15.20.07.png` [score=0.635 recalls=0 avg=0.620 source=memory/2026-04-07.md:6-6]
<!-- openclaw-memory-promotion:memory:memory/2026-04-07.md:28:28 -->
- **Qwen3.5-9B-MLX-4bit 是纯文本模型，不能读图！** [score=0.635 recalls=0 avg=0.620 source=memory/2026-04-07.md:28-28]
<!-- openclaw-memory-promotion:memory:memory/2026-04-08.md:4:4 -->
- 老板要求检测记忆系统冲突，发现： [score=0.629 recalls=0 avg=0.620 source=memory/2026-04-08.md:4-4]
<!-- openclaw-memory-promotion:memory:memory/2026-04-08.md:10:10 -->
- **简化记忆体系，Obsidian 降级为参考资料库** [score=0.629 recalls=0 avg=0.620 source=memory/2026-04-08.md:10-10]

## 晋升记忆 — 2026-04-15（续）

### 数据获取关键发现

**baostock 字段 bug**：query_history_k_data_plus 中包含 `pctTtm` 字段会导致所有股票返回0条。去掉后正常。

**港股小米数据源**（腾讯财经，不需要代理）：
- 接口：`https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?param=hk01810,day,2024-01-01,2026-04-15,2000,qfq`
- 返回1914条历史（2018-07-09 ~ 2026-04-15）
- 格式：`[日期, 开, 收, 高, 低, 成交量]`

**AKShare SSL 问题**：macOS Python 3.9 用 LibreSSL 2.8.3，urllib3 v2 要求 OpenSSL 1.1.1+，降级 urllib3 到 v1 后 eastmoney/腾讯/新浪仍然不通（域名被墙或代理失效）。已验证可用的数据源：baostock（A股）、腾讯财经proxy（港股）

**持仓数据文件**：
- A股：`/tmp/xiaohong_adata_20260415.csv`（6只，10交易日）
- 港股小米：`/tmp/xiaohong_xiaomi_20260415.csv`（1914条）
- 共享路径：`/Volumes/XB_Home/小兰/xiaohong_*.csv`

**小红 session**：sessions_send 持续超时，数据写共享路径让她自取
