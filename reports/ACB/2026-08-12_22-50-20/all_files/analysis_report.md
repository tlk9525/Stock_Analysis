# Báo cáo ngày 2026-08-12 - ACB

## Tổng quan

- Dữ liệu: 2008-03-06 -> 2026-08-12, 4,597 phiên.
- Giá đóng cửa: 22.75 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 22.59; SMA60 22.32; RSI14 54.4.
- MACD 0.019; đường tín hiệu 0.006; biểu đồ cột 0.013.
- ATR14 0.48; ATR% 2.1%; ADX14 21.9.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 54.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 21.9.
- Thanh khoản: Thấp - 0.68 lần trung bình.
- Stochastic: Cực trị - %K 95.0, %D 83.6.

## Phân tích cơ bản

- Doanh nghiệp: ACB.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.39.
- P/B: 1.32.
- ROE: 16.3%.
- ROA: 1.5%.
- Market cap: 131,470.2 tỷ.
- Revenue Growth: -1.6%.
- Profit Growth: -12.1%.
- P/E 8.39: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.3%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.75: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.0%: đang ở mức kiểm soát.
- Revenue Growth -1.6% YoY.
- Profit Growth -12.1% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.20 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:36:23+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-20 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.513; AUC 0.522; log-loss 0.690.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.3%; Sharpe -0.60; mức sụt giảm tối đa -10.8%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.03; relative_strength_20d=12.16; return_1d=11.34; return_2d=11.34; beta_60d=10.33; return_5d=10.29.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 22.10; mục tiêu 1 24.79; mục tiêu 2 24.79.
- Tỷ lệ lợi nhuận/rủi ro 2.51; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 22.56 (-0.82%).
- P10/P90 cuối kỳ 20.88 / 24.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.522 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.513 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5217332843299838, AUC logistic=0.5274523337845227.
- Điều kiện phát hành tín hiệu: Probability 48.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10298540999999994, Sharpe=-0.6023229276200178.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Mô hình Logistic đối chứng: 46.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.7%.
- Mức dừng lỗ tham chiếu 22.10, mục tiêu 1 24.79, tỷ lệ lợi nhuận/rủi ro 2.51.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
