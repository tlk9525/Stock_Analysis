# VN Stock Daily Analysis

Folder nay dung de chay phan tich va du bao so bo cho bat ky ma co phieu Viet Nam nao ma `vnstock` ho tro.

Ban khong can sua code khi muon doi ma. Chi can truyen ma vao lenh chay.

Project nay dung PostgreSQL 18 database `stock_db` de luu ket qua phan tich.

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
.venv/bin/python vn_stock_daily_analysis.py --once --symbol HCM
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
- `history_chart.png`: bieu do gia, SMA, volume, drawdown.
- `forecast_chart.png`: bieu do du bao voi vung P10/P50/P90.
- `history_features.csv`: du lieu gia + chi bao.
- `forecast_20_sessions.csv`: bang du bao cac phien toi.
- `model_metrics.json`: ket qua test model.
- `latest_levels.json`: cac muc gia/chi bao moi nhat.
- `model_test_predictions.csv`: du doan tren tap test.

Dong thoi, ket qua duoc luu vao PostgreSQL:

- `daily_runs`: tom tat moi lan chay.
- `history_features`: du lieu gia + chi bao.
- `forecasts`: bang du bao.
- `model_test_predictions`: du doan tren tap test.
- `model_metrics`: diem danh gia model.

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
  "daily_run_time": "15:30"
}
```

Giai thich:

- `source`: nguon du lieu cua vnstock, mac dinh `VCI`.
- `forecast_sessions`: so phien muon du bao.
- `daily_run_time`: gio chay tu dong moi ngay.

`symbol` trong config dang de rong de tranh hard-code. Ban nen truyen ma qua lenh chay.

## Cai thu vien neu may bao loi thieu package

```bash
./setup_env.sh
```

## Luu y

Day la cong cu hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
Du bao ngan han co sai so lon, nen luon can quan tri rui ro.
