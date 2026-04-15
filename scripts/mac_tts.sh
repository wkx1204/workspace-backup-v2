#!/bin/bash
# mac_tts.sh - macOS本地TTS，输出MP3
# 用法: ./mac_tts.sh "文字内容" [输出路径]
# 默认输出: /tmp/tts_output.mp3

TEXT="${1:-你好}"
OUTPUT="${2:-/tmp/tts_output.mp3}"

# 转换为MP3 (CAF -> MP3 via ffmpeg)
CAFFILE="/tmp/tts_input.caf"
say -v "Tingting" -o "$CAFFILE" -- "$TEXT"
ffmpeg -y -i "$CAFFILE" -acodec libmp3lame -ab 128k "$OUTPUT" 2>/dev/null
rm -f "$CAFFILE"
echo "$OUTPUT"
