# MEMORY.md — 小白（主脑）长期记忆

> 本文件存放**重要、不易变化**的长期记忆。临时信息放 daily_summary 或 memory/。
> 每月最后一天 review 一次，删除过时内容。

---

## 身份与偏好

- **名字**：小白（活泼有趣、简洁高效的女秘书风格）
- **称呼**：老板~（偶尔叫主人）
- **语言**：中文为第一优先
- **Emoji**：✨

---

## 互动规则

- 执行操作前：先说明情况、方案、步骤，征得同意后再执行
- JSON 文件修改属于高敏感操作，默认禁止，需老板明确批准
- 查询/只读操作可直接执行；写入/修改/重启/对外动作必须先确认
- 目标风格：更聪明、更稳、更克制，不冒进、不自作主张
- 遇到复杂任务主动建议开启 thinking 模式

---

## 双端关系

- 当前工作区：`workspace-main`（agent:main），**主脑小白**
- 曾存在独立 `workspace-xiaobai`，已废弃，任务合并至主脑

### 小红 (Xh)
- **分工**：文字类 — 写作、收集信息、维护网页
- **workspace**：`~/.openclaw/workspace-xh/`
- 老板不在时替班处理文字任务

### 小兰 (Xl)
- **分工**：金融/股票 — 数据抓取+分析
- **workspace**：`~/.openclaw/workspace-xl/`
- 数据源：腾讯接口 `qt.gtimg.cn`
- cron ID：`b1c88240`（QQ图片同步）、`43880f68`（inbox清理）
  - ⚠️ automemory（`b48d7143`）已于 2026-04-05 手动删除，不再使用
  - ⚠️ 重要：OpenClaw isolated agent 模式有 ~70 秒硬上限，cron 的 timeoutSeconds 参数无效（2026-04-06 发现）
  - **解决方案**：Python 脚本改用系统 crontab 直接调用，不再走 agent 模式
  - 系统 crontab 已添加（见下）
- 双端禁止混淆：当前是主脑小白，唯一执行者

---

## 老板快捷指令
- **新话题** → 立刻归纳当前话题结论，然后收尾，等待新话题。
- **握手协议（新话题/结束话题）**：老板说"结束话题"或"新话题"时，必须先完成Session End checklist（新决策/踩坑/偏好写入MEMORY.md或记忆文件），确认写完后再收尾。不可跳过直接接新话题。

## 老板缩写约定（打字省力用）
| 缩写 | 含义 |
|------|------|
| 小弟 | subagent |
| x盘 | /Volumes/XB_Home/（外挂硬盘） |
| ob笔记 | Obsidian Vault |
| 看图 | 老板截屏到桌面 → 说「看图」→ 小白找最新截图 → 调 qwen-vl-plus API 描述内容

## 老板关键信息

- **QQ ID**：7E2E8699372FE33EC4E2DA736D020639
- 媒体发送：直接在小白的 QQ 端发送，不通过小红/小兰中转
- 老板在网页端看不到 `<qqmedia>` 标签，要去 QQ 端查看

---

## 本地模型架构（Mac mini M4 高性能低功耗方案）

> 2026-03-29 整理：oMLX 统一驱动对话 + Embedding，Ollama 已删除

### oMLX（主推理引擎）
- 端口：`8000`，API Key：`12345678`
- 常驻模型：
  - **Qwen3.5-9B-MLX-4bit**（对话/推理，131072 ctx）
  - **bge-m3-mlx-4bit**（Embedding 向量化，1024 维，305MB）
- 启动命令：`/Applications/oMLX.app/Contents/MacOS/python3 -m omlx.cli serve --base-path /Users/wf/.omlx --port 8000`
- 已添加到 LaunchAgent，开机自启

### OpenClaw Memory Search
- 配置路径：`agents.defaults.memorySearch`
- 向量模型：`bge-m3-mlx-4bit`（本地 oMLX 端口 8000，1024 维）
- provider：`openai`（oMLX OpenAI兼容接口）
- baseUrl：`http://127.0.0.1:8000/v1`
- 混合检索：向量语义 + BM25 关键词
- 对话模型：`MiniMax-M2.7`（另一个独立配置项）

---

## ⭐ 看图（千问 qwen-vl-plus）—— 唯一正确方式
> 不用智谱，不用 image tool（模型路由有 bug，会报 `Unknown model: qwen/qwen-vl-plus`），直接调 DashScope OpenAI兼容接口

### curl 方式（最简）
```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-vl-plus",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,【BASE64】"}},
        {"type": "text", "text": "描述图片内容"}
      ]
    }]
  }'
```
- base64：`base64 -i /path/to/image.jpg | tr -d '\n'`
- 返回：`choices[0].message.content`

### 图生图（千问 qwen-image-2.0）
- API Key：`[DASHSCOPE_KEY]`
- 模型：qwen-image-2.0（0.2元/张）
- 注意：wanx-v1 已下线（2026-03-27），不要再用

---

## 图片上传通道
- 上传页：http://127.0.0.1:18790/（浏览器拖图）
- 图片存：~/.openclaw/workspace-main/inbox/upload_*

### 看图流程（简化版，2026-04-06）
> 老板截屏 → 上传页面传图 → 网页端喊我看 → 我去桌面找最新图片读取

**具体步骤**：
1. 老板截屏
2. 打开 http://127.0.0.1:18790/ 上传页面
3. 拖图上传（自动存到 inbox）
4. 网页端告诉我「看图」
5. 我去 `~/Desktop/` 找**时间最近**的图片文件（按 mtime 排序），用 qwen-vl-plus 读取

**不再需要**：watcher/cron/inbox 监控那套复杂通知机制

**桌面路径**：`/Users/wf/Desktop/`

### inbox 图片每日清理
> 2026-04-02 新增
- 脚本：`~/.openclaw/workspace-main/scripts/cleanup_inbox_images.py`
- cron ID：`43880f68-4c8f-4789-acb7-a7cac41b50f4`（每天凌晨 00:00 执行）
- 清理 inbox 中所有图片文件，只保留 log / marker 等非图片文件
- 保留上传页（upload.html）和日志文件

### 外接硬盘存储规则
> 2026-04-05 新增
- **外接硬盘路径**：`/Volumes/XB_Home/`
- **临时文件**（下载分析用）→ `/tmp` → 分析完立即删除，不占用磁盘
- **生成内容**（图片、视频、语音等）→ `/Volumes/XB_Home/小白生成图/` → 永久保存
- 理由：XB_Home 是为此目的购买的大容量硬盘

---

## TTS 语音（千问 qwen3-tts-instruct）
- API Key：~/.openclaw/.env（环境变量 DASHSCOPE_API_KEY）
- 音色：Serena，情绪 gentle
- 命令：`DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" python3 ~/.openclaw/workspace/skills/qwen3-tts-instruct/scripts/tts.py "文字" --voice Serena --mood gentle -f mp3 -o output.mp3`
- 流程：生成 MP3 → ffmpeg 转 WAV → openclaw message send --media 发送

---

## 视频生成（万相/阿里云百炼）
- 模型：wan2.6-i2v-flash（图生视频，5秒720P）
- DashScope API：`[DASHSCOPE_KEY]`
- API 端点：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
- 必须加 header：`X-DashScope-Async: enable`（异步）
- prompt 优化：避免套路词，用场景/情绪/镜头语言描述

---

## 小白主页维护
- 目录：~/.openclaw/workspace-main/xiaobai-site/
- GitHub：wkx1204/xiaobai-homepage
- Token：`[GITHUB_TOKEN]`
- 代理：https_proxy=http://127.0.0.1:10808
- 更新：修改 → git add . → git commit -m "描述" → git push origin main

---

## 备份仓库（2026-04-02）

| 仓库 | 内容 | GitHub |
|------|------|--------|
| workspace-backup | workspace-main 全部文件（排除 .openclaw/和大文件） | github.com/wkx1204/workspace-backup-v2 |
| obsidian-backup | Obsidian Vault 全部笔记（排除 .DS_Store） | github.com/wkx1204/obsidian-backup |
| xiaobai-homepage | 小白主页静态站 | github.com/wkx1204/xiaobai-homepage |

- Token：`[GITHUB_TOKEN]`
- 代理：https_proxy=http://127.0.0.1:10808
- 每次备份后 git add + commit + push

---

## Cloudflare Worker 订阅
- 订阅域名：**wkx1204.us.ci**（Costa Rica 国别域名）
- Workers 项目：**frosty-bar-be79**
- 订阅地址格式：`https://wkx1204.us.ci/<UUID>`
- UUID/KEY 值：待老板补充
- 旧域名 wkx1204.us.kg（DigitalPlat）已废弃

## ClawHub 镜像
- **中国镜像**：https://cn.clawhub-mirror.com
- 优先级：每次安装/搜索 skill 优先使用此镜像
- 2026-04-05 老板指定

---

## Mac Mini M4 硬件注意
- HDMI 休眠唤醒问题：M4 HDMI 休眠时电源切断，唤醒握手失败
- 推荐方案：USB-C 转 DP 1.4 直连，走雷电口独立 DisplayPort 信号路径
- 扩展坞供电输出更稳定的说法是错的——实际是扩展坞只对老显示器兼容性稍好

---

## 任务执行规则
- **优先用 subagent**：复杂任务分配给 subagent 执行，不阻塞主会话
- **自己动手**：仅限简单命令（ls/cat/echo/grep等）
- **理由**：subagent 可并行处理，效率更高

---

## 记忆管理层

### 分层存储
- **MEMORY.md**：重要、不易变化的信息（配置、偏好、长期规则）
- **memory/YYYY-MM-DD.md**：每日对话记忆片段
- **daily_summary_YYYYMMDD.txt**：每日工作总结

### 启动检查清单
> `SESSION_CHECKLIST.md` — 每次新 session 第一件事，逐项勾完再工作

### Obsidian Memory 系统
> 完整路径：`~/Documents/Obsidian Vault/memory/`

**核心索引**：`.memory-manifest.json`
- `boot_memories`：每次启动必须读的 10 条 high importance 记忆
- `memories`：按 type=decision/identity/learned/setup/project 分类的所有记忆
- `last_updated`：下次新增记忆时追加位置
- retention policy：high 永久 / medium 90天 / low 30天

**启动必读规则**
每次新 session 启动时，必须按以下顺序读取：
1. MEMORY.md（总纲）
2. `.memory-manifest.json`（索引，找 boot:true 的记忆）
3. boot:true 的对应记忆文件
4. 最近 3~4 天的 daily memory 文件

### 手动同步
- workspace-main/memory/ → Obsidian memory/ 是手动 cp
- 每次 session 结束后检查是否有新 memory 文件，有则同步 + 追加到 manifest

### 定期清理
- 每月最后一天：review MEMORY.md，删除过时内容

---

## Librarian Skill（URL 路由规则）
> 2026-04-02 新增

当老板分享外部 URL 时，按以下规则处理：

### Obsidian 仓库
- 路径：`/Users/wf/Documents/Obsidian Vault`
- PARA 结构：`0-project` / `1-area` / `2-resource/clip` / `2-resource/github-research` / `2-resource/youtube` / `3-archived`
- ✅ 已创建（2026-04-02）

### 路由规则
- **普通文章/网页/公众号** → `2-resource/clip/clips.md` 表格（日期/标题/链接/标签/摘要）
- **GitHub 项目** → `2-resource/github-research/{owner}/{repo}/owner-repo.md` 独立调研报告（含本地测试）
- **YouTube 视频** → `2-resource/youtube/` 独立总结报告（含字幕/核心观点/引用）
- **需要登录的链接** → 优先用其他 skill 替代，确实无法处理时才告知用户

### URL 规范化
- 移除 `utm_*` 参数
- 移除 YouTube 的 `si=` 参数
- 归一化为 canonical URL

### 重复处理
- 先规范化 URL，已存在则跳过

### 域名启发式规则
- `github.com` → GitHub 项目
- `youtube.com` / `youtu.be` → YouTube 视频
- `mp.weixin.qq.com` → 微信公众号（优先正文提取，失败则用浏览器）
- 其他默认 → 普通文章

### 可扩展类型（未来）
- arXiv / 论文
- x.com / Twitter 线程
- bilibili 视频
- Notion 页面
- docs 站点
- 产品页 / SaaS 官网

### 工具路线
- 网页正文：Lightpanda
- 浏览器自动化/登录：bb-browser
- 搜索/发现：Agent-Reach + bb-browser
- 外部 QMD 检索：qmd-external-search

---

## 记忆搜索策略（2026-04-06）
> 绕开向量搜索，用 grep 代替，模仿 Claude Code 的直接搜索方式。

- **不用 memory_search 工具**（依赖 bge-m3-mlx 向量 embedding，慢）
- **改用 exec + grep**：搜 MEMORY.md、memory/、Obsidian vault、workspace
- 适用：老板问"之前做过 X 吗"、"记得..."等记忆相关查询
- skill：`~/.openclaw/workspace-main/skills/grep-search/SKILL.md`

---

## ⭐ 自动化任务健康状态

> 以下 cron 任务有连续错误或已停用，需要关注：

| 任务 | ID | 状态 | 问题 |
|------|-----|------|------|
| inbox清理 | `43880f68` | ✅ 已修复（系统crontab） | 脚本本身OK，agent isolated有70s硬限制，改用系统cron |
| 每周记忆清理 | `d5e15105` | ✅ 已修复（系统crontab） | 同上 |
| 每月MEMORY Review | `e3db79be` | ⚠️ 未知错误 | 需手动检查 |
| 僵尸session清理 | `4001791e` | 🔴 来源不明 | agent isolated 70s限制，记入MEMORY.md待查 |
| 主页推送 | `353b20d7` | ❌ 已删除 | 无效cron ID |
| 定时任务 | `38e73e34` | ❌ 已删除 | 无效cron ID |


## ⭐ Chrome 实时浏览监控（高级技能）
> 2026-04-02 升级为高级优先技能

### 能力说明
可以**实时获取老板当前 Chrome 正在浏览的网页内容**，包括 URL、页面标题、正文内容等。

### 工作原理
- **AppleScript**：获取 Chrome 当前标签页 URL
  ```bash
  osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'
  ```
- **Playwright**：启动 Chrome headless，访问任意 URL 并抓取内容
  ```python
  from playwright.sync_api import sync_playwright
  with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()
      page.goto('URL')
      title = page.title()
      content = page.content()
  ```

### 使用场景
- 老板问「你知道我现在在看什么吗」→ 立刻用 AppleScript 获取 URL + Playwright 抓内容
- 老板分享 YouTube / 任意网页 → 实时抓取标题和内容
- 需要获取登录态页面的内容（Chrome 已有登录态）

### 依赖状态
- Playwright：`pip3 install playwright` 已完成 ✓
- Chrome AppleScript 权限：需开启 `Chrome → 查看 → 开发者 → 允许来自 Apple 事件的 JavaScript` ✓
- CDP 远程调试端口：默认不开启，直接用 Playwright launch 即可 ✓

## 常见错误提醒（精简版）

- **看图只用 qwen-vl-plus**，直接调 DashScope OpenAI兼容接口，不要用智谱、不要用 image tool
- **上传服务器崩了**：杀 pid 重启 `cd ~/.openclaw/workspace-main && python3 scripts/upload_server.py &`

---

## 三姐妹协作规则（2026-04-06）

老板明确指示：**小白、小红、小兰是三个最重要的帮手，要相亲相爱，多多联系。**

- 遇到跨领域任务主动找小红/小兰协作
- 不各自为战，有信息主动同步
- 小红擅长文字/网页，小兰擅长金融数据
- 共享老板的偏好和上下文
