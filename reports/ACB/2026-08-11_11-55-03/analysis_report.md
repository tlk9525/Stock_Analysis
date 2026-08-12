# Báo cáo ngày 2026-08-11 - ACB

## Tổng quan

- Dữ liệu: 2008-03-06 -> 2026-08-11, 4,596 phiên.
- Giá đóng cửa: 22.65 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 22.61; SMA60 22.27; RSI14 52.9.
- MACD -0.003; đường tín hiệu 0.003; biểu đồ cột -0.006.
- ATR14 0.50; ATR% 2.2%; ADX14 22.8.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 52.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 22.8.
- Thanh khoản: Thấp - 0.28 lần trung bình.
- Stochastic: Cực trị - %K 87.0, %D 68.6.

## Phân tích cơ bản

- Doanh nghiệp: ACB.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.39.
- P/B: 1.32.
- ROE: 16.3%.
- ROA: 1.5%.
- Market cap: 131,470.2 tỷ.
- Revenue Growth: -1.6%.
- Profit Growth: -12.1%.
- P/E 8.39: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.3%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.75: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.0%: đang ở mức kiểm soát.
- Revenue Growth -1.6% YoY.
- Profit Growth -12.1% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.20 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:36:23+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-20 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.520; log-loss 0.690.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.2%; Sharpe -0.60; mức sụt giảm tối đa -10.8%.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=12.97; market_return_1d=12.81; beta_60d=11.72; return_1d=10.90; return_5d=10.74; excess_return_20d=10.68.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 22.04; mục tiêu 1 23.85; mục tiêu 2 24.69.
- Tỷ lệ lợi nhuận/rủi ro 1.51; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 22.44 (-0.92%).
- P10/P90 cuối kỳ 20.81 / 24.69.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.520 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5201961137099677, AUC logistic=0.5266732637639439.
- Điều kiện phát hành tín hiệu: Probability 51.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10245695999999993, Sharpe=-0.5993340384286274.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.9%.
- Mô hình Logistic đối chứng: 51.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.3%.
- Mức dừng lỗ tham chiếu 22.04, mục tiêu 1 23.85, tỷ lệ lợi nhuận/rủi ro 1.51.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
