# Báo cáo ngày 2026-08-09 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-07, 4,589 phiên.
- Giá đóng cửa: 215.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 216.63; SMA60 213.69; RSI14 48.7.
- MACD 0.420; đường tín hiệu 0.509; biểu đồ cột -0.089.
- ATR14 6.80; ATR% 3.2%; ADX14 12.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 48.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.3.
- Thanh khoản: Bình thường - 1.31 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 73.62.
- P/B: 9.82.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,668,870.1 tỷ.
- Revenue Growth: 154.0%.
- P/E 73.62: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 9.82: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 6.24: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.05: thanh khoản ngắn hạn khá.
- Revenue Growth 154.0% YoY.
- CFO/LNST 3.40: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 1.68 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T07:06:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.516; AUC 0.531.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: excess_return_20d=17.77; rsi_14=17.68; corr_60d=15.74; return_kurtosis_20d=15.72; market_return_20d=14.02; excess_return_1d=10.23.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 211.56; mục tiêu 1 224.00; mục tiêu 2 263.08.
- Tỷ lệ lợi nhuận/rủi ro 1.75; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 212.58 (-1.13%).
- P10/P90 cuối kỳ 171.85 / 263.08.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5069433608987362, AUC logistic=0.5312544115789551.
- Điều kiện phát hành tín hiệu: Probability 50.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7802033402356634.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.1%.
- Mô hình Logistic đối chứng: 59.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.5%.
- Mức dừng lỗ tham chiếu 211.56, mục tiêu 1 224.00, tỷ lệ lợi nhuận/rủi ro 1.75.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
