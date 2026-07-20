# Báo cáo ngày 2026-07-20 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-07-20, 2,145 phiên.
- Giá đóng cửa: 136.90 nghìn VND/cp.
- Bias kỹ thuật: Tieu cuc (điểm -7).
- Xác suất XGBoost cho phiên kế tiếp tăng: 50.7%.
- Trạng thái tín hiệu: NO_EDGE.

## Phân tích kỹ thuật

- SMA20 147.67; SMA60 146.04; RSI14 40.9.
- MACD -1.407; tín hiệu 0.143; histogram -1.550.
- ATR14 5.68; ATR% 4.1%; ADX14 17.4.
- Trend: Can than - Gia nam duoi SMA60.
- MACD: Can than - MACD duoi signal, histogram am.
- RSI14: Yeu - RSI 40.9.
- Bollinger: Gan bien duoi - Gia sat/vuot bien duoi.
- ADX: Di ngang - ADX 17.4.
- Thanh khoan: Thap - 0.67 lan trung binh.
- Stochastic: Cuc tri - %K 13.5, %D 26.1.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.91.
- P/B: 2.20.
- ROE: 27.8%.
- ROA: 8.4%.
- Market cap: 577,091.4 tỷ.
- Revenue Growth: 314.8%.
- Profit Growth: 850.3%.
- P/E 8.91: dinh gia tuong doi thap neu loi nhuan ben vung.
- P/B 2.20: nen doc cung ROE va dac thu nganh.
- ROE 27.8%: hieu qua von chu so huu tot.
- ROA 8.4%: kha tot, dac biet voi nhom ngan hang.
- Debt/Equity 2.19: don bay cao, can doc theo nganh.
- Current ratio 1.33: thanh khoan ngan han kha.
- Revenue Growth 314.8% YoY.
- Profit Growth 850.3% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-29 -> 2026-07-17.
- XGBoost balanced accuracy: 0.509; AUC: 0.510; log-loss: 0.696.
- Logistic baseline balanced accuracy: 0.530; AUC: 0.524.
- Majority baseline balanced accuracy: 0.500.
- Vòng boosting tốt nhất: 21.
- Thẩm định: expanding_walk_forward; 6 fold; khoảng cách 1 phiên.
- Backtest sau chi phí: tổng lợi nhuận 0.5%; Sharpe 0.07; drawdown tối đa -21.9%.
- Mức độ quan trọng của đặc trưng: range_pct=13.03; adx_14=8.88; atr_pct_14=8.14; volatility_20d=7.78; return_1d=7.17; close_vs_sma60=6.90.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; risk/lệnh 1.0%.
- Stop 132.16; mục tiêu 1 158.70; mục tiêu 2 168.20.
- Reward/risk 3.89; position 0 cp.

## Dự báo 20 phiên

- P50 cuối kỳ 134.55 (-1.71%).
- P10/P90 cuối kỳ 108.99 / 168.20.

## Khung hành động tham khảo

- Trạng thái tín hiệu: NO_EDGE.
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.509 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 50.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -7 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Bias kỹ thuật: Tieu cuc.
- XGBoost ước tính xác suất phiên kế tiếp tăng: 50.7%.
- Mốc so sánh Logistic: 50.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.7%.
- Stop tham chiếu 132.16, mục tiêu 1 158.70, R/R 3.89.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
