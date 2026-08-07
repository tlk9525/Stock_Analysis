# Báo cáo ngày 2026-08-06 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,588 phiên.
- Giá đóng cửa: 218.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 217.03; SMA60 213.91; RSI14 52.9.
- MACD 0.624; đường tín hiệu 0.531; biểu đồ cột 0.092.
- ATR14 6.82; ATR% 3.1%; ADX14 12.7.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.7.
- Thanh khoản: Bình thường - 1.20 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 75.33.
- P/B: 10.05.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,707,681.0 tỷ.
- Revenue Growth: 154.0%.
- P/E 75.33: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 10.05: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 6.24: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.05: thanh khoản ngắn hạn khá.
- Revenue Growth 154.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.517; AUC 0.532.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: excess_return_20d=20.61; market_return_20d=20.01; market_volatility_20d=15.55; corr_60d=15.46; return_kurtosis_20d=15.19; return_skew_20d=14.01.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 211.77; mục tiêu 1 266.30; mục tiêu 2 266.30.
- Tỷ lệ lợi nhuận/rủi ro 5.71; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 215.03 (-1.72%).
- P10/P90 cuối kỳ 174.36 / 266.30.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5066899100065558, AUC logistic=0.5323544311341558.
- Điều kiện phát hành tín hiệu: Probability 50.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7814308982273805.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.4%.
- Mô hình Logistic đối chứng: 60.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 211.77, mục tiêu 1 266.30, tỷ lệ lợi nhuận/rủi ro 5.71.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
