#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [[ "$(uname -s)" == "Darwin" ]] && ! .venv/bin/python -c "import xgboost" >/dev/null 2>&1; then
  echo "XGBoost trên macOS cần OpenMP. Chạy: brew install libomp"
fi

echo "Xong. Chạy thử: ./run_now.sh HCM"
