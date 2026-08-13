# Báo cáo ngày 2026-08-13 - NVL

## Tổng quan

- Dữ liệu: 2016-12-28 -> 2026-08-12, 2,400 phiên.
- Giá đóng cửa: 13.55 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 7).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Khuyến nghị sau phí: WAIT - Chờ điểm mua tốt hơn.
- Lý do khuyến nghị: Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 52.8%.

## Phân tích kỹ thuật

- SMA20 13.11; SMA60 13.04; RSI14 57.7.
- MACD 0.254; đường tín hiệu 0.167; biểu đồ cột 0.088.
- ATR14 0.52; ATR% 3.8%; ADX14 26.6.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.6, +DI vượt -DI.
- Thanh khoản: Bình thường - 0.86 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Novaland.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.33.
- P/B: 0.67.
- ROE: 9.5%.
- ROA: 1.7%.
- Market cap: 32,548.0 tỷ.
- Revenue Growth: -22.1%.
- P/E 7.33: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 0.67: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 2.96: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 2.12: thanh khoản ngắn hạn khá.
- Revenue Growth -22.1% YoY.
- CFO/LNST -3.46: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T10:14:03+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.497; AUC 0.534; log-loss 0.685.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.506; AUC 0.515.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 45.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -31.5%; Sharpe -0.90; mức sụt giảm tối đa -42.2%.

### Khuyến nghị đầu tư sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Khuyến nghị sau phí | WAIT | Chờ điểm mua tốt hơn |
| Lý do chính |  | Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 52.8%. |
| Xác suất hiện tại | 52.8% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.62 | Ngưỡng 0.62; net +1.3%; 3 vòng. |
| Baseline cấu hình | 50 vòng | Net sau phí -31.5%. |
| Reward/Risk | 3.78 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -12.2% | Gross PnL -12,184,692 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -24.7% | 50 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 20,303,711 VND. |
| Kịch bản sau chi phí | -31.5% | Net PnL -31,516,711 VND; gross - cost gap khoảng +19.3%. |
| Ngưỡng phí hòa vốn | -24.6 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 50 phiên active/50 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 50 | -12.2% | 24.7% | -31.5% | -0.90 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 13 | +0.5% | 6.4% | -5.8% | -0.29 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 5 | +3.2% | 2.5% | +0.6% | 0.13 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 3 | +2.8% | 1.5% | +1.3% | 0.40 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +7.7% | 5.0% | +2.5% | 0.22 | Ngưỡng xác suất trong nhóm: 59.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +3.2% | 2.5% | +0.6% | 0.13 | Ngưỡng xác suất trong nhóm: 60.5%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +2.4% | 0.5% | +1.9% | 0.60 | Ngưỡng xác suất trong nhóm: 63.9%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: market_return_1d=10.21; macd_pct=9.98; beta_60d=9.83; adx_14=9.62; excess_return_5d=9.20; stoch_k_14=8.44.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 12.91; mục tiêu 1 16.29; mục tiêu 2 16.29.
- Tỷ lệ lợi nhuận/rủi ro 3.78; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 13.29 (-1.90%).
- P10/P90 cuối kỳ 11.16 / 16.29.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.534 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.497 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.31516711, Sharpe=-0.9010415141402207.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Mô hình Logistic đối chứng: 46.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 44.5%.
- Mức dừng lỗ tham chiếu 12.91, mục tiêu 1 16.29, tỷ lệ lợi nhuận/rủi ro 3.78.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
