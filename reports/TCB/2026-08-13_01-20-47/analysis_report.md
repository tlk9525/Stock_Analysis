# Báo cáo ngày 2026-08-13 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-12, 2,048 phiên.
- Giá đóng cửa: 31.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 29.77; SMA60 31.49; RSI14 57.4.
- MACD -0.231; đường tín hiệu -0.582; biểu đồ cột 0.350.
- ATR14 0.84; ATR% 2.7%; ADX14 28.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.0, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.06 lần trung bình.
- Stochastic: Cực trị - %K 98.7, %D 94.7.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.10.
- P/B: 1.23.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 219,673.5 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.10: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.23: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.74: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:42:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.500; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Diagnostic classifier 1D legacy: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.

### Breakdown legacy 1D trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -10.3% | Gross PnL -10,309,127 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -20.6% | 42 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 18,776,580 VND. |
| Kịch bản sau chi phí | -27.1% | Net PnL -27,056,580 VND; gross - cost gap khoảng +16.7%. |
| Ngưỡng phí hòa vốn | -25.1 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 42 phiên active/42 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Phụ lục legacy 1D — Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 42 | -10.3% | 20.6% | -27.1% | -1.65 | Baseline lịch sử để đo turnover/phí; không phải số lệnh khuyến nghị. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 18 | -4.8% | 8.8% | -12.9% | -1.14 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 8 | -3.6% | 3.9% | -7.3% | -0.70 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 4 | -4.2% | 2.0% | -6.1% | -0.83 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -5.6% | 4.9% | -10.1% | -0.94 | Ngưỡng trong nhóm: 59.2%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -5.3% | 2.4% | -7.6% | -0.98 | Ngưỡng trong nhóm: 61.2%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -2.3% | 0.5% | -2.7% | -0.59 | Ngưỡng trong nhóm: 64.7%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
Ghi chú: baseline chỉ để đo turnover/phí. Không dùng bảng để chọn 1 lệnh hoặc DCA; các dòng threshold cần holdout/future đã khóa, còn 10/5/1 có selection bias vì số vòng được chọn sau khi đã thấy OOS. Khi signal chưa ACTIONABLE, lệnh mới hôm nay là 0.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.5% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 6 điểm | Tích cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.5%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.29; bb_position_20=11.07; atr_pct_14=10.33; relative_strength_20d=9.83; excess_return_5d=9.70; market_return_1d=9.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.17; mục tiêu 1 35.12; mục tiêu 2 35.12.
- Tỷ lệ lợi nhuận/rủi ro 7.14; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.43 (-0.24%).
- P10/P90 cuối kỳ 27.91 / 35.12.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 4 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Expected excess return 0.004561764188110828 chưa vượt chi phí + margin 0.0100..
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 49.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.8%.
- Mức dừng lỗ tham chiếu 31.17, mục tiêu 1 35.12, tỷ lệ lợi nhuận/rủi ro 7.14.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
