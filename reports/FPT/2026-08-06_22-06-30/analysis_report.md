# Báo cáo ngày 2026-08-06 - FPT

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,589 phiên.
- Giá đóng cửa: 70.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.30; SMA60 71.01; RSI14 57.1.
- MACD -0.192; đường tín hiệu -1.091; biểu đồ cột 0.899.
- ATR14 2.01; ATR% 2.8%; ADX14 28.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.0, +DI vượt -DI.
- Thanh khoản: Thấp - 0.57 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.98.
- P/B: 3.02.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 120,517.1 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 11.98: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.575; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.560.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.
- Mức độ quan trọng của đặc trưng: return_1d=13.98; market_return_1d=12.76; close_vs_sma20=12.34; stoch_k_14=11.53; day_of_week=11.42; return_3d=11.39.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.30; mục tiêu 1 73.30; mục tiêu 2 78.97.
- Tỷ lệ lợi nhuận/rủi ro 2.96; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.23 (-0.67%).
- P10/P90 cuối kỳ 62.88 / 78.97.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 48.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8621401459602572.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Mô hình Logistic đối chứng: 40.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.7%.
- Mức dừng lỗ tham chiếu 70.30, mục tiêu 1 73.30, tỷ lệ lợi nhuận/rủi ro 2.96.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
