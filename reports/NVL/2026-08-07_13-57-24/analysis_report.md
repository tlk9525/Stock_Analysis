# Báo cáo ngày 2026-08-07 - NVL

## Tổng quan

- Dữ liệu: 2016-12-28 -> 2026-08-07, 2,397 phiên.
- Giá đóng cửa: 13.85 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 12.87; SMA60 13.13; RSI14 65.0.
- MACD 0.232; đường tín hiệu 0.077; biểu đồ cột 0.155.
- ATR14 0.54; ATR% 3.9%; ADX14 30.1.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 65.0.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Xu hướng tăng - ADX 30.1, +DI vượt -DI.
- Thanh khoản: Thấp - 0.56 lần trung bình.
- Stochastic: Cực trị - %K 82.9, %D 82.8.

## Phân tích cơ bản

- Doanh nghiệp: Novaland.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.41.
- P/B: 0.68.
- ROE: 9.5%.
- ROA: 1.7%.
- Market cap: 32,908.3 tỷ.
- Revenue Growth: -22.1%.
- P/E 7.41: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 0.68: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 2.96: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 2.12: thanh khoản ngắn hạn khá.
- Revenue Growth -22.1% YoY.
- CFO/LNST -3.46: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:14:03+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.497; AUC 0.534; log-loss 0.685.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.506; AUC 0.516.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 45.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -31.8%; Sharpe -0.91; mức sụt giảm tối đa -42.2%.
- Mức độ quan trọng của đặc trưng: beta_60d=10.51; market_return_1d=10.04; close_vs_sma60=10.00; excess_return_5d=9.91; macd_pct=9.57; rsi_14=9.30.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 13.04; mục tiêu 1 16.62; mục tiêu 2 16.62.
- Tỷ lệ lợi nhuận/rủi ro 3.06; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.59 (-1.89%).
- P10/P90 cuối kỳ 11.49 / 16.62.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.534 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.497 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 49.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3176097600000002, Sharpe=-0.9132482704221854.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Mô hình Logistic đối chứng: 48.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.3%.
- Mức dừng lỗ tham chiếu 13.04, mục tiêu 1 16.62, tỷ lệ lợi nhuận/rủi ro 3.06.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
