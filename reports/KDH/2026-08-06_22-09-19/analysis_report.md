# Báo cáo ngày 2026-08-06 - KDH

## Tổng quan

- Dữ liệu: 2010-02-01 -> 2026-08-06, 4,115 phiên.
- Giá đóng cửa: 17.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 18.16; SMA60 21.05; RSI14 37.2.
- MACD -0.883; đường tín hiệu -1.077; biểu đồ cột 0.194.
- ATR14 0.65; ATR% 3.6%; ADX14 48.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 37.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 48.8, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.74 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Nhà Khang Điền.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.59.
- P/B: 1.09.
- ROE: 9.5%.
- ROA: 4.8%.
- Market cap: 20,368.2 tỷ.
- Revenue Growth: -84.7%.
- Profit Growth: 276.7%.
- P/E 11.59: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.09: nên đọc cùng ROE và đặc thù ngành.
- ROA 4.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 10.06: thanh khoản ngắn hạn khá.
- Revenue Growth -84.7% YoY.
- Profit Growth 276.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.499; AUC 0.494; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.497.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 8.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 2.5%; Sharpe 0.16; mức sụt giảm tối đa -8.8%.
- Mức độ quan trọng của đặc trưng: return_5d=13.68; return_1d=12.17; return_3d=11.55; macd_hist_pct=10.36; volatility_20d=10.08; relative_strength_20d=9.91.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 16.83; mục tiêu 1 20.40; mục tiêu 2 20.75.
- Tỷ lệ lợi nhuận/rủi ro 2.36; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 17.49 (-1.76%).
- P10/P90 cuối kỳ 15.55 / 20.40.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.494 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.499 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4936828853970758, AUC logistic=0.49728508159922347.
- Điều kiện phát hành tín hiệu: Probability 49.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Mô hình Logistic đối chứng: 47.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.1%.
- Mức dừng lỗ tham chiếu 16.83, mục tiêu 1 20.40, tỷ lệ lợi nhuận/rủi ro 2.36.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
