# Báo cáo ngày 2026-08-06 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-08-06, 4,269 phiên.
- Giá đóng cửa: 59.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 57.25; SMA60 60.19; RSI14 53.7.
- MACD -0.225; đường tín hiệu -0.841; biểu đồ cột 0.616.
- ATR14 1.45; ATR% 2.5%; ADX14 28.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 53.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.6, +DI vượt -DI.
- Thanh khoản: Thấp - 0.58 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.90.
- P/B: 1.99.
- ROE: 17.9%.
- ROA: 1.7%.
- Market cap: 495,491.5 tỷ.
- Revenue Growth: 47.6%.
- Profit Growth: 64.7%.
- P/E 11.90: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.99: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.9%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.69: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 47.6% YoY.
- Profit Growth 64.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.467; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.477; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 30.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -26.4%; Sharpe -2.25; mức sụt giảm tối đa -26.4%.
- Mức độ quan trọng của đặc trưng: macd_pct=12.40; rsi_14=12.39; return_1d=12.05; month_of_year=11.03; market_return_20d=10.86; atr_pct_14=10.34.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 56.82; mục tiêu 1 66.01; mục tiêu 2 66.01.
- Tỷ lệ lợi nhuận/rủi ro 2.72; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.08 (-1.57%).
- P10/P90 cuối kỳ 53.08 / 66.01.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.467 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4671939970367538, AUC logistic=0.4902260670075993.
- Điều kiện phát hành tín hiệu: Probability 49.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.26417005000000016, Sharpe=-2.25441076021559.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.7%.
- Mô hình Logistic đối chứng: 46.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.7%.
- Mức dừng lỗ tham chiếu 56.82, mục tiêu 1 66.01, tỷ lệ lợi nhuận/rủi ro 2.72.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
