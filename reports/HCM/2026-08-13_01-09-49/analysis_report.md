# Báo cáo ngày 2026-08-13 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-12, 4,301 phiên.
- Giá đóng cửa: 26.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 25.51; SMA60 24.40; RSI14 59.9.
- MACD 0.420; đường tín hiệu 0.365; biểu đồ cột 0.055.
- ATR14 0.85; ATR% 3.3%; ADX14 15.4.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 59.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.4.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Chứng khoán HSC.
- Ngành: Financial Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 20.17.
- P/B: 2.06.
- ROE: 9.8%.
- ROA: 3.1%.
- Market cap: 35,773.6 tỷ.
- Revenue Growth: 15.1%.
- Profit Growth: 42.0%.
- P/E 20.17: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.06: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.54: thanh khoản ngắn hạn khá.
- Revenue Growth 15.1% YoY.
- Profit Growth 42.0% YoY.
- CFO/LNST 1.16: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-11T09:51:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.518; AUC 0.558; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.519; AUC 0.563.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 51.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -12.6%; Sharpe -0.34; mức sụt giảm tối đa -20.4%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | +0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 4 điểm | Hồi phục / nghiêng tăng; news warning: không. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +18.3% | Gross PnL 18,289,135 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.3% | 61 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,355,115 VND. |
| Kịch bản sau chi phí | -12.6% | Net PnL -12,580,115 VND; gross - cost gap khoảng +30.9%. |
| Ngưỡng phí hòa vốn | 30.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì xem khung HOLD/REDUCE/SELL riêng theo model health, kỹ thuật, tin và stop-loss. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 61 phiên active/61 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 61 | +18.3% | 30.3% | -12.6% | -0.34 | Baseline lịch sử để đo turnover/phí; không phải số lệnh khuyến nghị. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 38 | +18.1% | 18.9% | -2.2% | -0.02 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 31 | +16.6% | 15.4% | +0.0% | 0.05 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 20 | +17.9% | 10.0% | +6.8% | 0.30 | Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +11.6% | 5.0% | +6.2% | 0.41 | Ngưỡng trong nhóm: 66.3%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +13.0% | 2.5% | +10.2% | 0.70 | Ngưỡng trong nhóm: 69.0%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +6.1% | 0.5% | +5.6% | 0.60 | Ngưỡng trong nhóm: 75.2%. Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS. |
Ghi chú: baseline chỉ để đo turnover/phí. Không dùng bảng để chọn 1 lệnh hoặc DCA; các dòng threshold cần holdout/future đã khóa, còn 10/5/1 có selection bias vì số vòng được chọn sau khi đã thấy OOS. Khi signal chưa ACTIONABLE, lệnh mới hôm nay là 0.

## Chiến lược swing 5 phiên (research, T+2-aware)

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: net +0.0%; Sharpe N/A; 0 vòng; nắm giữ trung bình N/A phiên.
- Publish gate swing: CHƯA ĐẠT. Gate này yêu cầu frozen holdout, stress phí 1.5x, đủ số trade và T+2-aware; chưa đạt thì không thay NO_EDGE bằng BUY.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.74; macd_pct=12.47; return_1d=11.38; corr_60d=11.30; market_return_1d=10.80; return_20d=10.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.88; mục tiêu 1 29.82; mục tiêu 2 29.82.
- Tỷ lệ lợi nhuận/rủi ro 2.52; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.96 (-0.71%).
- P10/P90 cuối kỳ 22.79 / 29.82.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 5 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Expected excess return 0.0006463585887104273 chưa vượt chi phí + margin 0.0100..
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Mô hình Logistic đối chứng: 45.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.3%.
- Mức dừng lỗ tham chiếu 24.88, mục tiêu 1 29.82, tỷ lệ lợi nhuận/rủi ro 2.52.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
