# Báo cáo ngày 2026-08-06 - SAB

## Tổng quan

- Dữ liệu: 2016-12-06 -> 2026-08-05, 2,411 phiên.
- Giá đóng cửa: 44.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 43.81; SMA60 44.48; RSI14 53.0.
- MACD -0.037; đường tín hiệu -0.195; biểu đồ cột 0.157.
- ATR14 0.84; ATR% 1.9%; ADX14 18.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 53.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 18.5.
- Thanh khoản: Bình thường - 0.82 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: SABECO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.11.
- P/B: 2.96.
- ROE: 22.3%.
- ROA: 15.1%.
- Market cap: 57,843.6 tỷ.
- Revenue Growth: 1.2%.
- Profit Growth: -3.4%.
- P/E 12.11: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.96: nên đọc cùng ROE và đặc thù ngành.
- ROE 22.3%: hiệu quả vốn chủ sở hữu tốt.
- ROA 15.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.46: thanh khoản ngắn hạn khá.
- Revenue Growth 1.2% YoY.
- Profit Growth -3.4% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-25 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.514; AUC 0.509; log-loss 0.682.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.498; AUC 0.468.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 39.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -32.9%; Sharpe -1.24; mức sụt giảm tối đa -34.7%.
- Mức độ quan trọng của đặc trưng: stoch_k_14=12.94; market_return_20d=11.65; return_2d=11.54; rsi_14=11.24; macd_pct=10.90; close_vs_sma60=10.75.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 44.04; mục tiêu 1 48.40; mục tiêu 2 48.40.
- Tỷ lệ lợi nhuận/rủi ro 6.47; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 44.01 (-0.87%).
- P10/P90 cuối kỳ 40.91 / 48.40.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.509 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.514 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 49.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2433906174868021.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Mô hình Logistic đối chứng: 53.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.3%.
- Mức dừng lỗ tham chiếu 44.04, mục tiêu 1 48.40, tỷ lệ lợi nhuận/rủi ro 6.47.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
