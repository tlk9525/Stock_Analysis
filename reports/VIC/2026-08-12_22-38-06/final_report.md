# Báo cáo ngày 2026-08-12 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-12, 4,592 phiên.
- Giá đóng cửa: 215.50 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 215.38; SMA60 212.96; RSI14 50.4.
- MACD -0.644; đường tín hiệu -0.029; biểu đồ cột -0.615.
- ATR14 6.87; ATR% 3.2%; ADX14 12.7.
- Xu hướng: Tích cực - Giá nằm trên SMA20 và SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.7.
- Thanh khoản: Bình thường - 1.24 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

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

- Kiểm thử: 2023-08-25 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.530.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -33.5%; Sharpe -1.78; mức sụt giảm tối đa -35.1%.
- Mức độ quan trọng của đặc trưng: excess_return_20d=20.82; market_return_20d=19.92; return_kurtosis_20d=16.08; return_skew_20d=14.08; corr_60d=13.72; adx_14=11.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 210.83; mục tiêu 1 264.37; mục tiêu 2 264.37.
- Tỷ lệ lợi nhuận/rủi ro 8.30; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 213.12 (-1.10%).
- P10/P90 cuối kỳ 172.18 / 264.37.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.507 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.482 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5071380138854086, AUC logistic=0.5300555711148126.
- Điều kiện phát hành tín hiệu: Probability 50.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7765358368807573.
- Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 49.9%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.5%.
- Mức dừng lỗ tham chiếu 210.83, mục tiêu 1 264.37, tỷ lệ lợi nhuận/rủi ro 8.30.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, vi_mo: 2, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Tích cực (Giá nằm trên SMA20 và SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Trung tính (RSI 50.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 12.7.); Thanh khoản: Bình thường (1.24 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VinGroup; kỳ 2026-Q2; P/E 71.40; P/B 9.53; ROE 14.8%; ROA 1.9%; Debt/Equity 6.24; Revenue Growth 154.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, vi_mo: 2, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:38:23.187200+00:00; News Reader đọc được 4 bài. ML có 5 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.507 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.482 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5071380138854086, AUC logistic=0.5300555711148126
- ML decision artifact: NO_EDGE. Probability 50.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7765358368807573
- News Reader [Tạp chí Tài chính Doanh nghiệp]: VN-Index tăng gần 20 điểm, VIC một mình đỡ thị trường - Tạp chí Tài chính Doanh nghiệp | nhóm: nganh (2026-08-12T10:05:00+00:00)
- News Reader [Tin nhanh chứng khoán]: Gom mạnh cổ phiếu chứng khoán, khối ngoại mua ròng 333 tỷ đồng trong phiên 12/8 - Tin nhanh chứng khoán | nhóm: khác (2026-08-12T09:56:56+00:00)
- News Reader [Báo Dân trí]: Bộ đôi cổ phiếu của tỷ phú Phạm Nhật Vượng "đỡ" thị trường - Báo Dân trí | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-12T10:25:55+00:00)
- News Reader [Fili.vn]: Nhịp đập Thị trường 12/08: Tiếp tục giằng co, cổ phiếu VIC và VHM góp hơn 13.5 điểm tăng cho VN-Index - Fili.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-12T05:02:13+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.507 < 0.540
- ML guard: Balanced accuracy 0.482 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5071380138854086, AUC logistic=0.5300555711148126
- ML guard: Probability 50.0% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.3354625499999999, Sharpe=-1.7765358368807573
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Tạp chí Tài chính Doanh nghiệp] VN-Index tăng gần 20 điểm, VIC một mình đỡ thị trường - Tạp chí Tài chính Doanh nghiệp (2026-08-12T10:05:00+00:00): https://taichinhdoanhnghiep.net.vn/vn-index-tang-gan-20-diem-vic-mot-minh-do-thi-truong-d68945.html
- [Tin nhanh chứng khoán] Gom mạnh cổ phiếu chứng khoán, khối ngoại mua ròng 333 tỷ đồng trong phiên 12/8 - Tin nhanh chứng khoán (2026-08-12T09:56:56+00:00): https://m.tinnhanhchungkhoan.vn/gom-manh-co-phieu-chung-khoan-khoi-ngoai-mua-rong-333-ty-dong-trong-phien-128-post395819.amp
- [Báo Dân trí] Bộ đôi cổ phiếu của tỷ phú Phạm Nhật Vượng "đỡ" thị trường - Báo Dân trí (2026-08-12T10:25:55+00:00): https://dantri.com.vn/kinh-doanh/bo-doi-co-phieu-cua-ty-phu-pham-nhat-vuong-do-thi-truong-20260812170207591.htm
- [Fili.vn] Nhịp đập Thị trường 12/08: Tiếp tục giằng co, cổ phiếu VIC và VHM góp hơn 13.5 điểm tăng cho VN-Index - Fili.vn (2026-08-12T05:02:13+00:00): https://fili.vn/2026/08/nhip-dap-thi-truong-1208-vn-index-but-pha-dong-tien-tiep-tuc-do-vao-nhom-bat-dong-san-va-ngan-hang-1636-1479537.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VIC/2026-08-12_22-38-41_news_model`
- Số bài tin trong CSV cho mã: 12
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.498
- AUC OOS: 0.503
- Balanced accuracy OOS: 0.487
- Backtest total return: -0.304

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
