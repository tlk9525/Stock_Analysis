# Báo cáo ngày 2026-08-13 - SAB

## Tổng quan

- Dữ liệu: 2016-12-06 -> 2026-08-12, 2,416 phiên.
- Giá đóng cửa: 46.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 59.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 44.24; SMA60 44.52; RSI14 61.7.
- MACD 0.383; đường tín hiệu 0.076; biểu đồ cột 0.307.
- ATR14 0.95; ATR% 2.0%; ADX14 18.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.7.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 18.3.
- Thanh khoản: Bình thường - 1.30 lần trung bình.
- Stochastic: Cực trị - %K 93.5, %D 90.7.

## Phân tích cơ bản

- Doanh nghiệp: SABECO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.26.
- P/B: 2.99.
- ROE: 22.3%.
- ROA: 15.1%.
- Market cap: 58,549.0 tỷ.
- Revenue Growth: 1.2%.
- Profit Growth: -3.4%.
- P/E 12.26: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.99: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-09-25 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.513; AUC 0.512; log-loss 0.682.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.469.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 39.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -32.9%; Sharpe -1.24; mức sụt giảm tối đa -34.7%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 59.9% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 65 vòng | Net sau phí -32.9%. |
| Reward/Risk | 2.34 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 3 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -7.9% | Gross PnL -7,944,424 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -31.5% | 65 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 26,090,207 VND. |
| Kịch bản sau chi phí | -32.9% | Net PnL -32,891,207 VND; gross - cost gap khoảng +24.9%. |
| Ngưỡng phí hòa vốn | -12.6 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 65 phiên active/65 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 65 | -7.9% | 31.5% | -32.9% | -1.24 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 38 | -7.4% | 18.5% | -23.1% | -1.06 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 29 | -10.0% | 14.1% | -22.0% | -1.04 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 24 | -9.3% | 11.7% | -19.4% | -0.90 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -0.8% | 4.9% | -5.6% | -0.29 | Ngưỡng xác suất trong nhóm: 66.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +7.4% | 2.5% | +4.8% | 0.34 | Ngưỡng xác suất trong nhóm: 72.7%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +4.5% | 0.5% | +4.0% | 0.59 | Ngưỡng xác suất trong nhóm: 79.8%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: stoch_k_14=13.93; month_of_year=12.61; market_return_20d=11.61; return_1d=10.77; return_20d=10.39; rsi_14=10.27.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 44.88; mục tiêu 1 50.39; mục tiêu 2 50.39.
- Tỷ lệ lợi nhuận/rủi ro 2.34; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 45.85 (-0.98%).
- P10/P90 cuối kỳ 42.57 / 50.39.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.512 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.513 < 0.520.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2390332543596272.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 59.9%.
- Mô hình Logistic đối chứng: 48.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.1%.
- Mức dừng lỗ tham chiếu 44.88, mục tiêu 1 50.39, tỷ lệ lợi nhuận/rủi ro 2.34.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
