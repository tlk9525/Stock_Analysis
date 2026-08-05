# Báo cáo ngày 2026-08-06 - MSN

## Tổng quan

- Dữ liệu: 2009-11-05 -> 2026-08-05, 4,176 phiên.
- Giá đóng cửa: 67.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 66.66; SMA60 71.12; RSI14 47.1.
- MACD -0.874; đường tín hiệu -1.388; biểu đồ cột 0.514.
- ATR14 1.80; ATR% 2.7%; ADX14 40.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 40.8, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.99 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Masan.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.75.
- P/B: 2.49.
- ROE: 19.4%.
- ROA: 5.4%.
- Market cap: 99,889.6 tỷ.
- Revenue Growth: 53.5%.
- Profit Growth: 202.8%.
- P/E 14.75: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.49: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 5.4%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 0.87: thanh khoản ngắn hạn cần theo dõi.
- Revenue Growth 53.5% YoY.
- Profit Growth 202.8% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-12-25 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.498; AUC 0.495; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.512.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -15.4%; Sharpe -1.33; mức sụt giảm tối đa -18.3%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=20.60; atr_pct_14=13.36; return_kurtosis_20d=13.01; relative_strength_20d=12.84; range_pct=12.70; macd_hist_pct=12.41.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 64.50; mục tiêu 1 74.19; mục tiêu 2 74.19.
- Tỷ lệ lợi nhuận/rủi ro 2.19; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 66.97 (-0.34%).
- P10/P90 cuối kỳ 60.38 / 74.19.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.495 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.498 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4950590623662762, AUC logistic=0.5120363828156876.
- Điều kiện phát hành tín hiệu: Probability 50.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.3279471876297972.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.2%.
- Mô hình Logistic đối chứng: 53.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.2%.
- Mức dừng lỗ tham chiếu 64.50, mục tiêu 1 74.19, tỷ lệ lợi nhuận/rủi ro 2.19.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
