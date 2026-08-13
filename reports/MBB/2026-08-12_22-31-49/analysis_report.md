# Báo cáo ngày 2026-08-12 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-12, 3,687 phiên.
- Giá đóng cửa: 20.45 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 19.35; SMA60 19.86; RSI14 61.3.
- MACD 0.142; đường tín hiệu -0.056; biểu đồ cột 0.198.
- ATR14 0.45; ATR% 2.2%; ADX14 25.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.0, +DI vượt -DI.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Cực trị - %K 96.4, %D 93.7.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.27.
- P/B: 1.30.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 204,899.1 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.27: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.30: nên đọc cùng ROE và đặc thù ngành.
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
- Bài mới nhất: 2026-08-07T08:40:35+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.498; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.499.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 41.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -4.9%; Sharpe -0.17; mức sụt giảm tối đa -10.4%.
- Mức độ quan trọng của đặc trưng: return_1d=11.59; beta_60d=10.76; volatility_20d=10.25; return_2d=9.90; market_return_1d=9.58; excess_return_1d=9.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 19.78; mục tiêu 1 22.66; mục tiêu 2 22.66.
- Tỷ lệ lợi nhuận/rủi ro 2.73; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 20.15 (-1.44%).
- P10/P90 cuối kỳ 18.37 / 22.66.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.498 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49810467106872097, AUC logistic=0.49876701720061956.
- Điều kiện phát hành tín hiệu: Probability 53.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17041681469535072.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Mô hình Logistic đối chứng: 49.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.4%.
- Mức dừng lỗ tham chiếu 19.78, mục tiêu 1 22.66, tỷ lệ lợi nhuận/rủi ro 2.73.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
