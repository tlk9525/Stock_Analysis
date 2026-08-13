# Báo cáo ngày 2026-08-13 - PLX

## Tổng quan

- Dữ liệu: 2017-04-21 -> 2026-08-12, 2,325 phiên.
- Giá đóng cửa: 36.65 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 33.56; SMA60 35.98; RSI14 60.9.
- MACD 0.347; đường tín hiệu -0.316; biểu đồ cột 0.663.
- ATR14 1.31; ATR% 3.6%; ADX14 24.9.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 60.9.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 24.9.
- Thanh khoản: Bình thường - 1.15 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Petrolimex.
- Ngành: Oil & Gas.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.44.
- P/B: 1.81.
- ROE: 12.5%.
- ROA: 3.5%.
- Market cap: 46,503.7 tỷ.
- Revenue Growth: 78.0%.
- Profit Growth: 105.6%.
- P/E 14.44: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.81: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 2.01: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.06: thanh khoản ngắn hạn khá.
- Revenue Growth 78.0% YoY.
- Profit Growth 105.6% YoY.
- CFO/LNST -2.68: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-11T02:42:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-03 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.505; AUC 0.512; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.518; AUC 0.480.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 35.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -54.6%; Sharpe -1.78; mức sụt giảm tối đa -55.7%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 50.0% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 86 vòng | Net sau phí -54.6%. |
| Reward/Risk | 5.87 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -31.0% | Gross PnL -31,012,398 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -41.7% | 86 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 29,547,763 VND. |
| Kịch bản sau chi phí | -54.6% | Net PnL -54,641,763 VND; gross - cost gap khoảng +23.6%. |
| Ngưỡng phí hòa vốn | -37.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 86 phiên active/86 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 86 | -31.0% | 41.7% | -54.6% | -1.78 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 46 | -36.0% | 22.1% | -48.8% | -1.90 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 30 | -23.3% | 14.5% | -33.8% | -2.00 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 17 | -10.0% | 8.3% | -17.2% | -1.15 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -8.9% | 4.8% | -13.2% | -1.06 | Ngưỡng xác suất trong nhóm: 64.5%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -9.2% | 2.4% | -11.4% | -1.23 | Ngưỡng xác suất trong nhóm: 67.6%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -1.7% | 0.5% | -2.2% | -0.58 | Ngưỡng xác suất trong nhóm: 73.4%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_2d=11.68; volatility_20d=10.12; atr_pct_14=9.98; return_1d=9.53; month_of_year=9.48; macd_pct=9.23.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 35.62; mục tiêu 1 43.96; mục tiêu 2 43.96.
- Tỷ lệ lợi nhuận/rủi ro 5.87; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 36.06 (-1.62%).
- P10/P90 cuối kỳ 30.28 / 43.96.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.512 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.505 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7803806544822127.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 48.4%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.9%.
- Mức dừng lỗ tham chiếu 35.62, mục tiêu 1 43.96, tỷ lệ lợi nhuận/rủi ro 5.87.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
