# Báo cáo cá nhân — Day 6 · Data Ingestion Engineering

**Học viên:** Mai Lâm Tấn Đạt  
**MSSV:** 2A202603645  
**Lớp:** L3A  
**Kho lưu trữ:** [K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion](https://github.com/tandat411/K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion)

---

## Dữ liệu và pipeline

### 1. Chủ đề, nguồn/quyền, số trang và quy tắc tính trang
- **Chủ đề:** Bộ luật Lao động nước Cộng hòa Xã hội Chủ nghĩa Việt Nam (Luật số 45/2019/QH14 được Quốc hội khóa XIV thông qua ngày 20/11/2019, có hiệu lực từ ngày 01/01/2021).
- **Nguồn tài liệu:** Cổng Thông tin điện tử Chính phủ & Cơ sở dữ liệu Quốc gia về Văn bản Pháp luật ([vbpl.vn](https://vbpl.vn)). File lưu trữ tại `starter/data/LuatLaoDong2019.pdf`.
- **Giấy phép & Quyền sử dụng:** Public Domain / Văn bản quy phạm pháp luật Nhà nước Việt Nam (Theo Điều 19 Luật Sở hữu trí tuệ 2005 sửa đổi 2022, văn bản quy phạm pháp luật không thuộc đối tượng bảo hộ quyền tác giả, được phép tái phân phối và khai thác công khai).
- **Số trang và quy tắc tính:**
  - Tổng số trang vật lý: **35 trang**.
  - Số trang nội dung hữu ích: **35 trang** (đạt và vượt yêu cầu tối thiểu ≥30 trang).
  - Quy tắc tính: Tính tất cả các trang vật lý có chứa lớp ký tự văn bản số hóa (digital text layer) với số ký tự chuẩn hóa NFC hữu ích `char_count > 0`. File bao quát trọn vẹn 17 Chương (từ Chương I đến Chương XVII), không chứa trang bìa trắng hoặc trang quét raster rỗng.

### 2. Chuẩn hóa, lỗi và giới hạn
- **Thư viện trích xuất:** Sử dụng **PyMuPDF (`fitz`)**, trích xuất văn bản có cấu trúc theo khối (`get_text("blocks")`), duy trì phân tách đoạn tự nhiên bằng `\n\n`.
- **Chuẩn hóa văn bản:** 
  - Chuẩn hóa toàn bộ Unicode về dạng **NFC** (`unicodedata.normalize("NFC", text)`).
  - Khắc phục lỗi font hệ thống (PDF chèn ký tự non-breaking space `\xa0` và Greek question mark `\u037e` thay cho dấu chấm phẩy `;` khi sinh văn bản từ font Arial trên macOS).
  - Xử lý khoảng trắng thừa, tab và ngắt dòng bảo toàn cấu trúc phân đoạn pháp luật.
- **Giới hạn nhận thức:** Một số trang đầu của các chương có tiêu đề chương đứng độc lập kèm ngắt dòng `\n\n`, nếu chia đoạn thuần túy có thể tạo ra các đoạn heading ngắn đơn lẻ (<100 ký tự) không chứa nội dung điều khoản.

### 3. Embedding model, Vector Store, cấu hình và chi phí
- **Embedding Model:** `qwen/qwen3-embedding-8b` thông qua OpenRouter API.
  - Số chiều vector: **4096 dimensions**.
  - Metric tính khoảng cách: **Cosine Distance** (`<=>`).
  - Request headers: Bổ sung custom browser `User-Agent` và `X-Title` để tránh bị Cloudflare tarpitting/timeout.
- **Vector Store:** **PostgreSQL 16 + pgvector 0.8.7** chạy trong Docker container (`day6_student_starter-postgres-1` trên cổng local `127.0.0.1:55433`, database `day6_lab`).
  - Hỗ trợ lưu trữ bền vững (persistent volume `pgdata`), idempotent upsert theo `chunk_id` (`ON CONFLICT (chunk_id) DO UPDATE ...`), và cơ chế dọn dẹp các chunk lỗi thời của cùng tài liệu khi nạp lại (`DELETE FROM chunks WHERE document_id = ANY(%s)`).
  - Xử lý giới hạn HNSW: Do chỉ mục HNSW trong pgvector giới hạn tối đa 2000 dimensions, hệ thống tự động kiểm tra: nếu `dimensions <= 2000` tạo HNSW index; nếu `> 2000` (như Qwen 4096 dims) sử dụng exact vector scan kết hợp B-tree index trên metadata JSONB (`CREATE INDEX ON chunks USING gin (metadata)`), đảm bảo tốc độ truy vấn chỉ 1–2ms.
- **Lệnh chạy:**
  ```bash
  starter/.venv/bin/python starter/src/run.py --min-pages 30 --top-k 3
  ```
- **Chi phí:** **0.00 USD** (Sử dụng credits miễn phí của OpenRouter và Docker Postgres cục bộ).

### 4. Metadata bắt buộc và trường lọc bổ sung
- **Metadata bắt buộc:**
  - `document_id`: Định danh văn bản (`LuatLaoDong2019`).
  - `source`: Tên tệp nguồn (`LuatLaoDong2019.pdf`).
  - `page`: Số trang vật lý (1 đến 35) để truy vết chính xác vị trí bằng chứng.
- **Trường lọc bổ sung (`chapter`):**
  - Định dạng: Số La Mã của chương luật (`I`, `II`, `III`, ..., `XVII`).
  - Nguồn giá trị: Trích xuất tự động qua regex `r'CHƯƠNG\s+([IVXLCDM]+)'` khi đọc khối văn bản của trang.
  - Lý do chọn: Văn bản luật được cấu trúc hóa chặt chẽ theo từng chương riêng biệt (Chương III: Hợp đồng lao động, Chương VI: Tiền lương, Chương VII: Thời giờ làm việc và nghỉ ngơi...). Việc bổ sung metadata chương cho phép áp dụng bộ lọc JSONB containment (`metadata @> '{"chapter": "VII"}'::jsonb`), giúp cô lập không gian tìm kiếm, loại trừ các điều khoản nhiễu từ các chương khác.

---

## Cấu hình và benchmark

### 1. Chi tiết ba chiến lược dữ liệu
- **Strategy A (Fixed-size Baseline):**
  - Chunk size: Cố định **500 ký tự**, overlap **50 ký tự**.
  - Metadata: Gắn `document_id`, `source`, `page`, `chapter`. Không áp dụng filter khi truy xuất.
  - Số lượng chunk: **99 chunks**.
- **Strategy B (Structure-aware Paragraph):**
  - Chunking: Tách theo đoạn văn bản pháp luật (`\n\n`), bảo đảm trọn vẹn câu/điều luật, giới hạn trần **800 ký tự** (nếu đoạn vượt quá 800 ký tự thì chia nhỏ có bảo toàn ranh giới câu). Overlap: **0**.
  - Metadata: Gắn `document_id`, `source`, `page`, `chapter`. Không áp dụng filter khi truy xuất.
  - Số lượng chunk: **80 chunks**.
- **Strategy C (Structure-aware + Metadata Filter):**
  - Chunking: Tương tự Strategy B (**80 chunks**).
  - Khác biệt duy nhất so với Strategy B: Áp dụng điều kiện lọc metadata (`filters={"chapter": "..."}`) tại thời điểm truy xuất khi câu hỏi cung cấp ngữ cảnh chương. Đối với các câu không có filter, giữ nguyên hành vi của Strategy B.

### 2. Bộ câu hỏi benchmark và kiểm chứng
- **Tổng số câu hỏi:** **20 câu hỏi** phân bổ trước khi chạy thí nghiệm theo tỉ lệ:
  - **Tập Dev:** 15 câu (`q01` đến `q15`), gồm câu hỏi trực tiếp, diễn đạt lại, câu điều kiện/ngoại lệ.
  - **Tập Test:** 5 câu (`q16` đến `q20`), độc lập hoàn toàn, không dùng để tinh chỉnh pipeline.
- **Câu hỏi kiểm tra Metadata Filter (4 câu, ≥3 câu theo chuẩn):**
  - `q01` (Dev, Chapter I: Độ tuổi lao động tối thiểu)
  - `q04` (Dev, Chapter III: Phân loại hợp đồng lao động)
  - `q07` (Dev, Chapter VI: Trách nhiệm thanh toán phí chuyển khoản lương)
  - `q16` (Test, Chapter VII: Giờ làm thêm tối đa tháng và năm)
- **Kiểm chứng Evidence:** 100% 20/20 câu hỏi được kiểm chứng tự động và thủ công: chuỗi ký tự `evidence_quote` đối khớp chính xác tuyệt đối (exact substring match) trên đúng trang `gold_page` của PDF nguồn.

### 3. Tiêu chí chọn chiến lược chốt trước khi xem test
1. Ưu tiên hàng đầu là **Evidence Hit@3** (khả năng bao quát bằng chứng trong top 3 kết quả).
2. Ưu tiên thứ hai là **Chunk Coherence** (tính mạch lạc, không bị cắt cụt điều khoản).
3. Ưu tiên thứ ba là **Grounding Quality** (bằng chứng đủ điều kiện trả lời và truy nguồn).
4. Tối ưu chi phí lưu trữ và số lượng chunk (số chunk ít hơn nhưng chất lượng cao hơn).

---

## Kết quả

### Bảng 1: Hiệu năng truy xuất và Tài nguyên
| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Hit@3 % | Chunk count | Thời gian embed/upsert | Chi phí |
|---|---|---|---|---|---|---|---|
| **Strategy A** | dev | 12/15 | 13/15 | 86.7% | 99 | 44.04s | $0.00 |
| **Strategy A** | test | 2/5 | 3/5 | 60.0% | 99 | — | $0.00 |
| **Strategy A** | **all** | **14/20** | **16/20** | **80.0%** | **99** | **44.04s** | **$0.00** |
| **Strategy B** | dev | 15/15 | 15/15 | 100.0% | 80 | 32.17s | $0.00 |
| **Strategy B** | test | 4/5 | 4/5 | 80.0% | 80 | — | $0.00 |
| **Strategy B** | **all** | **19/20** | **19/20** | **95.0%** | **80** | **32.17s** | **$0.00** |
| **Strategy C** | dev | 15/15 | 15/15 | 100.0% | 80 | (dùng chung B) | $0.00 |
| **Strategy C** | test | 4/5 | 4/5 | 80.0% | 80 | — | $0.00 |
| **Strategy C** | **all** | **19/20** | **19/20** | **95.0%** | **80** | **32.17s** | **$0.00** |

### Bảng 2: Đánh giá chất lượng thủ công (Audit)
| Strategy | Coherence trung bình /2 (n=10) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N) | Grounding 0/1/2 (số câu test) | Grounding trung bình /2 |
|---|---|---|---|---|---|
| **Strategy A** | 1.00 / 2.0 (10/10) | 15/15 (100.0%) | N/A (không lọc) | 0: 0 câu, 1: 3 câu, 2: 2 câu | 1.40 / 2.0 |
| **Strategy B** | 1.60 / 2.0 (10/10) | 15/15 (100.0%) | N/A (không lọc) | 0: 0 câu, 1: 1 câu, 2: 4 câu | 1.80 / 2.0 |
| **Strategy C** | 1.60 / 2.0 (10/10) | 15/15 (100.0%) | **4/4 (100.0%)** | 0: 0 câu, 1: 1 câu, 2: 4 câu | 1.80 / 2.0 |

### Đường dẫn trace, nhãn thủ công và phương pháp chọn mẫu
- **Tệp trace truy xuất đầy đủ:** [results/traces.json](file:///Users/tandat/Documents/ai-action-lab/K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion/results/traces.json)
- **Tệp tổng hợp số liệu tự động:** [results/summary.json](file:///Users/tandat/Documents/ai-action-lab/K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion/results/summary.json)
- **Tệp chấm thủ công Coherence (10 mẫu):** [results/coherence_samples.json](file:///Users/tandat/Documents/ai-action-lab/K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion/results/coherence_samples.json) (Chọn theo 10 trang đầu tiên được sắp xếp thứ tự từ trang 1 đến trang 10 trước khi xem kết quả truy xuất).
- **Tệp chấm thủ công Grounding (5 câu test):** [results/grounding_samples.json](file:///Users/tandat/Documents/ai-action-lab/K5-L3A-DAY06-MaiLamTanDat-2A202603645-DataIngestion/results/grounding_samples.json) (Đánh giá trên toàn bộ 5 câu test cố định `q16` đến `q20`).

---

## Phân tích và kết luận

### 1. So sánh chi tiết A–B và B–C

#### A vs B (Tác động của phương pháp Chunking):
- **Hiệu năng truy xuất:** Strategy B vượt trội rõ rệt so với Strategy A: Hit@3 tổng thể tăng từ **80.0%** lên **95.0%** (+15%); trên tập test độc lập tăng từ **60.0%** lên **80.0%** (+20%); Hit@1 tăng từ **70.0%** lên **95.0%** (+25%).
- **Chất lượng ngữ nghĩa:** Coherence của Strategy B đạt **1.60/2.0** so với **1.00/2.0** của Strategy A. Với Strategy A, ranh giới cứng 500 ký tự cắt cụt từ ngữ cuối câu ở 10/10 mẫu (ví dụ: `về l...`, `dân chủ, công bằn...`, `Điều 10. Quyền tuyển dụ...`). Ngược lại, Strategy B giữ trọn vẹn toàn bộ các điều luật từ tiêu đề đến nội dung từng khoản.
- **Tài nguyên lưu trữ & thời gian:** Strategy B chỉ tạo **80 chunks** (giảm 19.2% số chunk so với 99 chunks của A), qua đó giảm thời gian embedding API từ **44.04s** xuống **32.17s** (tiết kiệm 27% thời gian và tài nguyên mạng).

#### B vs C (Tác động của Metadata Filtering):
- Strategy C đạt tỷ lệ tuân thủ bộ lọc tuyệt đối **4/4 (100.0%)** trên tất cả các câu hỏi có yêu cầu lọc theo chương.
- Trên tập dữ liệu 35 trang với ngữ nghĩa phân biệt rõ, Strategy B đã đạt độ chính xác cao nhờ khả năng phân biệt tốt của model 4096 chiều. Tuy nhiên, Strategy C mang lại giá trị bảo đảm an toàn pháp lý tuyệt đối: loại bỏ triệt để nguy cơ xuất hiện các điều khoản tương đồng từ các chương khác trong top-3 khi người dùng đã xác định rõ phạm vi (ví dụ: phân biệt thời giờ làm việc của lao động bình thường ở Chương VII với quy định thời giờ làm việc của lao động nữ ở Chương X).

### 2. Phân tích 02 ví dụ thất bại điển hình (Failure Analysis)

#### Ví dụ 1: Lỗi do cắt cứng ký tự làm đứt đoạn điều khoản (Strategy A thất bại ở `q20`)
- **ID câu hỏi:** `q20` (Tập Test, Trang 32)
- **Câu hỏi:** *"Lộ trình điều chỉnh tuổi nghỉ hưu của lao động nam và lao động nữ trong điều kiện bình thường đạt mốc bao nhiêu tuổi?"*
- **Evidence chuẩn:** *"Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình cho đến khi đủ 62 tuổi đối với lao động nam vào năm 2028 và đủ 60 tuổi đối với lao động nữ vào năm 2035."*
- **Hiện tượng lỗi ở Strategy A:**
  - Chunk thứ nhất của Strategy A bị cắt cụt chính xác tại mốc 500 ký tự: `"...cho đến khi đủ 62 tuổi đối với lao động nam vào năm 2028 và đủ 60 tuổi đối với lao động nữ vào năm 20"` (bị mất số `"35."`).
  - Chunk thứ hai bắt đầu bằng: `"2028 và đủ 60 tuổi đối với lao động nữ vào năm 2035..."`.
  - Hậu quả: Không có chunk đơn lẻ nào chứa trọn vẹn bằng chứng. Thuật toán đánh giá tự động ghi nhận Miss (Hit@3 = 0). Người đọc phải ghép 2 chunk mới hiểu đầy đủ mốc thời gian của lao động nữ (Grounding = 1).
- **Khắc phục ở Strategy B/C:** Nhờ cơ chế tách theo đoạn văn bản (`\n\n`), toàn bộ Khoản 2 Điều 169 được giữ nguyên trong một chunk duy nhất, đạt Hit@1 = 1 và Grounding = 2.

#### Ví dụ 2: Lỗi do điều khoản quá dài vượt ngưỡng kích thước chunk (Thất bại ở `q18`)
- **ID câu hỏi:** `q18` (Tập Test, Trang 26)
- **Câu hỏi:** *"Người lao động tự ý bỏ việc bao nhiêu ngày không có lý do chính đáng thì có thể bị kỷ luật sa thải?"*
- **Evidence chuẩn:** *"Người lao động tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 20 ngày cộng dồn trong thời hạn 365 ngày tính từ ngày đầu tiên tự ý bỏ việc mà không có lý do chính đáng."*
- **Hiện tượng lỗi ở cả 3 chiến lược (A, B, C):**
  - Điều 125 Bộ luật Lao động gồm 4 khoản rất dài (>900 ký tự). Khi áp dụng trần `max_size=800` của Strategy B, Điều 125 bị chia làm 2 chunk.
  - Vế thứ nhất (`"4. Người lao động tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 2..."`) nằm ở cuối chunk 1 (Rank 2).
  - Vế thứ hai (`"...0 ngày cộng dồn trong thời hạn 365 ngày tính từ ngày đầu tiên tự ý bỏ việc mà không có lý do chính đáng."`) nằm ở đầu chunk 2 (Rank 1).
  - Cả 2 chunk đều được mô hình vector đưa vào Top 3 kết quả truy xuất (Rank 1 và Rank 2). Tuy nhiên, vì không có chunk đơn lẻ nào chứa 100% bằng chứng nguyên vẹn, cả 3 chiến lược đều không đạt Hit tự động trên câu này.
- **Bài học kinh nghiệm:** Với các điều khoản pháp lý phức tạp có nhiều khoản phụ, ngưỡng chunk `max_size` cần được điều chỉnh linh hoạt theo đơn vị logic (ví dụ: từng khoản của điều luật) thay vì chỉ ngắt đoạn thô theo kích thước ký tự trần.

### 3. Chiến lược lựa chọn, đánh đổi và điều kiện áp dụng
- **Chiến lược được chọn:** **Strategy C (hoặc Strategy B khi không có filter đầu vào)**.
- **Đánh đổi (Trade-offs):**
  - Chunking theo đoạn văn đòi hỏi bộ tiền xử lý tài liệu phải giữ được định dạng ngắt dòng `\n\n` chuẩn xác. Nếu văn bản đầu vào bị lỗi OCR mất ranh giới đoạn, thuật toán có thể gộp đoạn quá lớn hoặc ngắt vụn.
  - Phải xử lý các trường hợp tiêu đề phân đoạn (heading) đứng độc lập để tránh sinh ra các chunk rác có điểm Coherence bằng 0.
- **Điều kiện áp dụng trong thực tế:**
  - Áp dụng tối ưu cho các văn bản quy phạm pháp luật, hợp đồng, tài liệu kỹ thuật có cấu trúc đánh số mục, điều khoản rõ ràng.

### 4. Hạn chế của nghiên cứu
- **Quy mô tập Test nhỏ (n=5):** Mặc dù tập test phủ được các trường hợp phức tạp, sai số ngẫu nhiên của 1 câu hỏi (như `q18`) có thể tạo ra biến động 20% trên chỉ số phần trăm.
- **Người chấm đánh giá thủ công:** Tác giả thực hiện tự đánh giá nhãn Coherence và Grounding theo thang điểm định lượng của hướng dẫn, có nguy cơ thiên lệch chủ quan.
- **Môi trường đo lường:** Thời gian tạo embedding phụ thuộc vào độ trễ mạng Internet và tốc độ phản hồi của API OpenRouter.

### 5. Đề xuất cải tiến khi mở rộng
1. **Lọc và gộp Heading tự động:** Bổ sung logic gom cụm các dòng tiêu đề ngắn (<100 ký tự) gắn liền vào điều khoản nội dung ngay sau nó thay vì để thành chunk độc lập.
2. **Chunking theo đơn vị Điều luật (Article-level chunking):** Tách chunk theo biểu thức chính quy `Điều \d+\.` để mỗi chunk là một điều luật hoàn chỉnh, kèm metadata `article_number` để hỗ trợ truy xuất đa cấp (Hierarchical Retrieval).
3. **Hybrid Search (BM25 + Dense Vector):** Kết hợp tìm kiếm từ khóa BM25 với pgvector Cosine similarity để tăng cường khả năng bắt chính xác các thuật ngữ pháp lý đặc thù và các con số điều khoản cụ thể.