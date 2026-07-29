# Báo cáo ngày 2026-07-23 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-07-23, 2,148 phiên.
- Giá đóng cửa: 132.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 144.70; SMA60 145.55; RSI14 39.4.
- MACD -3.322; đường tín hiệu -1.294; biểu đồ cột -2.028.
- ATR14 5.85; ATR% 4.4%; ADX14 21.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 39.4.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Đi ngang - ADX 21.9.
- Thanh khoản: Bình thường - 1.04 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.05.
- P/B: 1.99.
- ROE: 27.8%.
- ROA: 8.4%.
- Market cap: 521,230.6 tỷ.
- Revenue Growth: 314.8%.
- Profit Growth: 850.3%.
- P/E 8.05: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.99: nên đọc cùng ROE và đặc thù ngành.
- ROE 27.8%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.4%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 2.19: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.33: thanh khoản ngắn hạn khá.
- Revenue Growth 314.8% YoY.
- Profit Growth 850.3% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-10-24 -> 2026-07-22.
- XGBoost: độ chính xác cân bằng 0.499; AUC 0.516; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.534; AUC 0.557.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 3.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -8.6%; Sharpe -0.13; mức sụt giảm tối đa -16.5%.
- Mức độ quan trọng của đặc trưng: range_pct=14.10; atr_pct_14=11.63; return_3d=9.47; stoch_k_14=9.45; volatility_20d=9.08; macd_hist_pct=8.95.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 125.33; mục tiêu 1 158.70; mục tiêu 2 163.22.
- Tỷ lệ lợi nhuận/rủi ro 3.55; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 130.13 (-1.41%).
- P10/P90 cuối kỳ 105.20 / 163.22.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.516 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.499 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5155541125541125, AUC logistic=0.5565627705627706.
- Điều kiện phát hành tín hiệu: Probability 50.4% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -5 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.0860932100000007, Sharpe=-0.12576479585347888.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.4%.
- Mô hình Logistic đối chứng: 49.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.6%.
- Mức dừng lỗ tham chiếu 125.33, mục tiêu 1 158.70, tỷ lệ lợi nhuận/rủi ro 3.55.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
