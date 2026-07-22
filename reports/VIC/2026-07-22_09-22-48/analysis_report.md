# Báo cáo ngày 2026-07-22 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-07-22, 4,577 phiên.
- Giá đóng cửa: 215.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 220.32; SMA60 215.11; RSI14 48.0.
- MACD 1.834; đường tín hiệu 2.909; biểu đồ cột -1.075.
- ATR14 6.36; ATR% 3.0%; ADX14 12.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 48.0.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Đi ngang - ADX 12.0.
- Thanh khoản: Thấp - 0.01 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 144.28.
- P/B: 11.36.
- ROE: 7.9%.
- ROA: 1.1%.
- Market cap: 1,686,723.1 tỷ.
- Revenue Growth: 24.5%.
- Profit Growth: 4.3%.
- P/E 144.28: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 11.36: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.9%: hiệu quả vốn còn yếu.
- Debt/Equity 6.67: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.07: thanh khoản ngắn hạn khá.
- Revenue Growth 24.5% YoY.
- Profit Growth 4.3% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-11 -> 2026-07-21.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.527; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.510; AUC 0.514.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 35.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -0.9%; Sharpe 0.01; mức sụt giảm tối đa -18.5%.
- Mức độ quan trọng của đặc trưng: macd=11.35; bb_position_20=9.64; range_pct=9.41; close_vs_sma60=9.10; rsi_14=9.09; stoch_k_14=9.00.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 212.96; mục tiêu 1 232.00; mục tiêu 2 264.79.
- Tỷ lệ lợi nhuận/rủi ro 4.41; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 214.11 (-0.60%).
- P10/P90 cuối kỳ 172.67 / 264.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.527 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.520 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 49.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -5 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.0087462499999994, Sharpe=0.012635973469590604.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.0%.
- Mô hình Logistic đối chứng: 56.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.6%.
- Mức dừng lỗ tham chiếu 212.96, mục tiêu 1 232.00, tỷ lệ lợi nhuận/rủi ro 4.41.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
