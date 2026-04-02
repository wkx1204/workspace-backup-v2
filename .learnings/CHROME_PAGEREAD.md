# Chrome 页面内容读取方法
> 整理时间：2026-03-28
> 标签：#chrome #浏览器控制 #appleScript #javascript #openclaw

---

## 核心能力

开启 Chrome 的「允许 Apple 事件中的 JavaScript」后，OpenClaw 可以通过 AppleScript 执行 JavaScript，直接读取当前页面的文本内容。

**关键限制：** 页面内容只有用户本地可见，OpenClaw 需要用户主动触发才能读取。

---

## 开启方法

1. Chrome 菜单 → 查看(View) → 开发者(Developer)
2. 勾选「允许来自 Apple 事件的 JavaScript」(Allow JavaScript from Apple Events)
3. macOS 会弹出安全确认，点击允许

---

## AppleScript 读取页面内容

```bash
# 读取页面所有文本
osascript << 'EOF'
tell application "Google Chrome"
    tell active tab of front window
        set theText to execute javascript "document.body.innerText"
    end tell
    return theText
end tell
EOF

# 获取当前标签页 URL
osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'

# 获取所有标签页 URL
osascript -e 'tell application "Google Chrome" to get URL of every tab of every window'
```

---

## 应用场景

1. **读取登录态页面** — 豆包、Gemini 等需要账号的页面，无需重新登录
2. **实时获取页面数据** — 配合定时任务，定期抓取内容
3. **AI 联动** — 读取页面内容后喂给 AI 分析（无需截图）
4. **与小红小兰协作** — 她们可以通过此方法获取各自页面内容

---

## 注意事项

- 必须保持 Chrome 运行态
- 页面需完全加载后才能读取
- JavaScript 需页面内执行，部分扩展页面可能读取失败
- 此方法读不到 Cookie/Session，仅能读取 DOM 内容

---

## 相关工具对比

| 工具 | 能力 | 登录态 | 需要开启权限 |
|------|------|--------|------------|
| AppleScript + JS | 读取页面文本 | 无 | 是 |
| Playwright | 完整浏览器控制 | 无 | 否 |
| web_fetch | 抓取网页内容 | 无 | 否 |
| 智谱/gemini 看图 | OCR + 分析 | 无 | 否 |

---

## 使用时机

- 动态页面（JS 渲染）：AppleScript > web_fetch
- 需要登录态的内容：AppleScript
- 复杂交互自动化：Playwright
- 简单信息展示页：web_fetch
