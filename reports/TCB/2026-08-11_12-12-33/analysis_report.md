# Báo cáo ngày 2026-08-11 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-11, 2,047 phiên.
- Giá đóng cửa: 31.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 29.78; SMA60 31.51; RSI14 56.2.
- MACD -0.357; đường tín hiệu -0.665; biểu đồ cột 0.309.
- ATR14 0.85; ATR% 2.7%; ADX14 29.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 29.4, +DI vượt -DI.
- Thanh khoản: Thấp - 0.48 lần trung bình.
- Stochastic: Cực trị - %K 92.0, %D 89.3.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.19.
- P/B: 1.24.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 222,153.6 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.19: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.24: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.74: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:42:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-08 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.497; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.
- Mức độ quan trọng của đặc trưng: volatility_20d=14.89; bb_position_20=11.12; relative_strength_20d=10.37; close_vs_sma60=9.90; return_3d=9.77; return_2d=9.74.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.19; mục tiêu 1 32.20; mục tiêu 2 34.73.
- Tỷ lệ lợi nhuận/rủi ro 3.72; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.14 (-0.34%).
- P10/P90 cuối kỳ 27.76 / 34.73.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.497 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49738268188631385, AUC logistic=0.5009108728237057.
- Điều kiện phát hành tín hiệu: Probability 51.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6469342728240042.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Mô hình Logistic đối chứng: 52.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.4%.
- Mức dừng lỗ tham chiếu 31.19, mục tiêu 1 32.20, tỷ lệ lợi nhuận/rủi ro 3.72.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
