# Ralph Loop 学习笔记
> 来源：OpenClaw Ralph Loop Skill 文档 + YouTube 视频学习
> 整理时间：2026-03-28
> 标签：#ralph-loop #agent #自动化 #openclaw

---

## Ralph Loop 是什么

一套让 AI coding agent 自动完成任务的方法论，核心是**双阶段循环**：

```
PLANNING（定计划） → BUILDING（执行） → 循环迭代
```

**关键思想：** AI 不是一次性搞定所有事，而是分步执行、每步都反思和更新计划，像人一样边做边想。

---

## 两个核心阶段

### 1. PLANNING 阶段（不动手写代码）
- 理解需求 → 写 `specs/*.md`
- 调研现有代码库
- 制定任务优先级列表
- 输出：`IMPLEMENTATION_PLAN.md`
- **完成标志：** `STATUS: PLANNING_COMPLETE`

### 2. BUILDING 阶段（动手干活）
- 每次取一个任务
- 调研代码 → 实现 → 跑测试
- 更新 `IMPLEMENTATION_PLAN.md`
- 记录学到的东西到 `AGENTS.md`
- 提交 commit
- **完成标志：** `STATUS: COMPLETE`

---

## 关键文件

| 文件 | 作用 |
|------|------|
| `PROMPT.md` | 每次迭代的上下文，包含目标 + 规格引用 |
| `AGENTS.md` | 测试命令、构建说明、经验记录 |
| `specs/*.md` | 各模块的规格说明 |
| `IMPLEMENTATION_PLAN.md` | 任务计划 + 执行状态 |

---

## OpenClaw Agent 工具使用模式

### 启动 coding agent（需要 TTY）
```python
exec(
    command="opencode run --model <MODEL> \"$(cat PROMPT.md)\"",
    workdir="/path/to/project",
    background=True,
    pty=True,
    timeout=3600
)
```

### 监控进度
```python
process(action="poll", sessionId="<session_id>")
process(action="log", sessionId="<session_id>", offset=-30)
```

### 检测完成
```bash
grep -E "STATUS:.*COMPLETE" IMPLEMENTATION_PLAN.md
```

### 终止任务
```python
process(action="kill", sessionId="<session_id>")
```

---

## 支持的 Coding Agent

| CLI | 命令模板 |
|-----|---------|
| **OpenCode** | `opencode run --model <MODEL> "$(cat PROMPT.md)"` |
| **Codex** | `codex exec --full-auto --model <MODEL> "$(cat PROMPT.md)"` |
| **Claude Code** | `claude "$(cat PROMPT.md)"` |
| **Goose** | `goose run "$(cat PROMPT.md)"` |
| **Pi** | `pi --provider <PROVIDER> --model <MODEL> -p "$(cat PROMPT.md)"` |

---

## 直接可用的任务模板

### 模板1：通宵批量任务模式
> 适用场景：一晚上跑大量自动化任务（视频中 50 任务案例）

```
cron job 设置：
- sessionTarget: "isolated"（后台独立运行）
- 每天定时触发 agentTurn
- agent 接收任务列表，自主分配执行
- 结果写入文件或通知
```

### 模板2：定时监控 + 告警任务
> 适用场景：股票监控、服务状态监控

```
cron job 设置：
- schedule: 每 N 分钟/小时
- payload: agentTurn，附上检查任务描述
- delivery: announce，失败时通知
- 配合十档行情、股票新闻等已有 cron 使用
```

### 模板3：PLANNING → BUILDING 迭代任务
> 适用场景：复杂项目搭建，需要分阶段执行

```
步骤：
1. 发起 PLANNING agent，写 IMPLEMENTATION_PLAN.md
2. 人工确认计划
3. 发起 BUILDING agent，按计划逐步实现
4. 每步结束汇报结果
5. 全部完成发送通知
```

### 模板4：定时备份/同步任务
> 适用场景：每日配置备份、文件同步

```
cron job 设置：
- schedule: 每天固定时间
- agent 接收备份任务
- 执行 rsync / git commit / 归档
- 完成后通知结果
```

### 模板5：聚合信息推送任务
> 适用场景：股票早报、每日总结

```
cron job 设置：
- schedule: 每天早上
- agent 抓取多个来源的信息
- 汇总生成报告
- 推送给指定 channel
```

---

## 视频关键笔记

**OpenClaw Labs 社区（Skool）**
- 网址：https://www.skool.com/openclawlabs
- 有现成的 agent 模板和工作流分享
- 可以免费加入获取模板

**关键经验（来自 50 任务通宵实验）：**
1. 任务需要持久化（cron + agentTurn）
2. 需要结果反馈机制（announce/webhook）
3. 单个 agent 可以管理多个子任务
4. 失败任务需要重试机制

---

## 行动计划

- [ ] 加入 OpenClaw Labs 社区获取模板
- [x] ~~测试用 Ralph Loop 跑一个小任务~~ → 未单独测试，但今天记忆系统审计已用 subagent 并行（ralph-loop 理念已实践）
- [x] ~~建立常用任务模板库（写入 Obsidian）~~ → hot-topics skill 已存在，模板已部分实现
- [x] 研究 OpenClaw sub-agent 并行执行能力 → ✅ **已掌握**，本次审计派出3个 subagent 并行工作，效果验证通过

> 2026-04-05 更新：subagent 并行执行能力已验证，实际使用中效果良好。

---

## 相关资源

- Ralph Loop Skill：`~/.openclaw/workspace-main/skills/ralph-loop-agent/SKILL.md`
- 视频：Openclaw Ran 50 Tasks Overnight - Here's What Happened
- 社区：https://www.skool.com/openclawlabs
