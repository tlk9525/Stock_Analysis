# Bao cao ngay 2026-06-19 - MBB

## Tong quan

- Du lieu: 2011-11-01 -> 2026-06-19, 3,651 phien.
- Gia dong cua: 25.15 nghin VND/cp.
- Bias ky thuat: Trung tinh (score -1).
- XGBoost prob phien ke tiep tang: 50.0%.

## Phan tich ky thuat

- SMA20 25.00; SMA60 25.67; RSI14 49.4.
- MACD -0.109; signal -0.194; histogram 0.085.
- ATR14 0.34; ATR% 1.3%; ADX14 18.3.
- Trend: Can than - Gia nam duoi SMA60.
- MACD: Tich cuc - MACD tren signal, histogram duong.
- RSI14: Trung tinh - RSI 49.4.
- Bollinger: On dinh - Gia nam trong dai Bollinger.
- ADX: Di ngang - ADX 18.3.
- Thanh khoan: Thap - 0.17 lan trung binh.
- Stochastic: Yeu lai - %K nam duoi %D.

## Phan tich co ban

- Doanh nghiep: MBBank.
- Nganh: Banks.
- Ky ratio moi nhat: 2026-Q1.
- P/E: 7.34.
- P/B: 1.42.
- ROE: 20.1%.
- ROA: 1.9%.
- Market cap: 203,388.7 ty.
- Revenue Growth: 13.8%.
- Profit Growth: 14.4%.
- P/E 7.34: dinh gia tuong doi thap neu loi nhuan ben vung.
- P/B 1.42: nen doc cung ROE va dac thu nganh.
- ROE 20.1%: hieu qua von chu so huu tot.
- Debt/Equity 9.76: don bay cao, can doc theo nganh.
- NPL 1.4%: dang o muc kiem soat.
- Revenue Growth 13.8% YoY.
- Profit Growth 14.4% YoY.

## Mo hinh XGBoost

- Test: 2023-07-28 -> 2026-06-18.
- XGBoost balanced accuracy: 0.512; AUC: 0.531; log-loss: 0.693.
- Logistic baseline balanced accuracy: 0.501; AUC: 0.510.
- Majority baseline balanced accuracy: 0.500.
- Best boosting iteration: 0.
- Feature importance: volatility_20d=30.16; macd=11.83; return_1d=9.26; macd_hist=9.01; volume_z_20=7.25; stoch_k_14=5.99.

## Quan tri rui ro

- Von tham chieu 100,000,000 VND; risk/lenh 1.0%.
- Stop 24.65; target 1 25.29; target 2 28.22.
- Reward/risk 0.27; position 1,989 cp.

## Du bao 20 phien

- P50 cuoi ky 25.29 (0.54%).
- P10/P90 cuoi ky 22.67 / 28.22.

## Khung hanh dong tham khao

- Xu huong yeu: gia duoi SMA60, uu tien quan tri rui ro.
- Bias ky thuat: Trung tinh.
- XGBoost uoc tinh xac suat phien ke tiep tang: 50.0%.
- Logistic baseline: 38.9%.
- Monte Carlo uoc tinh xac suat ket thuc tren gia hien tai: 52.4%.
- Stop tham chieu 24.65, target 1 25.29, R/R 0.27.

Luu y: bao cao dung de hoc tap va lap kich ban, khong phai khuyen nghi mua/ban.
