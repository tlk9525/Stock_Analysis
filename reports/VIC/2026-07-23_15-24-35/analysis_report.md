# Báo cáo ngày 2026-07-23 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-07-23, 4,578 phiên.
- Giá đóng cửa: 214.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 61.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 219.10; SMA60 214.70; RSI14 48.4.
- MACD 0.489; đường tín hiệu 2.256; biểu đồ cột -1.767.
- ATR14 7.84; ATR% 3.7%; ADX14 14.6.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 48.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 14.6.
- Thanh khoản: Bình thường - 1.32 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 134.19.
- P/B: 10.56.
- ROE: 7.9%.
- ROA: 1.1%.
- Market cap: 1,568,737.9 tỷ.
- Revenue Growth: 24.5%.
- Profit Growth: 4.3%.
- P/E 134.19: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 10.56: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.9%: hiệu quả vốn còn yếu.
- Debt/Equity 6.67: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.07: thanh khoản ngắn hạn khá.
- Revenue Growth 24.5% YoY.
- Profit Growth 4.3% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-11 -> 2026-07-22.
- XGBoost: độ chính xác cân bằng 0.497; AUC 0.505; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.492; AUC 0.525.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 45.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -28.4%; Sharpe -0.83; mức sụt giảm tối đa -34.0%.
- Mức độ quan trọng của đặc trưng: month_of_year=11.03; return_kurtosis_20d=10.71; rsi_14=10.70; return_10d=10.56; stoch_k_14=10.36; bb_position_20=10.19.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 212.55; mục tiêu 1 228.90; mục tiêu 2 263.29.
- Tỷ lệ lợi nhuận/rủi ro 5.48; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 212.31 (-0.79%).
- P10/P90 cuối kỳ 171.05 / 263.29.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.505 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.497 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5048104891036829, AUC logistic=0.5250443758297162.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2844512600000003, Sharpe=-0.8337315681098532.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 61.3%.
- Mô hình Logistic đối chứng: 62.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.1%.
- Mức dừng lỗ tham chiếu 212.55, mục tiêu 1 228.90, tỷ lệ lợi nhuận/rủi ro 5.48.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
