# Báo cáo ngày 2026-08-06 - VIC

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,588 phiên.
- Giá đóng cửa: 220.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 217.14; SMA60 214.09; RSI14 54.3.
- MACD 0.487; đường tín hiệu 0.508; biểu đồ cột -0.021.
- ATR14 7.09; ATR% 3.2%; ADX14 13.0.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 54.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 13.0.
- Thanh khoản: Đột biến - 1.60 lần trung bình.
- Stochastic: Cực trị - %K 83.3, %D 70.8.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 74.64.
- P/B: 9.96.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,692,156.6 tỷ.
- Revenue Growth: 154.0%.
- P/E 74.64: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 9.96: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 6.24: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.05: thanh khoản ngắn hạn khá.
- Revenue Growth 154.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.506; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.518; AUC 0.533.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: range_pct=21.37; corr_60d=17.31; market_volatility_20d=15.46; return_kurtosis_20d=15.24; market_return_20d=14.13; excess_return_20d=10.20.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 211.95; mục tiêu 1 268.36; mục tiêu 2 268.36.
- Tỷ lệ lợi nhuận/rủi ro 5.16; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 217.31 (-1.22%).
- P10/P90 cuối kỳ 175.75 / 268.36.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.506 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5064351073762838, AUC logistic=0.5331914098972923.
- Điều kiện phát hành tín hiệu: Probability 49.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7826609992040359.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.9%.
- Mô hình Logistic đối chứng: 57.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.0%.
- Mức dừng lỗ tham chiếu 211.95, mục tiêu 1 268.36, tỷ lệ lợi nhuận/rủi ro 5.16.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
