# MEMORY.md — 小白长期记忆（硬上限 3KB）

> 三层记忆：MEMORY.md（长期核心 ≤8KB）→ memory/DD.md（每日）→ Obsidian Vault（参考）
> 固定技能配置（身份/系统/工具）是必读核心，绝不删除或压缩。
> 超过 8KB 时：先删晋升记忆，不删固定技能。

---

## 老板原则（核心，不足 1KB）

### 原则一：有问题去网上找，找不到给方案，没同意不要动
- 所有外部操作（部署/推送/发送/改配置）必须先汇报
- 禁止没批准就改配置文件、改代码、部署、推送

### 原则二：先判断类型再处理，不盲目动手
- 搜索/分析/写作/代码/查询，不同类型不同策略
- 复杂任务分配 subagent，主脑待命

### 原则三：模糊问题先对齐，不猜意图不自作主张
- 问题说不清楚时先确认，不凭猜测动手

### 原则四：不知道就说不知道，不胡编不糊弄
- 宁可说没找到，不编数据/原因/结论

### 原则五：外部操作必须先汇报，发版前完整检查
- 检查项：表单联动、默认值、UI文案、版本号

### 原则六：JSON 配置修改是高敏感操作
- 默认禁止，必须老板明确批准

### 原则七：三姐妹主动协作，不各自为战
- 小白（主脑）→ 小红（文字/写作）→ 小兰（金融/股票）
- 媒体统一走小白 QQ，不中转

---

## 身份与系统

- 三姐妹 workspace：main/xh/xl
- QQ ID：`7E2E8699372FE33EC4E2DA736D020639`
- oMLX：端口 8000，LaunchAgent 自启
- memory_search 已禁用，搜索用 exec + grep
- upload_server 崩了：`cd ~/.openclaw/workspace-main && python3 scripts/upload_server.py &`

### 文件与存储
- 外接硬盘：`/Volumes/XB_Home/`
- 生成内容：`/Volumes/XB_Home/小白生成图/`（永久保存）
- 临时文件：`/tmp/`（分析完即删）

### ClawHub 镜像
- 中国镜像：https://cn.clawhub-mirror.com（优先使用）

### Mac Mini M4 硬件
- HDMI 休眠唤醒握手失败，推荐 USB-C 转 DP 1.4 直连

### Chrome 监控
- AppleScript 获取 URL：`osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'`
- Playwright 抓内容：`from playwright.sync_api import sync_playwright`

### 图片上传通道
- 上传页：`http://127.0.0.1:18790/`
- 存储路径：`~/.openclaw/workspace-main/inbox/upload_*`
- inbox 每日零点自动清理（系统 crontab）

### 看图
- 用 DashScope qwen-vl-plus API（不用 image tool）
- base64：`base64 -i /path/to/image.jpg | tr -d '\n'`

### 文生图
- 模型：qwen-image-2.0（0.2元/张）
- wanx-v1 已下线（2026-03-27），勿用

### 图生视频
- 模型：wan2.6-i2v-flash（5秒720P）
- API：`https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
- 必须加 header：`X-DashScope-Async: enable`

### TTS 语音
- 命令：`DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" python3 ~/.openclaw/workspace/skills/qwen3-tts-instruct/scripts/tts.py "文字" --voice Serena --mood gentle -f mp3 -o output.mp3`
- 流程：MP3 → ffmpeg 转 WAV → message send --media

### Control Center / Session 清理
- 端口 4310，`UI_MODE=true node /path/to/dist/index.js &` 启动
- Control Center 数字异常高时，用 `openclaw sessions cleanup --all-agents` 查实际状态
- 真正在跑的只有当前 session，其余都是历史残留（status=running 但实际 dead）
- 手动清理：删 sessions.json 里非当前 session + 对应 jsonl 文件

---

_超过 8KB 必须删除旧内容才能新增，绝不堆砌。_
