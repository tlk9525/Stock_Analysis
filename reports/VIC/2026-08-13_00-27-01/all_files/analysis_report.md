# Báo cáo ngày 2026-08-13 - VIC

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,593 phiên.
- Giá đóng cửa: 215.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 215.38; SMA60 212.95; RSI14 50.4.
- MACD -0.644; đường tín hiệu -0.029; biểu đồ cột -0.615.
- ATR14 6.87; ATR% 3.2%; ADX14 12.7.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.7.
- Thanh khoản: Bình thường - 1.24 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

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

- Kiểm thử: 2023-08-25 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.530.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 50.0% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 69 vòng | Net sau phí -33.5%. |
| Reward/Risk | 8.30 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -6.6% | Gross PnL -6,559,802 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -34.0% | 69 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 29,226,255 VND. |
| Kịch bản sau chi phí | -33.5% | Net PnL -33,546,255 VND; gross - cost gap khoảng +27.0%. |
| Ngưỡng phí hòa vốn | -9.7 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 69 phiên active/69 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 69 | -6.6% | 34.0% | -33.5% | -1.78 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 41 | -4.5% | 20.2% | -22.0% | -1.44 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 31 | -0.0% | 15.3% | -14.2% | -0.95 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 19 | +5.0% | 9.4% | -4.4% | -0.34 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +5.9% | 5.0% | +0.8% | 0.15 | Ngưỡng xác suất trong nhóm: 64.9%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +5.0% | 2.5% | +2.5% | 0.61 | Ngưỡng xác suất trong nhóm: 69.5%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +2.3% | 0.5% | +1.8% | 0.58 | Ngưỡng xác suất trong nhóm: 74.9%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: excess_return_20d=20.82; market_return_20d=19.92; return_kurtosis_20d=16.08; return_skew_20d=14.08; corr_60d=13.72; adx_14=11.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 210.83; mục tiêu 1 264.37; mục tiêu 2 264.37.
- Tỷ lệ lợi nhuận/rủi ro 8.30; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 213.12 (-1.10%).
- P10/P90 cuối kỳ 172.18 / 264.37.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5071380138854086, AUC logistic=0.5300555711148126.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7765358368807573.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 49.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.5%.
- Mức dừng lỗ tham chiếu 210.83, mục tiêu 1 264.37, tỷ lệ lợi nhuận/rủi ro 8.30.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
