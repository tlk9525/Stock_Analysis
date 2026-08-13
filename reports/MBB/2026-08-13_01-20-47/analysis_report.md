# Báo cáo ngày 2026-08-13 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-12, 3,687 phiên.
- Giá đóng cửa: 20.45 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 19.35; SMA60 19.86; RSI14 61.3.
- MACD 0.142; đường tín hiệu -0.056; biểu đồ cột 0.198.
- ATR14 0.45; ATR% 2.2%; ADX14 25.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.0, +DI vượt -DI.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Cực trị - %K 96.4, %D 93.7.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.27.
- P/B: 1.30.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 204,899.1 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.27: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.30: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:40:35+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.498; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.499.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 41.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Diagnostic classifier 1D legacy: tổng lợi nhuận -4.9%; Sharpe -0.17; mức sụt giảm tối đa -10.4%.

### Breakdown legacy 1D trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +23.6% | Gross PnL 23,571,720 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -26.3% | 53 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 25,628,642 VND. |
| Kịch bản sau chi phí | -4.9% | Net PnL -4,944,642 VND; gross - cost gap khoảng +28.5%. |
| Ngưỡng phí hòa vốn | 44.9 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì xem khung HOLD/REDUCE/SELL riêng theo model health, kỹ thuật, tin và stop-loss. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 53 phiên active/53 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Phụ lục legacy 1D — Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 53 | +23.6% | 26.3% | -4.9% | -0.17 | Baseline lịch sử để đo turnover/phí; không phải số lệnh khuyến nghị. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 27 | +22.9% | 13.4% | +7.5% | 0.43 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 16 | +20.9% | 8.0% | +11.7% | 0.68 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 10 | +17.1% | 5.0% | +11.4% | 0.79 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +17.1% | 5.0% | +11.4% | 0.79 | Ngưỡng trong nhóm: 62.1%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +16.9% | 2.5% | +14.1% | 0.98 | Ngưỡng trong nhóm: 64.3%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +6.4% | 0.5% | +5.9% | 0.63 | Ngưỡng trong nhóm: 70.8%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
Ghi chú: baseline chỉ để đo turnover/phí. Không dùng bảng để chọn 1 lệnh hoặc DCA; các dòng threshold cần holdout/future đã khóa, còn 10/5/1 có selection bias vì số vòng được chọn sau khi đã thấy OOS. Khi signal chưa ACTIONABLE, lệnh mới hôm nay là 0.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.2% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 5 điểm | Tích cực; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.2%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_1d=11.59; beta_60d=10.76; volatility_20d=10.25; return_2d=9.90; market_return_1d=9.58; excess_return_1d=9.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 19.78; mục tiêu 1 22.66; mục tiêu 2 22.66.
- Tỷ lệ lợi nhuận/rủi ro 2.73; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 20.15 (-1.44%).
- P10/P90 cuối kỳ 18.37 / 22.66.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 4 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Expected excess return 0.0015503921313211322 chưa vượt chi phí + margin 0.0100..
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Mô hình Logistic đối chứng: 49.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.4%.
- Mức dừng lỗ tham chiếu 19.78, mục tiêu 1 22.66, tỷ lệ lợi nhuận/rủi ro 2.73.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
