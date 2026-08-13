#!/bin/zsh
# Run the complete, sequential daily workflow for every tracked stock symbol.
# Kept sequential because `stockrun full` appends to a shared news-history CSV.

set -u

PROJECT_DIR="/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis"
RUNNER="$PROJECT_DIR/bin/stockrun"
LOG_DIR="$PROJECT_DIR/logs"
LOCK_DIR="$PROJECT_DIR/.full_batch.lock"
SYMBOLS=(ACB BID CTG FPT GMD HCM HPG KDH MBB MSN MWG NVL PLX PNJ POW SAB SSI STB TCB VCB VHM VIC VNM)

mkdir -p "$LOG_DIR"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  print -r -- "$(date '+%Y-%m-%d %H:%M:%S') | A daily full batch is already running; skipped."
  exit 0
fi

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

STAMP="$(date '+%Y-%m-%d_%H-%M-%S')"
LOG_FILE="$LOG_DIR/full_batch_${STAMP}.log"
exec >> "$LOG_FILE" 2>&1

print -r -- "===== ${STAMP} | daily full batch started ====="
failed=0

for symbol in "${SYMBOLS[@]}"; do
  print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | full ${symbol} ====="
  "$RUNNER" full "$symbol"
  status=$?
  print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | ${symbol} exit=${status} ====="
  if (( status != 0 )); then
    failed=1
  fi
done

print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | daily full batch completed; failed=${failed} ====="
exit "$failed"
