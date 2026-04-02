# LEARNINGS.md — 小白学到的教训

> 每次被纠正后，立刻记录。不要拖。

---

## 2026-03-30

### 智谱看图模型名是 glm-4.6v-flashx（不是 glm-4v-flashx）

**问题**：一直用 `glm-4v-flashx`，报错"模型不存在"好几次。
**正确**：模型名是 `glm-4.6v-flashx`
**接口**：POST https://open.bigmodel.cn/api/paas/v4/chat/completions
**方法**：图片 base64 → `data:image/jpeg;base64,...` → max_tokens 500
**返回**：内容在 `reasoning_content` 字段，不在 `content` 字段
**额度**：还有 985 万 token，用不完

**教训**：遇到"模型不存在"错误时，第一反应应该是"模型名记错了"，而不是"模型过期了"。先去确认正确名称。

---

### Session Startup 必须读 LEARNINGS.md 和 ERRORS.md

**问题**：每次新对话都会重复犯同样的错误。
**原因**：只读了 MEMORY.md，没读 .learnings/ 下的文件。
**解决**：AGENTS.md 已更新 startup 步骤，必须同时读 LEARNINGS.md 和 ERRORS.md。

---

### Qwen3.5-9B-MLX-4bit 支持图片识别

**问题**：以为本地 oMLX 模型不支持图片。
**正确**：Qwen3.5-9B-MLX-4bit 支持 vision，可以通过 oMLX API 用图片。
**用法**：传 `image_url` 格式（data:image/jpeg;base64,...）给 Qwen 模型。

---

## 2026-03-29

### oMLX 统一驱动，Ollama 已删除

- oMLX 端口 8000，API Key: 12345678
- 常驻模型：Qwen3.5-9B-MLX-4bit（对话）+ bge-m3-mlx-4bit（Embedding）
- Ollama 已删除，不再使用

---

## 更早的教训

### 图片发送到 QQ后 网页端看不到
- 老板在网页端看不到 `<qqmedia>` 标签，要去 QQ 端查看
- 媒体发送：直接在小白的 QQ 端发送，不通过小红/小兰中转

### 生图（千问 qwen-image-2.0）
- 模型：qwen-image-2.0（0.2元/张）
- 注意：wanx-v1 已下线（2026-03-27），不要再用

## 2026-03-30：看图必须用 direct API，不能用 image tool
- MEMORY.md 里早就有智谱看图配置，但执行时没遵守，跑去修 image tool
- image tool (PiCodingAgent.ModelRegistry) 底层有 bug，模型无法识别，配置改不对
- 正确做法：直接调 POST https://open.bigmodel.cn/api/paas/v4/chat/completions，glm-4.6v-flashx
- 教训：MEMORY.md 里有明确方法的 → 直接用，不要绕路修工具
