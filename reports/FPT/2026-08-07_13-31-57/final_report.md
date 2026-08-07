# Báo cáo ngày 2026-08-07 - FPT

## Tổng quan

- Dữ liệu: 2008-03-11 -> 2026-08-07, 4,589 phiên.
- Giá đóng cửa: 71.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Tích cực (điểm 5).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 44.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).

## Phân tích kỹ thuật

- SMA20 67.31; SMA60 70.99; RSI14 58.0.
- MACD 0.029; đường tín hiệu -0.867; biểu đồ cột 0.896.
- ATR14 1.97; ATR% 2.8%; ADX14 26.9.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Tích cực - RSI 58.0.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 26.9, +DI vượt -DI.
- Thanh khoản: Thấp - 0.40 lần trung bình.
- Stochastic: Cực trị - %K 80.5, %D 77.7.

## Phân tích cơ bản

- Doanh nghiệp: FPT Corp.
- Ngành: Technology.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.05.
- P/B: 3.03.
- ROE: 26.5%.
- ROA: 12.8%.
- Market cap: 121,202.9 tỷ.
- Revenue Growth: -17.1%.
- Profit Growth: 13.7%.
- P/E 12.05: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.03: nên đọc cùng ROE và đặc thù ngành.
- ROE 26.5%: hiệu quả vốn chủ sở hữu tốt.
- ROA 12.8%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 1.56: thanh khoản ngắn hạn khá.
- Revenue Growth -17.1% YoY.
- Profit Growth 13.7% YoY.
- CFO/LNST 0.66: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.12 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T09:13:52+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-08 -> 2026-08-06.
- XGBoost: độ chính xác cân bằng 0.510; AUC 0.576; log-loss 0.687.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.528; AUC 0.561.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 27.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.
- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận -25.8%; Sharpe -0.86; mức sụt giảm tối đa -29.2%.
- Mức độ quan trọng của đặc trưng: close_vs_sma20=14.90; return_1d=14.71; stoch_k_14=11.95; atr_pct_14=11.76; day_of_week=11.61; market_return_1d=11.51.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 70.28; mục tiêu 1 73.30; mục tiêu 2 79.36.
- Tỷ lệ lợi nhuận/rủi ro 1.81; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- P50 cuối kỳ 70.53 (-0.67%).
- P10/P90 cuối kỳ 63.25 / 79.36.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Balanced accuracy 0.510 < 0.520.
- Điều kiện phát hành tín hiệu: Probability 44.0% < 55.0%.
- Điều kiện phát hành tín hiệu: Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8615619551711172.
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Tích cực.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 44.0%.
- Mô hình Logistic đối chứng: 40.0%.
- Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: 47.2%.
- Mức dừng lỗ tham chiếu 70.28, mục tiêu 1 73.30, tỷ lệ lợi nhuận/rủi ro 1.81.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: N/A
- Góc nhìn cơ bản: N/A
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 2, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-07T06:32:08.572515+00:00; News Reader đọc được 5 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Balanced accuracy 0.510 < 0.520
- ML decision artifact: NO_EDGE. Probability 44.0% < 55.0%
- ML decision artifact: NO_EDGE. Lợi thế OOS ròng không đạt: return=-0.2579965400000007, Sharpe=-0.8615619551711172
- News Reader [VOV.VN]: Một số cổ phiếu cần quan tâm 7/8: Cơ hội tiềm năng với FPT và VPB - VOV.VN | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-06T22:00:00+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-06T23:23:00+00:00)
- News Reader [Tuổi Trẻ]: Cổ phiếu FPT, PNJ, FRT... 'rủ nhau' tím trần, VN-Index tăng hơn 27 điểm - Tuổi Trẻ | nhóm: ket_qua_kinh_doanh, nganh (2026-08-03T08:30:00+00:00)
- News Reader [nguoiquansat.vn]: FPT phát hành hơn 171 triệu cổ phiếu thưởng, khoảng 1.700 tỷ đồng sắp 'về túi' nhà đầu tư - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-03T14:23:01+00:00)
- News Reader [Vietstock]: FPT Online sắp trả cổ tức tiền tỷ lệ 100% - Vietstock | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-05T12:47:00+00:00)

### Rủi ro cần kiểm chứng

- Nguy cơ pha loãng vốn chủ sở hữu nếu không có nguồn vốn ổn định
- Tăng trưởng doanh thu và lợi nhuận có thể không đạt kỳ vọng
- Cổ phiếu có thể biến động mạnh do yếu tố thị trường
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [VOV.VN] Một số cổ phiếu cần quan tâm 7/8: Cơ hội tiềm năng với FPT và VPB - VOV.VN (2026-08-06T22:00:00+00:00): http://vov.vn/thi-truong/mot-so-co-phieu-can-quan-tam-78-co-hoi-tiem-nang-voi-fpt-va-vpb-post1321824.vov
- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 7/8: FPT, GMD, SAB - thuonghieucongluan.com.vn (2026-08-06T23:23:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-7-8-fpt-gmd-sab-a329496.html
- [Tuổi Trẻ] Cổ phiếu FPT, PNJ, FRT... 'rủ nhau' tím trần, VN-Index tăng hơn 27 điểm - Tuổi Trẻ (2026-08-03T08:30:00+00:00): https://tuoitre.vn/co-phieu-fpt-pnj-frt-ru-nhau-tim-tran-vn-index-tang-hon-27-diem-100260803152039691.htm
- [nguoiquansat.vn] FPT phát hành hơn 171 triệu cổ phiếu thưởng, khoảng 1.700 tỷ đồng sắp 'về túi' nhà đầu tư - nguoiquansat.vn (2026-08-03T14:23:01+00:00): https://nguoiquansat.vn/fpt-phat-hanh-hon-171-trieu-co-phieu-thuong-khoang-1-700-ty-dong-sap-ve-tui-nha-dau-tu-308191.html
- [Vietstock] FPT Online sắp trả cổ tức tiền tỷ lệ 100% - Vietstock (2026-08-05T12:47:00+00:00): https://vietstock.vn/2026/08/fpt-online-sap-tra-co-tuc-tien-ty-le-100-738-1477175.htm

Lưu ý: Thông tin được tổng hợp từ các nguồn tin tức và báo cáo tài chính. Cổ phiếu có thể biến động mạnh do yếu tố thị trường, nên không nên đưa vào đầu tư mà chỉ làm nghiên cứu.
