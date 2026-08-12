# Báo cáo ngày 2026-08-11 - SAB

## Tổng quan

- Dữ liệu: 2016-12-06 -> 2026-08-11, 2,415 phiên.
- Giá đóng cửa: 46.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 57.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 44.10; SMA60 44.50; RSI14 61.5.
- MACD 0.304; đường tín hiệu 0.006; biểu đồ cột 0.298.
- ATR14 0.92; ATR% 2.0%; ADX14 18.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.5.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 18.3.
- Thanh khoản: Thấp - 0.35 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: SABECO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.49.
- P/B: 3.05.
- ROE: 22.3%.
- ROA: 15.1%.
- Market cap: 59,639.2 tỷ.
- Revenue Growth: 1.2%.
- Profit Growth: -3.4%.
- P/E 12.49: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.05: nên đọc cùng ROE và đặc thù ngành.
- ROE 22.3%: hiệu quả vốn chủ sở hữu tốt.
- ROA 15.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.46: thanh khoản ngắn hạn khá.
- Revenue Growth 1.2% YoY.
- Profit Growth -3.4% YoY.
- CFO/LNST 0.42: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là tiền mặt ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.24 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T11:04:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-25 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.513; AUC 0.510; log-loss 0.682.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.469.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 39.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -32.9%; Sharpe -1.24; mức sụt giảm tối đa -34.7%.
- Mức độ quan trọng của đặc trưng: stoch_k_14=13.59; market_return_20d=12.02; macd_pct=11.04; rsi_14=10.87; return_1d=10.31; adx_14=10.26.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 44.67; mục tiêu 1 50.08; mục tiêu 2 50.08.
- Tỷ lệ lợi nhuận/rủi ro 2.37; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 45.57 (-1.04%).
- P10/P90 cuối kỳ 42.34 / 50.08.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.513 < 0.520.
- Điều kiện phát hành tín hiệu: Technical score 1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2399010621517204.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 57.0%.
- Mô hình Logistic đối chứng: 49.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.3%.
- Mức dừng lỗ tham chiếu 44.67, mục tiêu 1 50.08, tỷ lệ lợi nhuận/rủi ro 2.37.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
