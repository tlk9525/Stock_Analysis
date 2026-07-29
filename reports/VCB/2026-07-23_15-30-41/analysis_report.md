# Báo cáo ngày 2026-07-23 - VCB

## Tổng quan

- Dữ liệu: 2009-06-30 -> 2026-07-23, 4,259 phiên.
- Giá đóng cửa: 54.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 59.30; SMA60 60.63; RSI14 18.6.
- MACD -1.573; đường tín hiệu -0.929; biểu đồ cột -0.644.
- ATR14 1.22; ATR% 2.3%; ADX14 27.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Quá bán - RSI 18.6.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Xu hướng giảm - ADX 27.2, -DI vượt +DI.
- Thanh khoản: Đột biến - 1.78 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Vietcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.67.
- P/B: 1.95.
- ROE: 16.1%.
- ROA: 1.5%.
- Market cap: 455,384.3 tỷ.
- Revenue Growth: 22.7%.
- Profit Growth: 8.7%.
- P/E 12.67: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.95: nên đọc cùng ROE và đặc thù ngành.
- ROE 16.1%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 9.90: đòn bẩy cao, cần đọc theo ngành.
- NPL 0.6%: đang ở mức kiểm soát.
- Revenue Growth 22.7% YoY.
- Profit Growth 8.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-11-14 -> 2026-07-22.
- XGBoost: độ chính xác cân bằng 0.492; AUC 0.422; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.497; AUC 0.471.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 19.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -24.2%; Sharpe -1.56; mức sụt giảm tối đa -25.0%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=12.46; return_1d=11.49; atr_pct_14=10.97; macd_pct=10.25; return_20d=10.23; bb_position_20=9.74.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 52.17; mục tiêu 1 59.79; mục tiêu 2 62.58.
- Tỷ lệ lợi nhuận/rủi ro 2.62; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 53.36 (-1.19%).
- P10/P90 cuối kỳ 48.96 / 59.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.422 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.492 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4215850216517167, AUC logistic=0.47062519331889885.
- Điều kiện phát hành tín hiệu: Probability 48.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -4 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2422861599999997, Sharpe=-1.561934357541227.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.9%.
- Mô hình Logistic đối chứng: 53.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.0%.
- Mức dừng lỗ tham chiếu 52.17, mục tiêu 1 59.79, tỷ lệ lợi nhuận/rủi ro 2.62.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
