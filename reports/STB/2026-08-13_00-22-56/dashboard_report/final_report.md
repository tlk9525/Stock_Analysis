# Báo cáo ngày 2026-08-13 - STB

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,595 phiên.
- Giá đóng cửa: 74.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: WEAK - Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, AUC của mô hình, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng.
- Nếu chưa có cổ phiếu: WAIT - Ngưỡng sau phí đang tốt hơn là 0.58, nhưng xác suất hiện tại chỉ 50.0%.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm.

## Phân tích kỹ thuật

- SMA20 72.78; SMA60 71.38; RSI14 56.8.
- MACD 0.700; đường tín hiệu 0.494; biểu đồ cột 0.206.
- ATR14 2.00; ATR% 2.7%; ADX14 15.5.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 15.5.
- Thanh khoản: Thấp - 0.39 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: NH Sài Gòn Tài Lộc (SACOMBANK).
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 45.48.
- P/B: 2.23.
- ROE: 5.0%.
- ROA: 0.4%.
- Market cap: 140,071.5 tỷ.
- Revenue Growth: 28.1%.
- Profit Growth: -53.5%.
- P/E 45.48: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 2.23: nên đọc cùng ROE và đặc thù ngành.
- ROE 5.0%: hiệu quả vốn còn yếu.
- Debt/Equity 13.20: đòn bẩy cao, cần đọc theo ngành.
- NPL 7.5%: cần theo dõi.
- Revenue Growth 28.1% YoY.
- Profit Growth -53.5% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T09:37:32+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.504; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.511.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 33.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -13.4%; Sharpe -0.48; mức sụt giảm tối đa -19.5%.

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Model health | WEAK | Có ngưỡng sau phí dương trong sensitivity, nhưng model health chưa sạch: Kiểm thử chiến lược có lợi thế ròng, AUC của mô hình, Độ chính xác cân bằng của mô hình, XGBoost vượt mô hình Logistic đối chứng. |
| Nếu chưa có cổ phiếu | WAIT | Chờ điểm mua tốt hơn |
| Lý do cho mua mới |  | Ngưỡng sau phí đang tốt hơn là 0.58, nhưng xác suất hiện tại chỉ 50.0%. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm. |
| Xác suất hiện tại | 50.0% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.58 | Ngưỡng 0.58; net +7.7%; 14 vòng. |
| Baseline cấu hình | 38 vòng | Net sau phí -13.4%. |
| Reward/Risk | 2.92 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |
| Kỹ thuật / tin | 4 điểm | Hồi phục / nghiêng tăng; news warning: không; sentiment 0.00. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +4.2% | Gross PnL 4,214,366 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -18.5% | 38 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 17,977,860 VND. |
| Kịch bản sau chi phí | -13.4% | Net PnL -13,432,860 VND; gross - cost gap khoảng +17.6%. |
| Ngưỡng phí hòa vốn | 11.4 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì xem khung HOLD/REDUCE/SELL riêng theo model health, kỹ thuật, tin và stop-loss. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 38 phiên active/38 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 38 | +4.2% | 18.5% | -13.4% | -0.48 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 14 | +15.3% | 6.9% | +7.7% | 0.45 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 7 | +0.7% | 3.4% | -2.7% | -0.32 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 2 | -1.6% | 1.0% | -2.6% | -0.78 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +10.8% | 4.9% | +5.5% | 0.34 | Ngưỡng xác suất trong nhóm: 58.5%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | -2.4% | 2.4% | -4.8% | -0.71 | Ngưỡng xác suất trong nhóm: 60.7%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -1.3% | 0.5% | -1.8% | -0.58 | Ngưỡng xác suất trong nhóm: 69.2%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: market_return_1d=13.54; return_5d=11.91; beta_60d=11.88; range_pct=11.51; return_1d=11.23; bb_position_20=11.11.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.09; mục tiêu 1 84.34; mục tiêu 2 84.34.
- Tỷ lệ lợi nhuận/rủi ro 2.92; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 73.34 (-1.03%).
- P10/P90 cuối kỳ 64.53 / 84.34.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.504 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.504 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 45.2%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.0%.
- Mức dừng lỗ tham chiếu 71.09, mục tiêu 1 84.34, tỷ lệ lợi nhuận/rủi ro 2.92.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 56.8.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 15.5.); Thanh khoản: Thấp (0.39 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: NH Sài Gòn Tài Lộc (SACOMBANK); kỳ 2026-Q2; P/E 45.48; P/B 2.23; ROE 5.0%; ROA 0.4%; Debt/Equity 13.20; Revenue Growth 28.1%; Profit Growth -53.5%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, nganh: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:23:13.056235+00:00; News Reader đọc được 1 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.504 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.504 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163
- ML decision artifact: NO_EDGE. Probability 50.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394
- News Reader [dautucophieu.net]: Cập nhật cổ phiếu STB – Q2/2026: Chi phí dự phòng gia tăng áp lực lên lợi nhuận - dautucophieu.net | nhóm: ket_qua_kinh_doanh, nganh, rui_ro (2026-08-11T04:22:31+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.504 < 0.540
- ML guard: Balanced accuracy 0.504 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5035330612004303, AUC logistic=0.5105512901752163
- ML guard: Probability 50.0% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.13432860000000035, Sharpe=-0.48071319287150394
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [dautucophieu.net] Cập nhật cổ phiếu STB – Q2/2026: Chi phí dự phòng gia tăng áp lực lên lợi nhuận - dautucophieu.net (2026-08-11T04:22:31+00:00): https://dautucophieu.net/cap-nhat-co-phieu-stb-q2-2026-chi-phi-du-phong-gia-tang-ap-luc-len-loi-nhuan/

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/STB/2026-08-13_00-22-56/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 2
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.500
- AUC OOS: 0.512
- Balanced accuracy OOS: 0.497
- Backtest total return: -0.097
- Base XGBoost probability: 0.500
- Chênh lệch News-adjusted - Base: +0.000
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
