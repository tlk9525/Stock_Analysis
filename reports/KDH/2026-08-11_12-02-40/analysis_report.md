# Báo cáo ngày 2026-08-11 - KDH

## Tổng quan

- Dữ liệu: 2010-02-01 -> 2026-08-11, 4,118 phiên.
- Giá đóng cửa: 18.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 17.88; SMA60 20.79; RSI14 44.4.
- MACD -0.653; đường tín hiệu -0.904; biểu đồ cột 0.251.
- ATR14 0.59; ATR% 3.2%; ADX14 42.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 44.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 42.8, -DI vượt +DI.
- Thanh khoản: Thấp - 0.52 lần trung bình.
- Stochastic: Cực trị - %K 84.0, %D 77.3.

## Phân tích cơ bản

- Doanh nghiệp: Nhà Khang Điền.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.59.
- P/B: 1.09.
- ROE: 9.5%.
- ROA: 4.8%.
- Market cap: 20,368.2 tỷ.
- Revenue Growth: -84.7%.
- Profit Growth: 276.7%.
- P/E 11.59: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.09: nên đọc cùng ROE và đặc thù ngành.
- ROA 4.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 10.06: thanh khoản ngắn hạn khá.
- Revenue Growth -84.7% YoY.
- Profit Growth 276.7% YoY.
- CFO/LNST -1.10: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:54:28+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.499; AUC 0.490; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.498; AUC 0.496.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 8.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 2.5%; Sharpe 0.16; mức sụt giảm tối đa -8.8%.
- Mức độ quan trọng của đặc trưng: return_1d=13.82; return_5d=12.16; return_3d=11.47; adx_14=9.82; return_skew_20d=9.59; corr_60d=9.59.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 17.42; mục tiêu 1 19.90; mục tiêu 2 20.51.
- Tỷ lệ lợi nhuận/rủi ro 1.55; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 17.87 (-2.34%).
- P10/P90 cuối kỳ 15.93 / 20.51.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.490 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.499 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49001021511837517, AUC logistic=0.4955984857589232.
- Điều kiện phát hành tín hiệu: Probability 49.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.1%.
- Mô hình Logistic đối chứng: 47.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 40.6%.
- Mức dừng lỗ tham chiếu 17.42, mục tiêu 1 19.90, tỷ lệ lợi nhuận/rủi ro 1.55.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
