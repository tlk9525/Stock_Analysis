# Báo cáo ngày 2026-08-11 - MBB

## Tổng quan

- Dữ liệu: 2011-11-01 -> 2026-08-11, 3,686 phiên.
- Giá đóng cửa: 20.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 19.33; SMA60 19.85; RSI14 61.8.
- MACD 0.106; đường tín hiệu -0.103; biểu đồ cột 0.210.
- ATR14 0.47; ATR% 2.3%; ADX14 25.7.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.8.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.7, +DI vượt -DI.
- Thanh khoản: Thấp - 0.67 lần trung bình.
- Stochastic: Cực trị - %K 98.2, %D 93.1.

## Phân tích cơ bản

- Doanh nghiệp: MBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.49.
- P/B: 1.31.
- ROE: 20.7%.
- ROA: 1.9%.
- Market cap: 195,333.7 tỷ.
- Revenue Growth: 18.5%.
- Profit Growth: 40.0%.
- P/E 6.49: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.31: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2024-01-17 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.521; AUC 0.497; log-loss 0.694.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.500; AUC 0.498.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 41.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -4.9%; Sharpe -0.17; mức sụt giảm tối đa -10.4%.
- Mức độ quan trọng của đặc trưng: return_1d=12.34; return_2d=10.42; beta_60d=10.16; volatility_20d=9.92; excess_return_1d=9.83; day_of_week=9.73.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 19.80; mục tiêu 1 22.79; mục tiêu 2 22.79.
- Tỷ lệ lợi nhuận/rủi ro 2.71; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 20.23 (-1.31%).
- P10/P90 cuối kỳ 18.43 / 22.79.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.497 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4973404255319149, AUC logistic=0.49803600654664487.
- Điều kiện phát hành tín hiệu: Probability 48.1% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17055054221419277.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.1%.
- Mô hình Logistic đối chứng: 49.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 42.9%.
- Mức dừng lỗ tham chiếu 19.80, mục tiêu 1 22.79, tỷ lệ lợi nhuận/rủi ro 2.71.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, nganh: 2, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 61.8.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.7, +DI vượt -DI.); Thanh khoản: Thấp (0.67 lần trung bình.); Stochastic: Cực trị (%K 98.2, %D 93.1.)
- Góc nhìn cơ bản: Artifact cơ bản: MBBank; kỳ 2026-Q2; P/E 6.49; P/B 1.31; ROE 20.7%; ROA 1.9%; Debt/Equity 10.06; Revenue Growth 18.5%; Profit Growth 40.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 2, nganh: 2, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:03:57.142010+00:00; News Reader đọc được 4 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.497 < 0.540
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4973404255319149, AUC logistic=0.49803600654664487
- ML decision artifact: NO_EDGE. Probability 48.1% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17055054221419277
- News Reader [Tin nhanh chứng khoán]: MB chốt quyền chia cổ tức 15%, phát hành chào bán gần 805,5 triệu cổ phiếu giá 10.000 đồng/CP - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-04T08:39:02+00:00)
- News Reader [nguoiquansat.vn]: Tuần tới, MB chốt quyền nhận cổ tức 15%, mua thêm cổ phiếu giá 10.000 đồng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-09T06:38:01+00:00)
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 5/8: Cơ hội đầu tư tiềm năng với HPG và MBB - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-04T22:00:00+00:00)
- News Reader [24HMoney]: MBB: lãi tăng 41%, cổ phiếu đã vào sóng? - 24HMoney | nhóm: ket_qua_kinh_doanh, rui_ro (2026-08-05T03:42:58+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.497 < 0.540
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4973404255319149, AUC logistic=0.49803600654664487
- ML guard: Probability 48.1% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.04944642000000066, Sharpe=-0.17055054221419277
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

- [Tin nhanh chứng khoán] MB chốt quyền chia cổ tức 15%, phát hành chào bán gần 805,5 triệu cổ phiếu giá 10.000 đồng/CP - Tin nhanh chứng khoán (2026-08-04T08:39:02+00:00): https://www.tinnhanhchungkhoan.vn/mb-chot-quyen-chia-co-tuc-15-phat-hanh-chao-ban-gan-8055-trieu-co-phieu-gia-10000-dongcp-post395281.html
- [nguoiquansat.vn] Tuần tới, MB chốt quyền nhận cổ tức 15%, mua thêm cổ phiếu giá 10.000 đồng - nguoiquansat.vn (2026-08-09T06:38:01+00:00): https://nguoiquansat.vn/tuan-toi-mb-chot-quyen-nhan-co-tuc-15-mua-them-co-phieu-gia-10-000-dong-309416.html
- [VOV.VN] Một số cổ phiếu cần quan tâm 5/8: Cơ hội đầu tư tiềm năng với HPG và MBB - VOV.VN (2026-08-04T22:00:00+00:00): https://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-58-co-hoi-dau-tu-tiem-nang-voi-hpg-va-mbb-post1321179.vov
- [24HMoney] MBB: lãi tăng 41%, cổ phiếu đã vào sóng? - 24HMoney (2026-08-05T03:42:58+00:00): https://24hmoney.vn/news/mbb-lai-tang-41-co-phieu-da-vao-song-c30a2816737.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
