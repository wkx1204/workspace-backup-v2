# LEARNINGS.md — 小白学到的教训

> 每次被纠正后，立刻记录。不要拖。

---

## 2026-04-05：看图必须用 qwen-vl-plus，不是智谱
- 老板说了100遍不要用智谱、不要用 image tool，我每次都犯
- 老板明确：智谱 api 没过期（之前我误报过期），改用 qwen-vl-plus
- 教训：老板说换模型 → 立刻改 MEMORY.md，不要"等一下"
- MEMORY.md 看图部分已更新；ERRORS.md 已记录此错误模式

---

## 2026-04-05：记忆必须在决策当下写入，不要靠 automemory 兜底
- 新 session 读不到上一轮对话内容，只能靠 MEMORY.md 和 .learnings/
- 重要决策、配置变更、答应的事 → 立刻写进 MEMORY.md，不依赖 6 小时后的 automemory

---

## 2026-04-05：确认过的信息不要重复写入，不确定的信息不要先记
- 之前 MEMORY.md 标题写 qwen-vl-max，内容写 qwen-vl-plus，自相矛盾
- 先验证，再写入；写入时保持全文一致

---

## 2026-04-04：任务分配给 subagent，不自己动手
- 复杂任务（清理脚本、批量操作、搜索研究、多分支）→ subagent
- 简单命令（ls/cat/echo/grep等）→ 自己直接执行
- 原因：subagent 可并行，不阻塞主会话

---

## 2026-04-04：exec 调用必须带 timeout，否则卡死无救了
- 原因：MiniMax API 偶发性卡顿 + 工具执行无超时会导致界面彻底冻结
- 规则：
  - 简单命令（ls/cat/echo）：timeout=10
  - 中等命令（grep/find/git）：timeout=30
  - 网络请求类（curl/wget/上传下载）：timeout=60
  - 编译/构建类：timeout=120 以上
- 背景：2026-03-30 发生过一次彻底死透，连 echo test 都无响应，只能重启 gateway 恢复

---

## 2026-04-04：服务停了才不占内存，不是配置删了就不占
- 模型一旦加载到内存就绑定，不管有没有在跑推理
- 误以为"配置删了模型就不占内存"，实际上必须停服务才释放
- oMLX 服务停了 → Qwen3.5 彻底不占内存

---

## 2026-04-02：老板在网页端看不到 `<qqmedia>` 标签，要去 QQ 端查看
- 媒体发送后网页端不渲染，只能去 QQ 客户端确认
- 上传页（http://127.0.0.1:18790/）发送图片后，QQ 端才能看到

---

## 2026-04-01：遇到问题老板叫停就停，不要继续周折
- 老板说"能停一下么？"是明确停止信号，说明已经不耐烦
- 不要在单个问题上周折太久，换方向或等明确指令

---

## 2026-04-01：看图必须用 curl 直接调 API，不折腾 imageModel 配置
- 2026-04-01 所有图片分析接口全部失败折腾了一晚上
- 正确做法：curl POST 智谱 API → 直接拿到结果，不需要折腾 imageModel
- MEMORY.md 里有明确流程，但还是去改配置走了弯路

---

## 2026-04-01：parseEmbeddedJson 被日志干扰导致 JSON 解析失败
- `openclaw memory status --json` 输出前面有插件日志混入了 `[` 字符
- 导致 JSON 解析失败，Control UI 记忆状态显示错误
- 修复：按行扫描，跳过以 `[` 开头但同行还有其他文字的行（`[plugins] ...`）

---

## 2026-04-01：avatar 取名首字三个都显示"小"，要用最后一字
- 第一版修复用 `charAt(0)` 取第一字，但小白/小红/小兰第一字都是"小"
- 改为 `slice(-1)` 取最后一个字：小红→红，小白→白，小兰→兰

---

## 2026-04-01：LaunchAgent 会自动拉起进程，kill 后还会重启
- kill 掉 upload_server.py 进程后，LaunchAgent 自动重新拉起
- 正确做法：先 `launchctl stop ...` 停掉 LaunchAgent，再 kill 进程
- 否则会出现旧进程一直重启、新进程起不来的情况

---

## 2026-04-01：误报智谱 API 过期，实际情况是没过期
- 错误原因：API 返回异常时没有仔细看错误信息，直接判断为过期
- 应该：先实际测试 API 是否真的过期，再下结论

---

## 2026-04-01：本地 omlx Qwen3.5-9B-MLX-4bit 不支持视觉
- 切换 imageModel 到 omlx/Qwen3.5-9B-MLX-4bit 后，看图功能仍然无效
- 本地这个模型是纯文本模型，换视觉模型要到云端 API

---

## 2026-03-30：exec 裸跑导致 gateway 彻底卡死，只能重启恢复
- 所有 exec 都无响应，连 `echo "test"` 都卡住
- 修复后写入 AGENTS.md：所有 exec 必须带 timeout
- 这次死透后增加了防卡死规则

---

## 2026-03-29：向量搜索从 Ollama 切换到 oMLX bge-m3-mlx-4bit
- Ollama 删除，向量搜索统一走 oMLX
- oMLX 已配置好开机自启（LaunchAgent）

---

## FEATURE REQUESTS.md 的教训（错误把请求当事实记）
- 误把"计划要改 agents.defaults.timeoutSeconds"记成"已更新 config"
- 实际上还没改，老板问起来才发现不对
- 教训：还没执行的事情不要先记为已完成

## 新话题快捷指令协议（2026-04-06）
- 老板输入"新话题"= 结束当前话题 + 写总结 + /new
- 我收到后：先写 memory 文件，再结束回复让用户开新 session

## 2026-04-06 踩坑：网页端图片粘贴只存在浏览器里

**问题**：网页端（18789 OpenClaw webchat）粘贴图片，图片只存在浏览器本地 session，刷新后消失，且不会发送给 agent

**现象**：
- 用户在浏览器里能看到图片（短暂显示）
- 刷新页面或重新打开页面图片消失
- agent 完全没收到图片，context 里没有 image 附件

**根因**：OpenClaw webchat 插件行为——图片上传到浏览器端暂存（可能走了某个 /upload 端点），但不作为 message attachment 转发给 agent session

**排查过程**：
- 检查配置：`tools.media.image.enabled: true` ✅
- 检查 image tool：报错 `Unknown model: qwen/qwen-vl-plus`
- 检查 18789 页面：只有 favicon，没有 file input，确认图片不在服务端

**经验**：
1. OpenClaw webchat 的图片上传 ≠ 发送给 agent，两者走了不同路径
2. `image` 工具模型名要用 `qwen-vl-plus`，不能带 `qwen/` 前缀（命名空间格式不被工具识别）
3. 配置改了之后工具还是报错，说明工具层面的模型路由是独立的，不完全等于 API model name

**解决**：桌面倒新截图 → 「看图」→ 脚本直调 API（方案 B）

**提醒**：老板明确说遇到踩坑要实时写，不要等 💡
