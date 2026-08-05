# Báo cáo ngày 2026-08-06 - CTG

## Tổng quan

- Dữ liệu: 2009-07-16 -> 2026-08-05, 4,256 phiên.
- Giá đóng cửa: 31.85 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.89; SMA60 32.83; RSI14 54.7.
- MACD -0.461; đường tín hiệu -0.781; biểu đồ cột 0.320.
- ATR14 0.81; ATR% 2.5%; ADX14 30.3.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 30.3, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.01 lần trung bình.
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

- Kiểm thử: 2023-12-08 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.502; AUC 0.491; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.507; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 17.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.9%; Sharpe -0.38; mức sụt giảm tối đa -13.8%.
- Mức độ quan trọng của đặc trưng: return_1d=16.23; atr_pct_14=14.82; beta_60d=14.53; return_2d=13.25; rsi_14=13.15; market_return_1d=12.99.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 30.63; mục tiêu 1 35.09; mục tiêu 2 35.09.
- Tỷ lệ lợi nhuận/rủi ro 2.24; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.68 (-0.52%).
- P10/P90 cuối kỳ 28.70 / 35.09.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.491 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.502 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 50.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37793722681637665.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Mô hình Logistic đối chứng: 49.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.3%.
- Mức dừng lỗ tham chiếu 30.63, mục tiêu 1 35.09, tỷ lệ lợi nhuận/rủi ro 2.24.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
