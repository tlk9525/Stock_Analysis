# All-Vietnam panel model

## Chạy

Smoke test snapshot thị trường hiện tại:

```bash
scripts/run_all_vietnam_panel.sh --max-symbols 20 --no-postgres
```

Chạy toàn bộ snapshot HOSE/HNX/UPCOM:

```bash
scripts/run_all_vietnam_panel.sh --no-postgres
```

Snapshot hiện tại chỉ dùng nghiên cứu và luôn fail `point_in_time_universe`.
Muốn có khả năng qua publish gate, dùng registry lịch sử:

```bash
bin/stockrun rank \
  --universe-csv data/universe_registry.csv \
  --foreign-flow-csv data/foreign_flow_history.csv \
  --horizons 5,10,20 \
  --no-postgres
```

## Contract universe point-in-time

| Cột | Ý nghĩa |
|---|---|
| `symbol` | Mã cổ phiếu |
| `exchange` | `HOSE`, `HNX`, `UPCOM` |
| `sector` | Ngành biết tại thời điểm đó |
| `listed_at` | Thời điểm bắt đầu đủ điều kiện |
| `delisted_at` | Thời điểm hủy niêm yết, có thể rỗng |
| `available_at` | Thời điểm hệ thống thực sự biết record |
| `status` | `active` hoặc `delisted` |

Không được dựng `available_at` từ dữ liệu tải về hôm nay rồi gắn ngược về quá
khứ. Registry phải chứa cả mã hủy niêm yết để tránh survivorship bias.

## Contract foreign flow

CSV bắt buộc có:

```text
symbol,date,available_at,foreign_buy_value,foreign_sell_value
```

Feature chỉ được nối nếu `available_at <= 15:00 Asia/Ho_Chi_Minh` của ngày tín
hiệu. Thiếu dữ liệu giữ nguyên `NaN`; pipeline không coi thiếu là dòng tiền 0.

## Logic production

- Train rộng trên mọi row đủ feature và target.
- Target: excess return so với VNINDEX sau estimated round-trip cost, cho
  5/10/20 phiên.
- Trade hẹp: chỉ mã có tối thiểu 252 phiên, ít nhất 15/20 phiên có giao dịch và
  median traded value 20 phiên đạt 5 tỷ VND.
- Prediction net phải vượt margin chọn trong validation.
- Frozen holdout, Rank IC HAC, net return/Sharpe và stress cost 1.5x phải đạt.
- Snapshot universe hiện tại, flow/tin không point-in-time hoặc sample thiếu đều
  giữ trạng thái `NO_EDGE`.

## Artifact audit

Mỗi run sinh thêm:

- `universe_registry.csv`
- `universe_summary.json`
- `feature_availability.json`
- `panel_features.csv` có `is_tradable`, cost và target net
- ranking/backtest/trade ledger riêng cho 5/10/20 phiên
- dashboard BI có chart động, dark/light, cost và trạng thái thanh khoản từng mã
