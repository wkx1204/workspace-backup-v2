#!/bin/bash
# backup-workspace.sh — workspace-main 每日备份
# 用法: ./backup-workspace.sh
# Cron: 0 23 * * * ~/.openclaw/workspace-main/scripts/backup-workspace.sh >> ~/.backup/workspace-main/backup.log 2>&1

set -e

WORKSPACE_DIR="/Users/wf/.openclaw/workspace-main"
BACKUP_DIR="/Users/wf/.backup/workspace-main"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
MANIFEST="${BACKUP_DIR}/manifest.json"

# 要排除的目录/文件（不备份）
EXCLUDE_DIRS=(
    "--exclude=.git"
    "--exclude=node_modules"
    "--exclude=*.db-journal"
    "--exclude=.DS_Store"
    "--exclude=xiaobai-site/node_modules"
)

# ========================
# Step 1: 创建备份文件
# ========================
BACKUP_FILE="${BACKUP_DIR}/workspace-main-${DATE}-${TIME}.tar.gz"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始备份..."

tar -czf "${BACKUP_FILE}" \
    "${EXCLUDE_DIRS[@]}" \
    -C "${WORKSPACE_DIR}" . 2>/dev/null

FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 备份完成: ${BACKUP_FILE} (${FILE_SIZE})"

# ========================
# Step 2: 更新 manifest
# ========================
TMP_MANIFEST=$(mktemp)

# 读取现有 manifest 或创建新的
if [ -f "${MANIFEST}" ]; then
    cp "${MANIFEST}" "${TMP_MANIFEST}"
else
    echo '{"backups":[]}' > "${TMP_MANIFEST}"
fi

# 追加新记录
python3 - <<EOF
import json, sys

with open("${TMP_MANIFEST}") as f:
    data = json.load(f)

data["backups"].append({
    "date": "${DATE}",
    "time": "${TIME}",
    "filename": "workspace-main-${DATE}-${TIME}.tar.gz",
    "size": "${FILE_SIZE}",
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
})

# 只保留最近 30 天的记录
data["backups"] = data["backups"][-30:]

with open("${TMP_MANIFEST}", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"manifest 更新完成，当前共 {len(data['backups'])} 条记录")
EOF

mv "${TMP_MANIFEST}" "${MANIFEST}"

# ========================
# Step 3: 清理旧备份（保留最近 30 天）
# ========================
python3 - <<EOF
import os, json
from datetime import datetime, timedelta

manifest_path = "${MANIFEST}"
backup_dir = "${BACKUP_DIR}"
cutoff = datetime.now() - timedelta(days=30)

with open(manifest_path) as f:
    data = json.load(f)

valid_files = set(b["filename"] for b in data["backups"])

removed = 0
for fname in os.listdir(backup_dir):
    if fname.endswith(".tar.gz") and fname not in valid_files:
        os.remove(os.path.join(backup_dir, fname))
        print(f"🗑️  删除旧备份: {fname}")
        removed += 1

if removed:
    print(f"已清理 {removed} 个旧备份，保留最近 30 天")
else:
    print("无需清理")
EOF

# ========================
# Step 4: Git add + tag + commit
# ========================
cd "${WORKSPACE_DIR}"
git add -A >/dev/null 2>&1
if git diff --cached --quiet; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️  无需 git 提交（无变化）"
else
    git commit -m "auto-backup: ${DATE} ${TIME}" >/dev/null 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Git 提交完成"
fi

# 打 tag（方便回滚）
TAG_NAME="bak-${DATE}"
if git tag | grep -q "^${TAG_NAME}$"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️  Tag ${TAG_NAME} 已存在"
else
    git tag -a "${TAG_NAME}" -m "每日备份 ${DATE}" >/dev/null 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🏷️  Tag ${TAG_NAME} 已打"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎉 备份全部完成！"
