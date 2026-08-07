# Báo cáo ngày 2026-08-06 - STB

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,590 phiên.
- Giá đóng cửa: 72.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 71.84; SMA60 71.24; RSI14 51.1.
- MACD 0.335; đường tín hiệu 0.286; biểu đồ cột 0.049.
- ATR14 2.02; ATR% 2.8%; ADX14 13.6.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 51.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 13.6.
- Thanh khoản: Thấp - 0.36 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 44.81.
- P/B: 2.20.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 137,997.8 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 44.81: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.20: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.503; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.513; AUC 0.509.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.22; return_5d=11.47; beta_60d=11.14; return_1d=11.08; return_10d=10.98; market_volatility_20d=10.95.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.53; mục tiêu 1 81.81; mục tiêu 2 81.81.
- Tỷ lệ lợi nhuận/rủi ro 4.54; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 71.28 (-1.27%).
- P10/P90 cuối kỳ 62.71 / 81.81.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.503 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5031645569620253, AUC logistic=0.5093447505584512.
- Điều kiện phát hành tín hiệu: Probability 53.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.4820189082562739.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.3%.
- Mô hình Logistic đối chứng: 51.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.8%.
- Mức dừng lỗ tham chiếu 70.53, mục tiêu 1 81.81, tỷ lệ lợi nhuận/rủi ro 4.54.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
