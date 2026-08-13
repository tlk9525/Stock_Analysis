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

Script này sẽ tạo `.venv` và cài các thư viện cốt lõi:

- `vnstock`
- `pandas`
- `numpy`
- `matplotlib`
- `psycopg[binary]`
- `xgboost`
- `pytest`

Nếu muốn style biểu đồ publication-ready thì cài thêm `cnsplots`:

```bash
.venv/bin/python -m pip install cnsplots
```

Trên macOS, nếu XGBoost báo thiếu `libomp.dylib`:

```bash
brew install libomp
```

## Cấu trúc mã nguồn

```text
src/
├── data/
│   ├── fetch.py
│   ├── news.py
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
- Khi `market_features.enabled=true`, pipeline ghép `VNINDEX` theo ngày và thêm return thị trường, excess return, relative strength, beta và correlation; mọi feature chỉ dùng dữ liệu đến `close[t]`.
- Expanding walk-forward nhiều fold theo thứ tự `train → gap → validation → gap → test`.
- Early stopping chỉ dùng validation; metrics cuối chỉ lấy các block OOS.
- Backtest tính commission, slippage, thuế bán, lô 100 cổ phiếu, vốn và giới hạn thanh khoản.
- Publish guard chỉ cho trạng thái `ACTIONABLE` khi chất lượng mô hình, xác suất, kỹ thuật, reward/risk, độ mới dữ liệu và lợi nhuận OOS sau chi phí đều đạt.
- Nếu chưa có lợi thế ròng, hệ thống trả `NO_EDGE` và ẩn position sizing.
- Monte Carlo dùng moving-block bootstrap để giữ cụm biến động và đuôi dày tốt hơn giả định phân phối chuẩn.

Các artifact kiểm toán bổ sung gồm `data_quality_report.json`, `signal_decision.json`, `resolved_config.json` và `run_metadata.json`.

### Chiến lược swing 5 phiên và ràng buộc T+2

Luồng một mã còn chạy thêm một strategy research riêng, mặc định bật trong
`swing_strategy` của `config.json`. Khi bật, đây là **contract duy nhất** dùng
để phát hành tín hiệu; classifier phiên-kế-tiếp và sensitivity của nó chỉ còn
là diagnostic/legacy. Strategy học **excess return 5 phiên** theo contract:

```text
signal sau close[t]
entry = open[t+1]
exit target = close[t+5]
target = stock return - VNINDEX return trong cùng cửa sổ
```

Backtest dùng trạng thái `CASH → LONG → CASH`, không biến mỗi signal thành một
round-trip: lệnh mua tại `open[t+1]` được đóng đúng tại `close[t+5]`. T+2 là ràng
buộc tối thiểu đã được thỏa bởi horizon 5D, không phải một rule kéo dài vị thế
theo score. Margin vào lệnh được chọn trong validation của từng fold; holdout
cuối được khóa, chỉ dùng để đánh giá. Publish gate yêu cầu development/frozen
đủ số trade, correlation dự báo-return dương, net và Sharpe dương sau phí, và
không âm ở stress chi phí 1.5×.

Các artifact bổ sung của mỗi run:

```text
swing_model_metrics.json
xgboost_swing_5d.json
swing_development_oos.csv
swing_development_backtest.csv
swing_development_trades.csv
swing_frozen_holdout.csv
swing_frozen_backtest.csv
swing_frozen_trades.csv
```

Nếu strategy chưa qua toàn bộ gate, `signal_decision.json` vẫn giữ `NO_EDGE` và
dashboard trả `INSUFFICIENT_EDGE` khi sample/ranking chưa đủ, thay vì diễn giải
0 trade là lợi nhuận 0%. Không dùng bảng sensitivity/top-N của classifier cũ để
chọn rule swing, theo dõi ngưỡng live, hoặc suy ra “lệnh tốt nhất”.

### Báo cáo tài chính và tin tức doanh nghiệp

Mỗi lần chạy một mã, hệ thống lấy dữ liệu từ `vnstock` và tạo hai lớp phân tích bổ sung:

- **BCTC:** tỷ số, báo cáo kết quả kinh doanh, bảng cân đối kế toán và lưu chuyển tiền tệ. Dashboard có thêm CFO, free cash flow, CFO/LNST, nợ vay ròng và khả năng trả lãi khi nguồn hỗ trợ.
- **Tin tức:** `Company.news()` được chuẩn hóa thành tiêu đề, thời gian công bố, nguồn, sự kiện và sentiment keyword-based có thể audit.
- Raw snapshot được lưu tại `reports/SYMBOL/TIMESTAMP/raw/financial_statements/` và `raw/news/articles.csv` để đối chiếu với báo cáo.

Hai nhóm này hiện mặc định là `snapshot_only`/`research_only`: **chưa phải feature của XGBoost hay panel model**. BCTC từ provider chưa có lịch sử `published_at` chính thức nên không được backfill vào lịch sử giá; bài tin thiếu `published_at` cũng bị loại khỏi feature point-in-time. Điều này tránh dùng dữ liệu tương lai khi backtest.

Muốn tắt lấy tin để chạy nhanh hoặc khi nguồn tạm lỗi, đặt trong `config.json`:

```json
{
  "news": { "enabled": false }
}
```

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

### Train panel với sentiment tin tức

Mặc định panel vẫn dùng feature giá/kỹ thuật/benchmark để giữ baseline sạch. Khi đã có file tin lịch sử có timestamp công bố thật, có thể bật thêm feature tin tức point-in-time:

```bash
./run_panel.sh \
  --symbols FPT,VCB,MBB,TCB,HPG,VNM,MWG,SSI,HCM,VIC,VHM,GAS \
  --benchmark VNINDEX \
  --horizons 5,20 \
  --top-k 3 \
  --news-articles-csv data/news_history.csv \
  --use-news \
  --no-postgres
```

CSV tin tối thiểu cần các cột:

```text
symbol,available_at,sentiment_score,sentiment_label,event_type
```

Các cột khuyến nghị để audit/deduplicate tốt hơn:

```text
source_name,title,source_url
```

Quy tắc chống leakage: feature ngày `t` chỉ dùng tin có `available_at` không muộn hơn 15:00 giờ Việt Nam của ngày `t`; tin ra sau giờ đóng cửa sẽ chỉ đi vào feature của ngày giao dịch kế tiếp. Output có thêm `news_model_summary.json` để ghi lại cột feature tin đã bật, file nguồn và lookback.

Để biết tin tức có thật sự giúp model hay không, chạy hai lần:

```bash
./run_panel.sh --no-postgres
./run_panel.sh --news-articles-csv data/news_history.csv --use-news --no-postgres
```

Sau đó so sánh `metrics_5d.json`, `metrics_20d.json`, Rank IC, top-k return sau chi phí và publish guard giữa hai report trong `reports/PANEL/`.

### Train riêng từng mã với tin tức

Nếu muốn mỗi mã có một model riêng, trước hết gom tin tích lũy vào một CSV chung:

```bash
stockrun collect-news \
  --symbols VCB,MBB,TCB,ACB,BID,CTG,STB \
  --output data/news_articles.csv \
  --hours 720 \
  --limit 20 \
  --read-limit 10
```

Sau đó train riêng từng mã:

```bash
stockrun train-symbol-news MBB \
  --news-articles-csv data/news_articles.csv \
  --lookback-days 5
```

Output nằm trong `reports/SYMBOL/YYYY-MM-DD_HH-MM-SS_news_model/`, gồm `model_metrics.json`, `latest_probabilities.json`, `feature_importance.json`, `history_features_with_news.csv` và `symbol_news_model_summary.json`.

Lưu ý: lệnh này dùng target một phiên kế tiếp (`target_next_up`) của pipeline một mã hiện tại. Nếu CSV tin chỉ dựng từ snapshot live gần đây, kết quả chỉ dùng để smoke test/research; muốn đánh giá nghiêm túc cần chạy `collect-news` đều đặn hoặc nhập nguồn tin lịch sử có `available_at` nhiều tháng/năm.

Lãi suất và dữ liệu vĩ mô chưa được trộn vào target/model của hai giai đoạn này; nên triển khai ở giai đoạn tiếp theo với timestamp công bố point-in-time để tránh look-ahead bias.

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
- `company_overview.csv`, `financial_ratios.csv`, `income_statement.csv`, `balance_sheet.csv`, `cash_flow.csv`: dữ liệu cơ bản thô nếu nguồn hỗ trợ.
- `news_articles.csv`, `news_features_latest.csv`, `news_summary.json`: tin tức, feature as-of mới nhất và metadata phân tích tin.
- `raw/financial_statements/`, `raw/news/articles.csv`: snapshot dữ liệu gốc, không ghi đè giữa các lần chạy.
- `model_test_predictions.csv`: dự đoán trên tập kiểm thử.
- `backtest_oos.csv`: vị thế, số cổ phiếu, chi phí, P&L, equity và drawdown OOS theo từng phiên.

Đồng thời, kết quả được lưu vào PostgreSQL:

- `daily_runs`: tóm tắt mỗi lần chạy.
- `history_features`: dữ liệu giá và chỉ báo.
- `forecasts`: bảng dự báo.
- `model_test_predictions`: dự đoán trên tập kiểm thử.
- `model_metrics`: điểm đánh giá mô hình.
- `fundamental_metrics`: các chỉ số cơ bản đã tóm tắt.
- `financial_statement_lines`: từng dòng BCTC theo kỳ, nguồn và thời điểm lấy; `available_at` để trống khi chưa có giờ công bố đáng tin cậy.
- `news_articles`, `news_entities`: bài tin đã chuẩn hóa và bằng chứng gán mã cổ phiếu.
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

## FinAI CLI: portfolio và Ollama

Lớp CLI mới bọc lại pipeline ML hiện có; không train một model thứ hai. Cài
dependencies rồi xem các lệnh:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.finai_cli --help
.venv/bin/python -m src.finai_cli doctor
```

Phân tích một mã hoặc chạy panel nhiều mã:

```bash
.venv/bin/python -m src.finai_cli analyze FPT
.venv/bin/python -m src.finai_cli rank --symbols FPT,VCB,HPG,VNM,MWG --horizons 5,20
```

Để gọi ngắn gọn từ bất kỳ thư mục nào trên macOS/Linux, cài launcher một lần:

```bash
ln -sfn "$(pwd)/bin/stockrun" "$HOME/.local/bin/stockrun"
```

Sau đó, một lệnh sẽ lần lượt tạo ML report, lấy tin web 7 ngày gần nhất và
để Ollama đọc cả report lẫn tin vừa lưu. Terminal chỉ in đường dẫn báo cáo cuối;
chi tiết chạy được lưu trong `stockrun.log` cùng thư mục report:

```bash
stockrun MBB
stockrun HCM
```

Sau khi có live research hoặc AI analysis, `dashboard.html` trong report được
bổ sung bảng headline có link nguồn, bảng News Reader với trích đoạn có thể mở,
phần AI đã khóa theo artifact và ba mục BCTC mở rộng cho 4 kỳ gần nhất. Mỗi mục
BCTC có link tới CSV đầy đủ; tin và trích đoạn vẫn chỉ phục vụ research, không
được hiểu là tín hiệu mua/bán.

`stockrun FPT --no-postgres` và `stockrun FPT --forecast-sessions 20` vẫn chuyển
đúng option vào pipeline. Mặc định lấy tối đa 10 headline trong 168 giờ, đọc tối
đa 5 bài gốc rồi dùng Ollama model `qwen3:1.7b`; có thể đổi bằng
`stockrun FPT --hours 72 --limit 15 --read-limit 8 --model qwen3:4b`.
Các tác vụ riêng lẻ vẫn giữ cú pháp rõ nghĩa, ví dụ `stockrun doctor`,
`stockrun analyze FPT`, `stockrun research FPT` hoặc `stockrun ai analyze FPT`.

Portfolio dùng PostgreSQL `stock_db` theo transaction ledger; giá trị vị thế
được tính lại từ lệnh mua/bán, không lưu `current_value` có thể stale:

```bash
.venv/bin/python -m src.finai_cli portfolio create "Dai han"
.venv/bin/python -m src.finai_cli portfolio buy "Dai han" FPT --qty 100 --price 70000 --fee 10
.venv/bin/python -m src.finai_cli portfolio summary "Dai han"
```

AI chỉ đọc các artifact đã sinh ra (`signal_decision.json`, technical,
fundamental và news summaries), không tự tạo dữ liệu giá. Cài Ollama native,
khởi động service và tải model trước khi dùng:

```bash
ollama pull qwen3:1.7b
.venv/bin/python -m src.finai_cli ai analyze FPT
```

Kết quả AI bị khóa theo `decision_status` của report gốc. `NO_EDGE` vẫn là
`NO_EDGE`, không thể bị prompt biến thành khuyến nghị mua/bán. Sau khi Ollama
phản hồi, các trường hiển thị cho người dùng gồm trạng thái, bằng chứng, nguồn,
góc nhìn kỹ thuật/cơ bản, rủi ro và disclaimer đều được dựng lại từ artifact đã
lưu; câu khẳng định hoặc rủi ro chỉ do model tự sinh sẽ bị loại bỏ.
Model mặc định 1.7B được chọn cho máy 8 GB RAM; model được unload sau mỗi câu
trả lời để tránh chiếm bộ nhớ khi chạy các tác vụ ML khác.

### Live web research và News Reader có nguồn

Lệnh này lấy headline, URL, publisher và thời gian công bố từ Google News RSS,
lưu snapshot `live_research.json` vào report gần nhất của mã. Mặc định News
Reader sẽ giải mã URL RSS, mở tối đa 5 bài gốc, trích đoạn HTML giới hạn, lọc
bài quảng cáo/trùng/không đọc được và lưu `news_reader.json`. Mỗi trích đoạn
giữ publisher, URL gốc/final URL, thời điểm và nhóm research: kết quả kinh
doanh, cổ tức/hành động doanh nghiệp, vĩ mô, ngành, rủi ro.
Mỗi nhóm có một checklist “tác động cần kiểm chứng” gắn với nguồn, thay vì tự
suy luận tăng/giảm giá từ bài báo.

```bash
.venv/bin/python -m src.finai_cli research FPT --hours 72 --limit 10
.venv/bin/python -m src.finai_cli ai analyze FPT
```

Tùy chỉnh số bài gốc cần đọc hoặc chỉ lấy headline:

```bash
.venv/bin/python -m src.finai_cli research MBB --hours 168 --limit 15 --read-limit 8
.venv/bin/python -m src.finai_cli research HCM --no-read
```

Ollama chỉ được đọc các snapshot đã lưu, không tự do duyệt web hay thực thi chỉ
dẫn xuất hiện trong tin. News Reader không đánh nhãn sentiment hay suy luận tác
động giá; AI phải dẫn đúng URL có trong artifact và giữ nguyên `NO_EDGE`.
Live research chỉ dùng để research/report. Không đưa headline, trích đoạn hoặc
BCTC snapshot vào train/backtest cho tới khi từng bản ghi có lịch sử
`available_at` đáng tin cậy.

## Lưu ý

Đây là công cụ học tập và lập kịch bản, không phải khuyến nghị mua/bán.
Dự báo ngắn hạn có sai số lớn, nên luôn cần quản trị rủi ro.
