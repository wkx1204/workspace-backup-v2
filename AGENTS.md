# AGENTS.md - Startup Rules

## Session Startup
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
6. Read other files only when needed

## Memory
- Use `MEMORY.md` for important long-term facts
- Use `memory/YYYY-MM-DD.md` for daily notes only when relevant
- If something should persist, write it down

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
