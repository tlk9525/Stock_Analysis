# Báo cáo ngày 2026-08-06 - SAB

## Tổng quan

- Dữ liệu: 2016-12-06 -> 2026-08-06, 2,412 phiên.
- Giá đóng cửa: 43.70 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 43.79; SMA60 44.48; RSI14 46.7.
- MACD -0.062; đường tín hiệu -0.168; biểu đồ cột 0.106.
- ATR14 0.83; ATR% 1.9%; ADX14 17.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 46.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 17.8.
- Thanh khoản: Bình thường - 0.96 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: SABECO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.93.
- P/B: 2.91.
- ROE: 22.3%.
- ROA: 15.1%.
- Market cap: 56,945.8 tỷ.
- Revenue Growth: 1.2%.
- Profit Growth: -3.4%.
- P/E 11.93: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.91: nên đọc cùng ROE và đặc thù ngành.
- ROE 22.3%: hiệu quả vốn chủ sở hữu tốt.
- ROA 15.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.46: thanh khoản ngắn hạn khá.
- Revenue Growth 1.2% YoY.
- Profit Growth -3.4% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-25 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.514; AUC 0.509; log-loss 0.682.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.467.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 39.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -32.9%; Sharpe -1.24; mức sụt giảm tối đa -34.7%.
- Mức độ quan trọng của đặc trưng: stoch_k_14=13.20; market_return_20d=12.13; return_2d=11.00; rsi_14=10.67; return_1d=10.61; market_return_5d=10.53.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 42.46; mục tiêu 1 47.69; mục tiêu 2 47.69.
- Tỷ lệ lợi nhuận/rủi ro 2.58; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 43.39 (-0.70%).
- P10/P90 cuối kỳ 40.31 / 47.69.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.509 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.514 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 47.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2425154671395457.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.2%.
- Mô hình Logistic đối chứng: 47.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.4%.
- Mức dừng lỗ tham chiếu 42.46, mục tiêu 1 47.69, tỷ lệ lợi nhuận/rủi ro 2.58.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
