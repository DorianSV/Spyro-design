#!/bin/bash
# Weekly Job Radar run for macOS / Linux. Used by cron (see README). Test it once by hand first:
#   bash run-weekly.sh
cd "$(dirname "$0")" || exit 1
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"
mkdir -p logs
LOG="logs/run-$(date +%Y-%m-%d).log"

claude -p "/job-radar" \
  --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Agent,Bash(python3 *)" \
  > "$LOG" 2>&1
STATUS=$?

if [ "$(uname)" = "Darwin" ]; then
  if [ $STATUS -eq 0 ]; then MSG="Job Radar finished. Open tracker.html."; else MSG="Job Radar failed. See $LOG"; fi
  osascript -e "display notification \"$MSG\" with title \"Job Radar\""
fi
exit $STATUS
