# Báo cáo ngày 2026-08-06 - PLX

## Tổng quan

- Dữ liệu: 2017-04-21 -> 2026-08-05, 2,320 phiên.
- Giá đóng cửa: 34.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 33.25; SMA60 36.40; RSI14 52.6.
- MACD -0.699; đường tín hiệu -1.021; biểu đồ cột 0.321.
- ATR14 1.21; ATR% 3.5%; ADX14 27.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 27.4, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.16 lần trung bình.
- Stochastic: Cực trị - %K 87.3, %D 67.3.

## Phân tích cơ bản

- Doanh nghiệp: Petrolimex.
- Ngành: Oil & Gas.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 13.19.
- P/B: 1.65.
- ROE: 12.5%.
- ROA: 3.5%.
- Market cap: 42,501.3 tỷ.
- Revenue Growth: 78.0%.
- Profit Growth: 105.6%.
- P/E 13.19: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.65: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 2.01: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.06: thanh khoản ngắn hạn khá.
- Revenue Growth 78.0% YoY.
- Profit Growth 105.6% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-03 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.506; AUC 0.511; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.518; AUC 0.481.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 35.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -53.5%; Sharpe -1.74; mức sụt giảm tối đa -55.7%.
- Mức độ quan trọng của đặc trưng: return_1d=11.50; return_2d=10.80; volatility_20d=9.96; return_3d=9.79; atr_pct_14=9.63; beta_60d=9.25.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 32.44; mục tiêu 1 40.89; mục tiêu 2 40.89.
- Tỷ lệ lợi nhuận/rủi ro 3.27; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 33.70 (-1.59%).
- P10/P90 cuối kỳ 28.24 / 40.89.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.511 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.506 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.5351089299999998, Sharpe=-1.7369172296951783.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Mô hình Logistic đối chứng: 48.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.7%.
- Mức dừng lỗ tham chiếu 32.44, mục tiêu 1 40.89, tỷ lệ lợi nhuận/rủi ro 3.27.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
