# Báo cáo ngày 2026-08-16 - KBC

## Tổng quan

- Dữ liệu: 2009-12-18 -> 2026-08-14, 4,153 phiên.
- Giá đóng cửa: 26.95 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 47.0%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 27.76; SMA60 29.04; RSI14 34.2.
- MACD -0.302; đường tín hiệu -0.307; biểu đồ cột 0.005.
- ATR14 0.69; ATR% 2.6%; ADX14 22.0.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Yếu - RSI 34.2.
- Bollinger: Gần biên dưới - Giá sát/vượt biên dưới.
- ADX: Đi ngang - ADX 22.0.
- Thanh khoản: Bình thường - 1.47 lần trung bình.
- Stochastic: Cực trị - %K 13.0, %D 28.7.

## Phân tích cơ bản

- Doanh nghiệp: TCT Đô thị Kinh Bắc.
- Ngành: Real Estate.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 21.97.
- P/B: 1.01.
- ROE: 4.7%.
- ROA: 1.6%.
- Market cap: 25,380.3 tỷ.
- Revenue Growth: 2.5%.
- Profit Growth: -96.2%.
- P/E 21.97: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.
- P/B 1.01: nên đọc cùng ROE và đặc thù ngành.
- ROE 4.7%: hiệu quả vốn còn yếu.
- Current ratio 4.35: thanh khoản ngắn hạn khá.
- Revenue Growth 2.5% YoY.
- Profit Growth -96.2% YoY.
- CFO/LNST -126.28: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động.
- Dòng tiền tự do quý gần nhất âm; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là nợ vay ròng; không dùng một mình để kết luận rủi ro.
- Khả năng trả lãi 0.81 lần: cần theo dõi áp lực lãi vay.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.02 (keyword_heuristic_v1).
- Bài mới nhất: 2026-07-30T09:51:33+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2024-01-05 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.507; AUC 0.575; log-loss 0.679.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.521; AUC 0.567.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 109.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | -0.0% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -2 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: -0.0%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: day_of_week=9.28; return_skew_20d=9.20; market_volatility_20d=8.79; range_pct=8.35; stoch_k_14=8.34; return_2d=8.29.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 25.94; mục tiêu 1 28.95; mục tiêu 2 31.97.
- Tỷ lệ lợi nhuận/rủi ro 1.63; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 27.15 (0.74%).
- P10/P90 cuối kỳ 21.84 / 31.97.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04552807664196856 (dự báo điểm -0.00046467059291899204) chưa vượt chi phí + margin 0.0100..
- Điều kiện phát hành tín hiệu: Technical score -2 < 2..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 47.0%.
- Mô hình Logistic đối chứng: 57.9%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 40.9%.
- Mức dừng lỗ tham chiếu 25.94, mục tiêu 1 28.95, tỷ lệ lợi nhuận/rủi ro 1.63.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 4 bài để phân loại chủ đề (ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 3), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Yếu (RSI 34.2.); Bollinger: Gần biên dưới (Giá sát/vượt biên dưới.); ADX: Đi ngang (ADX 22.0.); Thanh khoản: Bình thường (1.47 lần trung bình.); Stochastic: Cực trị (%K 13.0, %D 28.7.)
- Góc nhìn cơ bản: Artifact cơ bản: TCT Đô thị Kinh Bắc; kỳ 2026-Q2; P/E 21.97; P/B 1.01; ROE 4.7%; ROA 1.6%; Debt/Equity 1.75; Revenue Growth 2.5%; Profit Growth -96.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 4 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 4, co_tuc_va_hanh_dong_doanh_nghiep: 4, vi_mo: 4, nganh: 4, rui_ro: 3. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T05:50:02.225455+00:00; News Reader đọc được 4 bài. ML có 7 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04552807664196856 (dự báo điểm -0.00046467059291899204) chưa vượt chi phí + margin 0.0100.
- ML decision artifact: NO_EDGE. Technical score -2 < 2.
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 12/8: TNG, DGW, KBC và VNM có gì đáng kỳ vọng? - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-11T23:21:00+00:00)
- News Reader [VietstockFinance]: KBC: Khuyến nghị THEO DÕI với giá mục tiêu 28,950 đồng/cổ phiếu - VietstockFinance | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-10T02:49:58+00:00)
- News Reader [MoneyF]: 4 cổ phiếu được khuyến nghị mua và tăng tỷ trọng trước phiên ngày 12/8 - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-12T01:13:00+00:00)
- News Reader [index.vn]: Cổ phiếu 12/8: TNG, DGW, KBC, VNM được khuyến nghị, kỳ vọng tăng giá tới 22% - index.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-12T01:37:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: Cận dưới expected excess return -0.04552807664196856 (dự báo điểm -0.00046467059291899204) chưa vượt chi phí + margin 0.0100.
- ML guard: Technical score -2 < 2.
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

- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 12/8: TNG, DGW, KBC và VNM có gì đáng kỳ vọng? - thuonghieucongluan.com.vn (2026-08-11T23:21:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-12-8-tng-dgw-kbc-va-vnm-co-gi-dang-ky-vong-a330120.html
- [VietstockFinance] KBC: Khuyến nghị THEO DÕI với giá mục tiêu 28,950 đồng/cổ phiếu - VietstockFinance (2026-08-10T02:49:58+00:00): https://finance.vietstock.vn/bao-cao-phan-tich/21414/kbc-khuyen-nghi-theo-doi-voi-gia-muc-tieu-28950-dongco-phieu.htm
- [MoneyF] 4 cổ phiếu được khuyến nghị mua và tăng tỷ trọng trước phiên ngày 12/8 - MoneyF (2026-08-12T01:13:00+00:00): https://moneyf.vn/4-co-phieu-duoc-khuyen-nghi-mua-va-tang-ty-trong-t-bdc33w84
- [index.vn] Cổ phiếu 12/8: TNG, DGW, KBC, VNM được khuyến nghị, kỳ vọng tăng giá tới 22% - index.vn (2026-08-12T01:37:00+00:00): https://index.vn/tin-tuc/co-phieu-12-8-tng-dgw-kbc-vnm-duoc-khuyen-nghi-ky-vong-tang-gia-toi-22

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/KBC/2026-08-16_12-49-46/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 4
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.513
- AUC OOS: 0.556
- Balanced accuracy OOS: 0.507
- Backtest total return: 0.000
- Base XGBoost probability: 0.470
- Chênh lệch News-adjusted - Base: +0.042
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
