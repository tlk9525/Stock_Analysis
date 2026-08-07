# Báo cáo ngày 2026-08-07 - FPT

## Tổng quan

- Dữ liệu: 2008-03-11 -> 2026-08-07, 4,589 phiên.
- Giá đóng cửa: 71.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 44.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.31; SMA60 70.99; RSI14 58.0.
- MACD 0.029; đường tín hiệu -0.867; biểu đồ cột 0.896.
- ATR14 1.97; ATR% 2.8%; ADX14 26.9.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 58.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.9, +DI vượt -DI.
- Thanh khoản: Thấp - 0.39 lần trung bình.
- Stochastic: Cực trị - %K 80.5, %D 77.7.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.05.
- P/B: 3.03.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 121,202.9 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.05: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.03: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.
- CFO/LNST 0.66: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T09:13:52+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.576; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.561.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=14.90; return_1d=14.71; stoch_k_14=11.95; atr_pct_14=11.76; day_of_week=11.61; market_return_1d=11.51.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.28; mục tiêu 1 73.30; mục tiêu 2 79.36.
- Tỷ lệ lợi nhuận/rủi ro 1.81; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.53 (-0.67%).
- P10/P90 cuối kỳ 63.25 / 79.36.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 44.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8615619551711172.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 44.0%.
- Mô hình Logistic đối chứng: 40.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 70.28, mục tiêu 1 73.30, tỷ lệ lợi nhuận/rủi ro 1.81.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
