# Báo cáo ngày 2026-08-13 - KDH

## Tổng quan

- Dữ liệu: 2010-02-01 -> 2026-08-12, 4,119 phiên.
- Giá đóng cửa: 18.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 17.81; SMA60 20.72; RSI14 42.5.
- MACD -0.600; đường tín hiệu -0.844; biểu đồ cột 0.245.
- ATR14 0.58; ATR% 3.2%; ADX14 41.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 42.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 41.1, -DI vượt +DI.
- Thanh khoản: Bình thường - 0.91 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Nhà Khang Điền.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.63.
- P/B: 1.10.
- ROE: 9.5%.
- ROA: 4.8%.
- Market cap: 20,424.3 tỷ.
- Revenue Growth: -84.7%.
- Profit Growth: 276.7%.
- P/E 11.63: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.10: nên đọc cùng ROE và đặc thù ngành.
- ROA 4.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 10.06: thanh khoản ngắn hạn khá.
- Revenue Growth -84.7% YoY.
- Profit Growth 276.7% YoY.
- CFO/LNST -1.10: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:54:28+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.499; AUC 0.493; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.495.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 8.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 2.5%; Sharpe 0.16; mức sụt giảm tối đa -8.8%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +14.2% | Gross PnL 14,217,262 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -10.9% | 22 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 11,229,176 VND. |
| Kịch bản sau chi phí | +2.5% | Net PnL 2,472,824 VND; gross - cost gap khoảng +11.7%. |
| Ngưỡng phí hòa vốn | 65.3 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Sau phí vẫn dương; có thể xem tiếp các gate còn lại trước khi cân nhắc hành động. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 22 phiên active/22 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 22 | +14.2% | 10.9% | +2.5% | 0.16 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 6 | +6.3% | 3.0% | +3.2% | 0.32 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 3 | -0.9% | 1.5% | -2.4% | -0.95 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 2 | -0.2% | 1.0% | -1.2% | -0.81 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +6.7% | 4.9% | +1.5% | 0.14 | Ngưỡng xác suất trong nhóm: 57.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +6.3% | 2.5% | +3.7% | 0.37 | Ngưỡng xác suất trong nhóm: 59.2%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +0.0% | 0.5% | -0.5% | -0.58 | Ngưỡng xác suất trong nhóm: 64.7%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_1d=14.81; return_5d=12.24; return_3d=11.30; adx_14=10.21; return_2d=9.92; return_skew_20d=9.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 17.29; mục tiêu 1 20.29; mục tiêu 2 20.29.
- Tỷ lệ lợi nhuận/rủi ro 2.15; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 17.79 (-1.97%).
- P10/P90 cuối kỳ 15.89 / 20.29.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.493 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.499 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4926427575034874, AUC logistic=0.4954251601193958.
- Điều kiện phát hành tín hiệu: Probability 48.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Mô hình Logistic đối chứng: 47.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 41.8%.
- Mức dừng lỗ tham chiếu 17.29, mục tiêu 1 20.29, tỷ lệ lợi nhuận/rủi ro 2.15.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.
