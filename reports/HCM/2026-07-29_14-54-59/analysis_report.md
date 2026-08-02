# Báo cáo ngày 2026-07-29 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-07-29, 4,291 phiên.
- Giá đóng cửa: 25.25 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.77; SMA60 24.25; RSI14 55.6.
- MACD 0.407; đường tín hiệu 0.365; biểu đồ cột 0.042.
- ATR14 0.95; ATR% 3.8%; ADX14 14.4.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 14.4.
- Thanh khoản: Thấp - 0.38 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.06.
- P/B: 1.97.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 34,153.6 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.06: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.97: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-07-28.
- XGBoost: độ chính xác cân bằng 0.514; AUC 0.510; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.505; AUC 0.543.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -9.1%; Sharpe -0.31; mức sụt giảm tối đa -14.6%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=14.01; volatility_20d=13.52; return_1d=13.44; atr_pct_14=11.77; adx_14=11.68; return_2d=11.15.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.01; mục tiêu 1 28.76; mục tiêu 2 28.76.
- Tỷ lệ lợi nhuận/rủi ro 2.47; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.01 (-0.95%).
- P10/P90 cuối kỳ 21.92 / 28.76.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.514 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5100529762649647, AUC logistic=0.5430108872481542.
- Điều kiện phát hành tín hiệu: Probability 51.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.09095504999999948, Sharpe=-0.31465122834304093.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.1%.
- Mô hình Logistic đối chứng: 49.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.5%.
- Mức dừng lỗ tham chiếu 24.01, mục tiêu 1 28.76, tỷ lệ lợi nhuận/rủi ro 2.47.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
