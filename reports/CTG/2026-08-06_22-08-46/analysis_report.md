# Báo cáo ngày 2026-08-06 - CTG

## Tổng quan

- Dữ liệu: 2009-07-16 -> 2026-08-06, 4,257 phiên.
- Giá đóng cửa: 31.35 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.78; SMA60 32.76; RSI14 49.6.
- MACD -0.390; đường tín hiệu -0.703; biểu đồ cột 0.313.
- ATR14 0.79; ATR% 2.5%; ADX14 28.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 28.6, -DI vượt +DI.
- Thanh khoản: Thấp - 0.61 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VietinBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.16.
- P/B: 1.24.
- ROE: 21.8%.
- ROA: 1.4%.
- Market cap: 247,377.2 tỷ.
- Revenue Growth: 26.1%.
- Profit Growth: 21.4%.
- P/E 6.16: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.24: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.8%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 13.79: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.2%: đang ở mức kiểm soát.
- Revenue Growth 26.1% YoY.
- Profit Growth 21.4% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-12-08 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.502; AUC 0.490; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.507; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 17.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.9%; Sharpe -0.38; mức sụt giảm tối đa -13.8%.
- Mức độ quan trọng của đặc trưng: beta_60d=16.04; return_1d=15.78; atr_pct_14=14.94; market_volatility_20d=13.40; return_2d=13.33; market_return_1d=12.66.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 30.16; mục tiêu 1 33.78; mục tiêu 2 34.51.
- Tỷ lệ lợi nhuận/rủi ro 1.69; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.10 (-0.79%).
- P10/P90 cuối kỳ 28.21 / 34.51.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.490 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.502 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 50.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.3776510745901127.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Mô hình Logistic đối chứng: 51.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.9%.
- Mức dừng lỗ tham chiếu 30.16, mục tiêu 1 33.78, tỷ lệ lợi nhuận/rủi ro 1.69.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
