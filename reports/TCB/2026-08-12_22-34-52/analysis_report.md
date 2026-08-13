# Báo cáo ngày 2026-08-12 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-12, 2,048 phiên.
- Giá đóng cửa: 31.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 29.77; SMA60 31.49; RSI14 57.4.
- MACD -0.231; đường tín hiệu -0.582; biểu đồ cột 0.350.
- ATR14 0.84; ATR% 2.7%; ADX14 28.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.0, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.06 lần trung bình.
- Stochastic: Cực trị - %K 98.7, %D 94.7.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.10.
- P/B: 1.23.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 219,673.5 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.10: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.23: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-09-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.500; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.29; bb_position_20=11.07; atr_pct_14=10.33; relative_strength_20d=9.83; excess_return_5d=9.70; market_return_1d=9.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.17; mục tiêu 1 35.12; mục tiêu 2 35.12.
- Tỷ lệ lợi nhuận/rủi ro 7.14; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.43 (-0.24%).
- P10/P90 cuối kỳ 27.91 / 35.12.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.500 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4998236331569665, AUC logistic=0.50100452419293.
- Điều kiện phát hành tín hiệu: Probability 50.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6457936868409828.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 49.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.8%.
- Mức dừng lỗ tham chiếu 31.17, mục tiêu 1 35.12, tỷ lệ lợi nhuận/rủi ro 7.14.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
