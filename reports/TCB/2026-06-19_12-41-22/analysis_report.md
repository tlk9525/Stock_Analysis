# Bao cao ngay 2026-06-19 - TCB

## Tong quan

- Du lieu: 2018-06-04 -> 2026-06-19, 2,010 phien.
- Gia dong cua: 31.05 nghin VND/cp.
- Bias ky thuat: Tieu cuc (score -5).
- XGBoost prob phien ke tiep tang: 49.7%.

## Phan tich ky thuat

- SMA20 31.77; SMA60 31.70; RSI14 41.1.
- MACD -0.301; signal -0.263; histogram -0.038.
- ATR14 0.54; ATR% 1.7%; ADX14 16.4.
- Trend: Can than - Gia nam duoi SMA60.
- MACD: Can than - MACD duoi signal, histogram am.
- RSI14: Yeu - RSI 41.1.
- Bollinger: On dinh - Gia nam trong dai Bollinger.
- ADX: Di ngang - ADX 16.4.
- Thanh khoan: Thap - 0.25 lan trung binh.
- Stochastic: Cuc tri - %K 15.6, %D 21.0.

## Phan tich co ban

- Doanh nghiep: Techcombank.
- Nganh: Banks.
- Ky ratio moi nhat: 2026-Q1.
- P/E: 8.49.
- P/B: 1.25.
- P/S: 3.99.
- ROE: 14.7%.
- ROA: 2.3%.
- Gross margin: 69.3%.
- Net margin: 46.9%.
- Debt/Equity: 5.38.
- Current ratio: 0.00.
- NPL: 1.1%.
- P/E 8.49: dinh gia tuong doi thap neu loi nhuan ben vung.
- P/B 1.25: nen doc cung ROE va dac thu nganh.
- ROA 2.3%: kha tot, dac biet voi nhom ngan hang.
- Debt/Equity 5.38: don bay cao, can doc theo nganh.
- NPL 1.1%: dang o muc kiem soat.

## Mo hinh XGBoost

- Test: 2024-11-20 -> 2026-06-18.
- XGBoost balanced accuracy: 0.533; AUC: 0.535; log-loss: 0.692.
- Logistic baseline balanced accuracy: 0.476; AUC: 0.499.
- Majority baseline balanced accuracy: 0.500.
- Best boosting iteration: 9.
- Feature importance: atr_pct_14=11.24; macd=9.14; volatility_20d=8.48; rsi_14=7.95; close_vs_sma20=7.44; return_5d=7.07.

## Quan tri rui ro

- Von tham chieu 100,000,000 VND; risk/lenh 1.0%.
- Stop 30.49; target 1 32.85; target 2 33.70.
- Reward/risk 3.23; position 1,792 cp.

## Du bao 5 phien

- P50 cuoi ky 31.02 (-0.11%).
- P10/P90 cuoi ky 29.30 / 32.85.

## Khung hanh dong tham khao

- Xu huong yeu: gia duoi SMA60, uu tien quan tri rui ro.
- Bias ky thuat: Tieu cuc.
- XGBoost uoc tinh xac suat phien ke tiep tang: 49.7%.
- Logistic baseline: 43.9%.
- Monte Carlo uoc tinh xac suat ket thuc tren gia hien tai: 49.2%.
- Stop tham chieu 30.49, target 1 32.85, R/R 3.23.

Luu y: bao cao dung de hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
