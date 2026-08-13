# Báo cáo ngày 2026-08-12 - SAB

## Tổng quan

- Dữ liệu: 2016-12-06 -> 2026-08-12, 2,416 phiên.
- Giá đóng cửa: 46.30 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 59.9%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 44.24; SMA60 44.52; RSI14 61.7.
- MACD 0.383; đường tín hiệu 0.076; biểu đồ cột 0.307.
- ATR14 0.95; ATR% 2.0%; ADX14 18.3.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 61.7.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 18.3.
- Thanh khoản: Bình thường - 1.30 lần trung bình.
- Stochastic: Cực trị - %K 93.5, %D 90.7.

## Phân tích cơ bản

- Doanh nghiệp: SABECO.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.26.
- P/B: 2.99.
- ROE: 22.3%.
- ROA: 15.1%.
- Market cap: 58,549.0 tỷ.
- Revenue Growth: 1.2%.
- Profit Growth: -3.4%.
- P/E 12.26: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.99: nên đọc cùng ROE và đặc thù ngành.
- ROE 22.3%: hiệu quả vốn chủ sở hữu tốt.
- ROA 15.1%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.46: thanh khoản ngắn hạn khá.
- Revenue Growth 1.2% YoY.
- Profit Growth -3.4% YoY.
- CFO/LNST 0.42: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là tiền mặt ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.24 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T11:04:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-09-25 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.513; AUC 0.512; log-loss 0.682.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.499; AUC 0.469.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 39.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -32.9%; Sharpe -1.24; mức sụt giảm tối đa -34.7%.
- Mức độ quan trọng của đặc trưng: stoch_k_14=13.93; month_of_year=12.61; market_return_20d=11.61; return_1d=10.77; return_20d=10.39; rsi_14=10.27.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 44.88; mục tiêu 1 50.39; mục tiêu 2 50.39.
- Tỷ lệ lợi nhuận/rủi ro 2.34; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 45.85 (-0.98%).
- P10/P90 cuối kỳ 42.57 / 50.39.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.512 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.513 < 0.520.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2390332543596272.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 59.9%.
- Mô hình Logistic đối chứng: 48.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.1%.
- Mức dừng lỗ tham chiếu 44.88, mục tiêu 1 50.39, tỷ lệ lợi nhuận/rủi ro 2.34.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 2, nganh: 3, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 3. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 61.7.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Đi ngang (ADX 18.3.); Thanh khoản: Bình thường (1.30 lần trung bình.); Stochastic: Cực trị (%K 93.5, %D 90.7.)
- Góc nhìn cơ bản: Artifact cơ bản: SABECO; kỳ 2026-Q2; P/E 12.26; P/B 2.99; ROE 22.3%; ROA 15.1%; Debt/Equity 0.48; Revenue Growth 1.2%; Profit Growth -3.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 2, vi_mo: 2, nganh: 3, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:32:38.585189+00:00; News Reader đọc được 3 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.512 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.513 < 0.520
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2390332543596272
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T23:23:00+00:00)
- News Reader [Vietnam.vn]: DSC khuyến nghị theo dõi cổ phiếu SAB - Vietnam.vn | nhóm: ket_qua_kinh_doanh, nganh (2026-08-07T01:56:20+00:00)
- News Reader [Tin nhanh chứng khoán]: Cổ phiếu cần quan tâm ngày 7/8 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T10:30:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.512 < 0.540
- ML guard: Balanced accuracy 0.513 < 0.520
- ML guard: Lợi thế OOS ròng không đạt: return=-0.32891206999999945, Sharpe=-1.2390332543596272
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
- [Vietnam.vn] DSC khuyến nghị theo dõi cổ phiếu SAB - Vietnam.vn (2026-08-07T01:56:20+00:00): https://www.vietnam.vn/dsc-khuyen-nghi-theo-doi-co-phieu-sab
- [Tin nhanh chứng khoán] Cổ phiếu cần quan tâm ngày 7/8 - Tin nhanh chứng khoán (2026-08-06T10:30:00+00:00): https://www.tinnhanhchungkhoan.vn/co-phieu-can-quan-tam-ngay-78-post395431.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/SAB/2026-08-12_22-32-49_news_model`
- Số bài tin trong CSV cho mã: 7
- Số dòng giá có news feature: 9
- XGBoost probability mới nhất: 0.636
- AUC OOS: 0.514
- Balanced accuracy OOS: 0.507
- Backtest total return: -0.443

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
