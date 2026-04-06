---
name: Grep Search
slug: grep-search
version: 1.0.0
description: Fast grep-based search across memory files, workspace, and Obsidian vault — no vector search, no API calls. Emulates Claude Code's direct search approach.
---

## When to Use

- User asks about something we've done before ("我们之前做过 X 吗")
- User asks to search/recall information from past sessions
- User asks "记得..." or "搜索..." or "找..."
- `memory_search` would have been called, but we use this instead

## Search Scope

Search these locations in order:
1. `~/.openclaw/workspace-main/MEMORY.md`
2. `~/.openclaw/workspace-main/memory/*.md`
3. `~/Documents/Obsidian Vault/memory/*.md`
4. `~/Documents/Obsidian Vault/*.md` (top-level Obsidian notes)
5. `~/.openclaw/workspace-main/**/*.md`

## Search Command

```bash
grep -rni "keyword" ~/.openclaw/workspace-main/MEMORY.md ~/.openclaw/workspace-main/memory/ ~/Documents/Obsidian\ Vault/memory/ ~/Documents/Obsidian\ Vault/ 2>/dev/null | head -50
```

For Obsidian vault:
```bash
grep -ri "keyword" ~/Documents/Obsidian\ Vault/ 2>/dev/null | head -30
```

## Response Format

After search, summarize findings:
- Which files matched
- Key context from each match
- Direct quotes where helpful

## Rules

- Always use grep, never call the vector embedding API
- Case-insensitive by default (-i flag)
- Show file path and line number (-n flag)
- Limit to 50 results to avoid flooding
- If no results, suggest alternative keywords

## Example

User: "我们之前讨论过 Claude Code 吗"

```bash
grep -rni "claude code" ~/Documents/Obsidian\ Vault/ ~/.openclaw/workspace-main/ 2>/dev/null | head -20
```

Then summarize the matches.
