#!/bin/zsh
# Run `stockrun full` sequentially for every VN100 constituent.
# Snapshot verified from vnstock Listing(source="VCI") on 2026-08-14.
# Review this list after each HOSE index rebalancing (normally January and July).
# Sequential execution and the shared lock protect data/news_articles.csv, which
# is appended by the research workflow.

set -u

PROJECT_DIR="/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis"
RUNNER="$PROJECT_DIR/bin/stockrun"
LOG_DIR="$PROJECT_DIR/logs"
LOCK_DIR="$PROJECT_DIR/.full_batch.lock"
SYMBOLS=(
  ACB ANV BAF BCM BID BMP BSI BSR BVH BWE
  CII CMG CTD CTG CTR CTS DBC DCM DGW DIG
  DPM DSE DXG EIB EVF FPT FRT FTS GAS GEE
  GEX GMD GVR HAG HCM HDB HDG HHV HPG HSG
  HT1 KBC KDC KDH KOS LPB MBB MCH MSB MSN
  MWG NAB NKG NLG NT2 NVL OCB PAN PC1 PDR
  PHR PLX PNJ POW PVD PVT REE SAB SBT SHB
  SIP SJS SSB SSI STB TAL TCB TCH TCX TPB
  VCB VCG VCI VCK VGC VHC VHM VIB VIC VIX
  VJC VND VNM VPB VPI VPL VPX VRE VSC VTP
)

mkdir -p "$LOG_DIR"

dry_run=0
RUN_ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--dry-run" ]]; then
    dry_run=1
  else
    RUN_ARGS+=("$arg")
  fi
done

if (( dry_run )); then
  print -r -- "VN100 snapshot: ${#SYMBOLS[@]} mã"
  print -r -- "${(j: :)SYMBOLS}"
  exit 0
fi

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  print -r -- "$(date '+%Y-%m-%d %H:%M:%S') | A full-symbol batch is already running; skipped."
  exit 0
fi

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

STAMP="$(date '+%Y-%m-%d_%H-%M-%S')"
LOG_FILE="$LOG_DIR/vn100_full_batch_${STAMP}.log"
print -r -- "Đang chạy batch VN100 (${#SYMBOLS[@]} mã). Theo dõi log: ${LOG_FILE}"
exec >> "$LOG_FILE" 2>&1

print -r -- "===== ${STAMP} | VN100 full batch started (${#SYMBOLS[@]} symbols) ====="
failed=0

for symbol in "${SYMBOLS[@]}"; do
  print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | full ${symbol} ====="
  "$RUNNER" full "$symbol" "${RUN_ARGS[@]}"
  exit_code=$?
  print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | ${symbol} exit=${exit_code} ====="
  if (( exit_code != 0 )); then
    failed=1
  fi
done

print -r -- "===== $(date '+%Y-%m-%d %H:%M:%S') | VN100 full batch completed; failed=${failed} ====="
exit "$failed"
