# Báo cáo ngày 2026-08-06 - MWG

## Tổng quan

- Dữ liệu: 2014-07-14 -> 2026-08-06, 3,013 phiên.
- Giá đóng cửa: 71.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 71.42; SMA60 75.23; RSI14 47.2.
- MACD -1.398; đường tín hiệu -1.881; biểu đồ cột 0.482.
- ATR14 2.57; ATR% 3.6%; ADX14 32.3.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 32.3, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.02 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Thế giới di động.
- Ngành: Retail.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 10.83.
- P/B: 2.98.
- ROE: 29.2%.
- ROA: 11.2%.
- Market cap: 106,550.3 tỷ.
- Revenue Growth: 29.6%.
- Profit Growth: 100.4%.
- P/E 10.83: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.98: nên đọc cùng ROE và đặc thù ngành.
- ROE 29.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 11.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.44: thanh khoản ngắn hạn khá.
- Revenue Growth 29.6% YoY.
- Profit Growth 100.4% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-07-26 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.509; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.529; AUC 0.520.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -6.6%; Sharpe -0.19; mức sụt giảm tối đa -14.2%.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=9.59; stoch_k_14=8.90; volume_ratio_20=8.44; beta_60d=8.42; macd_hist_pct=8.33; day_of_week=8.14.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 67.34; mục tiêu 1 79.42; mục tiêu 2 79.42.
- Tỷ lệ lợi nhuận/rủi ro 1.87; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.48 (-1.01%).
- P10/P90 cuối kỳ 62.53 / 79.42.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.509 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5094815844531503, AUC logistic=0.5199039555162391.
- Điều kiện phát hành tín hiệu: Probability 48.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.19291747693017397.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Mô hình Logistic đối chứng: 47.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.7%.
- Mức dừng lỗ tham chiếu 67.34, mục tiêu 1 79.42, tỷ lệ lợi nhuận/rủi ro 1.87.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
