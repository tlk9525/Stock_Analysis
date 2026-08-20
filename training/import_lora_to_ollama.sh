#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Cách dùng: $0 /đường/dẫn/tới/thư_mục_adapter"
  exit 1
fi

ADAPTER_DIR=$1
if [ ! -f "$ADAPTER_DIR/adapter_model.safetensors" ]; then
  echo "Không tìm thấy adapter_model.safetensors trong: $ADAPTER_DIR"
  exit 1
fi

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT
cp "$ADAPTER_DIR/adapter_model.safetensors" "$WORK_DIR/adapter_model.safetensors"
cp training/Modelfile.stocklens "$WORK_DIR/Modelfile"
(
  cd "$WORK_DIR"
  ollama create stocklens-ai -f Modelfile
)
echo "Đã tạo model Ollama: stocklens-ai"
echo "Chạy app: FINAI_CHAT_MODEL=stocklens-ai .venv/bin/python -m src.web_server --port 8791"
