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
