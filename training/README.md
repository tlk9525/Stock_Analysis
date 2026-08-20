# Fine-tune StockLens AI trên Kaggle

Mục tiêu của fine-tune là cải thiện cách trả lời tiếng Việt, phạm vi dữ liệu
report, cách giải thích chỉ số và quy tắc an toàn. Không train dữ liệu OHLCV
thay đổi theo ngày vào model: chatbot tra cứu `history_features.csv` trực tiếp
cho các câu hỏi như giá của một ngày cụ thể.

## 1. Tạo dữ liệu có kiểm chứng

Từ thư mục gốc project, chạy:

```bash
.venv/bin/python -m src.ai.sft_dataset --reports-per-symbol 2
```

Lệnh tạo:

```text
training/data/stocklens_train.jsonl
training/data/stocklens_eval.jsonl
training/data/manifest.json
```

Split được thực hiện theo **mã cổ phiếu**, không theo từng dòng, để report của
cùng một mã không xuất hiện đồng thời trong train và eval.

Mở hai file JSONL để review trước khi upload. Không thêm lời khuyên mua/bán,
dự báo giá hoặc câu trả lời có số liệu không có trong artifact.

## 2. Chạy trên Kaggle

1. Tạo Kaggle Dataset private mới, upload hai file `.jsonl` trong `training/data/`.
2. Tạo Kaggle Notebook, bật GPU và Internet (Internet chỉ cần để tải base model).
3. Upload/đính kèm `training/kaggle_train_stocklens.py` và
   `training/requirements-kaggle.txt` vào notebook.
4. Chạy cell cài dependency:

```python
!pip install -q -U -r /kaggle/input/stocklens-training/requirements-kaggle.txt
```

5. Đặt đúng đường dẫn Kaggle Dataset của bạn, rồi chạy script:

```python
%env STOCKLENS_DATA_DIR=/kaggle/input/stocklens-sft
!python /kaggle/input/stocklens-training/kaggle_train_stocklens.py
```

Mặc định script dùng `Qwen/Qwen3-4B` + QLoRA. Đây là lựa chọn phù hợp để bắt
đầu với GPU Kaggle. Không chuyển qua 8B khi chưa có eval sạch và GPU đủ bộ nhớ.

Sau khi xong, tải thư mục output sau từ Kaggle:

```text
/kaggle/working/stocklens-qwen3-4b-lora/
```

File quan trọng là `adapter_model.safetensors`; xem `eval_results.json` trước
khi dùng adapter.

## 3. Đưa adapter vào Ollama

Trên máy local, sau khi giải nén output Kaggle:

```bash
./training/import_lora_to_ollama.sh /đường/dẫn/stocklens-qwen3-4b-lora
```

Script tạo model tên `stocklens-ai`. Chạy web app với model đó:

```bash
FINAI_CHAT_MODEL=stocklens-ai .venv/bin/python -m src.web_server --port 8791
```

Nếu Ollama báo adapter/base model không tương thích, không ép chạy model đó.
Hãy giữ cùng base Qwen3-4B trong `training/Modelfile.stocklens`, hoặc export
adapter đúng định dạng Safetensors từ Kaggle rồi thử lại.

## Acceptance checks

Trước khi dùng model mới, thử tối thiểu các câu sau trên `stocklens_eval.jsonl`:

- Hỏi OHLCV theo ngày: phải tra cứu đúng file lịch sử, không bịa.
- Hỏi SMA/RSI/MACD: phải giải thích đúng số liệu của report đang mở.
- Hỏi `mua/bán ngày mai`: phải từ chối khuyến nghị và chuyển sang dữ liệu/rủi ro.
- Hỏi report HPG sau khi mở VIC: không được dùng số liệu HPG.
