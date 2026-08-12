# Báo cáo ngày 2026-08-09 - VNM

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-07, 4,590 phiên.
- Giá đóng cửa: 62.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 8).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 42.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 58.73; SMA60 57.34; RSI14 65.1.
- MACD 0.957; đường tín hiệu 0.816; biểu đồ cột 0.140.
- ATR14 1.48; ATR% 2.4%; ADX14 25.4.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 65.1.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Xu hướng tăng - ADX 25.4, +DI vượt -DI.
- Thanh khoản: Đột biến - 2.43 lần trung bình.
- Stochastic: Cực trị - %K 82.3, %D 58.4.

## Phân tích cơ bản

- Doanh nghiệp: VINAMILK.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.82.
- P/B: 4.07.
- ROE: 33.9%.
- ROA: 19.8%.
- Market cap: 129,577.2 tỷ.
- Revenue Growth: 12.7%.
- Profit Growth: 28.0%.
- P/E 11.82: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 4.07: nên đọc cùng ROE và đặc thù ngành.
- ROE 33.9%: hiệu quả vốn chủ sở hữu tốt.
- ROA 19.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.91: thanh khoản ngắn hạn khá.
- Revenue Growth 12.7% YoY.
- Profit Growth 28.0% YoY.
- CFO/LNST 1.01: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:57:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.527; log-loss 0.683.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.537; AUC 0.559.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 89.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.9%; Sharpe -1.41; mức sụt giảm tối đa -35.8%.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=11.82; return_1d=11.16; month_of_year=10.64; close_vs_sma20=10.50; bb_position_20=10.27; return_3d=10.25.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.78; mục tiêu 1 67.72; mục tiêu 2 67.72.
- Tỷ lệ lợi nhuận/rủi ro 2.13; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 61.46 (-0.87%).
- P10/P90 cuối kỳ 56.14 / 67.72.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.527 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5269330041521715, AUC logistic=0.5587556310819694.
- Điều kiện phát hành tín hiệu: Probability 42.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.4084940690286425.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 42.0%.
- Mô hình Logistic đối chứng: 51.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.8%.
- Mức dừng lỗ tham chiếu 59.78, mục tiêu 1 67.72, tỷ lệ lợi nhuận/rủi ro 2.13.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
