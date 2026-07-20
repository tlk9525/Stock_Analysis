# Bao cao ngay 2026-07-19 - HCM

## Tong quan

- Du lieu: 2009-05-19 -> 2026-07-17, 4,287 phien.
- Gia dong cua: 25.40 nghin VND/cp.
- Bias ky thuat: Tich cuc (score 7).
- XGBoost prob phien ke tiep tang: 52.3%.

## Phan tich ky thuat

- SMA20 24.02; SMA60 23.94; RSI14 62.0.
- MACD 0.177; signal 0.100; histogram 0.077.
- ATR14 0.80; ATR% 3.2%; ADX14 16.1.
- Trend: Tich cuc - Gia nam tren SMA20 va SMA60.
- MACD: Tich cuc - MACD tren signal, histogram duong.
- RSI14: Tich cuc - RSI 62.0.
- Bollinger: Gan bien tren - Gia sat/vuot bien tren.
- ADX: Di ngang - ADX 16.1.
- Thanh khoan: Dot bien - 1.63 lan trung binh.
- Stochastic: Hoi phuc - %K nam tren %D.

## Phan tich co ban

- Doanh nghiep: Chứng khoán HSC.
- Nganh: Financial Services.
- Ky ratio moi nhat: 2026-Q2.
- P/E: 18.38.
- P/B: 2.00.
- ROE: 10.0%.
- ROA: 3.0%.
- Market cap: 34,288.6 ty.
- Revenue Growth: 46.7%.
- Profit Growth: 28.2%.
- P/E 18.38: can so sanh them voi doanh nghiep cung nganh.
- P/B 2.00: nen doc cung ROE va dac thu nganh.
- ROA 3.0%: kha tot, dac biet voi nhom ngan hang.
- Current ratio 1.55: thanh khoan ngan han kha.
- Revenue Growth 46.7% YoY.
- Profit Growth 28.2% YoY.

## Mo hinh XGBoost

- Test: 2023-02-24 -> 2026-07-16.
- XGBoost balanced accuracy: 0.512; AUC: 0.526; log-loss: 0.692.
- Logistic baseline balanced accuracy: 0.533; AUC: 0.524.
- Majority baseline balanced accuracy: 0.500.
- Best boosting iteration: 10.
- Feature importance: macd=11.87; atr_pct_14=11.56; stoch_k_14=10.67; close_vs_sma60=10.61; bb_position_20=10.34; volume_z_20=10.32.

## Quan tri rui ro

- Von tham chieu 100,000,000 VND; risk/lenh 1.0%.
- Stop 24.19; target 1 25.43; target 2 29.09.
- Reward/risk 0.03; position 828 cp.

## Du bao 20 phien

- P50 cuoi ky 25.43 (0.12%).
- P10/P90 cuoi ky 22.24 / 29.09.

## Khung hanh dong tham khao

- Xu huong ngan han thuan: gia tren SMA20 va SMA60.
- Bias ky thuat: Tich cuc.
- XGBoost uoc tinh xac suat phien ke tiep tang: 52.3%.
- Logistic baseline: 53.7%.
- Monte Carlo uoc tinh xac suat ket thuc tren gia hien tai: 50.5%.
- Stop tham chieu 24.19, target 1 25.43, R/R 0.03.

Luu y: bao cao dung de hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
