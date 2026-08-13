# Báo cáo ngày 2026-08-13 - HCM

## Tổng quan

- Dữ liệu: 2009-05-19 -> 2026-08-12, 4,301 phiên.
- Giá đóng cửa: 26.15 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: WEAK - Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng.
- Nếu chưa có cổ phiếu: WAIT - Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 52.6%.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm.

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
| Model health | WEAK | Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng. |
| Nếu chưa có cổ phiếu | WAIT | Chờ điểm mua tốt hơn |
| Lý do cho mua mới |  | Ngưỡng sau phí đang tốt hơn là 0.62, nhưng xác suất hiện tại chỉ 52.6%. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm. |
| Xác suất hiện tại | 52.6% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.62 | Ngưỡng 0.62; net +6.8%; 20 vòng. |
| Baseline cấu hình | 61 vòng | Net sau phí -12.6%. |
| Reward/Risk | 2.52 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 4 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +18.3% | Gross PnL 18,289,135 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -30.3% | 61 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,355,115 VND. |
| Kịch bản sau chi phí | -12.6% | Net PnL -12,580,115 VND; gross - cost gap khoảng +30.9%. |
| Ngưỡng phí hòa vốn | 30.2 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì xem khung HOLD/REDUCE/SELL riêng theo model health, kỹ thuật, tin và stop-loss. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 61 phiên active/61 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 61 | +18.3% | 30.3% | -12.6% | -0.34 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 38 | +18.1% | 18.9% | -2.2% | -0.02 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 31 | +16.6% | 15.4% | +0.0% | 0.05 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 20 | +17.9% | 10.0% | +6.8% | 0.30 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +11.6% | 5.0% | +6.2% | 0.41 | Ngưỡng xác suất trong nhóm: 66.3%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +13.0% | 2.5% | +10.2% | 0.70 | Ngưỡng xác suất trong nhóm: 69.0%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +6.1% | 0.5% | +5.6% | 0.60 | Ngưỡng xác suất trong nhóm: 75.2%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
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
- Live research: Live snapshot lấy lúc 2026-08-12T17:19:36.979118+00:00; News Reader đọc được 1 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

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

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/HCM/2026-08-13_00-19-21/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 18
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
