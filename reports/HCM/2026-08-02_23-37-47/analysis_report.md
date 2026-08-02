# Báo cáo ngày 2026-08-02 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-07-31, 4,293 phiên.
- Giá đóng cửa: 25.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 45.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.82; SMA60 24.29; RSI14 52.2.
- MACD 0.378; đường tín hiệu 0.377; biểu đồ cột 0.001.
- ATR14 0.94; ATR% 3.7%; ADX14 13.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 13.5.
- Thanh khoản: Thấp - 0.67 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 18.88.
- P/B: 1.95.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 33,748.6 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 18.88: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.95: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-11-03 -> 2026-07-30.
- XGBoost: độ chính xác cân bằng 0.496; AUC 0.524; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.566.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 69.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -31.1%; Sharpe -1.24; mức sụt giảm tối đa -31.1%.
- Mức độ quan trọng của đặc trưng: volatility_20d=10.88; corr_60d=10.44; rsi_14=10.33; return_1d=10.07; excess_return_20d=9.73; close_vs_sma20=9.70.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.05; mục tiêu 1 28.64; mục tiêu 2 28.64.
- Tỷ lệ lợi nhuận/rủi ro 3.25; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 24.91 (-0.35%).
- P10/P90 cuối kỳ 21.87 / 28.64.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.524 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.496 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5235953282828283, AUC logistic=0.5661826599326599.
- Điều kiện phát hành tín hiệu: Probability 45.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.31071326000000044, Sharpe=-1.2435942200972723.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 45.9%.
- Mô hình Logistic đối chứng: 47.3%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.6%.
- Mức dừng lỗ tham chiếu 24.05, mục tiêu 1 28.64, tỷ lệ lợi nhuận/rủi ro 3.25.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
