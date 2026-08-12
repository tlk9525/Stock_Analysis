# Báo cáo ngày 2026-08-11 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-08-11, 2,161 phiên.
- Giá đóng cửa: 72.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 70.55; SMA60 72.19; RSI14 50.3.
- MACD 0.642; đường tín hiệu 0.276; biểu đồ cột 0.365.
- ATR14 3.11; ATR% 4.3%; ADX14 23.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 23.4.
- Thanh khoản: Bình thường - 0.73 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.37.
- P/B: 2.26.
- ROE: 32.7%.
- ROA: 9.0%.
- Market cap: 588,181.4 tỷ.
- Revenue Growth: 177.8%.
- Profit Growth: 200.8%.
- P/E 7.37: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 2.26: nên đọc cùng ROE và đặc thù ngành.
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
- Bài mới nhất: 2026-08-10T03:53:05+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-19 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.523; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.545.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận 29.9%; Sharpe 0.74; mức sụt giảm tối đa -14.7%.
- Mức độ quan trọng của đặc trưng: range_pct=12.03; market_volatility_20d=11.45; atr_pct_14=11.22; return_1d=10.85; day_of_week=9.75; stoch_k_14=9.73.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.46; mục tiêu 1 81.70; mục tiêu 2 89.68.
- Tỷ lệ lợi nhuận/rủi ro 9.26; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 71.17 (-1.29%).
- P10/P90 cuối kỳ 57.63 / 89.68.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.523 < 0.540.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5229698912648313, AUC logistic=0.5453944541758932.
- Điều kiện phát hành tín hiệu: Probability 49.8% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score 0 < 2.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.8%.
- Mô hình Logistic đối chứng: 51.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.0%.
- Mức dừng lỗ tham chiếu 71.46, mục tiêu 1 81.70, tỷ lệ lợi nhuận/rủi ro 9.26.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 2, nganh: 1, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 0. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 50.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 23.4.); Thanh khoản: Bình thường (0.73 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vinhomes; kỳ 2026-Q2; P/E 7.37; P/B 2.26; ROE 32.7%; ROA 9.0%; Debt/Equity 3.05; Revenue Growth 177.8%; Profit Growth 200.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 2, nganh: 1, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:28:56.070035+00:00; News Reader đọc được 5 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.523 < 0.540
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5229698912648313, AUC logistic=0.5453944541758932
- ML decision artifact: NO_EDGE. Probability 49.8% < 55.0%
- ML decision artifact: NO_EDGE. Technical score 0 < 2
- News Reader [nguoiquansat.vn]: Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn | nhóm: khác (2026-08-10T08:50:01+00:00)
- News Reader [24HMoney]: Vingroup vừa chuyển gần 5 triệu cổ phiếu VHM, chuyện gì đang xảy ra? - 24HMoney | nhóm: khác (2026-08-10T09:00:20+00:00)
- News Reader [MoneyF]: Vingroup chuyển quyền sở hữu hơn 4,8 triệu cổ phiếu VHM, hạ sở hữu tại Vinhomes - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-10T09:48:00+00:00)
- News Reader [VietnamBiz]: Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz | nhóm: khác (2026-08-10T08:10:00+00:00)
- News Reader [VnEconomy]: Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - VnEconomy | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-10T08:30:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.523 < 0.540
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5229698912648313, AUC logistic=0.5453944541758932
- ML guard: Probability 49.8% < 55.0%
- ML guard: Technical score 0 < 2
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn (2026-08-10T08:50:01+00:00): https://nguoiquansat.vn/vingroup-chuyen-nhuong-gan-5-trieu-co-phieu-vhm-309619.html
- [24HMoney] Vingroup vừa chuyển gần 5 triệu cổ phiếu VHM, chuyện gì đang xảy ra? - 24HMoney (2026-08-10T09:00:20+00:00): https://24hmoney.vn/news/vingroup-vua-chuyen-gan-5-trieu-co-phieu-vhm-chuyen-gi-dang-xay-ra-c1a2818779.html
- [MoneyF] Vingroup chuyển quyền sở hữu hơn 4,8 triệu cổ phiếu VHM, hạ sở hữu tại Vinhomes - MoneyF (2026-08-10T09:48:00+00:00): https://moneyf.vn/vingroup-chuyen-quyen-so-huu-hon-48-trieu-co-phieu-cg6e6wqa
- [VietnamBiz] Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz (2026-08-10T08:10:00+00:00): https://vietnambiz.vn/vingroup-chuyen-nhuong-hon-48-trieu-co-phieu-vhm-202681014242741.htm
- [VnEconomy] Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - VnEconomy (2026-08-10T08:30:00+00:00): https://vneconomy.vn/tru-tiep-tuc-chim-sau-co-phieu-van-tang-bung-no.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
