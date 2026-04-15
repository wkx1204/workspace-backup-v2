#!/bin/bash
# 婷婷本地TTS，输出MP3
TEXT="$1"
OUTPUT="${2:-/tmp/tts_output.mp3}"
CAFFILE="/tmp/tts_input.caf"
say -v "Tingting" -o "$CAFFILE" -- "$TEXT"
ffmpeg -y -i "$CAFFILE" -acodec libmp3lame -ab 128k "$OUTPUT" 2>/dev/null
rm -f "$CAFFILE"
echo "$OUTPUT"
