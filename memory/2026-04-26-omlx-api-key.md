# Session: 2026-04-26 15:55:12 UTC

- **Session Key**: agent:main:main
- **Session ID**: 34c9dbb3-38ca-4394-a2b3-da5c027520d7
- **Source**: webchat

## Conversation Summary

assistant: 


assistant: 配置本身没问题——你本地的 `omlx` provider 已经配好了，指向 `http://127.0.0.1:8000/v1`，模型 ID 是 `Qwen3.5-9B-MLX-4bit`。

问题可能出在两个地方：

1. **你本地的服务真的在跑吗？** 在终端跑一下 `curl http://127.0.0.1:8000/v1/models`，看看能不能返回模型列表
2. **Web UI 刷新的是已注册的 provider 列表**，如果 omlx 服务没响应，OpenClaw 可能不会把它加到可用模型里

先在终端确认本地服务状态：

```bash
curl -s http://127.0.0.1:8000/v1/models | head -5
```

如果能返回内容，我去查查 Web UI 的 model selector 怎么刷新才能显示出来。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:42 GMT+8] wf@wfdeMac-mini ~ % curl -s http://127.0.0.1:8000/v1/models | head -5
{"error":{"message":"API key required","type":"authentication_error","param":null,"code":null}}% wf@wfdeMac-mini ~ %
user: [Sun 2026-04-26 23:42 GMT+8] wf@wfdeMac-mini ~ % curl -s http://127.0.0.1:8000/v1/models | head -5
{"error":{"message":"API key required","type":"authentication_error","param":null,"code":null}}% wf@wfdeMac-mini ~ %
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:42 GMT+8] wf@wfdeMac-mini ~ % curl -s http://127.0.0.1:8000/v1/models | head -5
{"error":{"message":"API key required","type":"authentication_error","param":null,"code":null}}% wf@wfdeMac-mini ~ %
assistant: 本地服务是活着的，只是要求 API key。OpenClaw 的 `omlx` provider 没配 `apiKey`，所以 OpenClaw 请求时没带过去，服务拒绝了。

搞个 API key 加上就好了。你本地跑的是 mlx-server 吗？它的 API key 是什么？一般来说默认可能是 `sk-xxx` 格式的随便填一个。

两种解法：

**简单方案** — 在配置里加上 apiKey。如果你本地 mlx 没校验的话，随便填一个 dummy key：

```bash
openclaw config set models.providers.omlx.apiKey "sk-no-key-required"
```

**如果本地服务真要校验** — 去查一下你启动 mlx-server 时指定的 `--api-key` 参数是什么，填进去就行。

加完刷新页面或者重启 gateway，应该就能在列表里看到了。
user: [Sun 2026-04-26 23:42 GMT+8] wf@wfdeMac-mini ~ % curl -s http://127.0.0.1:8000/v1/models | head -5
{"error":{"message":"API key required","type":"authentication_error","param":null,"code":null}}% wf@wfdeMac-mini ~ %
assistant: 本地服务是活着的，只是要求 API key。OpenClaw 的 `omlx` provider 没配 `apiKey`，所以 OpenClaw 请求时没带过去，服务拒绝了。

搞个 API key 加上就好了。你本地跑的是 mlx-server 吗？它的 API key 是什么？一般来说默认可能是 `sk-xxx` 格式的随便填一个。

两种解法：

**简单方案** — 在配置里加上 apiKey。如果你本地 mlx 没校验的话，随便填一个 dummy key：

```bash
openclaw config set models.providers.omlx.apiKey "sk-no-key-required"
```

**如果本地服务真要校验** — 去查一下你启动 mlx-server 时指定的 `--api-key` 参数是什么，填进去就行。

加完刷新页面或者重启 gateway，应该就能在列表里看到了。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:43 GMT+8] aoikey=12345678
user: [Sun 2026-04-26 23:43 GMT+8] aoikey=12345678
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:43 GMT+8] aoikey=12345678
assistant: 搞定，API key 加上了。先验证一下：


assistant: 服务正常响应了，现在重启 gateway 让配置生效：


user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:45 GMT+8] 你是什么模型?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sun 2026-04-26 23:45 GMT+8] 你是什么模型?
