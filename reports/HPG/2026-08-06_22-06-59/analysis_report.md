# Báo cáo ngày 2026-08-06 - HPG

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,589 phiên.
- Giá đóng cửa: 21.85 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.65; SMA60 23.01; RSI14 47.1.
- MACD -0.267; đường tín hiệu -0.441; biểu đồ cột 0.174.
- ATR14 0.57; ATR% 2.6%; ADX14 37.7.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 47.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 37.7, -DI vượt +DI.
- Thanh khoản: Thấp - 0.52 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.00.
- P/B: 1.32.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 185,745.2 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 8.00: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.14: thanh khoản ngắn hạn khá.
- Revenue Growth 53.6% YoY.
- Profit Growth 49.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.587; log-loss 0.675.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.516; AUC 0.565.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 119.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -29.9%; Sharpe -1.42; mức sụt giảm tối đa -37.0%.
- Mức độ quan trọng của đặc trưng: adx_14=10.38; market_return_1d=9.40; excess_return_5d=9.12; bb_position_20=9.07; macd_hist_pct=9.04; return_10d=8.95.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 20.99; mục tiêu 1 23.87; mục tiêu 2 23.87.
- Tỷ lệ lợi nhuận/rủi ro 1.98; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.65 (-0.93%).
- P10/P90 cuối kỳ 19.84 / 23.87.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.520 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 53.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.29859459999999893, Sharpe=-1.4169446005882858.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.5%.
- Mô hình Logistic đối chứng: 53.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.8%.
- Mức dừng lỗ tham chiếu 20.99, mục tiêu 1 23.87, tỷ lệ lợi nhuận/rủi ro 1.98.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
