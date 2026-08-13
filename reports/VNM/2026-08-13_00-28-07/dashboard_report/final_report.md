# Báo cáo ngày 2026-08-13 - VNM

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 61.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 57.4%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: WEAK - Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, AUC của mô hình, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng.
- Nếu chưa có cổ phiếu: WAIT - Ngưỡng sau phí đang tốt hơn là 0.60, nhưng xác suất hiện tại chỉ 57.4%.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm.

## Phân tích kỹ thuật

- SMA20 59.64; SMA60 57.55; RSI14 63.5.
- MACD 1.201; đường tín hiệu 0.984; biểu đồ cột 0.217.
- ATR14 1.43; ATR% 2.3%; ADX14 28.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 63.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.5, +DI vượt -DI.
- Thanh khoản: Thấp - 0.49 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VINAMILK.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 11.82.
- P/B: 4.07.
- ROE: 33.9%.
- ROA: 19.8%.
- Market cap: 129,577.2 tỷ.
- Revenue Growth: 12.7%.
- Profit Growth: 28.0%.
- P/E 11.82: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 4.07: nên đọc cùng ROE và đặc thù ngành.
- ROE 33.9%: hiệu quả vốn chủ sở hữu tốt.
- ROA 19.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.91: thanh khoản ngắn hạn khá.
- Revenue Growth 12.7% YoY.
- Profit Growth 28.0% YoY.
- CFO/LNST 1.01: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:57:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.503; AUC 0.526; log-loss 0.683.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.535; AUC 0.558.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 89.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.9%; Sharpe -1.41; mức sụt giảm tối đa -35.8%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | WEAK | Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, AUC của mô hình, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng. |
| Nếu chưa có cổ phiếu | WAIT | Chờ điểm mua tốt hơn |
| Lý do cho mua mới |  | Ngưỡng sau phí đang tốt hơn là 0.60, nhưng xác suất hiện tại chỉ 57.4%. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm. |
| Xác suất hiện tại | 57.4% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.60 | Ngưỡng 0.60; net +7.4%; 15 vòng. |
| Baseline cấu hình | 69 vòng | Net sau phí -33.9%. |
| Reward/Risk | 2.33 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 6 điểm | Tích cực; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -7.8% | Gross PnL -7,821,324 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -33.1% | 69 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 27,970,127 VND. |
| Kịch bản sau chi phí | -33.9% | Net PnL -33,866,127 VND; gross - cost gap khoảng +26.0%. |
| Ngưỡng phí hòa vốn | -11.8 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 69 phiên active/69 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 69 | -7.8% | 33.1% | -33.9% | -1.41 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 31 | +7.4% | 15.1% | -7.6% | -0.33 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 15 | +15.5% | 7.3% | +7.4% | 0.42 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 12 | +12.6% | 5.9% | +6.2% | 0.36 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +18.4% | 4.9% | +12.8% | 0.80 | Ngưỡng xác suất trong nhóm: 63.4%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +13.7% | 2.5% | +11.0% | 0.78 | Ngưỡng xác suất trong nhóm: 75.2%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +0.0% | 0.5% | -0.5% | -0.58 | Ngưỡng xác suất trong nhóm: 81.4%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=11.57; relative_strength_20d=11.12; return_1d=10.65; return_3d=10.43; month_of_year=10.12; volatility_20d=9.69.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 59.65; mục tiêu 1 67.83; mục tiêu 2 67.83.
- Tỷ lệ lợi nhuận/rủi ro 2.33; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 61.43 (-0.60%).
- P10/P90 cuối kỳ 56.15 / 67.83.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.526 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.503 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5261655414807923, AUC logistic=0.55789339758423.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.405609731775067.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 57.4%.
- Mô hình Logistic đối chứng: 56.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.4%.
- Mức dừng lỗ tham chiếu 59.65, mục tiêu 1 67.83, tỷ lệ lợi nhuận/rủi ro 2.33.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 2, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 6. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 63.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 28.5, +DI vượt -DI.); Thanh khoản: Thấp (0.49 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VINAMILK; kỳ 2026-Q2; P/E 11.82; P/B 4.07; ROE 33.9%; ROA 19.8%; Debt/Equity 0.61; Revenue Growth 12.7%; Profit Growth 28.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 2, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:28:24.892167+00:00; News Reader đọc được 4 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.526 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.503 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5261655414807923, AUC logistic=0.55789339758423
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.405609731775067
- News Reader [VietstockFinance]: VNM: Khuyến nghị MUA với giá mục tiêu 79,600 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-12T05:45:50+00:00)
- News Reader [Tin nhanh chứng khoán]: Sự kiện chứng khoán đáng chú ý ngày 13/8 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-12T10:52:41+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 12/8: TNG, DGW, KBC và VNM có gì đáng kỳ vọng? - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-11T23:21:00+00:00)
- News Reader [Vietstock]: VNM: Báo cáo kết quả giao dịch cổ phiếu của tổ chức có liên quan đến người nội bộ Công ty TNHH MTV Đầu tư SCIC - Vietstock | nhóm: khác (2026-08-12T10:25:33+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.526 < 0.540
- ML guard: Balanced accuracy 0.503 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5261655414807923, AUC logistic=0.55789339758423
- ML guard: Lợi thế OOS ròng không đạt: return=-0.3386612699999999, Sharpe=-1.405609731775067
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.
- Ollama AI chưa hoàn tất trong lệnh full: Exit: 

### Nguồn live research

- [VietstockFinance] VNM: Khuyến nghị MUA với giá mục tiêu 79,600 đồng/cổ phiếu - VietstockFinance (2026-08-12T05:45:50+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21532/vnm-khuyen-nghi-mua-voi-gia-muc-tieu-79600-dongco-phieu.htm
- [Tin nhanh chứng khoán] Sự kiện chứng khoán đáng chú ý ngày 13/8 - Tin nhanh chứng khoán (2026-08-12T10:52:41+00:00): https://m.tinnhanhchungkhoan.vn/su-kien-chung-khoan-dang-chu-y-ngay-138-post395823.amp
- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 12/8: TNG, DGW, KBC và VNM có gì đáng kỳ vọng? - thuonghieucongluan.com.vn (2026-08-11T23:21:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-12-8-tng-dgw-kbc-va-vnm-co-gi-dang-ky-vong-a330120.html
- [Vietstock] VNM: Báo cáo kết quả giao dịch cổ phiếu của tổ chức có liên quan đến người nội bộ Công ty TNHH MTV Đầu tư SCIC - Vietstock (2026-08-12T10:25:33+00:00): https://vietstock.vn/2026/08/vnm-bao-cao-ket-qua-giao-dich-co-phieu-cua-to-chuc-co-lien-quan-den-nguoi-noi-bo-cong-ty-tnhh-mtv-dau-tu-scic-737-1479829.amp

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VNM/2026-08-13_00-28-07/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 9
- Số dòng giá có news feature: 8
- XGBoost probability mới nhất: 0.543
- AUC OOS: 0.509
- Balanced accuracy OOS: 0.504
- Backtest total return: -0.245
- Base XGBoost probability: 0.574
- Chênh lệch News-adjusted - Base: -0.031
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
