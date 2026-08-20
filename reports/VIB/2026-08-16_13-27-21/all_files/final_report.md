# Báo cáo ngày 2026-08-16 - VIB

## Tổng quan

- Dữ liệu: 2017-01-09 -> 2026-08-14, 2,387 phiên.
- Giá đóng cửa: 14.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -4).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 43.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 14.63; SMA60 15.60; RSI14 37.6.
- MACD -0.245; đường tín hiệu -0.285; biểu đồ cột 0.040.
- ATR14 0.34; ATR% 2.3%; ADX14 26.1.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 37.6.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 26.1, -DI vượt +DI.
- Thanh khoản: Thấp - 0.68 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VIBBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.61.
- P/B: 1.02.
- ROE: 15.7%.
- ROA: 1.3%.
- Market cap: 49,017.7 tỷ.
- Revenue Growth: 4.9%.
- Profit Growth: -8.2%.
- P/E 6.61: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.02: nên đọc cùng ROE và đặc thù ngành.
- ROE 15.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 11.15: đòn bẩy cao, cần đọc theo ngành.
- NPL 2.9%: cần theo dõi.
- Revenue Growth 4.9% YoY.
- Profit Growth -8.2% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.22 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-11T07:07:29+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-07 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.504; AUC 0.492; log-loss 0.693.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.529; AUC 0.527.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 36.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.1% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -4 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.1%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: day_of_week=12.00; close_vs_sma20=11.80; macd_pct=10.35; month_of_year=10.07; atr_pct_14=9.99; return_10d=9.82.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 13.91; mục tiêu 1 15.40; mục tiêu 2 15.40.
- Tỷ lệ lợi nhuận/rủi ro 1.65; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 14.60 (1.40%).
- P10/P90 cuối kỳ 13.70 / 15.11.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.025144444258415888 (dự báo điểm 0.0011450171004980803) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -4 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 43.1%.
- Mô hình Logistic đối chứng: 47.0%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 36.9%.
- Mức dừng lỗ tham chiếu 13.91, mục tiêu 1 15.40, tỷ lệ lợi nhuận/rủi ro 1.65.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -4. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 37.6.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 26.1, -DI vượt +DI.); Thanh khoản: Thấp (0.68 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VIBBank; kỳ 2026-Q2; P/E 6.61; P/B 1.02; ROE 15.7%; ROA 1.3%; Debt/Equity 11.15; Revenue Growth 4.9%; Profit Growth -8.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 3, nganh: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T06:27:35.026300+00:00; News Reader đọc được 3 bài. ML có 10 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.025144444258415888 (dự báo điểm 0.0011450171004980803) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score -4 < 2.
- News Reader [Thời báo Tài chính Việt Nam]: VIB chốt ngày chia cổ phiếu thưởng 9,5%, tiếp đà tăng vốn khi dư nợ cho vay tiến sát 400.000 tỷ đồng - Thời báo Tài chính Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-11T10:43:17+00:00)
- News Reader [Vietstock]: VIB sắp phát hành thêm 323 triệu cổ cp, nâng vốn điều lệ lên 37,274 tỷ đồng - Vietstock | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-11T09:45:45+00:00)
- News Reader [Báo Pháp Luật Việt Nam]: VIB chốt quyền thưởng cổ phiếu tỷ lệ 9,5%, vốn điều lệ tiến sát mốc 37.300 tỷ đồng - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-11T10:38:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.025144444258415888 (dự báo điểm 0.0011450171004980803) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score -4 < 2.
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

- [Thời báo Tài chính Việt Nam] VIB chốt ngày chia cổ phiếu thưởng 9,5%, tiếp đà tăng vốn khi dư nợ cho vay tiến sát 400.000 tỷ đồng - Thời báo Tài chính Việt Nam (2026-08-11T10:43:17+00:00): https://thoibaotaichinhvietnam.vn/vib-chot-ngay-chia-co-phieu-thuong-9-5-tiep-da-tang-von-khi-du-no-cho-vay-tien-sat-400-000-ty-dong-202151.html
- [Vietstock] VIB sắp phát hành thêm 323 triệu cổ cp, nâng vốn điều lệ lên 37,274 tỷ đồng - Vietstock (2026-08-11T09:45:45+00:00): https://vietstock.vn/2026/08/vib-sap-phat-hanh-them-323-trieu-co-cp-nang-von-dieu-le-len-37274-ty-dong-757-1479222.htm
- [Báo Pháp Luật Việt Nam] VIB chốt quyền thưởng cổ phiếu tỷ lệ 9,5%, vốn điều lệ tiến sát mốc 37.300 tỷ đồng - Báo Pháp Luật Việt Nam (2026-08-11T10:38:00+00:00): https://doanhnhan.baophapluat.vn/vib-chot-quyen-thuong-co-phieu-ty-le-9-5-von-dieu-le-tien-sat-moc-37-300-ty-dong.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/VIB/2026-08-16_13-27-21/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 4
- Số dòng giá có news feature: 3
- XGBoost probability mới nhất: 0.400
- AUC OOS: 0.529
- Balanced accuracy OOS: 0.507
- Backtest total return: 0.000
- Base XGBoost probability: 0.431
- Chênh lệch News-adjusted - Base: -0.032
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
