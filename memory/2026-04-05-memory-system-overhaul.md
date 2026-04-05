# 2026-04-05 记忆体系大修

## 背景
老板批评我"老是什么都想不起来"——每次新 session 都是 fresh start，记忆完全断档。

## 根因
三层保险全部失效：
1. automemory cron 早已 timeout 坏掉（cron ID: b48d7143，已删除）
2. 我没有在 session 结束时写记忆的习惯
3. workspace-main/memory/ 和 Obsidian memory/ 没有同步

## 今天做的改动

### 1. 删除 automemory
- cron `b48d7143` 已删除，不再使用
- MEMORY.md 三处残留全部清理

### 2. SESSION_CHECKLIST.md（新建立）
- 路径：`~/.openclaw/workspace-main/SESSION_CHECKLIST.md`
- 每次新 session 第一件事：逐项勾完再工作
- 老板确认：强制执行

### 3. AGENTS.md 更新
**启动规则（第零步）：**
> 先读 SESSION_CHECKLIST.md，逐项完成后再开展其他工作

**新增启动步骤 6-8：**
- 步骤6：读 `.memory-manifest.json`（索引 + boot_memories）
- 步骤7：读 boot:true 的对应记忆文件
- 步骤8：读最近 3-4 天 daily memory 文件

**新增 Session End 规则：**
- 新决策/配置变更 → 写入 manifest + memory/
- 踩坑/被纠正 → 写入 LEARNINGS.md / ERRORS.md（实时）
- 老板新偏好 → 评估是否加入 boot_memories
- 禁止依赖 automemory，必须当下实时写

### 4. MEMORY.md 更新
- 删除 automemory 相关内容
- 新增「启动检查清单」章节
- 新增「Obsidian Memory 系统」章节（含 manifest 索引说明）
- 新增「手动同步」规则

### 5. 文件同步
- workspace-main/memory/ 9个文件 → 同步到 Obsidian memory/
- daily_summary 3个文件 → 同步到 Obsidian memory-boss/
- Obsidian memory/ 现在有 12 个文件

## 握手协议
老板说"结束话题"或"新话题"时：
1. 我先跑 Session End checklist
2. 确认写完记忆后再接新话题
3. 老板也确认这是合理的协议

## 老板缩写约定
| 缩写 | 含义 |
|------|------|
| 小弟 | subagent |
| x盘 | /Volumes/XB_Home/ |
| ob笔记 | Obsidian Vault |

## 遗留问题
- Control UI 右上角"21"之谜（未解决）
- oMLX stats.json embedding 统计 bug（确认是 oMLX 自身统计模块问题，非功能故障）

## 教训
- 有系统不用 = 没有系统
- automemory 是兜底保险，但它失效时我没有手动补位
- 老板的批评完全到位
