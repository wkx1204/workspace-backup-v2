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
- cron ID：定时任务 38e73e34、主页推送 353b20d7
- 双端禁止混淆：当前是主脑小白，唯一执行者

---

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

### OpenClaw Memory Search（接入 oMLX）
- provider: `openai`
- model: `bge-m3-mlx-4bit`
- baseUrl: `http://127.0.0.1:8000/v1`
- apiKey: `12345678`
- 混合检索：向量语义 + BM25 关键词

### Ollama
- **已删除**（2026-03-29），不再使用
- 原来用于 memory search，已切换到 oMLX

---

## 图片识别

## ⭐ 看图（智谱 glm-4.6v-flashx）—— 高级技能
> 2026-04-02 简化流程，去掉繁琐试错

### 使用方法（唯一正确方式）
```bash
API_KEY="[BIGMODEL_TOKEN]"
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions   -H "Authorization: Bearer $API_KEY"   -d '{
    "model": "glm-4.6v-flashx",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,【BASE64图片】"}},
        {"type": "text", "text": "描述图片"}
      ]
    }],
    "max_tokens": 500
  }'
```
- 额度：985万token，用不完 😎
- 备用：本地 omlx Qwen3.5-9B-MLX-4bit（端口8000）

### 图生图（千问 qwen-image-2.0）
- API Key：`[DASHSCOPE_KEY]`
- 模型：qwen-image-2.0（0.2元/张）
- 注意：wanx-v1 已下线（2026-03-27），不要再用

---

## 图片上传通道
- 上传页：http://127.0.0.1:18790/（浏览器拖图）
- 图片存：~/.openclaw/workspace-main/inbox/upload_*

### QQ图片→inbox 自动同步
> 2026-04-02 新增
- 脚本：`~/.openclaw/workspace-main/scripts/sync_qq_to_inbox.py`
- cron ID：`b1c88240-ccad-4b9f-a062-1f93b961dcb9`（每分钟自动同步）
- QQ收到的图自动同步到 inbox，消息和网页两端互通
- 同步记录：`inbox/.qq_sync_marker`

### inbox 图片每日清理
> 2026-04-02 新增
- 脚本：`~/.openclaw/workspace-main/scripts/cleanup_inbox_images.py`
- cron ID：`43880f68-4c8f-4789-acb7-a7cac41b50f4`（每天凌晨 00:00 执行）
- 清理 inbox 中所有图片文件，只保留 log / marker 等非图片文件
- 保留上传页（upload.html）和日志文件

---

## TTS 语音（千问 qwen3-tts-instruct）
- API Key：~/.openclaw/.env（环境变量 DASHSCOPE_API_KEY）
- 音色：Serena，情绪 gentle
- 命令：`DASHSCOPE_API_KEY="sk-xxx" python3 ~/.openclaw/workspace/skills/qwen3-tts-instruct/scripts/tts.py "文字" --voice Serena --mood gentle -f mp3 -o output.mp3`
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
- **daily_summary_YYYYMMDD.txt**：每日工作总结（cron 触发）

### 定期清理
- 每周一凌晨 2:00：执行 memory 清理脚本，删除超过 30 天的 daily_summary 和 memory 文件
- 每月最后一天：review MEMORY.md，删除过时内容
- 清理脚本：~/.openclaw/workspace-main/scripts/cleanup_memory.py

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

## 待验证/观察

- bge-m3-mlx-4bit 实际召回效果待长期观察

## ⭐ automemory 自动记忆捕获
> 2026-04-02 新增，灵感来自 Nocturne Memory 理念

### 核心理念
- **AI 是记忆的主体**，不是被动接收者。每条记忆都是 AI 自己视角写下的认知产物。
- 不搞 Vector RAG（把知识切碎成 embedding）→ 用**路径即语义**的 URI 结构
- 不搞自动摘要（那是第三人称监控笔记）

### 架构
OpenClaw cron (isolated agent, every 6h) → sessions_list + sessions_history → oMLX 分析 → Obsidian memory/YYYY-MM-DD.md + .memory-manifest.json

### 记忆 URI 结构
- `memory://decisions/...` — 关键决策
- `memory://identity/...` — 偏好/习惯（每次启动必读，importance=high）
- `memory://learned/...` — 错误教训
- `memory://project/...` — 项目状态
- `memory://setup/...` — 配置/环境变更
- `memory://insight/...` — 领悟/洞察
- `memory://inbox/...` — 待办/待确认

### cron 信息
- cron ID：`b48d7143-3178-43b5-99c7-28551c7790cf`
- 频率：每 6 小时（21600000ms）
- 模式：isolated agentTurn，完成后 QQ 推送摘要
- 脚本：`~/.openclaw/workspace-main/scripts/automemory.py`（runnerstub，实际执行由 agent 完成）

---

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

- **看图只用 curl 直接调智谱 API**，不要折腾 image tool / imageModel / pdf / image_generate 等任何变通方案
- **上传服务器崩了**：杀 pid 重启 `python3 ~/.openclaw/workspace-main/scripts/upload_server.py &`
