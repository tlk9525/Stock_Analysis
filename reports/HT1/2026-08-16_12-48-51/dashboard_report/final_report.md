# Báo cáo ngày 2026-08-16 - HT1

## Tổng quan

- Dữ liệu: 2008-03-10 -> 2026-08-14, 4,594 phiên.
- Giá đóng cửa: 13.00 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng (điểm 2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 50.3%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: HOLD_DISCIPLINED - Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge.

## Phân tích kỹ thuật

- SMA20 12.59; SMA60 13.20; RSI14 52.1.
- MACD 0.078; đường tín hiệu -0.038; biểu đồ cột 0.116.
- ATR14 0.40; ATR% 3.1%; ADX14 37.8.
- Xu hướng: Cẩn thận - Giá nằm dưới SMA60.
- MACD: Tích cực - MACD trên signal, histogram dương.
- RSI14: Trung tính - RSI 52.1.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Xu hướng tăng - ADX 37.8, +DI vượt -DI.
- Thanh khoản: Bình thường - 1.13 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: VICEM Hà Tiên.
- Ngành: Construction & Materials.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 12.83.
- P/B: 0.96.
- ROE: 7.6%.
- ROA: 4.9%.
- Market cap: 4,960.7 tỷ.
- Revenue Growth: 17.1%.
- Profit Growth: 23.1%.
- P/E 12.83: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 0.96: nên đọc cùng ROE và đặc thù ngành.
- ROE 7.6%: hiệu quả vốn còn yếu.
- ROA 4.9%: khá tốt, đặc biệt với nhóm ngân hàng.
- Current ratio 0.75: thanh khoản ngắn hạn cần theo dõi.
- Revenue Growth 17.1% YoY.
- Profit Growth 23.1% YoY.
- CFO/LNST 5.71: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.
- Dòng tiền tự do quý gần nhất dương; cần xem xu hướng nhiều quý và đặc thù ngành.
- Cấu trúc vốn hiện là tiền mặt ròng; không dùng một mình để kết luận rủi ro.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.06 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-13T08:18:13+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-08-28 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.489; AUC 0.523; log-loss 0.689.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.514; AUC 0.517.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 49.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 0/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | HOLD_DISCIPLINED | Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge. |
| Expected excess return 5D | -0.0% | Cần vượt chi phí + margin 1.0%. |
| Mẫu frozen holdout | 0/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | 2 điểm | Hồi phục / nghiêng tăng; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: -0.0%; safety margin đã chọn 0.5%.
- Frozen holdout: 0/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_1d=11.60; relative_strength_20d=10.64; stoch_k_14=10.60; return_5d=10.21; volatility_20d=9.72; close_vs_sma20=9.68.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 12.39; mục tiêu 1 14.69; mục tiêu 2 14.69.
- Tỷ lệ lợi nhuận/rủi ro 2.41; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 13.29 (2.20%).
- P10/P90 cuối kỳ 11.63 / 14.69.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn..
- Điều kiện phát hành tín hiệu: Development OOS chỉ có 3 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Frozen holdout chỉ có 0 trade; cần >= 10..
- Điều kiện phát hành tín hiệu: Correlation dự báo-return frozen holdout không dương..
- Điều kiện phát hành tín hiệu: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí..
- Điều kiện phát hành tín hiệu: Frozen holdout không chịu được stress phí 1.5x..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04219611136695789 (dự báo điểm -0.00043156801257282495) chưa vượt chi phí + margin 0.0100..
- Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro.
- Xu hướng kỹ thuật nghiêng về: Hồi phục / nghiêng tăng.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 50.3%.
- Mô hình Logistic đối chứng: 56.8%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 53.2%.
- Mức dừng lỗ tham chiếu 12.39, mục tiêu 1 14.69, tỷ lệ lợi nhuận/rủi ro 2.41.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 5 bài để phân loại chủ đề (ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 4, nganh: 5, rui_ro: 2), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Hồi phục / nghiêng tăng; điểm 2. Chi tiết artifact: Xu hướng: Cẩn thận (Giá nằm dưới SMA60.); MACD: Tích cực (MACD trên signal, histogram dương.); RSI14: Trung tính (RSI 52.1.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Xu hướng tăng (ADX 37.8, +DI vượt -DI.); Thanh khoản: Bình thường (1.13 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: VICEM Hà Tiên; kỳ 2026-Q2; P/E 12.83; P/B 0.96; ROE 7.6%; ROA 4.9%; Debt/Equity 0.49; Revenue Growth 17.1%; Profit Growth 23.1%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 5 bài; phân nhóm rule-based: ket_qua_kinh_doanh: 5, co_tuc_va_hanh_dong_doanh_nghiep: 3, vi_mo: 4, nganh: 5, rui_ro: 2. Tác động cần kiểm chứng: Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường. Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động. Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh. So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp. Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T05:49:09.443121+00:00; News Reader đọc được 5 bài. ML có 7 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML decision artifact: NO_EDGE. Development OOS chỉ có 3 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Frozen holdout chỉ có 0 trade; cần >= 10.
- ML decision artifact: NO_EDGE. Correlation dự báo-return frozen holdout không dương.
- ML decision artifact: NO_EDGE. Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML decision artifact: NO_EDGE. Frozen holdout không chịu được stress phí 1.5x.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04219611136695789 (dự báo điểm -0.00043156801257282495) chưa vượt chi phí + margin 0.0100.
- News Reader [bnews.vn]: Khuyến nghị cổ phiếu hôm nay: BSR, MBB được khuyến nghị mua; tăng tỷ trọng IDC, HT1 - bnews.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh (2026-08-14T01:35:00+00:00)
- News Reader [Báo Sức khỏe & Đời sống]: BSC khuyến nghị mua cổ phiếu HT1 - Báo Sức khỏe & Đời sống | nhóm: ket_qua_kinh_doanh, nganh (2026-08-10T00:32:00+00:00)
- News Reader [thuonghieucongluan.com.vn]: Cổ phiếu đáng chú ý ngày 10/8: Dòng tiền tìm kiếm cơ hội từ tăng trưởng lợi nhuận - thuonghieucongluan.com.vn | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-09T23:30:00+00:00)
- News Reader [MoneyF]: 4 cổ phiếu được “gọi tên” trước phiên 10/8: Một mã còn dư địa tăng 19%, một mã hưởng lợi đầu tư công - MoneyF | nhóm: ket_qua_kinh_doanh, co_tuc_va_hanh_dong_doanh_nghiep, vi_mo, nganh, rui_ro (2026-08-10T01:25:00+00:00)
- News Reader [bnews.vn]: Cổ phiếu nào được khuyến nghị tích cực trong quý III/2026? - bnews.vn | nhóm: ket_qua_kinh_doanh, vi_mo, nganh (2026-08-10T02:24:00+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Không có margin nào đạt số trade tối thiểu trong validation; strict no-entry fallback không phải rule đã chọn.
- ML guard: Development OOS chỉ có 3 trade; cần >= 10.
- ML guard: Frozen holdout chỉ có 0 trade; cần >= 10.
- ML guard: Correlation dự báo-return frozen holdout không dương.
- ML guard: Frozen holdout chưa có lợi thế ròng và Sharpe dương sau phí.
- ML guard: Frozen holdout không chịu được stress phí 1.5x.
- ML guard: Cận dưới expected excess return -0.04219611136695789 (dự báo điểm -0.00043156801257282495) chưa vượt chi phí + margin 0.0100.
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

- [bnews.vn] Khuyến nghị cổ phiếu hôm nay: BSR, MBB được khuyến nghị mua; tăng tỷ trọng IDC, HT1 - bnews.vn (2026-08-14T01:35:00+00:00): https://bnews.vn/khuyen-nghi-co-phieu-hom-nay-bsr-mbb-duoc-khuyen-nghi-mua-tang-ty-trong-idc-ht1/432732.html
- [Báo Sức khỏe & Đời sống] BSC khuyến nghị mua cổ phiếu HT1 - Báo Sức khỏe & Đời sống (2026-08-10T00:32:00+00:00): https://suckhoedoisong.vn/bsc-khuyen-nghi-mua-co-phieu-ht1-169260810072152762.htm
- [thuonghieucongluan.com.vn] Cổ phiếu đáng chú ý ngày 10/8: Dòng tiền tìm kiếm cơ hội từ tăng trưởng lợi nhuận - thuonghieucongluan.com.vn (2026-08-09T23:30:00+00:00): https://thuonghieucongluan.com.vn/co-phieu-dang-chu-y-ngay-10-8-dong-tien-tim-kiem-co-hoi-tu-tang-truong-loi-nhuan-a329839.html
- [MoneyF] 4 cổ phiếu được “gọi tên” trước phiên 10/8: Một mã còn dư địa tăng 19%, một mã hưởng lợi đầu tư công - MoneyF (2026-08-10T01:25:00+00:00): https://moneyf.vn/4-co-phieu-duoc-goi-ten-truoc-phien-108-mot-ma-con-sbohierc
- [bnews.vn] Cổ phiếu nào được khuyến nghị tích cực trong quý III/2026? - bnews.vn (2026-08-10T02:24:00+00:00): https://bnews.vn/co-phieu-nao-duoc-khuyen-nghi-tich-cuc-trong-quy-iii-2026/432077.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/HT1/2026-08-16_12-48-51/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 7
- Số dòng giá có news feature: 5
- XGBoost probability mới nhất: 0.503
- AUC OOS: 0.523
- Balanced accuracy OOS: 0.492
- Backtest total return: 0.000
- Base XGBoost probability: 0.503
- Chênh lệch News-adjusted - Base: -0.001
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
