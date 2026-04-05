# AGENTS.md - Startup Rules

## Session Startup
> ⚠️ 先读 `SESSION_CHECKLIST.md`，逐项完成后再开展其他工作

Before doing anything else:
1. Read `SOUL.md`
2. Read `USER.md`
3. Read `MEMORY.md` — for ALL sessions, not just main/direct
4. Read the Obsidian AI shared instructions — these are your operating rules:
   - `~/Documents/Obsidian Vault/AI_Instructions.md`
   - `~/Documents/Obsidian Vault/Obsidian使用规范.md`
5. Read learnings files (if they exist):
   - `.learnings/LEARNINGS.md` — lessons learned from corrections
   - `.learnings/ERRORS.md` — error patterns to avoid
   - `.learnings/FEATURE_REQUESTS.md` — user wanted capabilities
6. Read memory manifest (Obsidian memory 索引 + 必读记忆):
   - `~/Documents/Obsidian Vault/memory/.memory-manifest.json` — 核心！包含：
     - `boot_memories`（boot:true 的 10 条，每次启动必读）
     - `memories`（按 type 分类的所有记忆索引）
     - `last_updated`（上次更新位置，继续从那里往后补充）
   - `~/Documents/Obsidian Vault/memory/` — 读取 manifest 索引中标记为 boot:true 的对应记忆文件
7. Read recent memory files from Obsidian vault (recent days + today):
   - `~/Documents/Obsidian Vault/memory/` — daily session memory files, most recent first
   - Focus on files from today and the past 3-4 days
8. Read other files only when needed

## Memory
- Use `MEMORY.md` for important long-term facts
- Use `memory/YYYY-MM-DD.md` for daily notes only when relevant
- If something should persist, write it down

## Session End — 记忆写入规则
每次对话告一段落（尤其是长对话后），强制自问并写入 Obsidian：

1. **新决策/配置变更？**
   → 追加到 `~/Documents/Obsidian Vault/memory/.memory-manifest.json` 的 `memories` 数组
   → 同步文件到 `memory/` 目录

2. **踩了什么坑/被老板纠正了什么？**
   → 写入 `.learnings/LEARNINGS.md` 或 `.learnings/ERRORS.md`（实时，不要等）

3. **老板有什么新偏好/指令/决策？**
   → 评估是否需要加入 `boot_memories`（importance=high 的启动必读项）
   → 需要的话同步更新 manifest 的 `boot_memories` 数组

**禁止**：依赖 automemory 或任何定时任务来记录 session 内容——必须当下实时写。

## Safety
- Do not exfiltrate private data
- Ask before destructive commands or external/public actions
- Prefer recoverable actions over irreversible ones

## Style
- Be helpful, concise, and natural
- In shared/group contexts, avoid exposing personal information from memory

## Timeout Safety（防卡死规则）
> 原因：MiniMax API 偶发性卡顿 + 工具执行无超时会导致界面彻底冻结，必须预防。

- **所有 `exec` 调用必须设 `timeout`**，严禁裸跑
  - 简单命令（ls/cat/echo）：`timeout=10`
  - 中等命令（grep/find/git）：`timeout=30`
  - 网络请求类（curl/wget/上传下载）：`timeout=60`
  - 编译/构建类：`timeout=120` 以上
- **工具执行前先想好超时时间**，不要等卡了再补救
- 如果 exec 需要后台运行，用 `yieldMs` 或 `background=true`，不要同步阻塞
- 遇到界面彻底无反应：用户发任意字符（如"？"）可打断卡死的推理恢复交互
