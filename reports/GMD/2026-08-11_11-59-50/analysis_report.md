# Báo cáo ngày 2026-08-11 - GMD

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,593 phiên.
- Giá đóng cửa: 78.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 75.78; SMA60 75.57; RSI14 59.8.
- MACD 0.576; đường tín hiệu 0.186; biểu đồ cột 0.390.
- ATR14 2.21; ATR% 2.8%; ADX14 16.4.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 16.4.
- Thanh khoản: Thấp - 0.20 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Gemadept.
- Ngành: Industrial Goods & Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.91.
- P/B: 2.46.
- ROE: 19.4%.
- ROA: 12.8%.
- Market cap: 33,852.2 tỷ.
- Revenue Growth: 17.9%.
- Profit Growth: 154.6%.
- P/E 12.91: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.46: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.42: thanh khoản ngắn hạn khá.
- Revenue Growth 17.9% YoY.
- Profit Growth 154.6% YoY.
- CFO/LNST 0.54: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:30:10+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.508; AUC 0.529; log-loss 0.692.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.512; AUC 0.540.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 52.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -20.5%; Sharpe -0.75; mức sụt giảm tối đa -21.9%.
- Mức độ quan trọng của đặc trưng: return_3d=11.24; day_of_week=11.11; return_kurtosis_20d=9.98; close_vs_sma60=9.69; return_2d=9.67; relative_strength_20d=9.59.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 74.88; mục tiêu 1 87.75; mục tiêu 2 87.75.
- Tỷ lệ lợi nhuận/rủi ro 2.47; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 77.73 (-0.60%).
- P10/P90 cuối kỳ 68.60 / 87.75.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.529 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.508 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5286272421860939, AUC logistic=0.5396544483772272.
- Điều kiện phát hành tín hiệu: Probability 50.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7453750647674403.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 53.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.4%.
- Mức dừng lỗ tham chiếu 74.88, mục tiêu 1 87.75, tỷ lệ lợi nhuận/rủi ro 2.47.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
