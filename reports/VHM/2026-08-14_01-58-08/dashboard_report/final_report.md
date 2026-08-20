# Báo cáo ngày 2026-08-14 - VHM

## Tổng quan

- Dữ liệu: 2011-11-10 -> 2026-08-13, 2,163 phiên.
- Giá đóng cửa: 71.80 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 53.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 70.86; SMA60 72.05; RSI14 49.3.
- MACD 0.555; đường tín hiệu 0.398; biểu đồ cột 0.158.
- ATR14 3.10; ATR% 4.3%; ADX14 23.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 49.3.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 23.0.
- Thanh khoản: Bình thường - 1.22 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Vinhomes.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 7.59.
- P/B: 2.33.
- ROE: 32.7%.
- ROA: 9.0%.
- Market cap: 606,254.0 tỷ.
- Revenue Growth: 177.8%.
- Profit Growth: 200.8%.
- P/E 7.59: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 2.33: nên đọc cùng ROE và đặc thù ngành.
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

- Kiểm thử: 2023-10-19 -> 2026-08-12.
- XGBoost: độ chính xác cân bằng 0.530; AUC 0.523; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.530; AUC 0.546.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 25.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.6% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 0 điểm | Trung tính; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.6%; safety margin đã chọn 0.5%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: range_pct=11.59; market_volatility_20d=11.53; atr_pct_14=11.03; market_return_1d=10.59; day_of_week=10.31; return_1d=9.82.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 71.33; mục tiêu 1 81.70; mục tiêu 2 92.66.
- Tỷ lệ lợi nhuận/rủi ro 11.45; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 72.29 (0.68%).
- P10/P90 cuối kỳ 54.39 / 92.66.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.044942915070208755 (dự báo điểm 0.005812496412545443) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score 0 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 53.1%.
- Mô hình Logistic đối chứng: 50.4%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 61.1%.
- Mức dừng lỗ tham chiếu 71.33, mục tiêu 1 81.70, tỷ lệ lợi nhuận/rủi ro 11.45.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, nganh: 2, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 0. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 49.3.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 23.0.); Thanh khoản: Bình thường (1.22 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Vinhomes; kỳ 2026-Q2; P/E 7.59; P/B 2.33; ROE 32.7%; ROA 9.0%; Debt/Equity 3.05; Revenue Growth 177.8%; Profit Growth 200.8%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 1, co_tuc_va_hanh_dong_doanh_nghiep: 1, nganh: 2, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-13T18:58:46.414058+00:00; News Reader đọc được 4 bài. ML có 7 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest. Final report dùng fallback grounded từ artifact local.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.044942915070208755 (dự báo điểm 0.005812496412545443) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score 0 < 2.
- News Reader [nguoiquansat.vn]: Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn | nhóm: khác (2026-08-10T08:50:01+00:00)
- News Reader [VietnamBiz]: Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz | nhóm: khác (2026-08-10T08:10:00+00:00)
- News Reader [Vietstock]: Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock | nhóm: nganh (2026-08-10T10:04:47+00:00)
- News Reader [MoneyF]: Gần 40.000 tỷ đồng chờ đổ vào thị trường, VIC, VHM và loạt cổ phiếu lớn có thể được “gom” - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, nganh, rui_ro (2026-08-13T03:58:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 2 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.044942915070208755 (dự báo điểm 0.005812496412545443) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score 0 < 2.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.
- Ollama AI chưa hoàn tất trong lệnh full: Exit: 

### Nguồn live research

- [nguoiquansat.vn] Vingroup chuyển nhượng gần 5 triệu cổ phiếu VHM - nguoiquansat.vn (2026-08-10T08:50:01+00:00): https://nguoiquansat.vn/vingroup-chuyen-nhuong-gan-5-trieu-co-phieu-vhm-309619.html
- [VietnamBiz] Vingroup chuyển nhượng hơn 4,8 triệu cổ phiếu VHM - VietnamBiz (2026-08-10T08:10:00+00:00): https://vietnambiz.vn/vingroup-chuyen-nhuong-hon-48-trieu-co-phieu-vhm-202681014242741.htm
- [Vietstock] Nhịp đập Thị trường 10/08: Cổ phiếu VIC và VHM kìm hãm đà phục hồi của VN-Index - Vietstock (2026-08-10T10:04:47+00:00): https://vietstock.vn/2026/08/nhip-dap-thi-truong-1008-co-phieu-vic-va-vhm-kim-ham-da-phuc-hoi-cua-vn-index-1636-1478504.htm
- [MoneyF] Gần 40.000 tỷ đồng chờ đổ vào thị trường, VIC, VHM và loạt cổ phiếu lớn có thể được “gom” - MoneyF (2026-08-13T03:58:00+00:00): https://moneyf.vn/gan-40000-ty-dong-cho-do-vao-thi-truong-vic-vhm-va-d5z56ajc

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VHM/2026-08-14_01-58-08/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 13
- Số dòng giá có news feature: 6
- XGBoost probability mới nhất: 0.502
- AUC OOS: 0.533
- Balanced accuracy OOS: 0.520
- Backtest total return: 0.000
- Base XGBoost probability: 0.531
- Chênh lệch News-adjusted - Base: -0.029
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
