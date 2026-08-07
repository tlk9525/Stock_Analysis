# Báo cáo ngày 2026-08-06 - BID

## Tổng quan

- Dữ liệu: 2014-01-24 -> 2026-08-06, 3,123 phiên.
- Giá đóng cửa: 37.90 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 43.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 37.54; SMA60 40.43; RSI14 46.9.
- MACD -0.730; đường tín hiệu -1.048; biểu đồ cột 0.318.
- ATR14 1.07; ATR% 2.8%; ADX14 29.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 46.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 29.5, -DI vượt +DI.
- Thanh khoản: Thấp - 0.65 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: BIDV.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.35.
- P/B: 1.43.
- ROE: 17.7%.
- ROA: 1.0%.
- Market cap: 276,642.5 tỷ.
- Revenue Growth: 7.0%.
- Profit Growth: 20.6%.
- P/E 8.35: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.43: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 16.31: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.8%: đang ở mức kiểm soát.
- Revenue Growth 7.0% YoY.
- Profit Growth 20.6% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.577; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.540.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 93.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.3%; Sharpe -1.15; mức sụt giảm tối đa -29.1%.
- Mức độ quan trọng của đặc trưng: day_of_week=9.55; return_2d=9.44; excess_return_1d=9.39; return_1d=9.35; corr_60d=9.26; range_pct=8.87.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 36.29; mục tiêu 1 41.02; mục tiêu 2 42.41.
- Tỷ lệ lợi nhuận/rủi ro 1.63; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 37.33 (-1.51%).
- P10/P90 cuối kỳ 33.40 / 42.41.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 43.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1453695755811828.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 43.3%.
- Mô hình Logistic đối chứng: 39.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.1%.
- Mức dừng lỗ tham chiếu 36.29, mục tiêu 1 41.02, tỷ lệ lợi nhuận/rủi ro 1.63.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
