# Báo cáo ngày 2026-08-09 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-08-07, 2,159 phiên.
- Giá đóng cửa: 73.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 70.46; SMA60 72.29; RSI14 52.3.
- MACD 0.922; đường tín hiệu 0.044; biểu đồ cột 0.878.
- ATR14 3.25; ATR% 4.4%; ADX14 25.1.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 25.1, +DI vượt -DI.
- Thanh khoản: Đột biến - 1.56 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.51.
- P/B: 2.31.
- ROE: 32.7%.
- ROA: 9.0%.
- Market cap: 599,682.2 tỷ.
- Revenue Growth: 177.8%.
- Profit Growth: 200.8%.
- P/E 7.51: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 2.31: nên đọc cùng ROE và đặc thù ngành.
- ROE 32.7%: hiệu quả vốn chủ sở hữu tốt.
- ROA 9.0%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 3.05: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.17: thanh khoản ngắn hạn khá.
- Revenue Growth 177.8% YoY.
- Profit Growth 200.8% YoY.
- CFO/LNST 1.97: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-06T03:28:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-19 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.523; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.529; AUC 0.545.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 29.9%; Sharpe 0.74; mức sụt giảm tối đa -14.7%.
- Mức độ quan trọng của đặc trưng: close_vs_sma60=13.37; market_volatility_20d=11.96; range_pct=11.75; market_return_1d=11.06; atr_pct_14=11.00; relative_strength_20d=10.57.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.56; mục tiêu 1 81.70; mục tiêu 2 90.38.
- Tỷ lệ lợi nhuận/rủi ro 4.62; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 71.72 (-1.75%).
- P10/P90 cuối kỳ 58.01 / 90.38.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5228247319870356, AUC logistic=0.5447685531455165.
- Điều kiện phát hành tín hiệu: Probability 52.6% < 55.0%.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.6%.
- Mô hình Logistic đối chứng: 51.5%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.1%.
- Mức dừng lỗ tham chiếu 71.56, mục tiêu 1 81.70, tỷ lệ lợi nhuận/rủi ro 4.62.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tích cực; điểm 5. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 52.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 25.1, +DI vượt -DI.); Thanh khoản: Đột biến (1.56 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vinhomes; kỳ 2026-Q2; P/E 7.51; P/B 2.31; ROE 32.7%; ROA 9.0%; Debt/Equity 3.05; Revenue Growth 177.8%; Profit Growth 200.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:39:30.166897+00:00; News Reader đọc được 4 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.523 < 0.540
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5228247319870356, AUC logistic=0.5447685531455165
- ML decision artifact: NO_EDGE. Probability 52.6% < 55.0%
- News Reader [nguoiquansat.vn]: Sau VIC, VHM cũng tăng mạnh ngay ngày chia cổ phiếu, kịch bản cũ đang lặp lại? - nguoiquansat.vn | nhóm: khác (2026-08-06T04:38:01+00:00)
- News Reader [Báo Dân trí]: Nhóm cổ phiếu Vingroup dẫn dắt thị trường, khối ngoại mua VIC bán VHM - Báo Dân trí | nhóm: khác (2026-08-05T09:25:00+00:00)
- News Reader [24HMoney]: VHM vừa làm điều VIC từng làm trước cú tăng 60%: Lịch sử có lặp lại? - 24HMoney | nhóm: ket_qua_kinh_doanh, nganh (2026-08-06T07:48:33+00:00)
- News Reader [VietstockFinance]: VHM: Khuyến nghị NẮM GIỮ với giá mục tiêu 150,000 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-05T23:06:37+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.523 < 0.540
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5228247319870356, AUC logistic=0.5447685531455165
- ML guard: Probability 52.6% < 55.0%
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Sau VIC, VHM cũng tăng mạnh ngay ngày chia cổ phiếu, kịch bản cũ đang lặp lại? - nguoiquansat.vn (2026-08-06T04:38:01+00:00): https://nguoiquansat.vn/sau-vic-vhm-cung-tang-manh-ngay-ngay-chia-co-phieu-kich-ban-cu-dang-lap-lai-308783.html
- [Báo Dân trí] Nhóm cổ phiếu Vingroup dẫn dắt thị trường, khối ngoại mua VIC bán VHM - Báo Dân trí (2026-08-05T09:25:00+00:00): https://dantri.com.vn/kinh-doanh/nhom-co-phieu-vingroup-dan-dat-thi-truong-khoi-ngoai-mua-vic-ban-vhm-20260508155217795.htm
- [24HMoney] VHM vừa làm điều VIC từng làm trước cú tăng 60%: Lịch sử có lặp lại? - 24HMoney (2026-08-06T07:48:33+00:00): https://24hmoney.vn/news/vhm-vua-lam-dieu-vic-tung-lam-truoc-cu-tang-60-lich-su-co-lap-lai-c1a2817395.html
- [VietstockFinance] VHM: Khuyến nghị NẮM GIỮ với giá mục tiêu 150,000 đồng/cổ phiếu - VietstockFinance (2026-08-05T23:06:37+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21364/vhm-khuyen-nghi-nam-giu-voi-gia-muc-tieu-150000-dongco-phieu.htm?languageid=1

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
