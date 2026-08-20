# Báo cáo ngày 2026-08-14 - VHC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-13, 4,437 phiên.
- Giá đóng cửa: 54.10 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 1).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 53.53; SMA60 56.69; RSI14 48.5.
- MACD -1.092; đường tín hiệu -1.270; biểu đồ cột 0.178.
- ATR14 1.55; ATR% 2.9%; ADX14 30.9.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 48.5.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 30.9, -DI vượt +DI.
- Thanh khoản: Đột biến - 3.58 lần trung bình.
- Stochastic: Hồi phục - %K nằm trên %D.

## Phân tích cơ bản

- Doanh nghiệp: Thủy sản Vĩnh Hoàn.
- Ngành: Food & Beverage.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 8.22.
- P/B: 1.19.
- ROE: 15.0%.
- ROA: 10.7%.
- Market cap: 11,122.0 tỷ.
- Revenue Growth: 7.9%.
- Profit Growth: -8.9%.
- P/E 8.22: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.19: nên đọc cùng ROE và đặc thù ngành.
- ROA 10.7%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 2.54: thanh khoản ngắn hạn khá.
- Revenue Growth 7.9% YoY.
- Profit Growth -8.9% YoY.
- CFO/LNST 0.34: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: -0.04 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-29T14:31:00+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-23 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.498; AUC 0.491; log-loss 0.699.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.515.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 45.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | -0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 1 điểm | Trung tính; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: -0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: range_pct=13.56; return_1d=11.33; volume_ratio_20=11.12; close_vs_sma20=10.81; return_10d=10.58; macd_pct=10.43.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 51.77; mục tiêu 1 64.85; mục tiêu 2 64.85.
- Tỷ lệ lợi nhuận/rủi ro 4.03; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 54.63 (0.98%).
- P10/P90 cuối kỳ 45.86 / 64.85.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04769025759287049 (dự báo điểm -0.0009937694994732738) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score 1 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 42.7%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 46.4%.
- Mức dừng lỗ tham chiếu 51.77, mục tiêu 1 64.85, tỷ lệ lợi nhuận/rủi ro 4.03.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 4, nganh: 5, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 1. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 48.5.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 30.9, -DI vượt +DI.); Thanh khoản: Đột biến (3.58 lần trung bình.); Stochastic: Hồi phục (%K nằm trên %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Thủy sản Vĩnh Hoàn; kỳ 2026-Q2; P/E 8.22; P/B 1.19; ROE 15.0%; ROA 10.7%; Debt/Equity 0.38; Revenue Growth 7.9%; Profit Growth -8.9%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 4, nganh: 5, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T18:57:22.038799+00:00; News Reader đọc được 5 bài. ML có 6 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04769025759287049 (dự báo điểm -0.0009937694994732738) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score 1 < 2.
- News Reader [VietstockFinance]: VHC: Khuyến nghị MUA với giá mục tiêu 69,900 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-11T07:00:34+00:00)
- News Reader [Tin nhanh chứng khoán]: Cổ phiếu cần quan tâm ngày 10/8 - Tin nhanh chứng khoán | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-09T10:03:54+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 10/8: Dòng tiền tìm kiếm cơ hội từ tăng trưởng lợi nhuận - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-09T23:30:00+00:00)
- News Reader [bnews.vn]: Cổ phiếu nào được khuyến nghị tích cực trong quý III/2026? - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-10T02:24:00+00:00)
- News Reader [MoneyF]: 4 cổ phiếu được “gọi tên” trước phiên 10/8: Một mã còn dư địa tăng 19%, một mã hưởng lợi đầu tư công - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-10T01:25:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Cận dưới expected excess return -0.04769025759287049 (dự báo điểm -0.0009937694994732738) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score 1 < 2.
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

- [VietstockFinance] VHC: Khuyến nghị MUA với giá mục tiêu 69,900 đồng/cổ phiếu - VietstockFinance (2026-08-11T07:00:34+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21499/vhc-khuyen-nghi-mua-voi-gia-muc-tieu-69900-dongco-phieu.htm
- [Tin nhanh chứng khoán] Cổ phiếu cần quan tâm ngày 10/8 - Tin nhanh chứng khoán (2026-08-09T10:03:54+00:00): https://www.tinnhanhchungkhoan.vn/co-phieu-can-quan-tam-ngay-108-post395528.html
- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 10/8: Dòng tiền tìm kiếm cơ hội từ tăng trưởng lợi nhuận - thuonghieucongluan.com.vn (2026-08-09T23:30:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-10-8-dong-tien-tim-kiem-co-hoi-tu-tang-truong-loi-nhuan-a329839.html
- [bnews.vn] Cổ phiếu nào được khuyến nghị tích cực trong quý III/2026? - bnews.vn (2026-08-10T02:24:00+00:00): https://bnews.vn/co-phieu-nao-duoc-khuyen-nghi-tich-cuc-trong-quy-iii-2026/432077.html
- [MoneyF] 4 cổ phiếu được “gọi tên” trước phiên 10/8: Một mã còn dư địa tăng 19%, một mã hưởng lợi đầu tư công - MoneyF (2026-08-10T01:25:00+00:00): https://moneyf.vn/4-co-phieu-duoc-goi-ten-truoc-phien-108-mot-ma-con-sbohierc

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VHC/2026-08-14_01-56-56/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 5
- Số dòng giá có news feature: 4
- XGBoost probability mới nhất: 0.488
- AUC OOS: 0.515
- Balanced accuracy OOS: 0.493
- Backtest total return: 0.000
- Base XGBoost probability: 0.500
- Chênh lệch News-adjusted - Base: -0.012
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
