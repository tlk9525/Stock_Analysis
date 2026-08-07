# Báo cáo ngày 2026-08-06 - POW

## Tổng quan

- Dữ liệu: 2018-03-06 -> 2026-08-06, 2,096 phiên.
- Giá đóng cửa: 13.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 13.67; SMA60 13.94; RSI14 42.6.
- MACD -0.124; đường tín hiệu -0.145; biểu đồ cột 0.021.
- ATR14 0.41; ATR% 3.0%; ADX14 31.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 42.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.1, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.06 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Điện lực Dầu khí Việt Nam.
- Ngành: Utilities.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.58.
- P/B: 1.02.
- ROE: 16.5%.
- ROA: 6.5%.
- Market cap: 42,336.3 tỷ.
- Revenue Growth: 116.1%.
- Profit Growth: 484.1%.
- P/E 6.58: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 6.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.37: thanh khoản ngắn hạn khá.
- Revenue Growth 116.1% YoY.
- Profit Growth 484.1% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-12-21 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.531; AUC 0.586; log-loss 0.672.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.541; AUC 0.550.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 104.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -35.8%; Sharpe -1.42; mức sụt giảm tối đa -43.2%.
- Mức độ quan trọng của đặc trưng: return_1d=10.20; stoch_k_14=9.87; return_20d=9.00; macd_hist_pct=8.86; atr_pct_14=8.58; relative_strength_20d=8.34.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 12.79; mục tiêu 1 15.11; mục tiêu 2 15.11.
- Tỷ lệ lợi nhuận/rủi ro 2.43; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.34 (-0.48%).
- P10/P90 cuối kỳ 11.82 / 15.11.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 53.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3577952299999997, Sharpe=-1.4181049884618542.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.4%.
- Mô hình Logistic đối chứng: 59.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.6%.
- Mức dừng lỗ tham chiếu 12.79, mục tiêu 1 15.11, tỷ lệ lợi nhuận/rủi ro 2.43.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
