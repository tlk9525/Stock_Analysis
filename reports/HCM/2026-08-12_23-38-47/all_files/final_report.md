# Báo cáo ngày 2026-08-12 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-12, 4,301 phiên.
- Giá đóng cửa: 26.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

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

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +18.3% | Gross PnL 18,289,135 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.3% | 61 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,355,115 VND. |
| Kịch bản sau chi phí | -12.6% | Net PnL -12,580,115 VND; gross - cost gap khoảng +30.9%. |
| Ngưỡng phí hòa vốn | 30.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 61 phiên active/61 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Giảm vòng giao dịch bằng ngưỡng xác suất cao hơn

| Kịch bản | Net sau phí | Diễn giải |
|---|---:|---|
| Ngưỡng 0.55 | -12.6% | 61 phiên active/61 vòng; phí cộng dồn 30.3%; Sharpe -0.34. |
| Ngưỡng 0.58 | -2.2% | 38 phiên active/38 vòng; phí cộng dồn 18.9%; Sharpe -0.02. |
| Ngưỡng 0.60 | +0.0% | 31 phiên active/31 vòng; phí cộng dồn 15.4%; Sharpe 0.05. |
| Ngưỡng 0.62 | +6.8% | 20 phiên active/20 vòng; phí cộng dồn 10.0%; Sharpe 0.30. |
Ghi chú: bảng này không tự biến NO_EDGE thành BUY; nó chỉ cho thấy nếu bớt giao dịch thì phí và net thay đổi ra sao.

### Kịch bản chỉ chọn 10 / 5 / 1 vòng mạnh nhất

| Kịch bản | Net sau phí | Diễn giải |
|---|---:|---|
| Top 10 vòng mạnh nhất | +6.2% | Gross +11.6%; phí 5.0%; 10 vòng; xác suất thấp nhất được chọn 66.3%; Sharpe 0.41. |
| Top 5 vòng mạnh nhất | +10.2% | Gross +13.0%; phí 2.5%; 5 vòng; xác suất thấp nhất được chọn 69.0%; Sharpe 0.70. |
| Top 1 vòng mạnh nhất | +5.6% | Gross +6.1%; phí 0.5%; 1 vòng; xác suất thấp nhất được chọn 75.2%; Sharpe 0.60. |
Ghi chú: top-N chọn các phiên có xác suất cao nhất trong tập OOS để minh họa tác động của việc giảm số vòng; không phải khuyến nghị tự động mua/bán.
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
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.518 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029.
- Điều kiện phát hành tín hiệu: Probability 52.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Mô hình Logistic đối chứng: 45.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.3%.
- Mức dừng lỗ tham chiếu 24.88, mục tiêu 1 29.82, tỷ lệ lợi nhuận/rủi ro 2.52.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (co_tuc_va_hanh_dong_doanh_nghiep: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 59.9.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 15.4.); Thanh khoản: Thấp (0.59 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán HSC; kỳ 2026-Q2; P/E 20.17; P/B 2.06; ROE 9.8%; ROA 3.1%; Debt/Equity 1.82; Revenue Growth 15.1%; Profit Growth 42.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: co_tuc_va_hanh_dong_doanh_nghiep: 1. Tác động cần kiểm chứng: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T16:39:07.844286+00:00; News Reader đọc được 1 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.518 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029
- ML decision artifact: NO_EDGE. Probability 52.6% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055
- News Reader [Vietstock]: HFIC chi hơn 300 tỷ thực hiện quyền mua cổ phiếu HCM - Vietstock | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-12T04:37:51+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.518 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029
- ML guard: Probability 52.6% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.
- Ollama AI chưa hoàn tất trong lệnh full: Exit: 

### Nguồn live research

- [Vietstock] HFIC chi hơn 300 tỷ thực hiện quyền mua cổ phiếu HCM - Vietstock (2026-08-12T04:37:51+00:00): https://vietstock.vn/2026/08/hfic-chi-hon-300-ty-thuc-hien-quyen-mua-co-phieu-hcm-739-1479547.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/HCM/2026-08-12_23-38-47/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 17
- Số dòng giá có news feature: 13
- XGBoost probability mới nhất: 0.497
- AUC OOS: 0.545
- Balanced accuracy OOS: 0.524
- Backtest total return: -0.191
- Base XGBoost probability: 0.526
- Chênh lệch News-adjusted - Base: -0.029
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
