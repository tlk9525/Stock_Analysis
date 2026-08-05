# Báo cáo ngày 2026-08-06 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-05, 4,268 phiên.
- Giá đóng cửa: 59.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 57.33; SMA60 60.21; RSI14 55.2.
- MACD -0.344; đường tín hiệu -0.995; biểu đồ cột 0.651.
- ATR14 1.49; ATR% 2.5%; ADX14 30.3.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 30.3, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.72 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.04.
- P/B: 2.02.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 501,340.5 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 12.04: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.468; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.477; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.26; mức sụt giảm tối đa -26.4%.
- Mức độ quan trọng của đặc trưng: macd_pct=12.80; return_1d=11.98; month_of_year=11.64; day_of_week=10.90; market_return_20d=10.69; relative_strength_20d=10.66.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 57.07; mục tiêu 1 66.30; mục tiêu 2 66.30.
- Tỷ lệ lợi nhuận/rủi ro 2.65; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.39 (-1.53%).
- P10/P90 cuối kỳ 53.26 / 66.30.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.468 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4675529366676248, AUC logistic=0.4903612149084986.
- Điều kiện phát hành tín hiệu: Probability 51.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.2561214748632072.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.7%.
- Mô hình Logistic đối chứng: 47.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.7%.
- Mức dừng lỗ tham chiếu 57.07, mục tiêu 1 66.30, tỷ lệ lợi nhuận/rủi ro 2.65.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
