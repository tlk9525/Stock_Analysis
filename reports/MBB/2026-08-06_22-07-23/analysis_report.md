# Báo cáo ngày 2026-08-06 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-06, 3,683 phiên.
- Giá đóng cửa: 23.90 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 23.24; SMA60 23.84; RSI14 55.0.
- MACD -0.079; đường tín hiệu -0.306; biểu đồ cột 0.227.
- ATR14 0.59; ATR% 2.5%; ADX14 29.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 29.0, +DI vượt -DI.
- Thanh khoản: Thấp - 0.66 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.51.
- P/B: 1.31.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 195,736.5 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.51: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.31: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.526; AUC 0.521; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.511; AUC 0.504.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 12.6%; Sharpe 0.66; mức sụt giảm tối đa -5.0%.
- Mức độ quan trọng của đặc trưng: return_1d=13.40; beta_60d=13.21; volatility_20d=12.02; macd_hist_pct=11.74; return_skew_20d=11.46; excess_return_1d=11.34.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.60; mục tiêu 1 25.00; mục tiêu 2 26.71.
- Tỷ lệ lợi nhuận/rủi ro 2.32; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 23.48 (-1.75%).
- P10/P90 cuối kỳ 21.32 / 26.71.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.521 < 0.540.
- Điều kiện phát hành tín hiệu: Probability 53.5% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.5%.
- Mô hình Logistic đối chứng: 54.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.3%.
- Mức dừng lỗ tham chiếu 23.60, mục tiêu 1 25.00, tỷ lệ lợi nhuận/rủi ro 2.32.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
