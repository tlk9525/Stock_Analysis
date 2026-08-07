# Báo cáo ngày 2026-08-06 - MSN

## Tổng quan

- Dữ liệu: 2009-11-05 -> 2026-08-06, 4,177 phiên.
- Giá đóng cửa: 66.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 66.54; SMA60 70.91; RSI14 44.3.
- MACD -0.840; đường tín hiệu -1.279; biểu đồ cột 0.439.
- ATR14 1.75; ATR% 2.6%; ADX14 38.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 44.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 38.4, -DI vượt +DI.
- Thanh khoản: Thấp - 0.54 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Masan.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.49.
- P/B: 2.45.
- ROE: 19.4%.
- ROA: 5.4%.
- Market cap: 98,137.2 tỷ.
- Revenue Growth: 53.5%.
- Profit Growth: 202.8%.
- P/E 14.49: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.45: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 5.4%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 0.87: thanh khoản ngắn hạn cần theo dõi.
- Revenue Growth 53.5% YoY.
- Profit Growth 202.8% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-12-25 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.498; AUC 0.494; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.511.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -15.4%; Sharpe -1.33; mức sụt giảm tối đa -18.3%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=20.78; volume_z_20=13.79; relative_strength_20d=13.33; range_pct=12.94; atr_pct_14=12.34; close_vs_sma60=12.16.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 63.88; mục tiêu 1 73.27; mục tiêu 2 73.27.
- Tỷ lệ lợi nhuận/rủi ro 2.18; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 66.13 (-0.56%).
- P10/P90 cuối kỳ 59.81 / 73.27.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.494 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.498 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49407408877948067, AUC logistic=0.511226475025808.
- Điều kiện phát hành tín hiệu: Probability 48.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -4 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.15437910000000032, Sharpe=-1.326918136738502.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.0%.
- Mô hình Logistic đối chứng: 51.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 63.88, mục tiêu 1 73.27, tỷ lệ lợi nhuận/rủi ro 2.18.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
