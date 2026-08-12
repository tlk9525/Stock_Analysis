# Báo cáo ngày 2026-08-11 - MWG

## Tổng quan

- Dữ liệu: 2014-07-14 -> 2026-08-11, 3,016 phiên.
- Giá đóng cửa: 73.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 41.5%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 70.97; SMA60 74.92; RSI14 52.0.
- MACD -0.786; đường tín hiệu -1.445; biểu đồ cột 0.659.
- ATR14 2.43; ATR% 3.3%; ADX14 27.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 27.8, -DI vượt +DI.
- Thanh khoản: Thấp - 0.26 lần trung bình.
- Stochastic: Cực trị - %K 93.5, %D 82.9.

## Phân tích cơ bản

- Doanh nghiệp: Thế giới di động.
- Ngành: Retail.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 10.95.
- P/B: 3.01.
- ROE: 29.2%.
- ROA: 11.2%.
- Market cap: 107,730.9 tỷ.
- Revenue Growth: 29.6%.
- Profit Growth: 100.4%.
- P/E 10.95: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 29.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 11.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.44: thanh khoản ngắn hạn khá.
- Revenue Growth 29.6% YoY.
- Profit Growth 100.4% YoY.
- CFO/LNST 5.06: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T09:51:48+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-23 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.507; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.526.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 87.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -6.6%; Sharpe -0.21; mức sụt giảm tối đa -14.2%.
- Mức độ quan trọng của đặc trưng: beta_60d=8.25; stoch_k_14=7.75; day_of_week=7.66; return_2d=7.51; relative_strength_20d=7.25; excess_return_1d=7.25.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 69.36; mục tiêu 1 81.51; mục tiêu 2 81.51.
- Tỷ lệ lợi nhuận/rủi ro 2.03; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 72.49 (-0.69%).
- P10/P90 cuối kỳ 64.56 / 81.51.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.506640625, AUC logistic=0.5259515224358975.
- Điều kiện phát hành tín hiệu: Probability 41.5% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -2 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.21083208477105841.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 41.5%.
- Mô hình Logistic đối chứng: 43.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.0%.
- Mức dừng lỗ tham chiếu 69.36, mục tiêu 1 81.51, tỷ lệ lợi nhuận/rủi ro 2.03.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 52.0.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 27.8, -DI vượt +DI.); Thanh khoản: Thấp (0.26 lần trung bình.); Stochastic: Cực trị (%K 93.5, %D 82.9.)
- Góc nhìn cơ bản: Artifact cơ bản: Thế giới di động; kỳ 2026-Q2; P/E 10.95; P/B 3.01; ROE 29.2%; ROA 11.2%; Debt/Equity 1.89; Revenue Growth 29.6%; Profit Growth 100.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:05:28.762885+00:00; News Reader đọc được 4 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.507 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.511 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.506640625, AUC logistic=0.5259515224358975
- ML decision artifact: NO_EDGE. Probability 41.5% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -2 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.21083208477105841
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 10/8: Cơ hội tiềm năng với MWG và DMX - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh (2026-08-09T22:00:00+00:00)
- News Reader [Tin nhanh chứng khoán]: Thế giới Di động (MWG) sẽ không mua cổ phiếu quỹ trong năm 2026 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-05T00:21:38+00:00)
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 10/8: MSN, MWG, FPT - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-09T14:51:01+00:00)
- News Reader [VietstockFinance]: MWG: Khuyến nghị MUA với giá mục tiêu 107,300 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-08T03:01:23+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.507 < 0.540
- ML guard: Balanced accuracy 0.511 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.506640625, AUC logistic=0.5259515224358975
- ML guard: Probability 41.5% < 55.0%
- ML guard: Technical score -2 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.21083208477105841
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

- [VOV.VN] Một số cổ phiếu cần quan tâm 10/8: Cơ hội tiềm năng với MWG và DMX - VOV.VN (2026-08-09T22:00:00+00:00): https://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-108-co-hoi-tiem-nang-voi-mwg-va-dmx-post1322330.vov
- [Tin nhanh chứng khoán] Thế giới Di động (MWG) sẽ không mua cổ phiếu quỹ trong năm 2026 - Tin nhanh chứng khoán (2026-08-05T00:21:38+00:00): https://www.tinnhanhchungkhoan.vn/the-gioi-di-dong-mwg-se-khong-mua-co-phieu-quy-trong-nam-2026-post395305.html
- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 10/8: MSN, MWG, FPT - nguoiquansat.vn (2026-08-09T14:51:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-10-8-msn-mwg-fpt-309471.html
- [VietstockFinance] MWG: Khuyến nghị MUA với giá mục tiêu 107,300 đồng/cổ phiếu - VietstockFinance (2026-08-08T03:01:23+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21390/mwg-khuyen-nghi-mua-voi-gia-muc-tieu-107300-dongco-phieu.htm?languageid=1

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
