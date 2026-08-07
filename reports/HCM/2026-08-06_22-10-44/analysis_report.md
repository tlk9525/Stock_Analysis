# Báo cáo ngày 2026-08-06 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-06, 4,297 phiên.
- Giá đóng cửa: 25.45 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 25.03; SMA60 24.37; RSI14 55.8.
- MACD 0.320; đường tín hiệu 0.347; biểu đồ cột -0.027.
- ATR14 0.87; ATR% 3.4%; ADX14 12.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Tích cực - RSI 55.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.5.
- Thanh khoản: Thấp - 0.48 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.36.
- P/B: 1.99.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 34,491.1 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.36: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.99: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.557; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.520; AUC 0.565.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.53; return_1d=11.39; macd_pct=11.10; close_vs_sma20=10.94; beta_60d=10.86; corr_60d=10.85.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.15; mục tiêu 1 28.96; mục tiêu 2 28.96.
- Tỷ lệ lợi nhuận/rủi ro 2.36; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.16 (-1.13%).
- P10/P90 cuối kỳ 22.13 / 28.96.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5567763734200976, AUC logistic=0.5648521253076377.
- Điều kiện phát hành tín hiệu: Probability 47.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3380805896795832.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.1%.
- Mô hình Logistic đối chứng: 43.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.7%.
- Mức dừng lỗ tham chiếu 24.15, mục tiêu 1 28.96, tỷ lệ lợi nhuận/rủi ro 2.36.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
