# Báo cáo ngày 2026-08-11 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-11, 4,272 phiên.
- Giá đóng cửa: 60.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 57.41; SMA60 60.08; RSI14 59.2.
- MACD 0.225; đường tín hiệu -0.380; biểu đồ cột 0.605.
- ATR14 1.39; ATR% 2.3%; ADX14 26.8.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.8, +DI vượt -DI.
- Thanh khoản: Thấp - 0.40 lần trung bình.
- Stochastic: Cực trị - %K 91.7, %D 89.3.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.10.
- P/B: 2.03.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 503,847.2 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 12.10: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.03: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:03:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.468; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.477; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.25; mức sụt giảm tối đa -26.4%.
- Mức độ quan trọng của đặc trưng: month_of_year=11.72; return_1d=10.84; market_return_5d=10.79; atr_pct_14=10.74; market_return_20d=10.50; return_20d=10.49.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.48; mục tiêu 1 67.46; mục tiêu 2 67.46.
- Tỷ lệ lợi nhuận/rủi ro 6.10; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 59.38 (-1.53%).
- P10/P90 cuối kỳ 54.23 / 67.46.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.468 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4682519377641329, AUC logistic=0.489794758087441.
- Điều kiện phát hành tín hiệu: Probability 48.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.2493018719101534.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.4%.
- Mô hình Logistic đối chứng: 49.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.8%.
- Mức dừng lỗ tham chiếu 59.48, mục tiêu 1 67.46, tỷ lệ lợi nhuận/rủi ro 6.10.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
