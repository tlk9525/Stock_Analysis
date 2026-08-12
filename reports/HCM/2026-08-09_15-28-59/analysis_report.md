# Báo cáo ngày 2026-08-09 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-07, 4,298 phiên.
- Giá đóng cửa: 25.35 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 25.10; SMA60 24.38; RSI14 54.6.
- MACD 0.305; đường tín hiệu 0.338; biểu đồ cột -0.034.
- ATR14 0.84; ATR% 3.3%; ADX14 12.3.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 54.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.3.
- Thanh khoản: Thấp - 0.50 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.24.
- P/B: 1.97.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 34,221.1 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.24: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.97: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.
- CFO/LNST 1.16: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.16 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T10:19:59+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.557; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.564.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.23; return_1d=11.61; macd_pct=11.47; beta_60d=10.96; market_return_1d=10.71; corr_60d=10.65.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.13; mục tiêu 1 28.79; mục tiêu 2 28.79.
- Tỷ lệ lợi nhuận/rủi ro 2.46; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.05 (-1.17%).
- P10/P90 cuối kỳ 22.04 / 28.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.557401586588834, AUC logistic=0.5642535215952369.
- Điều kiện phát hành tín hiệu: Probability 48.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3378389084634233.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Mô hình Logistic đối chứng: 40.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.5%.
- Mức dừng lỗ tham chiếu 24.13, mục tiêu 1 28.79, tỷ lệ lợi nhuận/rủi ro 2.46.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
