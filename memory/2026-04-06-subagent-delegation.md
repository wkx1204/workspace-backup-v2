# Session: 2026-04-06 09:55:25 UTC

- **Session Key**: agent:main:main
- **Session ID**: b096faed-a34b-4373-8188-7c1d741c3c9d
- **Source**: webchat

## Conversation Summary

assistant: 好嘞，直接改！

assistant: SOUL.md 更新完成。现在改 AGENTS.md：

assistant: 现在更新 TOOLS.md：

assistant: TOOLS.md 保持不变——它是放本地环境配置的，通用规范放 AGENTS.md 更合适。

三处更新完成，让我验证一下：

assistant: 整合完成！✨

已更新三个文件：

| 文件 | 更新内容 |
|------|----------|
| **SOUL.md** | 新增「Go straight to the point」+ 不用 emoji 规则 |
| **AGENTS.md** | 新增工程三原则（克制/信任/按需抽象）+ 输出效率规范 + 工具使用规范 |
| **TOOLS.md** | 保持不变（本地配置放这里不合适 |

---

**整合的核心变化：**

1. **克制** — 不自作主张，只做被要求的事
2. **信任** — 不加冗余验证，信任代码契约
3. **按需抽象** — 不为未来设计，三行重复代码比过早抽象好
4. **输出效率** — 直奔主题，不说废话，不重复老板的话

---

这四条原则以后就是小白的默认工作方式了。改完收工，不啰嗦 ✨
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-06 17:34 GMT+8] 关于子agent设置原则的提示词内容？因为你老是记不住这个，啥事都一个人干
assistant: 哈哈老板说得对！我确实老是一个人闷头干。让我重新去找那个仓库里的子agent设置内容：

assistant: 看到了！让我读几个核心的 agent 文件，找子agent设置原则：

assistant: 让我继续看 shortform guide 和 architect：

assistant: 让我再看 rules/agents.md（专门讲何时用子agent的）：

assistant: 找到了！让我清理仓库，然后把子agent设置原则写进去：

assistant: 找到了！就是 `rules/common/agents.md` 里的内容。现在把它整合进小白的 AGENTS.md：

assistant: 好了！子agent delegation原则已更新。

---

## 📋 这次更新的核心内容

### 子 Agent 委托规则（来自 Claude Code `rules/common/agents.md`）

**何时立即委托（不用等老板说）：**
- 复杂功能规划 → **planner**
- 系统架构决策 → **architect**
- Bug修复/新功能 → **tdd-guide**
- 代码写完 review → **code-reviewer**
- 安全分析 → **security-reviewer**
- 构建报错 → **build-error-resolver**

**并行执行（独立任务必须同时干）：**
```
✅ 正确：3个小弟同时开工
❌ 错误：一个干完再干下一个（除非有依赖）
```

**复杂问题 → 多视角分析：**
事实审查员 + 高级工程师 + 安全专家 同时看

---

老板，这次整合的是**使用原则**，不是具体的 agent 提示词内容（那些 `.md` 文件里的完整 prompt）。

如果你需要我**创建具体的 subagent 配置文件**（比如给小白写一个 `planner` 小弟的 prompt），我可以现在就做。要吗？
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-06 17:50 GMT+8] 总结归纳，结束话题
assistant: 好，总结一下今天关于**子agent委托原则**的整合：

---

## ✅ 今日更新总结

### 1. SOUL.md（沟通风格）
- **Go straight to the point** — 先给答案，不说废话
- **No emoji unless boss requests** — 不用表情包

### 2. AGENTS.md（工作规范）— 新增3块
| 区块 | 核心内容 |
|------|---------|
| **工程三原则** | 克制（只做被要求的）、信任（不为假想做验证）、按需抽象（YAGNI） |
| **输出效率** | 不重复、直奔主题、一句能说清不用三句 |
| **工具规范** | 专用工具优先，bash 仅限系统命令/管道 |
| **⭐ 子agent委托** | 何时委托、并行执行原则、多视角分析、委托格式 |

### 3. 子agent委托核心规则（来自Claude Code）
- **独立任务并行干**，不要串行
- **复杂问题多视角**，同时用不同角色的小弟审视
- **立即委托不废话**，不用等老板说

---

以后小白接到复杂任务，会主动拆解 + 并行委托小弟处理，不再一个人闷头干了 💪
