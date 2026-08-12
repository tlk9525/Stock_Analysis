# Báo cáo ngày 2026-08-09 - POW

## Tổng quan

- Dữ liệu: 2018-03-06 -> 2026-08-07, 2,097 phiên.
- Giá đóng cửa: 13.60 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 13.64; SMA60 13.93; RSI14 46.7.
- MACD -0.119; đường tín hiệu -0.140; biểu đồ cột 0.021.
- ATR14 0.41; ATR% 3.0%; ADX14 30.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 46.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 30.6, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.89 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Điện lực Dầu khí Việt Nam.
- Ngành: Utilities.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.48.
- P/B: 1.01.
- ROE: 16.5%.
- ROA: 6.5%.
- Market cap: 41,722.7 tỷ.
- Revenue Growth: 116.1%.
- Profit Growth: 484.1%.
- P/E 6.48: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 6.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.37: thanh khoản ngắn hạn khá.
- Revenue Growth 116.1% YoY.
- Profit Growth 484.1% YoY.
- CFO/LNST 0.49: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.02 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:13:42+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-21 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.587; log-loss 0.672.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.543; AUC 0.552.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 104.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -35.8%; Sharpe -1.42; mức sụt giảm tối đa -43.2%.
- Mức độ quan trọng của đặc trưng: return_1d=10.55; stoch_k_14=9.44; close_vs_sma20=8.97; return_20d=8.74; macd_hist_pct=8.52; atr_pct_14=8.46.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 12.99; mục tiêu 1 15.34; mục tiêu 2 15.34.
- Tỷ lệ lợi nhuận/rủi ro 2.47; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.55 (-0.39%).
- P10/P90 cuối kỳ 12.00 / 15.34.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 47.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.4170100539659634.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Mô hình Logistic đối chứng: 47.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.3%.
- Mức dừng lỗ tham chiếu 12.99, mục tiêu 1 15.34, tỷ lệ lợi nhuận/rủi ro 2.47.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
