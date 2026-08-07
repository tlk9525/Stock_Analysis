# Báo cáo ngày 2026-08-06 - GMD

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-06, 4,590 phiên.
- Giá đóng cửa: 77.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 75.51; SMA60 75.54; RSI14 56.1.
- MACD 0.216; đường tín hiệu -0.084; biểu đồ cột 0.300.
- ATR14 2.17; ATR% 2.8%; ADX14 14.5.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 14.5.
- Thanh khoản: Bình thường - 0.72 lần trung bình.
- Stochastic: Cực trị - %K 88.6, %D 80.8.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Gemadept.
- Ngành: Industrial Goods & Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.57.
- P/B: 2.39.
- ROE: 19.4%.
- ROA: 12.8%.
- Market cap: 32,986.4 tỷ.
- Revenue Growth: 17.9%.
- Profit Growth: 154.6%.
- P/E 12.57: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.39: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.42: thanh khoản ngắn hạn khá.
- Revenue Growth 17.9% YoY.
- Profit Growth 154.6% YoY.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-05.
- XGBoost: độ chính xác cân bằng 0.508; AUC 0.528; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.512; AUC 0.539.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 52.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -20.5%; Sharpe -0.75; mức sụt giảm tối đa -21.9%.
- Mức độ quan trọng của đặc trưng: day_of_week=10.99; return_3d=10.55; close_vs_sma60=10.19; return_kurtosis_20d=10.15; volatility_20d=9.57; return_2d=9.55.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 74.78; mục tiêu 1 86.35; mục tiêu 2 86.35.
- Tỷ lệ lợi nhuận/rủi ro 3.28; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 76.49 (-0.79%).
- P10/P90 cuối kỳ 67.63 / 86.35.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.528 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.508 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5283786848072562, AUC logistic=0.5394708994708994.
- Điều kiện phát hành tín hiệu: Probability 48.3% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7468959862318822.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.3%.
- Mô hình Logistic đối chứng: 51.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.6%.
- Mức dừng lỗ tham chiếu 74.78, mục tiêu 1 86.35, tỷ lệ lợi nhuận/rủi ro 3.28.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
