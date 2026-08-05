# Báo cáo ngày 2026-08-06 - SSI

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,589 phiên.
- Giá đóng cửa: 24.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 51.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 24.14; SMA60 26.16; RSI14 48.2.
- MACD -0.597; đường tín hiệu -0.822; biểu đồ cột 0.225.
- ATR14 0.88; ATR% 3.6%; ADX14 35.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 48.2.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 35.2, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.73 lần trung bình.
- Stochastic: Cực trị - %K 81.8, %D 79.5.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán SSI.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.45.
- P/B: 1.51.
- ROE: 13.4%.
- ROA: 5.0%.
- Market cap: 61,401.9 tỷ.
- Revenue Growth: 10.9%.
- Profit Growth: 27.0%.
- P/E 11.45: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.51: nên đọc cùng ROE và đặc thù ngành.
- ROA 5.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.65: thanh khoản ngắn hạn khá.
- Revenue Growth 10.9% YoY.
- Profit Growth 27.0% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.500; AUC 0.545; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.539; AUC 0.548.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 19.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -1.0%; Sharpe -0.03; mức sụt giảm tối đa -8.2%.
- Mức độ quan trọng của đặc trưng: volume_z_20=13.38; return_1d=13.36; relative_strength_20d=13.26; beta_60d=12.75; macd_hist_pct=12.35; range_pct=12.34.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.08; mục tiêu 1 27.25; mục tiêu 2 27.51.
- Tỷ lệ lợi nhuận/rủi ro 1.89; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 24.18 (-0.90%).
- P10/P90 cuối kỳ 21.37 / 27.51.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.500 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5446086779894064, AUC logistic=0.548413306042093.
- Điều kiện phát hành tín hiệu: Probability 51.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.009731229999999313, Sharpe=-0.03008470840314397.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 51.6%.
- Mô hình Logistic đối chứng: 59.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.2%.
- Mức dừng lỗ tham chiếu 23.08, mục tiêu 1 27.25, tỷ lệ lợi nhuận/rủi ro 1.89.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
