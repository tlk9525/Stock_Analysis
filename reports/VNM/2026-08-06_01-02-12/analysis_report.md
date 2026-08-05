# Báo cáo ngày 2026-08-06 - VNM

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,589 phiên.
- Giá đóng cửa: 58.60 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 58.29; SMA60 57.26; RSI14 51.7.
- MACD 0.867; đường tín hiệu 0.780; biểu đồ cột 0.087.
- ATR14 1.30; ATR% 2.2%; ADX14 25.6.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 51.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.6, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.05 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VINAMILK.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.34.
- P/B: 3.90.
- ROE: 33.9%.
- ROA: 19.8%.
- Market cap: 124,352.3 tỷ.
- Revenue Growth: 12.7%.
- Profit Growth: 28.0%.
- P/E 11.34: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.90: nên đọc cùng ROE và đặc thù ngành.
- ROE 33.9%: hiệu quả vốn chủ sở hữu tốt.
- ROA 19.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.91: thanh khoản ngắn hạn khá.
- Revenue Growth 12.7% YoY.
- Profit Growth 28.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.527; log-loss 0.683.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.534; AUC 0.556.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 89.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.9%; Sharpe -1.41; mức sụt giảm tối đa -35.8%.
- Mức độ quan trọng của đặc trưng: return_1d=10.49; close_vs_sma20=10.46; relative_strength_20d=10.37; return_3d=10.35; bb_position_20=10.22; return_2d=10.12.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 56.69; mục tiêu 1 64.35; mục tiêu 2 64.35.
- Tỷ lệ lợi nhuận/rủi ro 2.48; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 58.50 (-0.18%).
- P10/P90 cuối kỳ 53.46 / 64.35.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.527 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5271855010660981, AUC logistic=0.5557763132389998.
- Điều kiện phát hành tín hiệu: Probability 52.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.4104268544972223.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.7%.
- Mô hình Logistic đối chứng: 62.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.9%.
- Mức dừng lỗ tham chiếu 56.69, mục tiêu 1 64.35, tỷ lệ lợi nhuận/rủi ro 2.48.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
