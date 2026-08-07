# Báo cáo ngày 2026-08-07 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-07, 3,684 phiên.
- Giá đóng cửa: 24.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 23.22; SMA60 23.83; RSI14 58.3.
- MACD -0.003; đường tín hiệu -0.246; biểu đồ cột 0.242.
- ATR14 0.58; ATR% 2.4%; ADX14 27.6.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 58.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 27.6, +DI vượt -DI.
- Thanh khoản: Thấp - 0.32 lần trung bình.
- Stochastic: Cực trị - %K 92.1, %D 88.9.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.40.
- P/B: 1.29.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 192,514.5 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.40: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.29: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:06:57+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.528; AUC 0.523; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.510; AUC 0.505.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 13.7%; Sharpe 0.71; mức sụt giảm tối đa -5.0%.
- Mức độ quan trọng của đặc trưng: return_1d=13.15; beta_60d=12.42; volatility_20d=11.90; return_skew_20d=11.52; stoch_k_14=11.30; excess_return_1d=10.60.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.59; mục tiêu 1 27.00; mục tiêu 2 27.00.
- Tỷ lệ lợi nhuận/rủi ro 3.36; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 23.85 (-1.66%).
- P10/P90 cuối kỳ 21.65 / 27.00.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: Probability 47.9% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Mô hình Logistic đối chứng: 45.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.5%.
- Mức dừng lỗ tham chiếu 23.59, mục tiêu 1 27.00, tỷ lệ lợi nhuận/rủi ro 3.36.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
