#!/bin/bash
# Rollback - 从检查点恢复
# 用法: bash rollback.sh [编号或latest]

WORKSPACE="/Users/wf/.openclaw/workspace-main"
CHECKPOINT_DIR="/Users/wf/.openclaw/checkpoints"
cd "$WORKSPACE"

if [ -z "$1" ]; then
    echo "📋 可用检查点:"
    ls -1t "$CHECKPOINT_DIR" | head -10 | nl
    echo ""
    echo "用法: bash ~/.openclaw/workspace-main/scripts/rollback.sh <编号或latest>"
    exit 0
fi

TARGET="$1"
if [ "$TARGET" = "latest" ]; then
    CHECKPOINT_PATH=$(ls -1t "$CHECKPOINT_DIR" | head -1)
elif [[ "$TARGET" =~ ^[0-9]+$ ]]; then
    CHECKPOINT_PATH=$(ls -1t "$CHECKPOINT_DIR" | sed -n "${TARGET}p")
fi

if [ -z "$CHECKPOINT_PATH" ] || [ ! -d "$CHECKPOINT_DIR/$CHECKPOINT_PATH" ]; then
    echo "❌ 检查点不存在: $TARGET"
    exit 1
fi

CHECKPOINT_FULL="$CHECKPOINT_DIR/$CHECKPOINT_PATH"
echo "🔄 回滚到: $CHECKPOINT_PATH"

if [ -f "$CHECKPOINT_FULL/meta.json" ]; then
    DESCRIPTION=$(grep '"description"' "$CHECKPOINT_FULL/meta.json" | cut -d'"' -f4)
    STASH_INDEX=$(grep '"stash_index"' "$CHECKPOINT_FULL/meta.json" | cut -d'"' -f4)
    echo "描述: $DESCRIPTION | Stash Index: $STASH_INDEX"
fi

if [ "$STASH_INDEX" != "none" ] && [ -n "$STASH_INDEX" ]; then
    echo "📦 恢复 Git stash..."
    git stash pop --index $((STASH_INDEX - 1)) 2>/dev/null || echo "⚠️ Stash 恢复失败"
fi

[ -f "$CHECKPOINT_FULL/memory.md.bak" ] && cp "$CHECKPOINT_FULL/memory.md.bak" "$WORKSPACE/MEMORY.md" && echo "📄 MEMORY.md 已恢复"
[ -f "$CHECKPOINT_FULL/heartbeat.md.bak" ] && cp "$CHECKPOINT_FULL/heartbeat.md.bak" "$WORKSPACE/HEARTBEAT.md" && echo "📄 HEARTBEAT.md 已恢复"

echo ""
echo "✅ 回滚完成！"
