# Báo cáo ngày 2026-08-14 - PAN

## Tổng quan

- Dữ liệu: 2010-12-15 -> 2026-08-13, 3,858 phiên.
- Giá đóng cửa: 20.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 20.88; SMA60 22.33; RSI14 36.7.
- MACD -0.348; đường tín hiệu -0.394; biểu đồ cột 0.046.
- ATR14 0.51; ATR% 2.5%; ADX14 39.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 36.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 39.1, -DI vượt +DI.
- Thanh khoản: Đột biến - 2.16 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn PAN.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 4.25.
- P/B: 0.97.
- ROE: 22.6%.
- ROA: 7.5%.
- Market cap: 5,188.9 tỷ.
- Revenue Growth: -10.1%.
- Profit Growth: 51.4%.
- P/E 4.25: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 0.97: nên đọc cùng ROE và đặc thù ngành.
- ROE 22.6%: hiệu quả vốn chủ sở hữu tốt.
- ROA 7.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.83: thanh khoản ngắn hạn khá.
- Revenue Growth -10.1% YoY.
- Profit Growth 51.4% YoY.
- CFO/LNST -4.75: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.20 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T11:32:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-11-22 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.493; AUC 0.501; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.508; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 5.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.0% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -2 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.0%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_1d=16.84; return_kurtosis_20d=14.17; return_5d=13.02; atr_pct_14=11.77; rsi_14=11.60; market_volatility_20d=11.00.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 19.73; mục tiêu 1 23.63; mục tiêu 2 23.63.
- Tỷ lệ lợi nhuận/rủi ro 3.47; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 20.54 (0.18%).
- P10/P90 cuối kỳ 17.59 / 23.63.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.043440757624761406 (dự báo điểm 0.0001454383018426597) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -2 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Mô hình Logistic đối chứng: 47.6%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 35.7%.
- Mức dừng lỗ tham chiếu 19.73, mục tiêu 1 23.63, tỷ lệ lợi nhuận/rủi ro 3.47.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
