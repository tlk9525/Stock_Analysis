# Báo cáo ngày 2026-08-11 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,591 phiên.
- Giá đóng cửa: 208.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 215.46; SMA60 213.14; RSI14 42.3.
- MACD -0.795; đường tín hiệu 0.125; biểu đồ cột -0.919.
- ATR14 6.76; ATR% 3.2%; ADX14 13.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 42.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 13.0.
- Thanh khoản: Thấp - 0.67 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 71.40.
- P/B: 9.53.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,618,415.9 tỷ.
- Revenue Growth: 154.0%.
- P/E 71.40: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 9.53: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-08-25 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.530.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: excess_return_20d=19.95; market_return_20d=19.43; market_volatility_20d=18.14; return_kurtosis_20d=16.13; corr_60d=14.33; return_skew_20d=14.19.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 198.36; mục tiêu 1 257.44; mục tiêu 2 257.44.
- Tỷ lệ lợi nhuận/rủi ro 4.28; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 207.20 (-0.62%).
- P10/P90 cuối kỳ 167.56 / 257.44.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5074462502679172, AUC logistic=0.5295300178118741.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -6 < 2.
- Điều kiện phát hành tín hiệu: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7777558182493016.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 54.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.6%.
- Mức dừng lỗ tham chiếu 198.36, mục tiêu 1 257.44, tỷ lệ lợi nhuận/rủi ro 4.28.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
