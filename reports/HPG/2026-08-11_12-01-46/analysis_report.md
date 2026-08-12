# Báo cáo ngày 2026-08-11 - HPG

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,592 phiên.
- Giá đóng cửa: 22.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.57; SMA60 22.92; RSI14 50.4.
- MACD -0.157; đường tín hiệu -0.317; biểu đồ cột 0.160.
- ATR14 0.53; ATR% 2.4%; ADX14 33.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 33.2, -DI vượt +DI.
- Thanh khoản: Thấp - 0.26 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.04.
- P/B: 1.32.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 186,589.5 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 8.04: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-08-24 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.587; log-loss 0.675.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.565.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 119.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -29.9%; Sharpe -1.41; mức sụt giảm tối đa -37.0%.
- Mức độ quan trọng của đặc trưng: adx_14=10.64; market_return_1d=9.91; bb_position_20=9.56; macd_pct=8.96; relative_strength_20d=8.95; macd_hist_pct=8.94.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.31; mục tiêu 1 23.99; mục tiêu 2 23.99.
- Tỷ lệ lợi nhuận/rủi ro 1.98; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.93 (-0.76%).
- P10/P90 cuối kỳ 20.13 / 23.99.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.520 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.29859459999999893, Sharpe=-1.4140387494208335.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Mô hình Logistic đối chứng: 54.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.3%.
- Mức dừng lỗ tham chiếu 21.31, mục tiêu 1 23.99, tỷ lệ lợi nhuận/rủi ro 1.98.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
