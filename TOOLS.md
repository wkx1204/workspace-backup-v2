# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### Image Analysis

- Supported formats: jpg, png, gif, webp
- Local paths allowed: workspace subdirs only (e.g. ./, projects/)
- External paths blocked: /Users/wf/.openclaw/qqbot/downloads/...
- Workaround: cp file to workspace/ then analyze

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Image Analysis

- Supported formats: jpg, png, gif, webp
- Local analysis path restriction: only files inside workspace can be sent to image analysis tools
- QQBot downloads land outside workspace by default: /Users/wf/.openclaw/qqbot/downloads/...
- Current workaround: copy incoming QQ images into ./inbox/ first, then analyze
- Local OCR helper script: ./scripts/ocr_image.py
- OCR dependency status: helper script installed; tesseract binary still needs successful installation to enable OCR text extraction

### Browser Control（浏览器控制）

三种方法，各有用途：

**1. AppleScript（无需 opencli）**
```bash
# 获取 Chrome 当前标签页 URL
grep osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'
```
- 无需 opencli 扩展
- 只适合获取 URL / 标题等简单信息

**2. Playwright（无需 opencli）**
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('URL')
    content = page.content()
```
- 无需 opencli 扩展
- 可抓取任意页面内容，支持登录态
- 适合：网页正文提取、登录页面操作、动态内容抓取

**3. opencli（需 Chrome 扩展）**
```bash
opencli gemini ask "问题"
opencli bilibili hot
opencli weibo post "内容"
```
- 需要 Chrome 扩展（~/.opencli/opencli-extension/）已加载
- 适合：结构化的网站操作（发微博/查排行/自动化表单等）
- 已装扩展：opencli v1.6.9，daemon 运行在 port 19825

**何时用哪个：**
- 下载视频/抓字幕 → yt-dlp + summarize skill（不开浏览器）
- 抓网页正文/登录态内容 → Playwright
- 快速结构化操作（微博/B站/gemini） → opencli
- 简单获取当前标签页 URL → AppleScript

### YouTube 处理

- 字幕/内容提取 → summarize skill 或 Playwright 抓 transcript API
- 视频下载 → yt-dlp（最稳）
  ```bash
  yt-dlp "URL" -o "%(title)s.%(ext)s"
  ```
- 视频帧提取 → video-frames skill（ffmpeg）
