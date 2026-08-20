# Báo cáo ngày 2026-08-16 - BSR

## Tổng quan

- Dữ liệu: 2018-03-01 -> 2026-08-14, 2,106 phiên.
- Giá đóng cửa: 25.35 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Trung tính (điểm 0).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 24.78; SMA60 25.76; RSI14 50.4.
- MACD 0.278; đường tín hiệu 0.080; biểu đồ cột 0.198.
- ATR14 1.10; ATR% 4.4%; ADX14 16.7.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 50.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 16.7.
- Thanh khoản: Bình thường - 1.08 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: Lọc Hoá dầu Việt Nam.
- Ngành: Oil & Gas.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 6.45.
- P/B: 1.71.
- ROE: 30.2%.
- ROA: 20.7%.
- Market cap: 126,935.0 tỷ.
- Revenue Growth: 59.7%.
- Profit Growth: 782.2%.
- P/E 6.45: định giá tương đối thấp nếu lợi nhuận bền vững.
- P/B 1.71: nên đọc cùng ROE và đặc thù ngành.
- ROE 30.2%: hiệu quả vốn chủ sở hữu tốt.
- ROA 20.7%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 3.03: thanh khoản ngắn hạn khá.
- Revenue Growth 59.7% YoY.
- Profit Growth 782.2% YoY.
- CFO/LNST 1.00: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.08 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T07:30:02+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-12-05 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.531; AUC 0.516; log-loss 0.696.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.510; AUC 0.481.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 32.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 2/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.2% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 2/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 0 điểm | Trung tính; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.2%; safety margin đã chọn 0.5%.
- Frozen holdout: 2/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: relative_strength_20d=11.08; market_volatility_20d=11.00; return_skew_20d=10.30; range_pct=10.09; close_vs_sma60=9.91; volatility_20d=9.83.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 23.70; mục tiêu 1 30.13; mục tiêu 2 30.13.
- Tỷ lệ lợi nhuận/rủi ro 2.61; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 24.19 (-4.59%).
- P10/P90 cuối kỳ 20.95 / 30.13.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 7 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 2 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04667523887523195 (dự báo điểm 0.002296397229656577) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score 0 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Trung tính.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 49.6%.
- Mô hình Logistic đối chứng: 47.1%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 45.6%.
- Mức dừng lỗ tham chiếu 23.70, mục tiêu 1 30.13, tỷ lệ lợi nhuận/rủi ro 2.61.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 4, nganh: 4, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Trung tính; điểm 0. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 50.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 16.7.); Thanh khoản: Bình thường (1.08 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: Lọc Hoá dầu Việt Nam; kỳ 2026-Q2; P/E 6.45; P/B 1.71; ROE 30.2%; ROA 20.7%; Debt/Equity 0.42; Revenue Growth 59.7%; Profit Growth 782.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 5, vi_mo: 4, nganh: 4, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T05:23:48.364295+00:00; News Reader đọc được 5 bài. ML có 10 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 7 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 2 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04667523887523195 (dự báo điểm 0.002296397229656577) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score 0 < 2.
- News Reader [nguoiquansat.vn]: Cổ phiếu đáng chú ý ngày 12/8: BSR, FRT, MBB - nguoiquansat.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-11T18:13:01+00:00)
- News Reader [bnews.vn]: Khuyến nghị cổ phiếu hôm nay: BSR, MBB được khuyến nghị mua; tăng tỷ trọng IDC, HT1 - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-14T01:35:00+00:00)
- News Reader [MoneyF]: 5 cổ phiếu vào “tầm ngắm” trước phiên 14/8, BSR dẫn đầu về triển vọng lợi nhuận - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-14T00:59:00+00:00)
- News Reader [Báo Pháp Luật Việt Nam]: Lọc hóa dầu Bình Sơn (BSR) chốt trả cổ tức tiền mặt, PVN thu về gần 1.400 tỷ đồng - Báo Pháp Luật Việt Nam | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep (2026-08-11T07:00:00+00:00)
- News Reader [hangthat.thuonghieucongluan.com.vn]: Dự báo chứng khoán ngày 14/8: Loạt cổ phiếu ngân hàng, dầu khí và khu công nghiệp được chú ý - hangthat.thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-14T02:48:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 7 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 2 trade; cần >= 10.
- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: MAE frozen holdout chưa tốt hơn baseline dự báo excess return bằng 0.
- ML guard: Cận dưới expected excess return -0.04667523887523195 (dự báo điểm 0.002296397229656577) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score 0 < 2.
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

- [nguoiquansat.vn] Cổ phiếu đáng chú ý ngày 12/8: BSR, FRT, MBB - nguoiquansat.vn (2026-08-11T18:13:01+00:00): https://nguoiquansat.vn/co-phieu-dang-chu-y-ngay-12-8-bsr-frt-mbb-309962.html
- [bnews.vn] Khuyến nghị cổ phiếu hôm nay: BSR, MBB được khuyến nghị mua; tăng tỷ trọng IDC, HT1 - bnews.vn (2026-08-14T01:35:00+00:00): https://bnews.vn/khuyen-nghi-co-phieu-hom-nay-bsr-mbb-duoc-khuyen-nghi-mua-tang-ty-trong-idc-ht1/432732.html
- [MoneyF] 5 cổ phiếu vào “tầm ngắm” trước phiên 14/8, BSR dẫn đầu về triển vọng lợi nhuận - MoneyF (2026-08-14T00:59:00+00:00): https://moneyf.vn/5-co-phieu-vao-tam-ngam-truoc-phien-148-bsr-dan-da-fn6193kh
- [Báo Pháp Luật Việt Nam] Lọc hóa dầu Bình Sơn (BSR) chốt trả cổ tức tiền mặt, PVN thu về gần 1.400 tỷ đồng - Báo Pháp Luật Việt Nam (2026-08-11T07:00:00+00:00): https://doanhnhan.baophapluat.vn/loc-hoa-dau-binh-son-bsr-chot-tra-co-tuc-tien-mat-pvn-thu-ve-gan-1-400-ty-dong.html
- [hangthat.thuonghieucongluan.com.vn] Dự báo chứng khoán ngày 14/8: Loạt cổ phiếu ngân hàng, dầu khí và khu công nghiệp được chú ý - hangthat.thuonghieucongluan.com.vn (2026-08-14T02:48:00+00:00): https://hangthat.thuonghieucongluan.com.vn/du-bao-chung-khoan-ngay-14-8-loat-co-phieu-ngan-hang-dau-khi-va-khu-cong-nghiep-duoc-chu-y-a292733.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/BSR/2026-08-16_12-23-35/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 9
- Số dòng giá có news feature: 4
- XGBoost probability mới nhất: 0.489
- AUC OOS: 0.519
- Balanced accuracy OOS: 0.517
- Backtest total return: 0.000
- Base XGBoost probability: 0.496
- Chênh lệch News-adjusted - Base: -0.006
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
