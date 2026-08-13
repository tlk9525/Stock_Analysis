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

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 60.9.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Đi ngang (ADX 24.9.); Thanh khoản: Bình thường (1.15 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Petrolimex; kỳ 2026-Q2; P/E 14.44; P/B 1.81; ROE 12.5%; ROA 3.5%; Debt/Equity 2.01; Revenue Growth 78.0%; Profit Growth 105.6%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:18:02.711428+00:00; News Reader đọc được 2 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.512 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.505 < 0.520
- ML decision artifact: NO_EDGE. Probability 50.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7803806544822127
- News Reader [24HMoney]: Petrolimex (PLX) bất ngờ điều chỉnh phương án bán cổ phiếu quỹ - 24HMoney | nhóm: khác (2026-08-10T07:28:22+00:00)
- News Reader [Báo Pháp Luật Việt Nam]: Petrolimex (PLX) dự chi hơn 1.500 tỷ đồng để trả cổ tức năm 2025 - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-11T10:23:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.512 < 0.540
- ML guard: Balanced accuracy 0.505 < 0.520
- ML guard: Probability 50.0% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7803806544822127
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [24HMoney] Petrolimex (PLX) bất ngờ điều chỉnh phương án bán cổ phiếu quỹ - 24HMoney (2026-08-10T07:28:22+00:00): https://24hmoney.vn/news/petrolimex-plx-bat-ngo-dieu-chinh-phuong-an-ban-co-phieu-quy-c1a2818732.html
- [Báo Pháp Luật Việt Nam] Petrolimex (PLX) dự chi hơn 1.500 tỷ đồng để trả cổ tức năm 2025 - Báo Pháp Luật Việt Nam (2026-08-11T10:23:00+00:00): https://doanhnhan.baophapluat.vn/petrolimex-plx-du-chi-hon-1-500-ty-dong-de-tra-co-tuc-nam-2025-0b2486da.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/PLX/2026-08-13_00-17-41/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 7
- Số dòng giá có news feature: 3
- XGBoost probability mới nhất: 0.512
- AUC OOS: 0.490
- Balanced accuracy OOS: 0.508
- Backtest total return: -0.485
- Base XGBoost probability: 0.500
- Chênh lệch News-adjusted - Base: +0.012
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
