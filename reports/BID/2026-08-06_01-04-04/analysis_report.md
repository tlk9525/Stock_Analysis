# Báo cáo ngày 2026-08-06 - BID

## Tổng quan

- Dữ liệu: 2014-01-24 -> 2026-08-05, 3,122 phiên.
- Giá đóng cửa: 38.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 44.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 37.68; SMA60 40.52; RSI14 47.5.
- MACD -0.827; đường tín hiệu -1.127; biểu đồ cột 0.300.
- ATR14 1.12; ATR% 3.0%; ADX14 31.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.2, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.81 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

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

- Kiểm thử: 2023-10-09 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.576; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.539.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 93.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.3%; Sharpe -1.15; mức sụt giảm tối đa -29.1%.
- Mức độ quan trọng của đặc trưng: return_1d=10.11; day_of_week=9.51; corr_60d=8.82; return_2d=8.78; range_pct=8.69; excess_return_1d=8.66.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 36.32; mục tiêu 1 41.27; mục tiêu 2 42.65.
- Tỷ lệ lợi nhuận/rủi ro 1.64; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 37.55 (-1.20%).
- P10/P90 cuối kỳ 33.57 / 42.65.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 44.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1461870062320803.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 44.5%.
- Mô hình Logistic đối chứng: 44.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.1%.
- Mức dừng lỗ tham chiếu 36.32, mục tiêu 1 41.27, tỷ lệ lợi nhuận/rủi ro 1.64.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
