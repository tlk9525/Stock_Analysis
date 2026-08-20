# Báo cáo ngày 2026-08-16 - TCH

## Tổng quan

- Dữ liệu: 2016-10-05 -> 2026-08-14, 2,462 phiên.
- Giá đóng cửa: 11.95 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -3).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 45.1%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 11.90; SMA60 13.75; RSI14 41.9.
- MACD -0.397; đường tín hiệu -0.516; biểu đồ cột 0.120.
- ATR14 0.54; ATR% 4.5%; ADX14 35.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 41.9.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng giảm - ADX 35.0, -DI vượt +DI.
- Thanh khoản: Bình thường - 1.35 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: ĐT DV Tài chính Hoàng Huy.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 34.59.
- P/B: 0.94.
- ROE: 2.6%.
- ROA: 1.4%.
- Market cap: 10,899.7 tỷ.
- Revenue Growth: 15.5%.
- Profit Growth: 231.2%.
- P/E 34.59: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 0.94: nên đọc cùng ROE và đặc thù ngành.
- ROE 2.6%: hiệu quả vốn còn yếu.
- Current ratio 2.60: thanh khoản ngắn hạn khá.
- Revenue Growth 15.5% YoY.
- Profit Growth 231.2% YoY.
- CFO/LNST -9.75: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là tiền mặt ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.22 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-13T07:48:16+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-09 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.509; AUC 0.505; log-loss 0.701.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.497; AUC 0.508.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.490.
- Vòng boosting tốt nhất: 55.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.0% | Cần vượt chi phí + margin 0.8%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -3 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.0%; safety margin đã chọn 0.2%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: corr_60d=9.95; beta_60d=9.28; day_of_week=8.06; macd_hist_pct=7.99; return_5d=7.84; return_1d=7.73.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 11.14; mục tiêu 1 14.70; mục tiêu 2 14.70.
- Tỷ lệ lợi nhuận/rủi ro 3.08; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 12.03 (0.68%).
- P10/P90 cuối kỳ 9.94 / 14.70.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.0566302510222092 (dự báo điểm 0.00011386556434445083) chưa vượt chi phí + margin 0.0075..
- Điều kiện phát hành tín hiệu: Technical score -3 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 45.1%.
- Mô hình Logistic đối chứng: 48.0%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 31.7%.
- Mức dừng lỗ tham chiếu 11.14, mục tiêu 1 14.70, tỷ lệ lợi nhuận/rủi ro 3.08.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 3 bài để phân loại chủ đề (ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, rui_ro: 1), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -3. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 41.9.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng giảm (ADX 35.0, -DI vượt +DI.); Thanh khoản: Bình thường (1.35 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: ĐT DV Tài chính Hoàng Huy; kỳ 2026-Q2; P/E 34.59; P/B 0.94; ROE 2.6%; ROA 1.4%; Debt/Equity 0.53; Revenue Growth 15.5%; Profit Growth 231.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 3 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 3, co_tuc_va_hanh_dong_doanh_nghiep: 3, rui_ro: 1. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T06:20:59.963741+00:00; News Reader đọc được 3 bài. ML có 8 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.0566302510222092 (dự báo điểm 0.00011386556434445083) chưa vượt chi phí + margin 0.0075.
- ML decision artifact: NO_EDGE. Technical score -3 < 2.
- News Reader [Báo Pháp Luật Việt Nam]: Tài chính Hoàng Huy (TCH): Chốt quyền phát hành hơn 91 triệu cổ phiếu thưởng, vốn điều lệ vượt 10.000 tỷ đồng - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-15T11:35:00+00:00)
- News Reader [cafeland.vn]: Công ty bất động sản Hải Phòng chuẩn bị phát hành 91 triệu cổ phiếu, vốn điều lệ vượt 10.000 tỷ đồng - cafeland.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, rui_ro (2026-08-14T13:00:00+00:00)
- News Reader [nguoiquansat.vn]: Tài chính Hoàng Huy (TCH) chuẩn bị tăng vốn lên hơn 10.000 tỷ đồng - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-14T05:26:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.0566302510222092 (dự báo điểm 0.00011386556434445083) chưa vượt chi phí + margin 0.0075.
- ML guard: Technical score -3 < 2.
- News Reader: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.
- News Reader: Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.
- News Reader: Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [Báo Pháp Luật Việt Nam] Tài chính Hoàng Huy (TCH): Chốt quyền phát hành hơn 91 triệu cổ phiếu thưởng, vốn điều lệ vượt 10.000 tỷ đồng - Báo Pháp Luật Việt Nam (2026-08-15T11:35:00+00:00): https://doanhnhan.baophapluat.vn/tai-chinh-hoang-huy-tch-chot-quyen-phat-hanh-hon-91-trieu-co-phieu-thuong-von-dieu-le-vuot-10-000-ty-dong.html
- [cafeland.vn] Công ty bất động sản Hải Phòng chuẩn bị phát hành 91 triệu cổ phiếu, vốn điều lệ vượt 10.000 tỷ đồng - cafeland.vn (2026-08-14T13:00:00+00:00): https://cafeland.vn/tin-tuc/cong-ty-bat-dong-san-hai-phong-chuan-bi-phat-hanh-91-trieu-co-phieu-von-dieu-le-vuot-10000-ty-dong-154170.html
- [nguoiquansat.vn] Tài chính Hoàng Huy (TCH) chuẩn bị tăng vốn lên hơn 10.000 tỷ đồng - nguoiquansat.vn (2026-08-14T05:26:01+00:00): https://nguoiquansat.vn/tai-chinh-hoang-huy-tch-chuan-bi-tang-von-len-hon-10-000-ty-dong-310469.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/TCH/2026-08-16_13-20-47/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 3
- Số dòng giá có news feature: 1
- XGBoost probability mới nhất: 0.467
- AUC OOS: 0.511
- Balanced accuracy OOS: 0.504
- Backtest total return: 0.000
- Base XGBoost probability: 0.451
- Chênh lệch News-adjusted - Base: +0.017
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
