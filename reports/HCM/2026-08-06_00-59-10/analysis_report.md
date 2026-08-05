# Báo cáo ngày 2026-08-06 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-05, 4,296 phiên.
- Giá đóng cửa: 25.55 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 46.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.97; SMA60 24.35; RSI14 56.9.
- MACD 0.326; đường tín hiệu 0.354; biểu đồ cột -0.028.
- ATR14 0.89; ATR% 3.5%; ADX14 12.7.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Tích cực - RSI 56.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.7.
- Thanh khoản: Đột biến - 1.53 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.01.
- P/B: 1.95.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 33,883.6 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.01: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.95: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.557; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.564.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.74; macd_pct=11.54; return_1d=11.31; close_vs_sma20=11.30; relative_strength_20d=11.06; beta_60d=10.96.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.22; mục tiêu 1 29.14; mục tiêu 2 29.14.
- Tỷ lệ lợi nhuận/rủi ro 2.38; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.30 (-0.97%).
- P10/P90 cuối kỳ 22.24 / 29.14.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5573059551689529, AUC logistic=0.5640849782535965.
- Điều kiện phát hành tín hiệu: Probability 46.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.33832279031544066.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 46.5%.
- Mô hình Logistic đối chứng: 40.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.9%.
- Mức dừng lỗ tham chiếu 24.22, mục tiêu 1 29.14, tỷ lệ lợi nhuận/rủi ro 2.38.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
