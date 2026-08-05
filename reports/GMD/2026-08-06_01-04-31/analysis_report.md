# Báo cáo ngày 2026-08-06 - GMD

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-05, 4,590 phiên.
- Giá đóng cửa: 76.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 75.45; SMA60 75.57; RSI14 52.9.
- MACD 0.100; đường tín hiệu -0.159; biểu đồ cột 0.259.
- ATR14 2.17; ATR% 2.9%; ADX14 14.9.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 14.9.
- Thanh khoản: Bình thường - 0.73 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Gemadept.
- Ngành: Industrial Goods & Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.62.
- P/B: 2.38.
- ROE: 19.4%.
- ROA: 12.8%.
- Market cap: 32,626.9 tỷ.
- Revenue Growth: 17.9%.
- Profit Growth: 154.6%.
- P/E 12.62: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.38: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.42: thanh khoản ngắn hạn khá.
- Revenue Growth 17.9% YoY.
- Profit Growth 154.6% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-04.
- XGBoost: độ chính xác cân bằng 0.508; AUC 0.529; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.512; AUC 0.539.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 52.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -20.5%; Sharpe -0.75; mức sụt giảm tối đa -21.9%.
- Mức độ quan trọng của đặc trưng: day_of_week=10.88; return_3d=10.81; close_vs_sma60=10.02; return_kurtosis_20d=10.02; return_2d=9.92; return_5d=9.38.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 74.82; mục tiêu 1 79.30; mục tiêu 2 85.53.
- Tỷ lệ lợi nhuận/rủi ro 1.54; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 75.87 (-0.43%).
- P10/P90 cuối kỳ 66.94 / 85.53.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.529 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.508 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5289695177434031, AUC logistic=0.538648771610555.
- Điều kiện phát hành tín hiệu: Probability 49.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7474050327534423.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.2%.
- Mô hình Logistic đối chứng: 54.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.2%.
- Mức dừng lỗ tham chiếu 74.82, mục tiêu 1 79.30, tỷ lệ lợi nhuận/rủi ro 1.54.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
