# Báo cáo ngày 2026-08-12 - STB

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 74.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 72.78; SMA60 71.38; RSI14 56.8.
- MACD 0.700; đường tín hiệu 0.494; biểu đồ cột 0.206.
- ATR14 2.00; ATR% 2.7%; ADX14 15.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.5.
- Thanh khoản: Thấp - 0.39 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 45.48.
- P/B: 2.23.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 140,071.5 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 45.48: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.23: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T09:37:32+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.504; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.511.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.54; return_5d=11.91; beta_60d=11.88; range_pct=11.51; return_1d=11.23; bb_position_20=11.11.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.09; mục tiêu 1 84.34; mục tiêu 2 84.34.
- Tỷ lệ lợi nhuận/rủi ro 2.92; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 73.34 (-1.03%).
- P10/P90 cuối kỳ 64.53 / 84.34.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.504 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 45.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 71.09, mục tiêu 1 84.34, tỷ lệ lợi nhuận/rủi ro 2.92.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
