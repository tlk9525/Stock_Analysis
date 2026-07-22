# Báo cáo ngày 2026-07-22 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-07-22, 4,286 phiên.
- Giá đóng cửa: 25.75 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.31; SMA60 24.08; RSI14 64.2.
- MACD 0.427; đường tín hiệu 0.232; biểu đồ cột 0.195.
- ATR14 0.83; ATR% 3.2%; ADX14 15.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 64.2.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 15.5.
- Thanh khoản: Thấp - 0.29 lần trung bình.
- Stochastic: Cực trị - %K 83.7, %D 83.7.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 19.30.
- P/B: 2.00.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 34,761.1 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 19.30: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.00: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-07-21.
- XGBoost: độ chính xác cân bằng 0.514; AUC 0.510; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.505; AUC 0.542.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -9.1%; Sharpe -0.32; mức sụt giảm tối đa -14.6%.
- Mức độ quan trọng của đặc trưng: return_1d=13.27; volatility_20d=12.46; rsi_14=12.06; close_vs_sma20=11.75; adx_14=11.03; atr_pct_14=10.92.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.50; mục tiêu 1 29.39; mục tiêu 2 29.39.
- Tỷ lệ lợi nhuận/rủi ro 2.55; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.51 (-0.91%).
- P10/P90 cuối kỳ 22.32 / 29.39.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.514 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5098544469831598, AUC logistic=0.5417280189557417.
- Điều kiện phát hành tín hiệu: Probability 51.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.09095504999999948, Sharpe=-0.31578310746675703.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.6%.
- Mô hình Logistic đối chứng: 42.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.6%.
- Mức dừng lỗ tham chiếu 24.50, mục tiêu 1 29.39, tỷ lệ lợi nhuận/rủi ro 2.55.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
