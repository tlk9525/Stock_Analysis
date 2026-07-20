# Báo cáo ngày 2026-07-20 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-07-20, 4,284 phiên.
- Giá đóng cửa: 25.75 nghìn VND/cp.
- Bias kỹ thuật: Tích cực (điểm 6).
- Xác suất XGBoost cho phiên kế tiếp tăng: 52.9%.
- Trạng thái tín hiệu: NO_EDGE.

## Phân tích kỹ thuật

- SMA20 24.08; SMA60 23.98; RSI14 64.2.
- MACD 0.285; tín hiệu 0.137; histogram 0.148.
- ATR14 0.85; ATR% 3.3%; ADX14 15.8.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 64.2.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 15.8.
- Thanh khoản: Đột biến - 1.60 lần trung bình.
- Stochastic: Cực trị - %K 83.7, %D 82.2.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 18.38.
- P/B: 2.00.
- ROE: 10.0%.
- ROA: 3.0%.
- Market cap: 34,288.6 tỷ.
- Revenue Growth: 46.7%.
- Profit Growth: 28.2%.
- P/E 18.38: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.00: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.55: thanh khoản ngắn hạn khá.
- Revenue Growth 46.7% YoY.
- Profit Growth 28.2% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-09 -> 2026-07-17.
- XGBoost balanced accuracy: 0.517; AUC: 0.536; log-loss: 0.694.
- Logistic baseline balanced accuracy: 0.508; AUC: 0.518.
- Majority baseline balanced accuracy: 0.500.
- Vòng boosting tốt nhất: 22.
- Thẩm định: expanding_walk_forward; 6 fold; khoảng cách 1 phiên.
- Backtest sau chi phí: tổng lợi nhuận -35.8%; Sharpe -1.30; drawdown tối đa -37.9%.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.58; return_1d=11.93; atr_pct_14=11.35; rsi_14=11.25; adx_14=10.53; macd_hist=10.15.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; risk/lệnh 1.0%.
- Stop 24.47; mục tiêu 1 29.26; mục tiêu 2 29.26.
- Reward/risk 2.40; position 0 cp.

## Dự báo 20 phiên

- P50 cuối kỳ 25.47 (-1.08%).
- P10/P90 cuối kỳ 22.35 / 29.26.

## Khung hành động tham khảo

- Trạng thái tín hiệu: NO_EDGE.
- Điều kiện phát hành tín hiệu: AUC 0.536 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.517 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.35837569, Sharpe=-1.3019168851384524.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Bias kỹ thuật: Tích cực.
- XGBoost ước tính xác suất phiên kế tiếp tăng: 52.9%.
- Mốc so sánh Logistic: 46.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 45.7%.
- Stop tham chiếu 24.47, mục tiêu 1 29.26, R/R 2.40.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
