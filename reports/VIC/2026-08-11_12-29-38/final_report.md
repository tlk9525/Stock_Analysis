# Báo cáo ngày 2026-08-11 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-11, 4,591 phiên.
- Giá đóng cửa: 208.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực (điểm -6).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 215.46; SMA60 213.14; RSI14 42.3.
- MACD -0.795; đường tín hiệu 0.125; biểu đồ cột -0.919.
- ATR14 6.76; ATR% 3.2%; ADX14 13.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 42.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 13.0.
- Thanh khoản: Thấp - 0.67 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 71.40.
- P/B: 9.53.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,618,415.9 tỷ.
- Revenue Growth: 154.0%.
- P/E 71.40: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 9.53: nên đọc cùng ROE và đặc thù ngành.
- Debt/Equity 6.24: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.05: thanh khoản ngắn hạn khá.
- Revenue Growth 154.0% YoY.
- CFO/LNST 3.40: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 1.68 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-04T07:06:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-25 -> 2026-08-10.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.530.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: excess_return_20d=19.95; market_return_20d=19.43; market_volatility_20d=18.14; return_kurtosis_20d=16.13; corr_60d=14.33; return_skew_20d=14.19.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 198.36; mục tiêu 1 257.44; mục tiêu 2 257.44.
- Tỷ lệ lợi nhuận/rủi ro 4.28; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 207.20 (-0.62%).
- P10/P90 cuối kỳ 167.56 / 257.44.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5074462502679172, AUC logistic=0.5295300178118741.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -6 < 2.
- Điều kiện phát hành tín hiệu: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7777558182493016.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Tiêu cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 54.6%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 48.6%.
- Mức dừng lỗ tham chiếu 198.36, mục tiêu 1 257.44, tỷ lệ lợi nhuận/rủi ro 4.28.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, nganh: 1, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Tiêu cực; điểm -6. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Yếu (RSI 42.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 13.0.); Thanh khoản: Thấp (0.67 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VinGroup; kỳ 2026-Q2; P/E 71.40; P/B 9.53; ROE 14.8%; ROA 1.9%; Debt/Equity 6.24; Revenue Growth 154.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, nganh: 1, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-11T05:30:12.755390+00:00; News Reader đọc được 4 bài. ML có 7 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.507 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.482 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5074462502679172, AUC logistic=0.5295300178118741
- ML decision artifact: NO_EDGE. Probability 50.0% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -6 < 2
- ML decision artifact: NO_EDGE. Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7777558182493016
- News Reader [nguoiquansat.vn]: Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn | nhóm: khác (2026-08-10T08:50:01+00:00)
- News Reader [Vietstock]: Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock | nhóm: nganh (2026-08-10T10:05:00+00:00)
- News Reader [VnEconomy]: Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - VnEconomy | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-10T08:30:00+00:00)
- News Reader [Báo Dân trí]: Nhóm cổ phiếu Vingroup dẫn dắt thị trường, khối ngoại mua VIC bán VHM - Báo Dân trí | nhóm: khác (2026-08-05T09:25:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.507 < 0.540
- ML guard: Balanced accuracy 0.482 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5074462502679172, AUC logistic=0.5295300178118741
- ML guard: Probability 50.0% < 55.0%
- ML guard: Technical score -6 < 2
- ML guard: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản
- ML guard: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7777558182493016
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
- [Vietstock] Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock (2026-08-10T10:05:00+00:00): https://vietstock.vn/2026/08/nhip-dap-thi-truong-1008-thi-truong-duy-tri-sac-xanh-1636-1478504.htm
- [VnEconomy] Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - VnEconomy (2026-08-10T08:30:00+00:00): https://vneconomy.vn/tru-tiep-tuc-chim-sau-co-phieu-van-tang-bung-no.htm
- [Báo Dân trí] Nhóm cổ phiếu Vingroup dẫn dắt thị trường, khối ngoại mua VIC bán VHM - Báo Dân trí (2026-08-05T09:25:00+00:00): https://dantri.com.vn/kinh-doanh/nhom-co-phieu-vingroup-dan-dat-thi-truong-khoi-ngoai-mua-vic-ban-vhm-20260508155217795.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
