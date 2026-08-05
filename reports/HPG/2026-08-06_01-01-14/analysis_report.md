# Báo cáo ngày 2026-08-06 - HPG

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,589 phiên.
- Giá đóng cửa: 22.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.72; SMA60 23.06; RSI14 48.9.
- MACD -0.295; đường tín hiệu -0.485; biểu đồ cột 0.189.
- ATR14 0.58; ATR% 2.6%; ADX14 39.7.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 48.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 39.7, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.02 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.05.
- P/B: 1.33.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 187,011.7 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 8.05: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.33: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.14: thanh khoản ngắn hạn khá.
- Revenue Growth 53.6% YoY.
- Profit Growth 49.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.523; AUC 0.579; log-loss 0.677.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.516; AUC 0.566.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 125.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -34.4%; Sharpe -1.71; mức sụt giảm tối đa -36.7%.
- Mức độ quan trọng của đặc trưng: adx_14=10.77; market_return_1d=9.59; bb_position_20=9.29; day_of_week=9.07; relative_strength_20d=9.00; close_vs_sma20=8.70.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.13; mục tiêu 1 24.11; mục tiêu 2 24.11.
- Tỷ lệ lợi nhuận/rủi ro 2.04; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 21.80 (-0.89%).
- P10/P90 cuối kỳ 19.96 / 24.11.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 48.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.34449049999999937, Sharpe=-1.7072970756168129.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.8%.
- Mô hình Logistic đối chứng: 52.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.0%.
- Mức dừng lỗ tham chiếu 21.13, mục tiêu 1 24.11, tỷ lệ lợi nhuận/rủi ro 2.04.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
