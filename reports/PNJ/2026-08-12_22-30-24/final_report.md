# Báo cáo ngày 2026-08-12 - PNJ

## Tổng quan

- Dữ liệu: 2009-03-23 -> 2026-08-12, 4,329 phiên.
- Giá đóng cửa: 35.05 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 35.45; SMA60 52.85; RSI14 36.5.
- MACD -4.115; đường tín hiệu -5.290; biểu đồ cột 1.175.
- ATR14 2.31; ATR% 6.6%; ADX14 37.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 36.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 37.4, -DI vượt +DI.
- Thanh khoản: Thấp - 0.24 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vàng Phú Nhuận.
- Ngành: Personal & Household Goods.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.14.
- P/B: 1.28.
- ROE: 21.6%.
- ROA: 14.9%.
- Market cap: 17,833.5 tỷ.
- Revenue Growth: 11.9%.
- Profit Growth: -164.7%.
- P/E 6.14: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.28: nên đọc cùng ROE và đặc thù ngành.
- ROE 21.6%: hiệu quả vốn chủ sở hữu tốt.
- ROA 14.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.74: thanh khoản ngắn hạn khá.
- Revenue Growth 11.9% YoY.
- Profit Growth -164.7% YoY.
- CFO/LNST 5.54: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi -6.08 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.02 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-10T08:24:18+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-14 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.492; AUC 0.487; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.487; AUC 0.503.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 13.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -5.5%; Sharpe -0.19; mức sụt giảm tối đa -19.7%.
- Mức độ quan trọng của đặc trưng: return_20d=11.88; market_return_1d=11.22; rsi_14=11.02; close_vs_sma60=10.77; excess_return_1d=10.59; adx_14=10.47.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 31.59; mục tiêu 1 40.81; mục tiêu 2 43.35.
- Tỷ lệ lợi nhuận/rủi ro 1.53; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 35.44 (1.10%).
- P10/P90 cuối kỳ 28.81 / 40.81.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.487 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.492 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4871697237055955, AUC logistic=0.5025029022521477.
- Điều kiện phát hành tín hiệu: Probability 48.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -4 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.05460289999999968, Sharpe=-0.1917641851198188.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.2%.
- Mô hình Logistic đối chứng: 58.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 53.4%.
- Mức dừng lỗ tham chiếu 31.59, mục tiêu 1 40.81, tỷ lệ lợi nhuận/rủi ro 1.53.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 2, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -4. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 36.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 37.4, -DI vượt +DI.); Thanh khoản: Thấp (0.24 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vàng Phú Nhuận; kỳ 2026-Q2; P/E 6.14; P/B 1.28; ROE 21.6%; ROA 14.9%; Debt/Equity 0.51; Revenue Growth 11.9%; Profit Growth -164.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 2, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:30:41.923219+00:00; News Reader đọc được 4 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.487 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.492 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4871697237055955, AUC logistic=0.5025029022521477
- ML decision artifact: NO_EDGE. Probability 48.2% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -4 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.05460289999999968, Sharpe=-0.1917641851198188
- News Reader [VietnamFinance]: Cổ phiếu tăng mạnh: PNJ tạo đáy, nhóm vốn hoá lớn hồi phục - VietnamFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-09T08:30:00+00:00)
- News Reader [Tin nhanh chứng khoán]: Top 10 cổ phiếu tăng/giảm mạnh nhất tuần: Dòng tiền lan tỏa, nhiều cổ phiếu bật tăng từ đáy - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-07T23:55:47+00:00)
- News Reader [Tin nhanh chứng khoán]: Vàng bạc Đá quý Phú Nhuận (PNJ) muốn điều chỉnh kế hoạch kinh doanh sau biến cố - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo (2026-08-05T23:42:56+00:00)
- News Reader [Chứng khoán DNSE]: PNJ tính điều chỉnh kế hoạch kinh doanh, cổ phiếu quay đầu giảm mạnh - Chứng khoán DNSE | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-06T08:46:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.487 < 0.540
- ML guard: Balanced accuracy 0.492 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.4871697237055955, AUC logistic=0.5025029022521477
- ML guard: Probability 48.2% < 55.0%
- ML guard: Technical score -4 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.05460289999999968, Sharpe=-0.1917641851198188
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

- [VietnamFinance] Cổ phiếu tăng mạnh: PNJ tạo đáy, nhóm vốn hoá lớn hồi phục - VietnamFinance (2026-08-09T08:30:00+00:00): https://vietnamfinance.vn/co-phieu-tang-manh-pnj-tao-day-nhom-von-hoa-lon-hoi-phuc-d148805.html
- [Tin nhanh chứng khoán] Top 10 cổ phiếu tăng/giảm mạnh nhất tuần: Dòng tiền lan tỏa, nhiều cổ phiếu bật tăng từ đáy - Tin nhanh chứng khoán (2026-08-07T23:55:47+00:00): https://www.tinnhanhchungkhoan.vn/top-10-co-phieu-tanggiam-manh-nhat-tuan-dong-tien-lan-toa-nhieu-co-phieu-bat-tang-tu-day-post395499.html
- [Tin nhanh chứng khoán] Vàng bạc Đá quý Phú Nhuận (PNJ) muốn điều chỉnh kế hoạch kinh doanh sau biến cố - Tin nhanh chứng khoán (2026-08-05T23:42:56+00:00): https://www.tinnhanhchungkhoan.vn/vang-bac-da-quy-phu-nhuan-pnj-muon-dieu-chinh-ke-hoach-kinh-doanh-sau-bien-co-post395376.html
- [Chứng khoán DNSE] PNJ tính điều chỉnh kế hoạch kinh doanh, cổ phiếu quay đầu giảm mạnh - Chứng khoán DNSE (2026-08-06T08:46:00+00:00): https://www.dnse.com.vn/senses/tin-tuc/pnj-tinh-dieu-chinh-ke-hoach-kinh-doanh-co-phieu-quay-dau-giam-manh-35261330

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/PNJ/2026-08-12_22-30-58_news_model`
- Số bài tin trong CSV cho mã: 12
- Số dòng giá có news feature: 13
- XGBoost probability mới nhất: 0.498
- AUC OOS: 0.488
- Balanced accuracy OOS: 0.506
- Backtest total return: 0.025

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
