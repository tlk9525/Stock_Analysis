# VN Stock Daily Analysis

Thư mục này dùng để chạy phân tích và dự báo sơ bộ cho bất kỳ mã cổ phiếu Việt Nam nào mà `vnstock` hỗ trợ.

Bạn không cần sửa mã nguồn khi muốn đổi mã cổ phiếu. Chỉ cần truyền mã vào lệnh chạy.

Dự án này dùng cơ sở dữ liệu PostgreSQL 18 `stock_db` để lưu kết quả phân tích.

Mô hình chính là XGBoost. Logistic Regression và majority class được giữ làm baseline để so sánh.

## Thiết lập môi trường Python

Chạy một lần:

```bash
./setup_env.sh
```

Script này sẽ tạo `.venv` và cài các thư viện:

- `vnstock`
- `pandas`
- `numpy`
- `matplotlib`
- `psycopg[binary]`
- `xgboost`
- `pytest`

Trên macOS, nếu XGBoost báo thiếu `libomp.dylib`:

```bash
brew install libomp
```

## Cấu trúc mã nguồn

```text
src/
├── data/
│   ├── fetch.py
│   └── transform.py
├── features/
│   ├── technical.py
│   └── fundamental.py
├── models/
│   ├── xgboost.py
│   ├── logistic.py
│   └── metrics.py
├── backtest/
│   └── engine.py
├── panel/
│   ├── data.py
│   ├── features.py
│   ├── model.py
│   ├── evaluation.py
│   └── report.py
├── forecast/
│   └── monte_carlo.py
├── risk/
│   ├── management.py
│   └── decision.py
├── reports/
│   └── dashboard.py
├── database/
│   └── postgres.py
├── config.py
├── metadata.py
├── panel_main.py
├── utils.py
└── main.py
```

`vn_stock_daily_analysis.py` chỉ là entrypoint tương thích ngược. Logic chính nằm trong `src/`.

## PostgreSQL 18 / stock_db

Nếu `psql` chưa có trong PATH, dùng đường dẫn của Postgres.app:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db
```

Tạo schema thủ công nếu cần:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db -f postgres_schema.sql
```

Mặc định ứng dụng kết nối bằng:

```text
postgresql:///stock_db
```

Có thể ghi đè bằng biến môi trường:

```bash
export DATABASE_URL="postgresql:///stock_db"
```

Hoặc truyền trực tiếp:

```bash
./run_now.sh HCM --database-url "postgresql:///stock_db"
```

## Chạy ngay với một mã

Ví dụ chạy mã HCM:

```bash
./run_now.sh HCM
```

Ví dụ chạy mã FPT:

```bash
./run_now.sh FPT
```

Ví dụ chạy mã VCB:

```bash
./run_now.sh VCB
```

Hoặc chạy bằng Python:

```bash
.venv/bin/python -m src.main --once --symbol HCM
```

Nếu bạn chạy `./run_now.sh` mà không nhập mã, chương trình sẽ hỏi mã trong terminal.

### Giai đoạn 1: kiểm định và tín hiệu an toàn hơn

Luồng một mã hiện dùng:

- Target có thể giao dịch: tạo tín hiệu sau `close[t]`, mua ở `open[t+1]` và bán ở `close[t+1]`.
- Expanding walk-forward nhiều fold theo thứ tự `train → gap → validation → gap → test`.
- Early stopping chỉ dùng validation; metrics cuối chỉ lấy các block OOS.
- Backtest tính commission, slippage, thuế bán, lô 100 cổ phiếu, vốn và giới hạn thanh khoản.
- Publish guard chỉ cho trạng thái `ACTIONABLE` khi chất lượng mô hình, xác suất, kỹ thuật, reward/risk, độ mới dữ liệu và lợi nhuận OOS sau chi phí đều đạt.
- Nếu chưa có lợi thế ròng, hệ thống trả `NO_EDGE` và ẩn position sizing.
- Monte Carlo dùng moving-block bootstrap để giữ cụm biến động và đuôi dày tốt hơn giả định phân phối chuẩn.

Các artifact kiểm toán bổ sung gồm `data_quality_report.json`, `signal_decision.json`, `resolved_config.json` và `run_metadata.json`.

## Giai đoạn 2: chạy panel nhiều cổ phiếu

Chạy universe mặc định trong `config.json`:

```bash
./run_panel.sh --no-postgres
```

Tùy chỉnh universe và horizon:

```bash
./run_panel.sh \
  --symbols FPT,VCB,MBB,TCB,HPG,VNM,MWG,SSI,HCM,VIC,VHM,GAS \
  --benchmark VNINDEX \
  --horizons 5,20 \
  --top-k 3 \
  --no-postgres
```

Panel thực hiện:

- Ghép dữ liệu point-in-time của từng mã với `VNINDEX`.
- Tạo target excess return 5/20 phiên từ `open[t+1]` đến `close[t+h]`.
- Huấn luyện XGBoost regression mặc định; có thể thử `--model-kind ranking`.
- Purge theo đúng horizon, validation riêng, early stopping và OOS prediction không chứa phần đuôi chưa có nhãn.
- Đánh giá Rank IC, top-k sau chi phí, Sharpe, drawdown, turnover và kết quả theo market regime. Vì mỗi target vào `open[t+1]` và thoát `close[t+h]`, mỗi cohort luôn chịu trọn chi phí mua + bán, kể cả khi cùng mã được chọn lại.
- Chỉ xuất `RESEARCH_OK` khi Rank IC dương, HAC/Newey-West t-stat đạt ngưỡng và top-k OOS sau chi phí có lợi nhuận cùng Sharpe dương; nếu không sẽ ghi `NO_EDGE`.

Kết quả nằm tại:

```text
reports/PANEL/YYYY-MM-DD_HH-MM-SS/
```

Các file chính gồm `panel_report.md`, `panel_dashboard.html`, `panel_performance.png`, `latest_rankings.csv`, `predictions_5d.csv`, `predictions_20d.csv`, `panel_backtests.csv`, metrics, fold metadata và model XGBoost theo từng horizon.

Lãi suất, dữ liệu vĩ mô và news sentiment chưa được trộn vào target/model của hai giai đoạn này; nên triển khai ở giai đoạn tiếp theo với timestamp công bố point-in-time để tránh look-ahead bias.

Giới hạn còn lại: universe hiện là danh sách mã cố định trong cấu hình nên có survivorship bias. Trước khi dùng cho nghiên cứu production, cần universe point-in-time gồm cả mã niêm yết/hủy niêm yết theo từng ngày và nguồn giá đã điều chỉnh corporate action nhất quán.

## Chạy tự động mỗi ngày

Chạy mỗi ngày cho HCM:

```bash
./run_daily_loop.sh HCM
```

Chạy mỗi ngày cho FPT:

```bash
./run_daily_loop.sh FPT
```

Mặc định giờ chạy nằm trong `config.json`, hiện là `15:30` theo múi giờ Việt Nam.

Bạn cũng có thể đổi giờ bằng tham số:

```bash
./run_daily_loop.sh HCM --run-time 20:00
```

## File đầu ra nằm ở đâu?

Mỗi lần chạy, chương trình tạo thư mục riêng theo mã:

```text
reports/SYMBOL/YYYY-MM-DD_HH-MM-SS/
```

Ví dụ:

```text
reports/HCM/2026-06-06_15-30-00/
reports/FPT/2026-06-06_15-30-00/
```

Bên trong có:

- `analysis_report.md`: báo cáo tóm tắt và khung kịch bản.
- `dashboard.html`: dashboard tổng hợp trực quan hơn, mở trực tiếp bằng trình duyệt.
- `history_chart.png`: biểu đồ giá, SMA, volume và drawdown.
- `technical_chart.png`: biểu đồ Bollinger Bands, MACD, RSI và ATR/ADX.
- `forecast_chart.png`: biểu đồ dự báo với vùng P10/P50/P90.
- `history_features.csv`: dữ liệu giá và chỉ báo.
- `forecast_20_sessions.csv`: bảng dự báo các phiên tới.
- `model_metrics.json`: kết quả kiểm thử mô hình.
- `xgboost_model.json`: mô hình XGBoost đã huấn luyện trên toàn bộ dữ liệu có nhãn.
- `latest_probabilities.json`: xác suất mới nhất từ XGBoost và logistic baseline.
- `latest_levels.json`: các mức giá và chỉ báo mới nhất.
- `technical_assessment.json`: bias và các tín hiệu kỹ thuật.
- `risk_plan.json`: stop, target, reward/risk và position sizing tham khảo.
- `fundamental_summary.json`: tóm tắt phân tích cơ bản nếu lấy được từ `vnstock`.
- `company_overview.csv`, `financial_ratios.csv`, `income_statement.csv`: dữ liệu cơ bản thô nếu nguồn hỗ trợ.
- `model_test_predictions.csv`: dự đoán trên tập kiểm thử.
- `backtest_oos.csv`: vị thế, số cổ phiếu, chi phí, P&L, equity và drawdown OOS theo từng phiên.

Đồng thời, kết quả được lưu vào PostgreSQL:

- `daily_runs`: tóm tắt mỗi lần chạy.
- `history_features`: dữ liệu giá và chỉ báo.
- `forecasts`: bảng dự báo.
- `model_test_predictions`: dự đoán trên tập kiểm thử.
- `model_metrics`: điểm đánh giá mô hình.
- `fundamental_metrics`: các chỉ số cơ bản đã tóm tắt.
- `panel_runs`: metadata mỗi lần chạy panel.
- `panel_predictions`: dự đoán OOS theo ngày, horizon và mã.
- `panel_latest_rankings`: ranking mới nhất theo horizon.
- `panel_metrics`: Rank IC, backtest top-k, regime và fold metadata.

Dashboard hiển thị P/E, P/B, ROE, ROA, Market Cap, Revenue Growth và Profit Growth. Hai chỉ số tăng trưởng được tính YoY từ quý mới nhất so với cùng quý năm trước.

Ví dụ truy vấn:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db -f sql_examples_postgres.sql
```

## Chỉnh cấu hình

Mở `config.json`.

Những mục thường dùng:

```json
{
  "source": "VCI",
  "forecast_sessions": 20,
  "xgboost": {
    "num_boost_round": 400,
    "learning_rate": 0.03,
    "max_depth": 4
  },
  "risk_per_trade_pct": 0.01,
  "risk_capital_vnd": 100000000,
  "atr_stop_multiplier": 1.5,
  "daily_run_time": "15:30"
}
```

Giải thích:

- `source`: nguồn dữ liệu của vnstock, mặc định là `VCI`.
- `forecast_sessions`: số phiên muốn dự báo.
- `xgboost`: tham số boosting, regularization và early stopping của mô hình chính.
- `risk_per_trade_pct`: tỷ lệ vốn chấp nhận rủi ro cho mỗi lệnh tham khảo.
- `risk_capital_vnd`: vốn tham chiếu để tính position sizing.
- `atr_stop_multiplier`: số ATR dùng để đặt stop tham chiếu.
- `daily_run_time`: giờ chạy tự động mỗi ngày.

`symbol` trong config đang để trống để tránh hard-code. Bạn nên truyền mã qua lệnh chạy.

## Cài thư viện nếu máy báo lỗi thiếu package

```bash
./setup_env.sh
```

Chạy bộ kiểm thử:

```bash
.venv/bin/python -m pytest -q
```

## Lưu ý

Đây là công cụ học tập và lập kịch bản, không phải khuyến nghị mua/bán.
Dự báo ngắn hạn có sai số lớn, nên luôn cần quản trị rủi ro.
