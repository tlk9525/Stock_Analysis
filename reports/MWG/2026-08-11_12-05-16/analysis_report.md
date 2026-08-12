# Báo cáo ngày 2026-08-11 - MWG

## Tổng quan

- Dữ liệu: 2014-07-14 -> 2026-08-11, 3,016 phiên.
- Giá đóng cửa: 73.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 41.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 70.97; SMA60 74.92; RSI14 52.0.
- MACD -0.786; đường tín hiệu -1.445; biểu đồ cột 0.659.
- ATR14 2.43; ATR% 3.3%; ADX14 27.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 27.8, -DI vượt +DI.
- Thanh khoản: Thấp - 0.26 lần trung bình.
- Stochastic: Cực trị - %K 93.5, %D 82.9.

## Phân tích cơ bản

- Doanh nghiệp: Thế giới di động.
- Ngành: Retail.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 10.95.
- P/B: 3.01.
- ROE: 29.2%.
- ROA: 11.2%.
- Market cap: 107,730.9 tỷ.
- Revenue Growth: 29.6%.
- Profit Growth: 100.4%.
- P/E 10.95: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 29.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 11.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.44: thanh khoản ngắn hạn khá.
- Revenue Growth 29.6% YoY.
- Profit Growth 100.4% YoY.
- CFO/LNST 5.06: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T09:51:48+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-23 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.507; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.526.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 87.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -6.6%; Sharpe -0.21; mức sụt giảm tối đa -14.2%.
- Mức độ quan trọng của đặc trưng: beta_60d=8.25; stoch_k_14=7.75; day_of_week=7.66; return_2d=7.51; relative_strength_20d=7.25; excess_return_1d=7.25.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 69.36; mục tiêu 1 81.51; mục tiêu 2 81.51.
- Tỷ lệ lợi nhuận/rủi ro 2.03; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 72.49 (-0.69%).
- P10/P90 cuối kỳ 64.56 / 81.51.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.506640625, AUC logistic=0.5259515224358975.
- Điều kiện phát hành tín hiệu: Probability 41.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.21083208477105841.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 41.5%.
- Mô hình Logistic đối chứng: 43.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.0%.
- Mức dừng lỗ tham chiếu 69.36, mục tiêu 1 81.51, tỷ lệ lợi nhuận/rủi ro 2.03.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
