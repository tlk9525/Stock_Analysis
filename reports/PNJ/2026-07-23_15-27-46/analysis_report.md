# Báo cáo ngày 2026-07-23 - PNJ

## Tổng quan

- Dữ liệu: 2009-03-23 -> 2026-07-23, 4,315 phiên.
- Giá đóng cửa: 33.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -7).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 49.71; SMA60 60.73; RSI14 18.1.
- MACD -7.248; đường tín hiệu -5.875; biểu đồ cột -1.373.
- ATR14 2.67; ATR% 8.1%; ADX14 50.3.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Quá bán - RSI 18.1.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Xu hướng giảm - ADX 50.3, -DI vượt +DI.
- Thanh khoản: Thấp - 0.10 lần trung bình.
- Stochastic: Cực trị - %K 0.0, %D 0.0.

## Phân tích cơ bản

- Doanh nghiệp: Vàng Phú Nhuận.
- Ngành: Personal & Household Goods.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 5.00.
- P/B: 1.26.
- ROE: 28.0%.
- ROA: 19.5%.
- Market cap: 18,166.1 tỷ.
- Revenue Growth: 79.0%.
- Profit Growth: 116.5%.
- P/E 5.00: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.26: nên đọc cùng ROE và đặc thù ngành.
- ROE 28.0%: hiệu quả vốn chủ sở hữu tốt.
- ROA 19.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 3.44: thanh khoản ngắn hạn khá.
- Revenue Growth 79.0% YoY.
- Profit Growth 116.5% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-11 -> 2026-07-22.
- XGBoost: độ chính xác cân bằng 0.495; AUC 0.510; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.492; AUC 0.495.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 37.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -17.0%; Sharpe -0.70; mức sụt giảm tối đa -26.2%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=9.01; day_of_week=8.60; volume_ratio_20=8.56; close_vs_sma60=8.31; volume_z_20=8.23; return_2d=8.13.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 32.72; mục tiêu 1 38.35; mục tiêu 2 64.80.
- Tỷ lệ lợi nhuận/rủi ro 10.35; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 33.67 (1.88%).
- P10/P90 cuối kỳ 27.94 / 38.35.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.495 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -7 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.17002153000000042, Sharpe=-0.7009693370364456.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.9%.
- Mô hình Logistic đối chứng: 61.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 56.4%.
- Mức dừng lỗ tham chiếu 32.72, mục tiêu 1 38.35, tỷ lệ lợi nhuận/rủi ro 10.35.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
