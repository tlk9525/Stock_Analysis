# Báo cáo ngày 2026-08-06 - SSI

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,589 phiên.
- Giá đóng cửa: 24.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.01; SMA60 26.10; RSI14 47.4.
- MACD -0.529; đường tín hiệu -0.764; biểu đồ cột 0.235.
- ATR14 0.87; ATR% 3.6%; ADX14 34.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 34.2, -DI vượt +DI.
- Thanh khoản: Thấp - 0.64 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán SSI.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.38.
- P/B: 1.50.
- ROE: 13.4%.
- ROA: 5.0%.
- Market cap: 61,026.8 tỷ.
- Revenue Growth: 10.9%.
- Profit Growth: 27.0%.
- P/E 11.38: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.50: nên đọc cùng ROE và đặc thù ngành.
- ROA 5.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.65: thanh khoản ngắn hạn khá.
- Revenue Growth 10.9% YoY.
- Profit Growth 27.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.500; AUC 0.544; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.538; AUC 0.547.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 19.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -1.0%; Sharpe -0.03; mức sụt giảm tối đa -8.2%.
- Mức độ quan trọng của đặc trưng: return_2d=14.24; volume_z_20=13.72; return_1d=13.25; relative_strength_20d=13.07; beta_60d=13.06; range_pct=12.51.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.00; mục tiêu 1 27.05; mục tiêu 2 27.29.
- Tỷ lệ lợi nhuận/rủi ro 1.85; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 24.03 (-1.13%).
- P10/P90 cuối kỳ 21.23 / 27.29.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.500 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5438735978922589, AUC logistic=0.5474046878532064.
- Điều kiện phát hành tín hiệu: Probability 51.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.009731229999999313, Sharpe=-0.030064235651748497.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.8%.
- Mô hình Logistic đối chứng: 58.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.4%.
- Mức dừng lỗ tham chiếu 23.00, mục tiêu 1 27.05, tỷ lệ lợi nhuận/rủi ro 1.85.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
