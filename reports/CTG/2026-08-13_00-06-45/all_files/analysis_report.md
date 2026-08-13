# Báo cáo ngày 2026-08-13 - CTG

## Tổng quan

- Dữ liệu: 2009-07-16 -> 2026-08-12, 4,261 phiên.
- Giá đóng cửa: 32.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 30.82; SMA60 32.58; RSI14 55.1.
- MACD 0.034; đường tín hiệu -0.320; biểu đồ cột 0.354.
- ATR14 0.77; ATR% 2.4%; ADX14 23.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 23.5.
- Thanh khoản: Thấp - 0.56 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VietinBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.24.
- P/B: 1.26.
- ROE: 21.8%.
- ROA: 1.4%.
- Market cap: 250,872.3 tỷ.
- Revenue Growth: 26.1%.
- Profit Growth: 21.4%.
- P/E 6.24: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.26: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.8%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 13.79: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.2%: đang ở mức kiểm soát.
- Revenue Growth 26.1% YoY.
- Profit Growth 21.4% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-11T07:43:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.502; AUC 0.490; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.505; AUC 0.490.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 17.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.9%; Sharpe -0.38; mức sụt giảm tối đa -13.8%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +4.8% | Gross PnL 4,811,418 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -10.8% | 22 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 10,698,101 VND. |
| Kịch bản sau chi phí | -5.9% | Net PnL -5,946,101 VND; gross - cost gap khoảng +10.8%. |
| Ngưỡng phí hòa vốn | 22.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 22 phiên active/22 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 22 | +4.8% | 10.8% | -5.9% | -0.38 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 13 | +5.0% | 6.4% | -1.5% | -0.09 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 7 | +1.4% | 3.4% | -2.0% | -0.31 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 3 | +0.5% | 1.5% | -0.9% | -0.15 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +1.3% | 4.9% | -3.6% | -0.44 | Ngưỡng xác suất trong nhóm: 58.8%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +0.3% | 2.4% | -2.1% | -0.34 | Ngưỡng xác suất trong nhóm: 61.1%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +2.4% | 0.5% | +1.9% | 0.62 | Ngưỡng xác suất trong nhóm: 64.6%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_1d=15.56; beta_60d=15.45; atr_pct_14=14.85; close_vs_sma60=13.16; rsi_14=12.59; market_return_1d=12.29.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.05; mục tiêu 1 35.49; mục tiêu 2 35.49.
- Tỷ lệ lợi nhuận/rủi ro 2.38; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 32.08 (-0.37%).
- P10/P90 cuối kỳ 29.11 / 35.49.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.490 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.502 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 50.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.059461009999999814, Sharpe=-0.37651293115339896.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 48.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.1%.
- Mức dừng lỗ tham chiếu 31.05, mục tiêu 1 35.49, tỷ lệ lợi nhuận/rủi ro 2.38.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
