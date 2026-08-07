# Báo cáo ngày 2026-08-06 - PLX

## Tổng quan

- Dữ liệu: 2017-04-21 -> 2026-08-06, 2,321 phiên.
- Giá đóng cửa: 33.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 33.20; SMA60 36.32; RSI14 49.2.
- MACD -0.598; đường tín hiệu -0.936; biểu đồ cột 0.338.
- ATR14 1.21; ATR% 3.6%; ADX14 25.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 25.6, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.79 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Petrolimex.
- Ngành: Oil & Gas.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 13.51.
- P/B: 1.69.
- ROE: 12.5%.
- ROA: 3.5%.
- Market cap: 43,517.8 tỷ.
- Revenue Growth: 78.0%.
- Profit Growth: 105.6%.
- P/E 13.51: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.69: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 2.01: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.06: thanh khoản ngắn hạn khá.
- Revenue Growth 78.0% YoY.
- Profit Growth 105.6% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-03 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.505; AUC 0.510; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.480.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 35.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -54.6%; Sharpe -1.79; mức sụt giảm tối đa -55.7%.
- Mức độ quan trọng của đặc trưng: return_2d=13.45; return_1d=12.10; excess_return_1d=9.83; volatility_20d=9.70; atr_pct_14=9.55; return_3d=9.19.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.88; mục tiêu 1 40.22; mục tiêu 2 40.22.
- Tỷ lệ lợi nhuận/rủi ro 3.19; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 33.16 (-1.61%).
- P10/P90 cuối kỳ 27.77 / 40.22.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.505 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 51.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.785182045901097.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.0%.
- Mô hình Logistic đối chứng: 50.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.9%.
- Mức dừng lỗ tham chiếu 31.88, mục tiêu 1 40.22, tỷ lệ lợi nhuận/rủi ro 3.19.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
