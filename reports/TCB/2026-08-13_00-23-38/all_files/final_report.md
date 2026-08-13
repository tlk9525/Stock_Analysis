# Báo cáo ngày 2026-08-13 - TCB

## Tổng quan

- Dữ liệu: 2018-06-04 -> 2026-08-12, 2,048 phiên.
- Giá đóng cửa: 31.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: BAD - Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS.
- Nếu chưa có cổ phiếu: NO_EDGE - Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế.
- Nếu đang nắm giữ: REDUCE_OR_EXIT - Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật.

## Phân tích kỹ thuật

- SMA20 29.77; SMA60 31.49; RSI14 57.4.
- MACD -0.231; đường tín hiệu -0.582; biểu đồ cột 0.350.
- ATR14 0.84; ATR% 2.7%; ADX14 28.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 57.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 28.0, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.06 lần trung bình.
- Stochastic: Cực trị - %K 98.7, %D 94.7.

## Phân tích cơ bản

- Doanh nghiệp: Techcombank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.10.
- P/B: 1.23.
- ROE: 14.8%.
- ROA: 2.3%.
- Market cap: 219,673.5 tỷ.
- Revenue Growth: 17.3%.
- Profit Growth: 17.7%.
- P/E 8.10: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.23: nên đọc cùng ROE và đặc thù ngành.
- ROA 2.3%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 5.74: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.1%: đang ở mức kiểm soát.
- Revenue Growth 17.3% YoY.
- Profit Growth 17.7% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.18 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:42:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.486; AUC 0.500; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.495; AUC 0.501.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 15.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -27.1%; Sharpe -1.65; mức sụt giảm tối đa -27.7%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | BAD | Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS. |
| Nếu chưa có cổ phiếu | NO_EDGE | Chưa có ngưỡng sau phí đủ tốt |
| Lý do cho mua mới |  | Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; không nên cố mở vị thế. |
| Nếu đang nắm giữ | REDUCE_OR_EXIT | Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật. |
| Xác suất hiện tại | 50.9% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | N/A | Chưa có threshold nào đạt net dương + Sharpe dương. |
| Baseline cấu hình | 42 vòng | Net sau phí -27.1%. |
| Reward/Risk | 7.14 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 6 điểm | Tích cực; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | -10.3% | Gross PnL -10,309,127 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -20.6% | 42 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 18,776,580 VND. |
| Kịch bản sau chi phí | -27.1% | Net PnL -27,056,580 VND; gross - cost gap khoảng +16.7%. |
| Ngưỡng phí hòa vốn | -25.1 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không đủ lợi thế sau phí; giữ NO_EDGE. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 42 phiên active/42 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 42 | -10.3% | 20.6% | -27.1% | -1.65 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 18 | -4.8% | 8.8% | -12.9% | -1.14 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 8 | -3.6% | 3.9% | -7.3% | -0.70 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 4 | -4.2% | 2.0% | -6.1% | -0.83 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | -5.6% | 4.9% | -10.1% | -0.94 | Ngưỡng xác suất trong nhóm: 59.2%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -5.3% | 2.4% | -7.6% | -0.98 | Ngưỡng xác suất trong nhóm: 61.2%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -2.3% | 0.5% | -2.7% | -0.59 | Ngưỡng xác suất trong nhóm: 64.7%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: volatility_20d=13.29; bb_position_20=11.07; atr_pct_14=10.33; relative_strength_20d=9.83; excess_return_5d=9.70; market_return_1d=9.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.17; mục tiêu 1 35.12; mục tiêu 2 35.12.
- Tỷ lệ lợi nhuận/rủi ro 7.14; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 31.43 (-0.24%).
- P10/P90 cuối kỳ 27.91 / 35.12.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.500 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.486 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4998236331569665, AUC logistic=0.50100452419293.
- Điều kiện phát hành tín hiệu: Probability 50.9% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6457936868409828.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.9%.
- Mô hình Logistic đối chứng: 49.1%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.8%.
- Mức dừng lỗ tham chiếu 31.17, mục tiêu 1 35.12, tỷ lệ lợi nhuận/rủi ro 7.14.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 4, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 6. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 57.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 28.0, +DI vượt -DI.); Thanh khoản: Bình thường (1.06 lần trung bình.); Stochastic: Cực trị (%K 98.7, %D 94.7.)
- Góc nhìn cơ bản: Artifact cơ bản: Techcombank; kỳ 2026-Q2; P/E 8.10; P/B 1.23; ROE 14.8%; ROA 2.3%; Debt/Equity 5.74; Revenue Growth 17.3%; Profit Growth 17.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 4, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:23:53.918297+00:00; News Reader đọc được 4 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.500 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.486 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4998236331569665, AUC logistic=0.50100452419293
- ML decision artifact: NO_EDGE. Probability 50.9% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6457936868409828
- News Reader [Tuổi Trẻ]: Tự doanh chứng khoán mua ròng hàng trăm tỉ đồng, cổ phiếu TCB áp sát kỷ lục lịch sử - Tuổi Trẻ | nhóm: nganh (2026-08-10T12:16:00+00:00)
- News Reader [VietnamFinance]: TCB cùng nhóm cổ phiếu doanh nghiệp Nhà nước 'kéo' VN-Index tăng gần 9 điểm - VietnamFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-10T09:22:36+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu TCB bứt phá, nhóm ngân hàng đồng loạt tăng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, nganh (2026-08-10T09:11:01+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-10T16:09:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.500 < 0.540
- ML guard: Balanced accuracy 0.486 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4998236331569665, AUC logistic=0.50100452419293
- ML guard: Probability 50.9% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2705657999999995, Sharpe=-1.6457936868409828
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Tuổi Trẻ] Tự doanh chứng khoán mua ròng hàng trăm tỉ đồng, cổ phiếu TCB áp sát kỷ lục lịch sử - Tuổi Trẻ (2026-08-10T12:16:00+00:00): https://tuoitre.vn/tu-doanh-chung-khoan-mua-rong-hang-tram-ti-dong-co-phieu-tcb-ap-sat-ky-luc-lich-su-100260810184528929.htm
- [VietnamFinance] TCB cùng nhóm cổ phiếu doanh nghiệp Nhà nước 'kéo' VN-Index tăng gần 9 điểm - VietnamFinance (2026-08-10T09:22:36+00:00): https://vietnamfinance.vn/tcb-cung-nhom-co-phieu-doanh-nghiep-nha-nuoc-keo-vn-index-tang-gan-9-diem-d148847.html
- [nguoiquansat.vn] Cổ phiếu TCB bứt phá, nhóm ngân hàng đồng loạt tăng - nguoiquansat.vn (2026-08-10T09:11:01+00:00): https://nguoiquansat.vn/co-phieu-tcb-but-pha-nhom-ngan-hang-dong-loat-tang-309624.html
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 11/8: TCB, GAS, VGC - nguoiquansat.vn (2026-08-10T16:09:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-11-8-tcb-gas-vgc-309709.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/TCB/2026-08-13_00-23-38/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 15
- Số dòng giá có news feature: 9
- XGBoost probability mới nhất: 0.497
- AUC OOS: 0.490
- Balanced accuracy OOS: 0.491
- Backtest total return: -0.150
- Base XGBoost probability: 0.509
- Chênh lệch News-adjusted - Base: -0.012
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
