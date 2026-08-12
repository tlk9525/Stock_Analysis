# Báo cáo ngày 2026-08-12 - HPG

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-12, 4,593 phiên.
- Giá đóng cửa: 22.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm -1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 21.55; SMA60 22.89; RSI14 50.4.
- MACD -0.132; đường tín hiệu -0.281; biểu đồ cột 0.149.
- ATR14 0.52; ATR% 2.3%; ADX14 31.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.9, -DI vượt +DI.
- Thanh khoản: Thấp - 0.61 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Hòa Phát.
- Ngành: Basic Resources.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.02.
- P/B: 1.32.
- ROE: 17.4%.
- ROA: 8.9%.
- Market cap: 186,167.4 tỷ.
- Revenue Growth: 53.6%.
- Profit Growth: 49.7%.
- P/E 8.02: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.32: nên đọc cùng ROE và đặc thù ngành.
- ROE 17.4%: hiệu quả vốn chủ sở hữu tốt.
- ROA 8.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.14: thanh khoản ngắn hạn khá.
- Revenue Growth 53.6% YoY.
- Profit Growth 49.7% YoY.
- CFO/LNST 0.82: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.26 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-30T07:51:50+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-24 -> 2026-08-11.
- XGBoost: độ chính xác cân bằng 0.522; AUC 0.589; log-loss 0.674.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.517; AUC 0.567.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 119.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -29.9%; Sharpe -1.41; mức sụt giảm tối đa -37.0%.
- Mức độ quan trọng của đặc trưng: adx_14=10.62; close_vs_sma20=9.49; market_return_1d=9.24; bb_position_20=9.04; return_3d=9.02; return_1d=8.80.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 21.32; mục tiêu 1 24.06; mục tiêu 2 24.06.
- Tỷ lệ lợi nhuận/rủi ro 2.08; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 22.00 (-0.46%).
- P10/P90 cuối kỳ 20.23 / 24.06.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Probability 48.7% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -1 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.29891389999999884, Sharpe=-1.4149497542280463.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 48.7%.
- Mô hình Logistic đối chứng: 48.7%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 21.32, mục tiêu 1 24.06, tỷ lệ lợi nhuận/rủi ro 2.08.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm -1. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 50.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 31.9, -DI vượt +DI.); Thanh khoản: Thấp (0.61 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Hòa Phát; kỳ 2026-Q2; P/E 8.02; P/B 1.32; ROE 17.4%; ROA 8.9%; Debt/Equity 0.97; Revenue Growth 53.6%; Profit Growth 49.7%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 1, nganh: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-12T15:12:23.121920+00:00; News Reader đọc được 4 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Probability 48.7% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -1 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.29891389999999884, Sharpe=-1.4149497542280463
- News Reader [24HMoney]: HPG đã hoàn thành 70% mục tiêu lợi nhuận năm, cổ phiếu ngành thép liệu sắp có sóng? - 24HMoney | nhóm: ket_qua_kinh_doanh, nganh (2026-08-12T01:15:45+00:00)
- News Reader [VnBusiness]: Cổ phiếu thép: Lợi nhuận tăng, dòng tiền hồi phục? - VnBusiness | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-12T00:39:09+00:00)
- News Reader [nguoiquansat.vn]: Tiết lộ bất ngờ về lượng sở hữu cổ phiếu HPG của con gái tỷ phú Trần Đình Long - nguoiquansat.vn | nhóm: co_tuc_va_hanh_dong_doanh_nghiep (2026-08-07T04:27:01+00:00)
- News Reader [24HMoney]: Bất ngờ với lượng cổ phiếu HPG mà con gái tỷ phú Trần Đình Long đang nắm giữ - 24HMoney | nhóm: khác (2026-08-07T08:28:07+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Probability 48.7% < 55.0%
- ML guard: Technical score -1 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.29891389999999884, Sharpe=-1.4149497542280463
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [24HMoney] HPG đã hoàn thành 70% mục tiêu lợi nhuận năm, cổ phiếu ngành thép liệu sắp có sóng? - 24HMoney (2026-08-12T01:15:45+00:00): https://24hmoney.vn/news/hpg-da-hoan-thanh-70-muc-tieu-loi-nhuan-nam-co-phieu-nganh-thep-lieu-sap-co-song-c1a2819498.html
- [VnBusiness] Cổ phiếu thép: Lợi nhuận tăng, dòng tiền hồi phục? - VnBusiness (2026-08-12T00:39:09+00:00): https://vnbusiness.vn/co-phieu-thep-loi-nhuan-bat-tang-dong-tien-co-tim-lai-suc-nong.html
- [nguoiquansat.vn] Tiết lộ bất ngờ về lượng sở hữu cổ phiếu HPG của con gái tỷ phú Trần Đình Long - nguoiquansat.vn (2026-08-07T04:27:01+00:00): https://nguoiquansat.vn/tiet-lo-bat-ngo-ve-luong-so-huu-co-phieu-hpg-cua-con-gai-ty-phu-tran-dinh-long-309030.html
- [24HMoney] Bất ngờ với lượng cổ phiếu HPG mà con gái tỷ phú Trần Đình Long đang nắm giữ - 24HMoney (2026-08-07T08:28:07+00:00): https://24hmoney.vn/news/bat-ngo-voi-luong-co-phieu-hpg-ma-con-gai-ty-phu-tran-dinh-long-dang-nam-giu-c1a2817854.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
