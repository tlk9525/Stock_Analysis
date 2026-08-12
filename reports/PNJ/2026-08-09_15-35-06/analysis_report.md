# Báo cáo ngày 2026-08-09 - PNJ

## Tổng quan

- Dữ liệu: 2009-03-23 -> 2026-08-07, 4,326 phiên.
- Giá đóng cửa: 36.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 36.88; SMA60 54.34; RSI14 37.9.
- MACD -4.999; đường tín hiệu -6.199; biểu đồ cột 1.200.
- ATR14 2.52; ATR% 7.0%; ADX14 43.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 37.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 43.5, -DI vượt +DI.
- Thanh khoản: Thấp - 0.38 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vàng Phú Nhuận.
- Ngành: Personal & Household Goods.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.35.
- P/B: 1.33.
- ROE: 21.6%.
- ROA: 14.9%.
- Market cap: 18,422.0 tỷ.
- Revenue Growth: 11.9%.
- Profit Growth: -164.7%.
- P/E 6.35: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.33: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.6%: hiệu quả vốn chủ sở hữu tốt.
- ROA 14.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.74: thanh khoản ngắn hạn khá.
- Revenue Growth 11.9% YoY.
- Profit Growth -164.7% YoY.
- CFO/LNST 5.54: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi -6.08 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T07:48:16+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-14 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.492; AUC 0.490; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.488; AUC 0.504.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.5%; Sharpe -0.19; mức sụt giảm tối đa -19.7%.
- Mức độ quan trọng của đặc trưng: macd_hist_pct=11.63; return_20d=11.63; rsi_14=11.14; close_vs_sma60=10.99; excess_return_1d=10.84; macd_pct=10.59.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 32.23; mục tiêu 1 46.90; mục tiêu 2 46.90.
- Tỷ lệ lợi nhuận/rủi ro 2.71; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 36.32 (0.88%).
- P10/P90 cuối kỳ 29.54 / 41.91.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.490 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.492 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4904799385318866, AUC logistic=0.5037574258353479.
- Điều kiện phát hành tín hiệu: Probability 47.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -4 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.05460289999999968, Sharpe=-0.19220090248872881.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.9%.
- Mô hình Logistic đối chứng: 50.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 52.8%.
- Mức dừng lỗ tham chiếu 32.23, mục tiêu 1 46.90, tỷ lệ lợi nhuận/rủi ro 2.71.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
