#!/bin/bash
# Run one scheduled script job safely.
#   run_job.sh <job-name> <command> [args...]
# - macOS: waits up to 10 minutes for a FULL wake. launchd can start a job during a
#   "dark wake" (lid closed, on battery); the Mac sleeps again within seconds and network
#   calls time out. `pmset -g systemstate` lists "Graphics" only when fully awake.
# - Keeps the Mac awake while the job runs (caffeinate -i).
# - Logs to ~/Library/Logs/<job>.log (macOS) or ~/.local/state/<job>.log (elsewhere).
# - On failure, posts a short alert through notify.py (if configured).
set -u
JOB="$1"; shift
HOME_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="$HOME_DIR/.venv/bin/python"
if [ "$(uname -s)" = "Darwin" ]; then LOG="$HOME/Library/Logs/$JOB.log"; else LOG="$HOME/.local/state/$JOB.log"; mkdir -p "$(dirname "$LOG")"; fi

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') $JOB"
  if [ "$(uname -s)" = "Darwin" ]; then
    for _ in $(seq 1 60); do
      pmset -g systemstate 2>/dev/null | grep -q Graphics && break
      echo "waiting for full wake…"; sleep 10
    done
    caffeinate -i "$@"
  else
    "$@"
  fi
  STATUS=$?
  echo "=== exit $STATUS"
} >>"$LOG" 2>&1

if [ "${STATUS:-1}" -ne 0 ] && [ -x "$PY" ]; then
  "$PY" "$HOME_DIR/scripts/notify.py" alert "$JOB failed (exit ${STATUS:-?}); see $LOG" >/dev/null 2>&1
fi
exit "${STATUS:-1}"
