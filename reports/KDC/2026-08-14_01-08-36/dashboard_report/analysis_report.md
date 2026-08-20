# Báo cáo ngày 2026-08-14 - KDC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-13, 4,592 phiên.
- Giá đóng cửa: 51.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 41.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 3/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 3/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 50.35; SMA60 50.11; RSI14 61.6.
- MACD 0.578; đường tín hiệu 0.427; biểu đồ cột 0.150.
- ATR14 1.14; ATR% 2.2%; ADX14 31.3.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.3, -DI vượt +DI.
- Thanh khoản: Thấp - 0.41 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn KIDO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 30.06.
- P/B: 2.44.
- ROE: 7.6%.
- ROA: 3.8%.
- Market cap: 14,314.7 tỷ.
- Revenue Growth: -7.3%.
- Profit Growth: -105.8%.
- P/E 30.06: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.44: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.6%: hiệu quả vốn còn yếu.
- ROA 3.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.02: thanh khoản ngắn hạn khá.
- Revenue Growth -7.3% YoY.
- Profit Growth -105.8% YoY.
- CFO/LNST -46.72: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 0.44 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T11:18:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.534; log-loss 0.680.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.492; AUC 0.529.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 54.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 3/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 3/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | -0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 3/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: -0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: 3/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_skew_20d=11.65; return_5d=11.64; volatility_20d=11.53; adx_14=11.42; volume_ratio_20=11.36; volume_z_20=11.24.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 49.79; mục tiêu 1 N/A; mục tiêu 2 54.50.
- Tỷ lệ lợi nhuận/rủi ro N/A; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 51.07 (-0.83%).
- P10/P90 cuối kỳ 49.04 / 54.50.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 3 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.03785301428313714 (dự báo điểm -0.001208605128340423) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Reward/risk N/A < 1.50..
- Điều kiện phát hành tín hiệu: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản..
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 41.4%.
- Mô hình Logistic đối chứng: 41.4%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 29.8%.
- Mức dừng lỗ tham chiếu 49.79, mục tiêu 1 N/A, tỷ lệ lợi nhuận/rủi ro N/A.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
