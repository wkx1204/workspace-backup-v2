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
