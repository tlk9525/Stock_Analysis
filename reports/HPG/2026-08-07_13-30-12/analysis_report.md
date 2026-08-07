# Báo cáo ngày 2026-08-07 - HPG

## Tổng quan

- Dữ liệu: 2008-03-11 -> 2026-08-07, 4,589 phiên.
- Giá đóng cửa: 22.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.61; SMA60 22.98; RSI14 50.9.
- MACD -0.218; đường tín hiệu -0.396; biểu đồ cột 0.179.
- ATR14 0.57; ATR% 2.6%; ADX14 36.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 36.1, -DI vượt +DI.
- Thanh khoản: Thấp - 0.29 lần trung bình.
- Stochastic: Cực trị - %K 80.4, %D 74.5.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.95.
- P/B: 1.31.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 184,478.8 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 7.95: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.31: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.14: thanh khoản ngắn hạn khá.
- Revenue Growth 53.6% YoY.
- Profit Growth 49.7% YoY.
- CFO/LNST 0.82: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.26 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-30T07:51:50+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.523; AUC 0.580; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.516; AUC 0.567.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 125.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -34.4%; Sharpe -1.70; mức sụt giảm tối đa -36.7%.
- Mức độ quan trọng của đặc trưng: adx_14=10.14; market_return_1d=9.65; bb_position_20=9.60; macd_pct=9.38; day_of_week=9.33; excess_return_20d=8.92.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.30; mục tiêu 1 24.07; mục tiêu 2 24.07.
- Tỷ lệ lợi nhuận/rủi ro 1.87; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.91 (-1.07%).
- P10/P90 cuối kỳ 20.10 / 24.07.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 48.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.34449049999999937, Sharpe=-1.7049489413587435.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Mô hình Logistic đối chứng: 46.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.9%.
- Mức dừng lỗ tham chiếu 21.30, mục tiêu 1 24.07, tỷ lệ lợi nhuận/rủi ro 1.87.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
