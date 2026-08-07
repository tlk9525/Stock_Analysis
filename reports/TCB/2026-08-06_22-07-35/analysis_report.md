# Báo cáo ngày 2026-08-06 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-06, 2,044 phiên.
- Giá đóng cửa: 29.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.01; SMA60 31.62; RSI14 39.7.
- MACD -0.766; đường tín hiệu -0.827; biểu đồ cột 0.061.
- ATR14 0.79; ATR% 2.7%; ADX14 33.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 39.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 33.5, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.86 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.74.
- P/B: 1.17.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 210,107.0 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 7.74: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.17: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.74: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-08 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.499; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.503.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.
- Mức độ quan trọng của đặc trưng: volatility_20d=14.37; return_2d=11.51; bb_position_20=11.06; close_vs_sma60=10.36; relative_strength_20d=10.14; macd_pct=10.10.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 28.02; mục tiêu 1 32.42; mục tiêu 2 33.20.
- Tỷ lệ lợi nhuận/rủi ro 2.31; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 29.01 (-0.64%).
- P10/P90 cuối kỳ 25.79 / 32.42.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.499 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4990532066803253, AUC logistic=0.5026386043335196.
- Điều kiện phát hành tín hiệu: Probability 49.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6503703121176383.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Mô hình Logistic đối chứng: 47.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.0%.
- Mức dừng lỗ tham chiếu 28.02, mục tiêu 1 32.42, tỷ lệ lợi nhuận/rủi ro 2.31.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
