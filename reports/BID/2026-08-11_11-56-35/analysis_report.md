# Báo cáo ngày 2026-08-11 - BID

## Tổng quan

- Dữ liệu: 2014-01-24 -> 2026-08-11, 3,126 phiên.
- Giá đóng cửa: 39.60 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 54.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 37.46; SMA60 40.22; RSI14 58.2.
- MACD -0.220; đường tín hiệu -0.711; biểu đồ cột 0.491.
- ATR14 1.04; ATR% 2.6%; ADX14 25.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 58.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.9, +DI vượt -DI.
- Thanh khoản: Thấp - 0.48 lần trung bình.
- Stochastic: Cực trị - %K 94.6, %D 94.3.

## Phân tích cơ bản

- Doanh nghiệp: BIDV.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.68.
- P/B: 1.49.
- ROE: 17.7%.
- ROA: 1.0%.
- Market cap: 287,562.6 tỷ.
- Revenue Growth: 7.0%.
- Profit Growth: 20.6%.
- P/E 8.68: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.49: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 16.31: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.8%: đang ở mức kiểm soát.
- Revenue Growth 7.0% YoY.
- Profit Growth 20.6% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.16 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:32:48+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.575; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.540.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 93.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.3%; Sharpe -1.14; mức sụt giảm tối đa -29.1%.
- Mức độ quan trọng của đặc trưng: return_1d=10.32; return_2d=9.81; day_of_week=9.54; corr_60d=8.81; range_pct=8.67; excess_return_1d=8.50.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 38.04; mục tiêu 1 44.23; mục tiêu 2 44.23.
- Tỷ lệ lợi nhuận/rủi ro 2.52; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 39.00 (-1.51%).
- P10/P90 cuối kỳ 35.01 / 44.23.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 54.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2526562499999999, Sharpe=-1.1429277374127638.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 54.5%.
- Mô hình Logistic đối chứng: 48.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.8%.
- Mức dừng lỗ tham chiếu 38.04, mục tiêu 1 44.23, tỷ lệ lợi nhuận/rủi ro 2.52.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
