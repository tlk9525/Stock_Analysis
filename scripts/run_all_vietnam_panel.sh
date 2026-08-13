#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Snapshot toàn thị trường dùng để train rộng. Publish guard vẫn chỉ cho phép
# giao dịch mã đạt history, thanh khoản, cost stress và frozen holdout.
exec "$PROJECT_DIR/bin/stockrun" rank \
  --universe all-vietnam \
  --horizons 5,10,20 \
  "$@"
