# Báo cáo ngày 2026-07-22 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-07-22, 2,033 phiên.
- Giá đóng cửa: 29.85 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 32.59; SMA60 32.38; RSI14 29.9.
- MACD -0.557; đường tín hiệu -0.138; biểu đồ cột -0.419.
- ATR14 0.74; ATR% 2.5%; ADX14 29.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Quá bán - RSI 29.9.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Xu hướng giảm - ADX 29.2, -DI vượt +DI.
- Thanh khoản: Thấp - 0.61 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.11.
- P/B: 1.19.
- ROE: 14.7%.
- ROA: 2.3%.
- Market cap: 211,170.0 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.11: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.19: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.38: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-09-13 -> 2026-07-21.
- XGBoost: độ chính xác cân bằng 0.493; AUC 0.483; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.482; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 7.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -10.1%; Sharpe -1.01; mức sụt giảm tối đa -12.6%.
- Mức độ quan trọng của đặc trưng: close_vs_sma60=10.75; return_kurtosis_20d=10.43; return_3d=10.19; range_pct=9.45; volume_ratio_20=9.34; volatility_20d=9.23.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 29.30; mục tiêu 1 33.35; mục tiêu 2 34.60.
- Tỷ lệ lợi nhuận/rủi ro 4.81; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 29.79 (-0.21%).
- P10/P90 cuối kỳ 26.48 / 33.35.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.483 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.493 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.48326071169208423, AUC logistic=0.5012184297587348.
- Điều kiện phát hành tín hiệu: Probability 50.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -6 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.10054951000000012, Sharpe=-1.0068974290724673.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Mô hình Logistic đối chứng: 45.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.9%.
- Mức dừng lỗ tham chiếu 29.30, mục tiêu 1 33.35, tỷ lệ lợi nhuận/rủi ro 4.81.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
