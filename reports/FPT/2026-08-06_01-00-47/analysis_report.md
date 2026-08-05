# Báo cáo ngày 2026-08-06 - FPT

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,589 phiên.
- Giá đóng cửa: 70.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 46.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.36; SMA60 71.04; RSI14 56.0.
- MACD -0.440; đường tín hiệu -1.315; biểu đồ cột 0.875.
- ATR14 2.08; ATR% 3.0%; ADX14 29.3.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 29.3, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.85 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.19.
- P/B: 3.07.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 122,574.3 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.19: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.07: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.577; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.561.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.
- Mức độ quan trọng của đặc trưng: return_1d=13.96; market_return_1d=12.22; return_3d=11.95; stoch_k_14=11.90; day_of_week=11.90; close_vs_sma20=11.67.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 67.18; mục tiêu 1 78.24; mục tiêu 2 78.24.
- Tỷ lệ lợi nhuận/rủi ro 2.18; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 69.61 (-0.98%).
- P10/P90 cuối kỳ 62.55 / 78.24.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 46.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8627195023819321.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 46.5%.
- Mô hình Logistic đối chứng: 41.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.7%.
- Mức dừng lỗ tham chiếu 67.18, mục tiêu 1 78.24, tỷ lệ lợi nhuận/rủi ro 2.18.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
