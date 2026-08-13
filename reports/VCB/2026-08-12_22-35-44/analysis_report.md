# Báo cáo ngày 2026-08-12 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-12, 4,273 phiên.
- Giá đóng cửa: 59.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 57.43; SMA60 60.00; RSI14 55.7.
- MACD 0.246; đường tín hiệu -0.261; biểu đồ cột 0.507.
- ATR14 1.38; ATR% 2.3%; ADX14 26.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.4, +DI vượt -DI.
- Thanh khoản: Thấp - 0.46 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.00.
- P/B: 2.01.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 499,669.4 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 12.00: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T09:03:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.468; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.478; AUC 0.489.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.25; mức sụt giảm tối đa -26.4%.
- Mức độ quan trọng của đặc trưng: rsi_14=12.14; return_1d=11.69; month_of_year=10.87; atr_pct_14=10.75; day_of_week=10.74; market_return_20d=10.35.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.40; mục tiêu 1 61.00; mục tiêu 2 66.79.
- Tỷ lệ lợi nhuận/rủi ro 1.67; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.81 (-1.49%).
- P10/P90 cuối kỳ 53.70 / 66.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.468 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4684203062960862, AUC logistic=0.4890527509926262.
- Điều kiện phát hành tín hiệu: Probability 47.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.247606612317961.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.7%.
- Mô hình Logistic đối chứng: 42.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.6%.
- Mức dừng lỗ tham chiếu 59.40, mục tiêu 1 61.00, tỷ lệ lợi nhuận/rủi ro 1.67.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
