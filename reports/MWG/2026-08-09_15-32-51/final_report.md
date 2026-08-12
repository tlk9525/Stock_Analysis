# Báo cáo ngày 2026-08-09 - MWG

## Tổng quan

- Dữ liệu: 2014-07-14 -> 2026-08-07, 3,014 phiên.
- Giá đóng cửa: 71.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 45.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 71.20; SMA60 75.07; RSI14 46.7.
- MACD -1.277; đường tín hiệu -1.760; biểu đồ cột 0.483.
- ATR14 2.49; ATR% 3.5%; ADX14 31.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 46.7.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 31.4, -DI vượt +DI.
- Thanh khoản: Thấp - 0.59 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Thế giới di động.
- Ngành: Retail.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 10.65.
- P/B: 2.93.
- ROE: 29.2%.
- ROA: 11.2%.
- Market cap: 104,779.4 tỷ.
- Revenue Growth: 29.6%.
- Profit Growth: 100.4%.
- P/E 10.65: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 2.93: nên đọc cùng ROE và đặc thù ngành.
- ROE 29.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 11.2%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.44: thanh khoản ngắn hạn khá.
- Revenue Growth 29.6% YoY.
- Profit Growth 100.4% YoY.
- CFO/LNST 5.06: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.10 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-05T00:21:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-07-26 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.511; AUC 0.510; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.520.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 46.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -6.6%; Sharpe -0.19; mức sụt giảm tối đa -14.2%.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=9.10; beta_60d=9.09; stoch_k_14=8.93; day_of_week=8.69; month_of_year=8.27; return_20d=8.18.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 67.27; mục tiêu 1 79.14; mục tiêu 2 79.14.
- Tỷ lệ lợi nhuận/rủi ro 1.90; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.35 (-0.92%).
- P10/P90 cuối kỳ 62.46 / 79.14.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: AUC 0.510 < 0.540.
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.511 < 0.520.
- Điều kiện phát hành tín hiệu: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5103149093506439, AUC logistic=0.5203041952900149.
- Điều kiện phát hành tín hiệu: Probability 45.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Technical score -3 < 2.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.1927899940362305.
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 45.0%.
- Mô hình Logistic đối chứng: 43.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 46.1%.
- Mức dừng lỗ tham chiếu 67.27, mục tiêu 1 79.14, tỷ lệ lợi nhuận/rủi ro 1.90.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 46.7.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 31.4, -DI vượt +DI.); Thanh khoản: Thấp (0.59 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Thế giới di động; kỳ 2026-Q2; P/E 10.65; P/B 2.93; ROE 29.2%; ROA 11.2%; Debt/Equity 1.89; Revenue Growth 29.6%; Profit Growth 100.4%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 4. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-09T08:33:03.197818+00:00; News Reader đọc được 4 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. AUC 0.510 < 0.540
- ML decision artifact: NO_EDGE. Balanced accuracy 0.511 < 0.520
- ML decision artifact: NO_EDGE. XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5103149093506439, AUC logistic=0.5203041952900149
- ML decision artifact: NO_EDGE. Probability 45.0% < 55.0%
- ML decision artifact: NO_EDGE. Technical score -3 < 2
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.1927899940362305
- News Reader [Tin nhanh chứng khoán]: Thế giới Di động (MWG) sẽ không mua cổ phiếu quỹ trong năm 2026 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-05T00:21:38+00:00)
- News Reader [VietstockFinance]: MWG: Khuyến nghị MUA với giá mục tiêu 107,300 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T08:54:35+00:00)
- News Reader [dautucophieu.net]: Cập nhật cổ phiếu MWG - Q2/2026: Lợi nhuận thuần tăng gấp đôi so với cùng kỳ, vượt xa dự báo - dautucophieu.net | nhóm: ket_qua_kinh_doanh, nganh (2026-08-05T04:31:03+00:00)
- News Reader [VietnamBiz]: Tổng Giám đốc MWG: Không mua cổ phiếu quỹ trong năm nay, lợi nhuận có thể về đích sớm 2-3 tháng - VietnamBiz | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-05T04:43:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: AUC 0.510 < 0.540
- ML guard: Balanced accuracy 0.511 < 0.520
- ML guard: XGBoost chưa vượt logistic baseline: AUC XGBoost=0.5103149093506439, AUC logistic=0.5203041952900149
- ML guard: Probability 45.0% < 55.0%
- ML guard: Technical score -3 < 2
- ML guard: Lợi thế OOS ròng không đạt: return=-0.06561506000000039, Sharpe=-0.1927899940362305
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Tin nhanh chứng khoán] Thế giới Di động (MWG) sẽ không mua cổ phiếu quỹ trong năm 2026 - Tin nhanh chứng khoán (2026-08-05T00:21:38+00:00): https://www.tinnhanhchungkhoan.vn/the-gioi-di-dong-mwg-se-khong-mua-co-phieu-quy-trong-nam-2026-post395305.html
- [VietstockFinance] MWG: Khuyến nghị MUA với giá mục tiêu 107,300 đồng/cổ phiếu - VietstockFinance (2026-08-06T08:54:35+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21390/mwg-khuyen-nghi-mua-voi-gia-muc-tieu-107300-dongco-phieu.htm
- [dautucophieu.net] Cập nhật cổ phiếu MWG - Q2/2026: Lợi nhuận thuần tăng gấp đôi so với cùng kỳ, vượt xa dự báo - dautucophieu.net (2026-08-05T04:31:03+00:00): https://dautucophieu.net/cap-nhat-co-phieu-mwg-q2-2026-loi-nhuan-thuan-tang-gap-doi-so-voi-cung-ky-vuot-xa-du-bao/
- [VietnamBiz] Tổng Giám đốc MWG: Không mua cổ phiếu quỹ trong năm nay, lợi nhuận có thể về đích sớm 2-3 tháng - VietnamBiz (2026-08-05T04:43:00+00:00): https://vietnambiz.vn/tong-giam-doc-mwg-khong-mua-co-phieu-quy-trong-nam-nay-loi-nhuan-co-the-ve-dich-som-2-3-thang-20268511123902.htm

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.
