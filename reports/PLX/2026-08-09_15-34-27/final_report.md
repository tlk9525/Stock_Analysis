# Báo cáo ngày 2026-08-09 - PLX

## Tổng quan

- Dữ liệu: 2017-04-21 -> 2026-08-07, 2,322 phiên.
- Giá đóng cửa: 35.95 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.2%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 33.26; SMA60 36.24; RSI14 60.4.
- MACD -0.331; đường tín hiệu -0.815; biểu đồ cột 0.484.
- ATR14 1.29; ATR% 3.6%; ADX14 24.5.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 60.4.
- Bollinger: Gần biên trên - Giá sát/vượt biên trên.
- ADX: Đi ngang - ADX 24.5.
- Thanh khoản: Đột biến - 3.28 lần trung bình.
- Stochastic: Cực trị - %K 98.1, %D 84.8.

## Phân tích cơ bản

- Doanh nghiệp: Petrolimex.
- Ngành: Oil & Gas.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 14.18.
- P/B: 1.77.
- ROE: 12.5%.
- ROA: 3.5%.
- Market cap: 45,677.8 tỷ.
- Revenue Growth: 78.0%.
- Profit Growth: 105.6%.
- P/E 14.18: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 1.77: nên đọc cùng ROE và đặc thù ngành.
- ROA 3.5%: khá tốt, đặc biệt với nhóm ngân hàng.
- Debt/Equity 2.01: đòn bẩy cao, cần đọc theo ngành.
- Current ratio 1.06: thanh khoản ngắn hạn khá.
- Revenue Growth 78.0% YoY.
- Profit Growth 105.6% YoY.
- CFO/LNST -2.68: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-31T07:12:34+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-03 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.505; AUC 0.511; log-loss 0.698.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.518; AUC 0.481.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 35.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -54.6%; Sharpe -1.78; mức sụt giảm tối đa -55.7%.
- Mức độ quan trọng của đặc trưng: return_2d=11.83; return_1d=10.59; volatility_20d=9.90; excess_return_1d=9.88; atr_pct_14=9.46; market_return_5d=9.16.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 35.88; mục tiêu 1 42.83; mục tiêu 2 42.83.
- Tỷ lệ lợi nhuận/rủi ro 26.77; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 35.25 (-1.96%).
- P10/P90 cuối kỳ 29.53 / 42.83.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.511 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.505 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 52.2% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7839780570150827.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.2%.
- Mô hình Logistic đối chứng: 42.8%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 43.5%.
- Mức dừng lỗ tham chiếu 35.88, mục tiêu 1 42.83, tỷ lệ lợi nhuận/rủi ro 26.77.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 2 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 2, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Tích cực (RSI 60.4.); Bollinger: Gần biên trên (Giá sát/vượt biên trên.); ADX: Đi ngang (ADX 24.5.); Thanh khoản: Đột biến (3.28 lần trung bình.); Stochastic: Cực trị (%K 98.1, %D 84.8.)
- Góc nhìn cơ bản: Artifact cơ bản: Petrolimex; kỳ 2026-Q2; P/E 14.18; P/B 1.77; ROE 12.5%; ROA 3.5%; Debt/Equity 2.01; Revenue Growth 78.0%; Profit Growth 105.6%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 2 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 2, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:34:38.110161+00:00; News Reader đọc được 2 bài. ML có 4 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.511 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.505 < 0.520
- ML decision artifact: NO_EDGE. Probability 52.2% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7839780570150827
- News Reader [Nhadautu.vn]: Những cổ phiếu vốn Nhà nước kỳ vọng hưởng lợi từ Quyết định 40 - Nhadautu.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh, rui_ro (2026-08-08T01:47:29+00:00)
- News Reader [Tạp chí Kinh tế chứng khoán Việt Nam]: Petrolimex (PLX) tiếp tục mở rộng mạng lưới, cổ phiếu được dự báo còn dư địa hơn 40% - Tạp chí Kinh tế chứng khoán Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-07T08:44:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.511 < 0.540
- ML guard: Balanced accuracy 0.505 < 0.520
- ML guard: Probability 52.2% < 55.0%
- ML guard: Lợi thế OOS ròng không đạt: return=-0.5464176299999998, Sharpe=-1.7839780570150827
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

- [Nhadautu.vn] Những cổ phiếu vốn Nhà nước kỳ vọng hưởng lợi từ Quyết định 40 - Nhadautu.vn (2026-08-08T01:47:29+00:00): https://nhadautu.vn/nhung-co-phieu-von-nha-nuoc-ky-vong-huong-loi-tu-quyet-dinh-40-d106854.html
- [Tạp chí Kinh tế chứng khoán Việt Nam] Petrolimex (PLX) tiếp tục mở rộng mạng lưới, cổ phiếu được dự báo còn dư địa hơn 40% - Tạp chí Kinh tế chứng khoán Việt Nam (2026-08-07T08:44:00+00:00): https://kinhtechungkhoan.vn/petrolimex-plx-tiep-tuc-mo-rong-mang-luoi-co-phieu-duoc-du-bao-con-du-dia-hon-40

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
