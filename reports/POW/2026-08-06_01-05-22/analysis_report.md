# Báo cáo ngày 2026-08-06 - POW

## Tổng quan

- Dữ liệu: 2018-03-06 -> 2026-08-05, 2,095 phiên.
- Giá đóng cửa: 13.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 13.70; SMA60 13.95; RSI14 49.6.
- MACD -0.107; đường tín hiệu -0.150; biểu đồ cột 0.043.
- ATR14 0.41; ATR% 2.9%; ADX14 31.7.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.7, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.14 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Điện lực Dầu khí Việt Nam.
- Ngành: Utilities.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.62.
- P/B: 1.03.
- ROE: 16.5%.
- ROA: 6.5%.
- Market cap: 42,643.1 tỷ.
- Revenue Growth: 116.1%.
- Profit Growth: 484.1%.
- P/E 6.62: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.03: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 6.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.37: thanh khoản ngắn hạn khá.
- Revenue Growth 116.1% YoY.
- Profit Growth 484.1% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-12-21 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.586; log-loss 0.672.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.541; AUC 0.551.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 104.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -35.8%; Sharpe -1.42; mức sụt giảm tối đa -43.2%.
- Mức độ quan trọng của đặc trưng: return_1d=11.21; stoch_k_14=9.29; atr_pct_14=9.17; return_10d=8.90; close_vs_sma20=8.89; macd_hist_pct=8.82.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 13.19; mục tiêu 1 15.54; mục tiêu 2 15.54.
- Tỷ lệ lợi nhuận/rủi ro 2.46; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.74 (-0.43%).
- P10/P90 cuối kỳ 12.12 / 15.54.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.419202465112688.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 52.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.2%.
- Mức dừng lỗ tham chiếu 13.19, mục tiêu 1 15.54, tỷ lệ lợi nhuận/rủi ro 2.46.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
