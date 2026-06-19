# VN Stock Daily Analysis

Folder nay dung de chay phan tich va du bao so bo cho bat ky ma co phieu Viet Nam nao ma `vnstock` ho tro.

Ban khong can sua code khi muon doi ma. Chi can truyen ma vao lenh chay.

Project nay dung PostgreSQL 18 database `stock_db` de luu ket qua phan tich.

Model chinh la XGBoost. Logistic Regression va majority class duoc giu lam baseline de so sanh.

## Setup moi truong Python

Chay 1 lan:

```bash
./setup_env.sh
```

Script nay se tao `.venv` va cai cac thu vien:

- `vnstock`
- `pandas`
- `numpy`
- `matplotlib`
- `psycopg[binary]`
- `xgboost`

Tren macOS, neu XGBoost bao thieu `libomp.dylib`:

```bash
brew install libomp
```

## Cau truc source

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
├── forecast/
│   └── monte_carlo.py
├── risk/
│   └── management.py
├── reports/
│   └── dashboard.py
├── database/
│   └── postgres.py
├── config.py
├── utils.py
└── main.py
```

`vn_stock_daily_analysis.py` chi la entrypoint tuong thich nguoc. Logic chinh nam trong `src/`.

## PostgreSQL 18 / stock_db

Neu `psql` chua co trong PATH, dung duong dan cua Postgres.app:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db
```

Tao schema bang tay neu can:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db -f postgres_schema.sql
```

Mac dinh app ket noi bang:

```text
postgresql:///stock_db
```

Co the override bang bien moi truong:

```bash
export DATABASE_URL="postgresql:///stock_db"
```

Hoac truyen truc tiep:

```bash
./run_now.sh HCM --database-url "postgresql:///stock_db"
```

## Chay ngay voi mot ma

Vi du chay ma HCM:

```bash
./run_now.sh HCM
```

Vi du chay ma FPT:

```bash
./run_now.sh FPT
```

Vi du chay ma VCB:

```bash
./run_now.sh VCB
```

Hoac chay bang Python:

```bash
.venv/bin/python -m src.main --once --symbol HCM
```

Neu ban chay `./run_now.sh` ma khong nhap ma, chuong trinh se hoi ma trong terminal.

## Chay tu dong moi ngay

Chay moi ngay cho HCM:

```bash
./run_daily_loop.sh HCM
```

Chay moi ngay cho FPT:

```bash
./run_daily_loop.sh FPT
```

Mac dinh gio chay nam trong `config.json`, hien la `15:30` theo mui gio Viet Nam.

Ban cung co the doi gio bang tham so:

```bash
./run_daily_loop.sh HCM --run-time 20:00
```

## File output nam o dau?

Moi lan chay, chuong trinh tao folder rieng theo ma:

```text
reports/SYMBOL/YYYY-MM-DD_HH-MM-SS/
```

Vi du:

```text
reports/HCM/2026-06-06_15-30-00/
reports/FPT/2026-06-06_15-30-00/
```

Ben trong co:

- `analysis_report.md`: bao cao tom tat va khung kich ban.
- `dashboard.html`: dashboard tong hop dep hon, mo truc tiep bang trinh duyet.
- `history_chart.png`: bieu do gia, SMA, volume, drawdown.
- `technical_chart.png`: bieu do Bollinger Bands, MACD, RSI, ATR/ADX.
- `forecast_chart.png`: bieu do du bao voi vung P10/P50/P90.
- `history_features.csv`: du lieu gia + chi bao.
- `forecast_20_sessions.csv`: bang du bao cac phien toi.
- `model_metrics.json`: ket qua test model.
- `xgboost_model.json`: model XGBoost da train tren toan bo du lieu co nhan.
- `latest_probabilities.json`: xac suat moi nhat tu XGBoost va logistic baseline.
- `latest_levels.json`: cac muc gia/chi bao moi nhat.
- `technical_assessment.json`: bias va cac tin hieu ky thuat.
- `risk_plan.json`: stop, target, reward/risk va position sizing tham khao.
- `fundamental_summary.json`: tom tat phan tich co ban neu lay duoc tu `vnstock`.
- `company_overview.csv`, `financial_ratios.csv`, `income_statement.csv`: du lieu co ban raw neu nguon ho tro.
- `model_test_predictions.csv`: du doan tren tap test.

Dong thoi, ket qua duoc luu vao PostgreSQL:

- `daily_runs`: tom tat moi lan chay.
- `history_features`: du lieu gia + chi bao.
- `forecasts`: bang du bao.
- `model_test_predictions`: du doan tren tap test.
- `model_metrics`: diem danh gia model.
- `fundamental_metrics`: cac chi so co ban da tom tat.

Dashboard hien thi P/E, P/B, ROE, ROA, Market Cap, Revenue Growth va Profit Growth. Hai chi so tang truong duoc tinh YoY tu quy moi nhat so voi cung quy nam truoc.

Vi du query:

```bash
/Applications/Postgres.app/Contents/Versions/18/bin/psql -d stock_db -f sql_examples_postgres.sql
```

## Chinh cau hinh

Mo `config.json`.

Nhung muc hay dung:

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

Giai thich:

- `source`: nguon du lieu cua vnstock, mac dinh `VCI`.
- `forecast_sessions`: so phien muon du bao.
- `xgboost`: tham so boosting, regularization va early stopping cua model chinh.
- `risk_per_trade_pct`: % von chap nhan rui ro cho moi lenh tham khao.
- `risk_capital_vnd`: von tham chieu de tinh position sizing.
- `atr_stop_multiplier`: so ATR dung de dat stop tham chieu.
- `daily_run_time`: gio chay tu dong moi ngay.

`symbol` trong config dang de rong de tranh hard-code. Ban nen truyen ma qua lenh chay.

## Cai thu vien neu may bao loi thieu package

```bash
./setup_env.sh
```

## Luu y

Day la cong cu hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
Du bao ngan han co sai so lon, nen luon can quan tri rui ro.
