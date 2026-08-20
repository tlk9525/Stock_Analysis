# Báo cáo ngày 2026-08-16 - LPB

## Tổng quan

- Dữ liệu: 2017-10-05 -> 2026-08-14, 2,203 phiên.
- Giá đóng cửa: 52.40 nghìn VND/cp.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận (điểm -2).
- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Model health: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 24/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu chưa có cổ phiếu: INSUFFICIENT_EDGE - Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 24/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định.
- Nếu đang nắm giữ: REDUCE - Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro.

## Phân tích kỹ thuật

- SMA20 53.17; SMA60 51.55; RSI14 48.4.
- MACD 0.279; đường tín hiệu 0.353; biểu đồ cột -0.074.
- ATR14 1.77; ATR% 3.4%; ADX14 11.4.
- Xu hướng: Trung tính - Giá trên SMA60 nhưng chưa vượt SMA20.
- MACD: Cẩn thận - MACD dưới signal, histogram âm.
- RSI14: Trung tính - RSI 48.4.
- Bollinger: Ổn định - Giá nằm trong dải Bollinger.
- ADX: Đi ngang - ADX 11.4.
- Thanh khoản: Bình thường - 1.33 lần trung bình.
- Stochastic: Yếu lại - %K nằm dưới %D.

## Phân tích cơ bản

- Doanh nghiệp: LPBank.
- Ngành: Banks.
- Kỳ tỷ số mới nhất: 2026-Q2.
- P/E: 13.86.
- P/B: 3.64.
- ROE: 24.7%.
- ROA: 1.9%.
- Market cap: 156,533.6 tỷ.
- Revenue Growth: 23.3%.
- Profit Growth: 5.2%.
- P/E 13.86: cần so sánh thêm với doanh nghiệp cùng ngành.
- P/B 3.64: nên đọc cùng ROE và đặc thù ngành.
- ROE 24.7%: hiệu quả vốn chủ sở hữu tốt.
- Debt/Equity 13.30: đòn bẩy cao, cần đọc theo ngành.
- NPL 1.9%: đang ở mức kiểm soát.
- Revenue Growth 23.3% YoY.
- Profit Growth 5.2% YoY.
- Ghi chú dữ liệu: Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử thời điểm công bố chính thức nên chưa được đưa vào model/backtest.

## Tin tức doanh nghiệp (research only)

- Nguồn: VCI; số bài lấy được: 50.
- Bài có timestamp đủ điều kiện point-in-time: 50.
- Sentiment trung bình: 0.19 (keyword_heuristic_v1).
- Bài mới nhất: 2026-08-03T10:15:11+00:00.
- Ghi chú dữ liệu: Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.
- Ghi chú dữ liệu: Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.

## Mô hình XGBoost

- Kiểm thử: 2023-10-26 -> 2026-08-13.
- XGBoost: độ chính xác cân bằng 0.514; AUC 0.550; log-loss 0.684.
- Mô hình Logistic đối chứng: độ chính xác cân bằng 0.531; AUC 0.542.
- Mô hình đa số đối chứng: độ chính xác cân bằng 0.500.
- Vòng boosting tốt nhất: 57.
- Thẩm định: expanding_walk_forward; 6 lần chia; khoảng cách 1 phiên.

## Chiến lược swing 5 phiên: contract phát hành tín hiệu

### Khuyến nghị hành động sau phí

| Mục | Kết quả | Diễn giải |
|---|---:|---|
| Lệnh mới hôm nay | 0 lệnh | Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate. |
| Trạng thái edge 5D | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 24/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu chưa có cổ phiếu | INSUFFICIENT_EDGE | Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout 24/10 trade; không dùng classifier 1D hay sensitivity legacy để quyết định. |
| Nếu đang nắm giữ | REDUCE | Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro. |
| Expected excess return 5D | +0.8% | Cần vượt chi phí + margin 0.5%. |
| Mẫu frozen holdout | 24/10 trade | Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live. |
| Kỹ thuật / tin | -2 điểm | Suy yếu / cẩn thận; news warning: không. |

- Target: signal after close[t]; enter open[t+1]; exit close[t+5] ; target is stock return minus VNINDEX return over the same window
- Expected excess return mới nhất: +0.8%; safety margin đã chọn 0.0%.
- Frozen holdout: 24/10 trade; net/Sharpe chỉ được kết luận khi đủ mẫu.
- Publish gate swing: CHƯA ĐẠT. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.
- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.
- Mức độ quan trọng của đặc trưng: return_20d=9.40; bb_position_20=9.19; day_of_week=9.07; market_volatility_20d=8.89; macd_hist_pct=8.85; market_return_5d=8.78.

## Quản trị rủi ro

- Vốn tham chiếu 100,000,000 VND; rủi ro mỗi lệnh 1.0%.
- Mức dừng lỗ 51.03; mục tiêu 1 56.00; mục tiêu 2 61.65.
- Tỷ lệ lợi nhuận/rủi ro 2.05; khối lượng vị thế 0 cổ phiếu.

## Dự báo 20 phiên

- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; toàn bộ horizon qua gate: chưa.
- P50 cuối kỳ 54.24 (3.51%).
- P10/P90 cuối kỳ 47.29 / 61.65.
- Lịch giao dịch: VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán.
- Ngày nghỉ đã loại khỏi forecast: 2026-01-01, 2026-01-02, 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20, 2026-04-27, 2026-04-30, 2026-05-01, 2026-08-31, 2026-09-01, 2026-09-02.

## Khung hành động tham khảo

- Trạng thái tín hiệu: CHƯA CÓ LỢI THẾ (NO_EDGE).
- Điều kiện phát hành tín hiệu: Correlation dự báo-return development OOS không dương..
- Điều kiện phát hành tín hiệu: Cận dưới expected excess return -0.04673175510209748 (dự báo điểm 0.007551148068159819) chưa vượt chi phí + margin 0.0050..
- Điều kiện phát hành tín hiệu: Technical score -2 < 2..
- Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20.
- Xu hướng kỹ thuật nghiêng về: Suy yếu / cẩn thận.
- XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: 52.8%.
- Mô hình Logistic đối chứng: 45.5%.
- Quantile forecast ước tính xác suất return cuối kỳ dương từ residual frozen holdout: 63.1%.
- Mức dừng lỗ tham chiếu 51.03, mục tiêu 1 56.00, tỷ lệ lợi nhuận/rủi ro 2.05.

Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.

---

## Tổng hợp AI từ report và tin web

- Trạng thái quyết định: NO_EDGE.
- Tóm tắt: ML decision hiện giữ nguyên NO_EDGE. News Reader đã trích đoạn có nguồn của 1 bài để phân loại chủ đề (chưa có nhóm khớp rule), nhưng các trích đoạn này không tạo bằng chứng mới cho quyết định đầu tư.
- Góc nhìn kỹ thuật: Artifact kỹ thuật: bias Suy yếu / cẩn thận; điểm -2. Chi tiết artifact: Xu hướng: Trung tính (Giá trên SMA60 nhưng chưa vượt SMA20.); MACD: Cẩn thận (MACD dưới signal, histogram âm.); RSI14: Trung tính (RSI 48.4.); Bollinger: Ổn định (Giá nằm trong dải Bollinger.); ADX: Đi ngang (ADX 11.4.); Thanh khoản: Bình thường (1.33 lần trung bình.); Stochastic: Yếu lại (%K nằm dưới %D.)
- Góc nhìn cơ bản: Artifact cơ bản: LPBank; kỳ 2026-Q2; P/E 13.86; P/B 3.64; ROE 24.7%; ROA 1.9%; Debt/Equity 13.30; Revenue Growth 23.3%; Profit Growth 5.2%.
- Tin doanh nghiệp: Đã đọc trích đoạn giới hạn của 1 bài; phân nhóm rule-based: chưa có nhóm khớp rule. Tác động cần kiểm chứng: mở URL gốc để xác minh bối cảnh. Đây không phải sentiment hay dự báo tác động giá.
- Live research: Live snapshot lấy lúc 2026-08-16T05:53:49.179319+00:00; News Reader đọc được 1 bài. ML có 3 lý do guard và vẫn là NO_EDGE. Không dùng tin live để train/backtest.

### Bằng chứng

- ML decision artifact: NO_EDGE. Correlation dự báo-return development OOS không dương.
- ML decision artifact: NO_EDGE. Cận dưới expected excess return -0.04673175510209748 (dự báo điểm 0.007551148068159819) chưa vượt chi phí + margin 0.0050.
- ML decision artifact: NO_EDGE. Technical score -2 < 2.
- News Reader [nguoiquansat.vn]: Dòng vốn thụ động 1,5 tỷ USD theo FTSE dự kiến vào Việt Nam qua 4 đợt: VIC, VHM, VCB, HPG, LPB, STB... được phân bổ ra sao? - nguoiquansat.vn | nhóm: khác (2026-08-12T07:33:01+00:00)

### Rủi ro cần kiểm chứng

- ML guard: Correlation dự báo-return development OOS không dương.
- ML guard: Cận dưới expected excess return -0.04673175510209748 (dự báo điểm 0.007551148068159819) chưa vượt chi phí + margin 0.0050.
- ML guard: Technical score -2 < 2.
- Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.
- Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.
- Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.
- Tin live/trích đoạn cần mở URL gốc để kiểm chứng bối cảnh, số liệu và thời điểm trước khi sử dụng.

### Nguồn live research

- [nguoiquansat.vn] Dòng vốn thụ động 1,5 tỷ USD theo FTSE dự kiến vào Việt Nam qua 4 đợt: VIC, VHM, VCB, HPG, LPB, STB... được phân bổ ra sao? - nguoiquansat.vn (2026-08-12T07:33:01+00:00): https://nguoiquansat.vn/dong-von-thu-dong-1-5-ty-usd-theo-ftse-du-kien-vao-viet-nam-qua-4-dot-vic-vhm-vcb-hpg-lpb-stb-duoc-phan-bo-ra-sao-310061.html

Lưu ý: Báo cáo chỉ tổng hợp artifact đã lưu để nghiên cứu; không phải khuyến nghị mua/bán. Quyết định và vị thế vẫn bị khóa theo signal_decision.json.

---

## News model riêng từng mã

- Symbol-news report: `/Users/tranlekhoa/Documents/DATA_SCI/vn_stock_analysis/reports/LPB/2026-08-16_12-53-34/all_files/symbol_news_model`
- Số bài tin trong CSV cho mã: 1
- Số dòng giá có news feature: 3
- XGBoost probability mới nhất: 0.511
- AUC OOS: 0.533
- Balanced accuracy OOS: 0.504
- Backtest total return: 0.000
- Base XGBoost probability: 0.528
- Chênh lệch News-adjusted - Base: -0.016
- Áp vào signal chính: not_applied
- Trạng thái news model: research_only
- Gate chưa đạt: min_articles_60, min_feature_rows_30, news_feature_gain_positive, auc_at_least_0_55, balanced_accuracy_at_least_0_52

News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.

Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.
