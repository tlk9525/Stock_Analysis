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
- Mức độ quan trọng của đặc trưng: volatility_20d=13.74; macd_pct=12.47; return_1d=11.38; corr_60d=11.30; market_return_1d=10.80; return_20d=10.52.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 24.88; mục tiêu 1 29.82; mục tiêu 2 29.82.
- Tỷ lệ lợi nhuận/rủi ro 2.52; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 25.96 (-0.71%).
- P10/P90 cuối kỳ 22.79 / 29.82.

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
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 2, nganh: 2, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 59.9.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 15.4.); Thanh khoản: Thấp (0.59 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Chứng khoán HSC; kỳ 2026-Q2; P/E 20.17; P/B 2.06; ROE 9.8%; ROA 3.1%; Debt/Equity 1.82; Revenue Growth 15.1%; Profit Growth 42.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 2, nganh: 2, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:11:31.608846+00:00; News Reader đọc được 5 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.518 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029
- ML decision artifact: NO_EDGE. Probability 52.6% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055
- News Reader [vietstock.vn]: HFIC chi hơn 300 tỷ thực hiện quyền mua cổ phiếu HCM - vietstock.vn | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-12T04:37:51+00:00)
- News Reader [Tin nhanh chứng khoán]: Cổ phiếu Hạ tầng GELEX (GEL) chính thức đủ điều kiện giao dịch ký quỹ - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, rui_ro (2026-08-12T00:14:54+00:00)
- News Reader [VietnamFinance]: Cổ phiếu HCM đi ngược nhóm chứng khoán, lập đỉnh lịch sử với mức tăng gần 40% từ đầu năm - VietnamFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-11T09:14:28+00:00)
- News Reader [nguoiquansat.vn]: Một tổ chức đăng ký mua hơn 30 triệu cổ phiếu Chứng khoán HSC - nguoiquansat.vn | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-12T07:52:01+00:00)
- News Reader [Nhịp sống kinh doanh]: Tiếp tục làm cổ đông lớn của HSC, HFIC chi hơn 304 tỷ đồng mua thêm cổ phiếu - Nhịp sống kinh doanh | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-12T07:40:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Balanced accuracy 0.518 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5579594897488298, AUC logistic=0.5625782846595029
- ML guard: Probability 52.6% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.12580115000000103, Sharpe=-0.3371169628402055
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

- [vietstock.vn] HFIC chi hơn 300 tỷ thực hiện quyền mua cổ phiếu HCM - vietstock.vn (2026-08-12T04:37:51+00:00): https://vietstock.vn/2026/08/hfic-chi-hon-300-ty-thuc-hien-quyen-mua-co-phieu-hcm-739-1479547.htm
- [Tin nhanh chứng khoán] Cổ phiếu Hạ tầng GELEX (GEL) chính thức đủ điều kiện giao dịch ký quỹ - Tin nhanh chứng khoán (2026-08-12T00:14:54+00:00): https://www.tinnhanhchungkhoan.vn/co-phieu-ha-tang-gelex-gel-chinh-thuc-du-dieu-kien-giao-dich-ky-quy-post395757.html
- [VietnamFinance] Cổ phiếu HCM đi ngược nhóm chứng khoán, lập đỉnh lịch sử với mức tăng gần 40% từ đầu năm - VietnamFinance (2026-08-11T09:14:28+00:00): https://vietnamfinance.vn/co-phieu-hcm-di-nguoc-nhom-chung-khoan-lap-dinh-lich-su-voi-muc-tang-gan-40-tu-dau-nam-d148930.html
- [nguoiquansat.vn] Một tổ chức đăng ký mua hơn 30 triệu cổ phiếu Chứng khoán HSC - nguoiquansat.vn (2026-08-12T07:52:01+00:00): https://nguoiquansat.vn/mot-to-chuc-dang-ky-mua-hon-30-trieu-co-phieu-chung-khoan-hsc-310067.html
- [Nhịp sống kinh doanh] Tiếp tục làm cổ đông lớn của HSC, HFIC chi hơn 304 tỷ đồng mua thêm cổ phiếu - Nhịp sống kinh doanh (2026-08-12T07:40:00+00:00): https://nhipsongkinhdoanh.vn/tiep-tuc-lam-co-dong-lon-cua-hsc--hfic-chi-hon-304-ty-dong-mua-them-co-phieu-31771.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
