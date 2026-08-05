# Báo cáo ngày 2026-08-06 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-05, 3,682 phiên.
- Giá đóng cửa: 24.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 23.27; SMA60 23.85; RSI14 60.1.
- MACD -0.140; đường tín hiệu -0.363; biểu đồ cột 0.223.
- ATR14 0.59; ATR% 2.4%; ADX14 30.7.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 60.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 30.7, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.97 lần trung bình.
- Stochastic: Cực trị - %K 93.7, %D 92.5.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.53.
- P/B: 1.32.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 196,542.0 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.53: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.527; AUC 0.522; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.511; AUC 0.505.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 15.0%; Sharpe 0.78; mức sụt giảm tối đa -5.0%.
- Mức độ quan trọng của đặc trưng: return_1d=13.38; beta_60d=13.01; volatility_20d=11.76; macd_hist_pct=11.70; excess_return_1d=11.49; return_skew_20d=11.34.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.61; mục tiêu 1 27.17; mục tiêu 2 27.17.
- Tỷ lệ lợi nhuận/rủi ro 3.40; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 23.90 (-1.64%).
- P10/P90 cuối kỳ 21.65 / 27.17.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.522 < 0.540.
- Điều kiện phát hành tín hiệu: Probability 52.7% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Mô hình Logistic đối chứng: 55.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.2%.
- Mức dừng lỗ tham chiếu 23.61, mục tiêu 1 27.17, tỷ lệ lợi nhuận/rủi ro 3.40.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
