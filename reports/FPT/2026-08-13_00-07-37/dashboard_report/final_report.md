# Báo cáo ngày 2026-08-13 - FPT

## Tổng quan

- Dữ liệu: 2008-03-07 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 70.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.61; SMA60 70.82; RSI14 56.1.
- MACD 0.462; đường tín hiệu -0.258; biểu đồ cột 0.720.
- ATR14 1.89; ATR% 2.7%; ADX14 25.2.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 56.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.2, +DI vượt -DI.
- Thanh khoản: Thấp - 0.53 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.14.
- P/B: 3.05.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 122,060.0 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.14: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.05: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.
- CFO/LNST 0.66: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T09:13:52+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.574; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.559.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.

### Breakdown trước phí / sau phí

| Kịch bản | Kết quả | Diễn giải |
|---|---:|---|
| Kịch bản trước chi phí | +2.2% | Gross PnL 2,177,779 VND; chưa trừ commission/slippage/tax. |
| Chi phí giao dịch | -31.9% | 67 vòng; entry 20.0 bps + exit 30.0 bps = 50.0 bps/vòng; tổng phí 28,972,654 VND. |
| Kịch bản sau chi phí | -25.8% | Net PnL -25,799,654 VND; gross - cost gap khoảng +28.0%. |
| Ngưỡng phí hòa vốn | 3.4 bps/vòng | Phí hiện tại 50.0 bps/vòng; cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm. |
| Kết luận hành động | CHƯA CÓ LỢI THẾ (NO_EDGE) | Không mở vị thế mới; nếu đang giữ thì ưu tiên giảm/bán theo kỷ luật vì sau phí vẫn âm. |
| Cách cải thiện cần test | Giảm turnover | Hiện có 67 phiên active/67 vòng; nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn. |

### Bảng chính: turnover, gross, phí và net

| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---|
| Gốc | Ngưỡng gốc ≥ 0.55 | 67 | +2.2% | 31.9% | -25.8% | -0.86 | Baseline 61 vòng nếu model phát tín hiệu nhiều. |
| Ngưỡng 0.58 | Chỉ vào lệnh khi xác suất ≥ 0.58 | 40 | +21.7% | 19.2% | +0.5% | 0.06 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.60 | Chỉ vào lệnh khi xác suất ≥ 0.60 | 25 | +23.9% | 12.0% | +10.0% | 0.46 | Tăng ngưỡng để giảm vòng lệnh. |
| Ngưỡng 0.62 | Chỉ vào lệnh khi xác suất ≥ 0.62 | 17 | +17.8% | 8.2% | +8.6% | 0.45 | Tăng ngưỡng để giảm vòng lệnh. |
| Giới hạn 10 vòng | Tối đa 10 vòng, ưu tiên xác suất cao hơn | 10 | +15.4% | 4.8% | +10.0% | 0.56 | Ngưỡng xác suất trong nhóm: 66.1%. |
| Giới hạn 5 vòng | Tối đa 5 vòng, ưu tiên xác suất cao hơn | 5 | +4.6% | 2.4% | +2.2% | 0.20 | Ngưỡng xác suất trong nhóm: 69.9%. |
| Giới hạn 1 vòng | Tối đa 1 vòng, ưu tiên xác suất cao hơn | 1 | -0.8% | 0.5% | -1.3% | -0.58 | Ngưỡng xác suất trong nhóm: 76.9%. |
Ghi chú: đọc bảng từ trái sang phải để thấy phí giảm khi turnover giảm; các dòng 10/5/1 giới hạn số vòng bằng xác suất model cao hơn, không phải chọn lệnh thắng sau khi biết kết quả và không tự biến NO_EDGE thành BUY.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=15.22; return_1d=14.67; stoch_k_14=12.02; day_of_week=11.51; beta_60d=11.35; excess_return_1d=11.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.11; mục tiêu 1 73.30; mục tiêu 2 79.18.
- Tỷ lệ lợi nhuận/rủi ro 2.05; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.39 (-0.58%).
- P10/P90 cuối kỳ 63.03 / 79.18.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 48.6% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8598343376559678.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.6%.
- Mô hình Logistic đối chứng: 46.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 70.11, mục tiêu 1 73.30, tỷ lệ lợi nhuận/rủi ro 2.05.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 56.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.2, +DI vượt -DI.); Thanh khoản: Thấp (0.53 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: FPT Corp; kỳ 2026-Q2; P/E 12.14; P/B 3.05; ROE 26.5%; ROA 12.8%; Debt/Equity 0.80; Revenue Growth -17.1%; Profit Growth 13.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T17:07:54.256713+00:00; News Reader đọc được 5 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.510 < 0.520
- ML decision artifact: NO_EDGE. Probability 48.6% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8598343376559678
- News Reader [dautucophieu.net]: Cập nhật cổ phiếu FPT – Cuộc gặp với chuyên viên phân tích: Nắm bắt cơ hội từ AI - dautucophieu.net | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-11T05:00:51+00:00)
- News Reader [Chungta]: Cổ phiếu FPT tăng 7 trong 10 phiên gần nhất - Chungta | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-07T07:14:00+00:00)
- News Reader [thoibaotaichinhvietnam.vn]: Gần 20 doanh nghiệp chốt quyền cổ tức trong tuần, mức cao nhất lên tới 100% - thoibaotaichinhvietnam.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-10T19:54:15+00:00)
- News Reader [tapchikinhtetaichinh.vn]: Ba doanh nghiệp trả cổ tức bằng tiền, FPT Online chi 10.000 đồng/cổ phiếu - tapchikinhtetaichinh.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-09T13:05:49+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T23:23:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.510 < 0.520
- ML guard: Probability 48.6% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8598343376559678
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

- [dautucophieu.net] Cập nhật cổ phiếu FPT – Cuộc gặp với chuyên viên phân tích: Nắm bắt cơ hội từ AI - dautucophieu.net (2026-08-11T05:00:51+00:00): https://dautucophieu.net/cap-nhat-co-phieu-fpt-cuoc-gap-voi-chuyen-vien-phan-tich-nam-bat-co-hoi-tu-ai/
- [Chungta] Cổ phiếu FPT tăng 7 trong 10 phiên gần nhất - Chungta (2026-08-07T07:14:00+00:00): https://chungta.vn/kinh-doanh/co-phieu-fpt-tang-7-trong-10-phien-gan-nhat-1141876.html
- [thoibaotaichinhvietnam.vn] Gần 20 doanh nghiệp chốt quyền cổ tức trong tuần, mức cao nhất lên tới 100% - thoibaotaichinhvietnam.vn (2026-08-10T19:54:15+00:00): https://thoibaotaichinhvietnam.vn/gan-20-doanh-nghiep-chot-quyen-co-tuc-trong-tuan-muc-cao-nhat-len-toi-100-202075.html
- [tapchikinhtetaichinh.vn] Ba doanh nghiệp trả cổ tức bằng tiền, FPT Online chi 10.000 đồng/cổ phiếu - tapchikinhtetaichinh.vn (2026-08-09T13:05:49+00:00): https://tapchikinhtetaichinh.vn/ba-doanh-nghiep-tra-co-tuc-bang-tien-fpt-online-chi-10-000-dong-co-phieu-164034.html
- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn (2026-08-06T23:23:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-7-8-fpt-gmd-sab-a329496.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/FPT/2026-08-13_00-07-37/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 13
- Số dòng giá có news feature: 13
- XGBoost probability mới nhất: 0.496
- AUC OOS: 0.575
- Balanced accuracy OOS: 0.509
- Backtest total return: -0.224
- Base XGBoost probability: 0.486
- Chênh lệch News-adjusted - Base: +0.010
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
