# Báo cáo ngày 2026-08-13 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-12, 3,687 phiên.
- Giá đóng cửa: 20.45 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Khuyến nghị sau phí: WAIT - Chờ điểm mua tốt hơn.
- Lý do khuyến nghị: Ngưỡng sau phí đang tốt hơn là 0.60, nhưng xác suất hiện tại chỉ 53.7%.

## Phân tích kỹ thuật

- SMA20 19.35; SMA60 19.86; RSI14 61.3.
- MACD 0.142; đường tín hiệu -0.056; biểu đồ cột 0.198.
- ATR14 0.45; ATR% 2.2%; ADX14 25.0.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.0, +DI vượt -DI.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Cực trị - %K 96.4, %D 93.7.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.27.
- P/B: 1.30.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 204,899.1 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.27: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.30: nên đọc cùng ROE và đặc thù ngành.
- ROE 20.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 10.06: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.4%: đang ở mức kiểm soát.
- Revenue Growth 18.5% YoY.
- Profit Growth 40.0% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:40:35+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-17 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.520; AUC 0.498; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.499.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 41.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -4.9%; Sharpe -0.17; mức sụt giảm tối đa -10.4%.

### Khuyến nghị đầu tư sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Khuyến nghị sau phí | WAIT | Chờ điểm mua tốt hơn |
| Lý do chính |  | Ngưỡng sau phí đang tốt hơn là 0.60, nhưng xác suất hiện tại chỉ 53.7%. |
| Xác suất hiện tại | 53.7% | So với ngưỡng sau phí được chọn từ OOS. |
| Ngưỡng sau phí chọn | 0.60 | Ngưỡng 0.60; net +11.7%; 16 vòng. |
| Baseline cấu hình | 53 vòng | Net sau phí -4.9%. |
| Reward/Risk | 2.73 | Chỉ dùng nếu decision cuối cùng cho phép mở vị thế. |

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +23.6% | Gross PnL 23,571,720 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -26.3% | 53 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 25,628,642 VND. |
| Kịch bản sau chi phí | -4.9% | Net PnL -4,944,642 VND; gross - cost gap khoảng +28.5%. |
| Ngưỡng phí hòa vốn | 44.9 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 53 phiên active/53 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 53 | +23.6% | 26.3% | -4.9% | -0.17 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 27 | +22.9% | 13.4% | +7.5% | 0.43 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 16 | +20.9% | 8.0% | +11.7% | 0.68 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 10 | +17.1% | 5.0% | +11.4% | 0.79 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +17.1% | 5.0% | +11.4% | 0.79 | Ngưỡng xác suất trong nhóm: 62.1%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +16.9% | 2.5% | +14.1% | 0.98 | Ngưỡng xác suất trong nhóm: 64.3%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | +6.4% | 0.5% | +5.9% | 0.63 | Ngưỡng xác suất trong nhóm: 70.8%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: return_1d=11.59; beta_60d=10.76; volatility_20d=10.25; return_2d=9.90; market_return_1d=9.58; excess_return_1d=9.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 19.78; mục tiêu 1 22.66; mục tiêu 2 22.66.
- Tỷ lệ lợi nhuận/rủi ro 2.73; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 20.15 (-1.44%).
- P10/P90 cuối kỳ 18.37 / 22.66.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.498 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49810467106872097, AUC logistic=0.49876701720061956.
- Điều kiện phát hành tín hiệu: Probability 53.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17041681469535072.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.7%.
- Mô hình Logistic đối chứng: 49.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.4%.
- Mức dừng lỗ tham chiếu 19.78, mục tiêu 1 22.66, tỷ lệ lợi nhuận/rủi ro 2.73.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 61.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.0, +DI vượt -DI.); Thanh khoản: Thấp (0.59 lần trung bình.); Stochastic: Cực trị (%K 96.4, %D 93.7.)
- Góc nhìn cơ bản: Artifact cơ bản: MBBank; kỳ 2026-Q2; P/E 6.27; P/B 1.30; ROE 20.7%; ROA 1.9%; Debt/Equity 10.06; Revenue Growth 18.5%; Profit Growth 40.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:13:53.079769+00:00; News Reader đọc được 3 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.498 < 0.540
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49810467106872097, AUC logistic=0.49876701720061956
- ML decision artifact: NO_EDGE. Probability 53.7% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17041681469535072
- News Reader [Báo Pháp Luật Việt Nam]: MBBank (MBB) sắp chào bán cổ phiếu và trả cổ tức cho cổ đông - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-10T14:52:51+00:00)
- News Reader [bnews.vn]: Cổ phiếu đáng chú ý ngày 12/8: BSR, FRT và MBB - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, rui_ro (2026-08-12T01:27:00+00:00)
- News Reader [nguoiquansat.vn]: Tuần tới, MB chốt quyền nhận cổ tức 15%, mua thêm cổ phiếu giá 10.000 đồng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-09T06:38:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.498 < 0.540
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.49810467106872097, AUC logistic=0.49876701720061956
- ML guard: Probability 53.7% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17041681469535072
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Báo Pháp Luật Việt Nam] MBBank (MBB) sắp chào bán cổ phiếu và trả cổ tức cho cổ đông - Báo Pháp Luật Việt Nam (2026-08-10T14:52:51+00:00): https://doanhnhan.baophapluat.vn/mbbank-mbb-sap-chao-ban-co-phieu-va-tra-co-tuc-cho-co-dong.html
- [bnews.vn] Cổ phiếu đáng chú ý ngày 12/8: BSR, FRT và MBB - bnews.vn (2026-08-12T01:27:00+00:00): https://bnews.vn/co-phieu-dang-chu-y-ngay-12-8-bsr-frt-va-mbb/432403.html
- [nguoiquansat.vn] Tuần tới, MB chốt quyền nhận cổ tức 15%, mua thêm cổ phiếu giá 10.000 đồng - nguoiquansat.vn (2026-08-09T06:38:01+00:00): https://nguoiquansat.vn/tuan-toi-mb-chot-quyen-nhan-co-tuc-15-mua-them-co-phieu-gia-10-000-dong-309416.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/MBB/2026-08-13_00-13-37/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 13
- Số dòng giá có news feature: 8
- XGBoost probability mới nhất: 0.520
- AUC OOS: 0.482
- Balanced accuracy OOS: 0.514
- Backtest total return: -0.105
- Base XGBoost probability: 0.537
- Chênh lệch News-adjusted - Base: -0.017
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
