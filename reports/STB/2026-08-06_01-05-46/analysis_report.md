# Báo cáo ngày 2026-08-06 - STB

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,590 phiên.
- Giá đóng cửa: 73.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 71.78; SMA60 71.26; RSI14 55.3.
- MACD 0.371; đường tín hiệu 0.274; biểu đồ cột 0.098.
- ATR14 2.07; ATR% 2.8%; ADX14 14.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 14.5.
- Thanh khoản: Thấp - 0.66 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 45.36.
- P/B: 2.22.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 139,694.5 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 45.36: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.22: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.503; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.513; AUC 0.509.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.21; return_1d=11.76; return_5d=10.98; return_2d=10.53; beta_60d=10.42; relative_strength_20d=10.28.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.55; mục tiêu 1 83.24; mục tiêu 2 83.24.
- Tỷ lệ lợi nhuận/rủi ro 3.21; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 72.27 (-1.28%).
- P10/P90 cuối kỳ 63.55 / 83.24.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.503 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5034637205135861, AUC logistic=0.5093684681994626.
- Điều kiện phát hành tín hiệu: Probability 50.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48234700295803407.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.6%.
- Mô hình Logistic đối chứng: 49.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.1%.
- Mức dừng lỗ tham chiếu 70.55, mục tiêu 1 83.24, tỷ lệ lợi nhuận/rủi ro 3.21.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
