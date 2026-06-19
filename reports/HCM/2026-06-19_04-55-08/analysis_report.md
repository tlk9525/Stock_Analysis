# Bao cao ngay 2026-06-19 - HCM

## Tong quan

- Du lieu: 2009-05-19 -> 2026-06-18, 4,266 phien.
- Gia dong cua: 28.45 nghin VND/cp.
- Bias ky thuat: Tich cuc (score 5).
- XGBoost prob phien ke tiep tang: 47.7%.

## Phan tich ky thuat

- SMA20 27.54; SMA60 26.56; RSI14 58.6.
- MACD 0.115; signal 0.098; histogram 0.016.
- ATR14 0.88; ATR% 3.1%; ADX14 14.7.
- Trend: Tich cuc - Gia nam tren SMA20 va SMA60.
- MACD: Tich cuc - MACD tren signal, histogram duong.
- RSI14: Tich cuc - RSI 58.6.
- Bollinger: Gan bien tren - Gia sat/vuot bien tren.
- ADX: Di ngang - ADX 14.7.
- Thanh khoan: Binh thuong - 1.47 lan trung binh.
- Stochastic: Cuc tri - %K 84.8, %D 75.7.

## Phan tich co ban

- Doanh nghiep: Chứng khoán HSC.
- Nganh: Financial Services.
- Ky ratio moi nhat: 2026-Q1.
- P/E: 19.88.
- P/B: 2.06.
- P/S: 5.30.
- ROE: 10.0%.
- ROA: 3.0%.
- Gross margin: 37.2%.
- Net margin: 22.2%.
- Debt/Equity: 1.81.
- Current ratio: 1.55.
- NPL: 0.0%.
- P/E 19.88: can so sanh them voi doanh nghiep cung nganh.
- P/B 2.06: nen doc cung ROE va dac thu nganh.
- ROA 3.0%: kha tot, dac biet voi nhom ngan hang.
- Current ratio 1.55: thanh khoan ngan han kha.

## Mo hinh XGBoost

- Test: 2023-02-01 -> 2026-06-17.
- XGBoost balanced accuracy: 0.530; AUC: 0.549; log-loss: 0.690.
- Logistic baseline balanced accuracy: 0.529; AUC: 0.523.
- Majority baseline balanced accuracy: 0.500.
- Best boosting iteration: 68.
- Feature importance: rsi_14=8.11; adx_14=7.54; return_5d=7.14; volatility_20d=7.05; range_pct=6.86; macd=6.71.

## Quan tri rui ro

- Von tham chieu 100,000,000 VND; risk/lenh 1.0%.
- Stop 27.14; target 1 28.63; target 2 32.70.
- Reward/risk 0.14; position 761 cp.

## Du bao 20 phien

- P50 cuoi ky 28.63 (0.64%).
- P10/P90 cuoi ky 25.08 / 32.70.

## Khung hanh dong tham khao

- Xu huong ngan han thuan: gia tren SMA20 va SMA60.
- Bias ky thuat: Tich cuc.
- XGBoost uoc tinh xac suat phien ke tiep tang: 47.7%.
- Logistic baseline: 48.7%.
- Monte Carlo uoc tinh xac suat ket thuc tren gia hien tai: 52.4%.
- Stop tham chieu 27.14, target 1 28.63, R/R 0.14.

Luu y: bao cao dung de hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
