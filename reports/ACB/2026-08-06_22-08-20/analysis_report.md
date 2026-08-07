# Báo cáo ngày 2026-08-06 - ACB

## Tổng quan

- Dữ liệu: 2008-03-06 -> 2026-08-06, 4,593 phiên.
- Giá đóng cửa: 22.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 22.62; SMA60 22.13; RSI14 45.2.
- MACD -0.044; đường tín hiệu 0.024; biểu đồ cột -0.068.
- ATR14 0.53; ATR% 2.4%; ADX14 24.1.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 45.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 24.1.
- Thanh khoản: Thấp - 0.48 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: ACB.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.31.
- P/B: 1.31.
- ROE: 16.3%.
- ROA: 1.5%.
- Market cap: 130,309.3 tỷ.
- Revenue Growth: -1.6%.
- Profit Growth: -12.1%.
- P/E 8.31: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.31: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.3%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.75: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.0%: đang ở mức kiểm soát.
- Revenue Growth -1.6% YoY.
- Profit Growth -12.1% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-11-20 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.520; log-loss 0.690.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.2%; Sharpe -0.60; mức sụt giảm tối đa -10.8%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.29; relative_strength_20d=12.13; return_5d=11.80; return_1d=11.71; bb_position_20=11.20; beta_60d=11.20.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.91; mục tiêu 1 23.85; mục tiêu 2 24.20.
- Tỷ lệ lợi nhuận/rủi ro 4.50; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.94 (-0.96%).
- P10/P90 cuối kỳ 20.30 / 24.20.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.520 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5202928566237919, AUC logistic=0.5266332388634547.
- Điều kiện phát hành tín hiệu: Probability 51.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10245695999999993, Sharpe=-0.6006663177345457.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.5%.
- Mô hình Logistic đối chứng: 51.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.4%.
- Mức dừng lỗ tham chiếu 21.91, mục tiêu 1 23.85, tỷ lệ lợi nhuận/rủi ro 4.50.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
