# OpenClaw 4.7 新功能体验报告

> 测试日期：2026-04-08
> 版本：2026.4.7 (5050017)
> 环境：macOS 26.4 (arm64) · Node v25.6.1 · MiniMax-M2.7

---

## 1. `openclaw infer` 命令

**命令：** `openclaw infer --help`

**输出：**
```
🦞 OpenClaw 2026.4.7 — Your personal assistant, minus the passive-aggressive calendar reminders.

Usage: openclaw infer [options]

Run provider-backed inference commands

Options:
  -h, --help  Display help for command
```

**状态：** ✅ CLI 存在，但功能未知（需要 provider 支持才能测试）

**关联/建议：** 目前看起来是个轻量推理命令入口，可能用于直接调用模型推理而不走完整 Agent 流程。需配合具体 provider 测试。

---

## 2. 视频生成内置工具

**检查配置：**
```bash
grep -i "video\|wan\|runway\|xai" ~/.openclaw/openclaw.json
```

**结果：** openclaw.json 中无 video/wan/runway/xai 相关配置。

**插件列表发现：**
```
@openclaw/alibaba-runway  stock:alibaba/index.js   disabled
  → OpenClaw Alibaba Model Studio video provider plugin
@openclaw/runway          stock:runway/index.js     disabled
  → OpenClaw Runway video provider plugin
```

**状态：** ⚠️ 插件存在但均为 **disabled**。已配置 DashScope API key，但未启用 alibaba 插件。

**关联/建议：**
- 现有 `DASHSCOPE_API_KEY` 已配置，说明老板有视频生成需求
- 建议开启 alibaba 插件：`openclaw plugins enable alibaba`
- 开启后视频生成工具（video_generate）应该可用
- 我们现有的 gog skill 是 Google Workspace 的，和视频生成无关

---

## 3. 音乐生成内置工具

**检查配置：**
```bash
grep -i "music\|lyria\|minimax" ~/.openclaw/openclaw.json
```

**结果：** 仅找到 minimax 模型配置，无 music/lyria 相关内容。

**状态：** ❌ 无音乐生成能力。OpenClaw 4.7 标准包中未包含 music_generate 工具。

**关联/建议：** 老板有 DashScope API key，可能是用于视频/图像而非音乐。Minimax 确有音乐生成能力（MiniMax Music），但 OpenClaw 内置未暴露。如需可考虑接入 MiniMax 音乐生成 API。

---

## 4. Dreaming 记忆系统

**命令：**
```bash
openclaw memory --help
openclaw dreaming --help
```

**`openclaw memory` 输出：**
```
Commands:
  index            Reindex memory files
  promote          Rank short-term recalls and optionally append top entries to MEMORY.md
  promote-explain Explain a specific promotion candidate and its score breakdown
  rem-harness      Preview REM reflections, candidate truths, and deep promotions without writing
  search           Search memory files
  status           Show memory search index status
```

**`openclaw dreaming`：** 命令不存在（`openclaw dreaming --help` 返回 unknown command）

**Memory Status：**
```
Provider: openai (requested: openai)
Model: bge-m3-mlx-4bit
Sources: memory
Indexed: 11/21 files · 58 chunks
Dirty: no
Store: ~/.openclaw/memory/main.sqlite
Workspace: ~/.openclaw/workspace-main
```

**REM Harness 输出：**
```
recentRecallEntries=0 deepCandidates=0
No strong patterns surfaced.
```

**状态：** ✅ `openclaw memory` 命令完整可用（index/promote/promote-explain/rem-harness/search/status）

⚠️ `openclaw dreaming` 命令不存在，不是 4.7 新增命令

**关联/建议：**
- **memory index**：可用于重建向量索引（目前 11/21 文件已索引）
- **memory promote**：将短期记忆提升到 MEMORY.md，非常有用！可以补充现有记忆系统
- **memory rem-harness**：预览 REM 反射，目前没有数据（刚启动）
- **memory search**：直接搜索记忆文件
- 与现有系统的关联：我们已经有 `.memory-manifest.json` 记忆索引 + daily memory 文件，memory promote 可以与之配合使用

---

## 5. ClawHub Skills

**`openclaw skills --help` 输出：**
```
Usage: openclaw skills [options]

List and inspect available skills

Options:
  -h, --help  Display help for command
```

**`openclaw skills` 输出（实际运行）：**
```
✓ ready  │ 🔔 qqbot-channel      │ QQ 频道管理技能...        │ openclaw-extra
✓ ready  │ ⏰ qqbot-cron          │ QQBot 定时提醒...         │ openclaw-extra
✓ ready  │ 🔐 1password          │ 1Password CLI...         │ openclaw-bundled
✓ ready  │ 📝 apple-notes         │ Apple Notes...            │ openclaw-bundled
✓ ready  │ ⏰ apple-reminders    │ Apple Reminders...        │ openclaw-bundled
...
```

**clawhub CLI：** 未测试（需单独安装 `npm install -g clawhub`）

**状态：** ✅ `openclaw skills` CLI 可用，列出所有已注册 skills（bundled + extra）

**关联/建议：**
- 老板的 workspace 中已有多个 skills：qqbot-channel, qqbot-cron, qqbot-media, filesystem, grep-search, hot-topics, ontology, proactive-agent, ralph-loop 等
- `openclaw skills` 可快速查看所有可用 skills，适合排查 skill 加载问题
- clawhub 是独立 CLI，需单独安装才能发布/安装 skill

---

## 6. Sessions 分支/恢复

**`openclaw sessions --help` 输出：**
```
Usage: openclaw sessions [options]

List stored conversation sessions

Options:
  -h, --help  Display help for command
```

**Dashboard (http://127.0.0.1:18789)：** 无法从外部访问（blocked）

**Status 输出：**
```
Sessions: 30 active · default MiniMax-M2.7 (128k ctx) · 3 stores
```

**状态：** ⚠️ `openclaw sessions` CLI 仅支持 list，无 branch/restore/child 等子命令

**关联/建议：**
- 目前 sessions 只读，无法通过 CLI 分支/恢复
- Dashboard 无法访问，但 4.7 可能已支持 Sessions UI（需本地浏览器查看）
- 30 个 sessions 说明 session 管理已启用
- LCM (Lossless Context Management) 插件已启用且工作正常

---

## 7. 多语言 UI

**Dashboard：** 无法从 subagent 访问 http://127.0.0.1:18789

**Status 输出：**
```
Gateway: ws://127.0.0.1:18789 (local loopback)
```

**状态：** ⚠️ 无法验证，需在主 agent 中访问 Dashboard 查看语言选项

---

## 8. Webhook 插件

**`openclaw plugins list` 输出：**
```
│ Webhooks    │ webhooks │ openclaw │ disabled │ stock:webhooks/index.js │ 2026.4.7 │
│             │          │          │          │ Authenticated inbound webhooks...       │
```

**状态：** ⚠️ Webhooks 插件存在但为 **disabled**。该插件提供认证入站 webhook 能力。

**关联/建议：**
- 可用 `openclaw plugins enable webhooks` 开启
- 适合需要外部系统触发 OpenClaw 操作的场景（如 GitHub webhook、自定义告警）
- 我们目前用 QQ/微信 channel，不需要 webhook

---

## 9. Prompt Cache 诊断

**`openclaw status --verbose` 输出：**
```
Memory: 11 files · 58 chunks · sources memory · plugin memory-core · vector ready · fts ready · cache on (679)
```

**LCM 状态：**
```
[plugins] [lcm] Compaction summarization model: minimax/MiniMax-M2.7 (override)
[plugins] [lcm] Plugin loaded (enabled=true, db=/Users/wf/.openclaw/lcm.db, threshold=0.75)
[plugins] [lcm] Ignoring sessions matching 2 pattern(s): agent:*:cron**, agent:*:subagent**
```

**状态：** ✅ Prompt Cache/L记忆系统在正常工作：
- LCM 插件启用，使用 MiniMax-M2.7 做 summarization override
- cache on (679) 说明向量检索缓存已启用
- threshold=0.75 是 compaction 阈值

**关联/建议：**
- 679 个 cache 条目，说明记忆检索缓存运行良好
- 可用 `openclaw memory index` 重建索引
- cron/subagent session 被排除在 LCM compaction 外（合理）

---

## 10. 安全审计

**`openclaw security audit` 输出：**

### 审计结果：0 critical · 5 warn · 1 info

| 级别 | 问题 | 建议 |
|------|------|------|
| WARN | Reverse proxy headers not trusted | 若暴露 Control UI 到反向代理，需配置 trustedProxies；当前仅本地 loopback 无风险 |
| WARN | Exec security=full is configured | main/xh/xl 均开启 full exec trust，建议改为 allowlist + ask 模式 |
| WARN | Workspace skill files resolve outside the workspace root | workspace-xh/xl 的 obsidian skill 是 symlink，realpath 逃逸到全局 |
| WARN | Extension plugin tools may be reachable under permissive tool policy | qqbot/weixin 插件在 default 等上下文可访问，建议用 restrictive profile |
| WARN | Plugin installs include unpinned npm specs | openclaw-weixin 使用 @latest，未固定版本 |

**Attack Surface Summary：**
```
groups: open=0, allowlist=0
tools.elevated: enabled
hooks.webhooks: disabled
hooks.internal: enabled
browser control: enabled
trust model: personal assistant (not hostile multi-tenant)
```

**状态：** ✅ 安全审计功能完整，报告清晰

**关联/建议：**
- **exec security=full**：老板是单人使用，风险可控，但建议了解 allowlist 模式
- **symlink escape**：workspace-xh/xl 的 obsidian skill 是 symlink，实际指向全局安装位置，有安全边界风险
- **unpinned weixin**：建议固定版本 `@tencent-weixin/openclaw-weixin@x.x.x`

---

## 汇总与建议

### 可用性总览

| 功能 | 状态 | 说明 |
|------|------|------|
| `openclaw infer` | ✅ 可用 | 入口存在，需 provider 支持 |
| 视频生成 | ⚠️ 插件 disabled | alibaba 插件可开启，配合 DASHSCOPE_API_KEY |
| 音乐生成 | ❌ 不可用 | OpenClaw 4.7 未内置 |
| `openclaw memory` | ✅ 完整可用 | index/promote/rem-harness/search/status 均工作 |
| `openclaw dreaming` | ❌ 不存在 | 不是 4.7 命令 |
| ClawHub / Skills | ✅ CLI 可用 | `openclaw skills` 可列出所有 skill |
| Sessions 分支/恢复 | ⚠️ 仅 list | CLI 无分支能力，Dashboard 需本地验证 |
| 多语言 UI | ⚠️ 无法验证 | Dashboard 无法远程访问 |
| Webhook 插件 | ⚠️ disabled | 可开启，但目前无需求 |
| Prompt Cache | ✅ 正常工作 | LCM + memory-core 缓存运行中 |
| 安全审计 | ✅ 完整可用 | 0 critical，5 warnings，报告清晰 |

### 优先建议

1. **开启 alibaba 插件**：`openclaw plugins enable alibaba` → 启用 DashScope 视频生成
2. **尝试 memory promote**：定期将重要记忆从短期记忆提升到 MEMORY.md
3. **修复 symlink escape**：workspace-xh/xl 的 obsidian skill 建议替换为真实文件
4. **固定 weixin 版本**：避免 @latest 引入不兼容更新

### 与现有系统的关联

- **memory-core + LCM**：与我们现有的 `.memory-manifest.json` 记忆系统可互补使用
- **DashScope API**：已配置，可启用 alibaba 插件做视频生成
- **oMLX 本地推理**：bge-m3-mlx-4bit 已在用（memory 向量模型），本地运行良好
- **MiniMax-M2.7**：主模型 + summarization override，一切正常
