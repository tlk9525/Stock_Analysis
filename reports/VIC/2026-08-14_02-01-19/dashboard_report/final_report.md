# Báo cáo ngày 2026-08-14 - VIC

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-13, 4,593 phiên.
- Giá đóng cửa: 207.90 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 214.62; SMA60 212.78; RSI14 43.3.
- MACD -1.125; đường tín hiệu -0.248; biểu đồ cột -0.877.
- ATR14 6.96; ATR% 3.3%; ADX14 12.4.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Yếu - RSI 43.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 12.4.
- Thanh khoản: Bình thường - 1.28 lần trung bình.
- Stochastic: Cực trị - %K 13.1, %D 34.5.

## Phân tích cơ bản

- Doanh nghiệp: VinGroup.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 73.79.
- P/B: 9.84.
- ROE: 14.8%.
- ROA: 1.9%.
- Market cap: 1,672,751.2 tỷ.
- Revenue Growth: 154.0%.
- P/E 73.79: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 9.84: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-08-25 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.482; AUC 0.507; log-loss 0.695.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.515; AUC 0.530.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 1.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.5% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -4 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.5%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: excess_return_20d=20.00; market_return_20d=19.91; return_kurtosis_20d=16.17; return_skew_20d=14.06; corr_60d=13.91; adx_14=11.63.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 198.00; mục tiêu 1 277.07; mục tiêu 2 277.07.
- Tỷ lệ lợi nhuận/rủi ro 6.23; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 210.09 (1.05%).
- P10/P90 cuối kỳ 152.05 / 277.07.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.0615983867741412 (dự báo điểm 0.0048114582896232605) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -4 < 2..
- Điều kiện phát hành tín hiệu: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.0%.
- Mô hình Logistic đối chứng: 51.9%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 71.4%.
- Mức dừng lỗ tham chiếu 198.00, mục tiêu 1 277.07, tỷ lệ lợi nhuận/rủi ro 6.23.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -4. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Yếu (RSI 43.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 12.4.); Thanh khoản: Bình thường (1.28 lần trung bình.); Stochastic: Cực trị (%K 13.1, %D 34.5.)
- Góc nhìn cơ bản: Artifact cơ bản: VinGroup; kỳ 2026-Q2; P/E 73.79; P/B 9.84; ROE 14.8%; ROA 1.9%; Debt/Equity 6.24; Revenue Growth 154.0%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 2, co_tuc_va_hanh_dong_doanh_nghiep: 1, vi_mo: 2, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T19:01:44.228774+00:00; News Reader đọc được 4 bài. ML có 8 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.0615983867741412 (dự báo điểm 0.0048114582896232605) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score -4 < 2.
- ML decision artifact: NO_EDGE. Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- News Reader [VietnamBiz]: Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz | nhóm: khác (2026-08-10T08:10:00+00:00)
- News Reader [Vietstock]: Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock | nhóm: nganh (2026-08-10T10:04:47+00:00)
- News Reader [vneconomy.vn]: Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - vneconomy.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-10T08:30:00+00:00)
- News Reader [thuonghieucongluan.com.vn]: Chứng khoán ngày 13/8: Cổ phiếu đồng loạt chịu áp lực, VN-Index lùi bước - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-13T10:33:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: Cận dưới expected excess return -0.0615983867741412 (dự báo điểm 0.0048114582896232605) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score -4 < 2.
- ML guard: Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.
- Ollama AI chưa hoàn tất trong lệnh full: Exit: 

### Nguồn live research

- [VietnamBiz] Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz (2026-08-10T08:10:00+00:00): https://vietnambiz.vn/vingroup-chuyen-nhuong-hon-48-trieu-co-phieu-vhm-202681014242741.htm
- [Vietstock] Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock (2026-08-10T10:04:47+00:00): https://vietstock.vn/2026/08/nhip-dap-thi-truong-1008-co-phieu-vic-va-vhm-kim-ham-da-phuc-hoi-cua-vn-index-1636-1478504.htm
- [vneconomy.vn] Trụ tiếp tục “chìm” sâu, cổ phiếu vẫn tăng bùng nổ - vneconomy.vn (2026-08-10T08:30:00+00:00): https://vneconomy.vn/tru-tiep-tuc-chim-sau-co-phieu-van-tang-bung-no.htm
- [thuonghieucongluan.com.vn] Chứng khoán ngày 13/8: Cổ phiếu đồng loạt chịu áp lực, VN-Index lùi bước - thuonghieucongluan.com.vn (2026-08-13T10:33:00+00:00): https://thuonghieucongluan.com.vn/chung-khoan-ngay-13-8-co-phieu-dong-loat-chiu-ap-luc-vn-index-lui-buoc-a330342.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VIC/2026-08-14_02-01-19/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 16
- Số dòng giá có news feature: 6
- XGBoost probability mới nhất: 0.498
- AUC OOS: 0.503
- Balanced accuracy OOS: 0.487
- Backtest total return: 0.000
- Base XGBoost probability: 0.500
- Chênh lệch News-adjusted - Base: -0.002
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
