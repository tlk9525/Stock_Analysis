# Báo cáo ngày 2026-08-12 - GMD

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-12, 4,594 phiên.
- Giá đóng cửa: 77.20 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 75.75; SMA60 75.58; RSI14 55.1.
- MACD 0.530; đường tín hiệu 0.245; biểu đồ cột 0.285.
- ATR14 2.18; ATR% 2.8%; ADX14 17.0.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 55.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 17.0.
- Thanh khoản: Thấp - 0.62 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Tập đoàn Gemadept.
- Ngành: Industrial Goods & Services.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.78.
- P/B: 2.43.
- ROE: 19.4%.
- ROA: 12.8%.
- Market cap: 33,505.9 tỷ.
- Revenue Growth: 17.9%.
- Profit Growth: 154.6%.
- P/E 12.78: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.43: nên đọc cùng ROE và đặc thù ngành.
- ROE 19.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.42: thanh khoản ngắn hạn khá.
- Revenue Growth 17.9% YoY.
- Profit Growth 154.6% YoY.
- CFO/LNST 0.54: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.14 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-07T08:30:10+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-23 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.508; AUC 0.528; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.512; AUC 0.539.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 52.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -20.5%; Sharpe -0.74; mức sụt giảm tối đa -21.9%.
- Mức độ quan trọng của đặc trưng: day_of_week=10.66; return_kurtosis_20d=9.95; return_3d=9.95; macd_pct=9.90; return_10d=9.88; return_2d=9.57.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 74.83; mục tiêu 1 82.00; mục tiêu 2 86.82.
- Tỷ lệ lợi nhuận/rủi ro 1.60; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 76.96 (-0.31%).
- P10/P90 cuối kỳ 67.89 / 86.82.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.528 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.508 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5276393751683275, AUC logistic=0.5390295358649789.
- Điều kiện phát hành tín hiệu: Probability 48.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7448701519430575.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Mô hình Logistic đối chứng: 50.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.7%.
- Mức dừng lỗ tham chiếu 74.83, mục tiêu 1 82.00, tỷ lệ lợi nhuận/rủi ro 1.60.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 3, nganh: 4, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 4. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 55.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 17.0.); Thanh khoản: Thấp (0.62 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Tập đoàn Gemadept; kỳ 2026-Q2; P/E 12.78; P/B 2.43; ROE 19.4%; ROA 12.8%; Debt/Equity 0.36; Revenue Growth 17.9%; Profit Growth 154.6%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 3, nganh: 4, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:10:35.808086+00:00; News Reader đọc được 5 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.528 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.508 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5276393751683275, AUC logistic=0.5390295358649789
- ML decision artifact: NO_EDGE. Probability 48.1% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7448701519430575
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T23:23:00+00:00)
- News Reader [vietstock.vn]: GMD: Thông báo nhận được công văn của UBCKNN về tài liệu báo cáo phát hành cổ phiếu theo chương trình lựa chọn cho người lao động - vietstock.vn | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-07T08:30:10+00:00)
- News Reader [doanhnhan.baophapluat.vn]: Tập đoàn Gemadept (GMD): Phát hành thành công gần 6,4 triệu cổ phiếu ESOP, lãi quý II tăng bằng lần - doanhnhan.baophapluat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh (2026-08-06T02:06:00+00:00)
- News Reader [MoneyF]: Cổ phiếu đáng chú ý ngày 7/8: FPT hưởng lợi từ làn sóng AI, GMD chờ cú hích Gemalink - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-07T00:41:00+00:00)
- News Reader [nguoiquansat.vn]: CTCK khuyến nghị 6 cổ phiếu hot trong tháng 8/2026, tiềm năng tăng giá hàng chục % - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T00:06:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.528 < 0.540
- ML guard: Balanced accuracy 0.508 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5276393751683275, AUC logistic=0.5390295358649789
- ML guard: Probability 48.1% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.2050639400000005, Sharpe=-0.7448701519430575
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

- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn (2026-08-06T23:23:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-7-8-fpt-gmd-sab-a329496.html
- [vietstock.vn] GMD: Thông báo nhận được công văn của UBCKNN về tài liệu báo cáo phát hành cổ phiếu theo chương trình lựa chọn cho người lao động - vietstock.vn (2026-08-07T08:30:10+00:00): https://vietstock.vn/2026/08/gmd-thong-bao-nhan-duoc-cong-van-cua-ubcknn-ve-tai-lieu-bao-cao-phat-hanh-co-phieu-theo-chuong-trinh-lua-chon-cho-nguoi-lao-dong-830-1478078.amp
- [doanhnhan.baophapluat.vn] Tập đoàn Gemadept (GMD): Phát hành thành công gần 6,4 triệu cổ phiếu ESOP, lãi quý II tăng bằng lần - doanhnhan.baophapluat.vn (2026-08-06T02:06:00+00:00): https://doanhnhan.baophapluat.vn/tap-doan-gemadept-gmd-phat-hanh-thanh-cong-gan-6-4-trieu-co-phieu-esop-lai-quy-ii-tang-bang-lan.html
- [MoneyF] Cổ phiếu đáng chú ý ngày 7/8: FPT hưởng lợi từ làn sóng AI, GMD chờ cú hích Gemalink - MoneyF (2026-08-07T00:41:00+00:00): https://moneyf.vn/co-phieu-dang-chu-y-ngay-78-fpt-huong-loi-tu-lan-s-krbgudrq
- [nguoiquansat.vn] CTCK khuyến nghị 6 cổ phiếu hot trong tháng 8/2026, tiềm năng tăng giá hàng chục % - nguoiquansat.vn (2026-08-06T00:06:01+00:00): https://nguoiquansat.vn/ctck-khuyen-nghi-6-co-phieu-hot-trong-thang-8-2026-tiem-nang-tang-gia-hang-chuc-308720.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
