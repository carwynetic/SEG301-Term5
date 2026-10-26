# 🔍 SEG301 - Hệ Thống Ôn Thi Toàn Diện Môn Search Engines (Term 5)

> **Cổng ôn thi và thực hành trắc nghiệm chuyên ngành Search Engines (SEG301)** được xây dựng chuẩn kỹ thuật phần mềm, chạy hoàn toàn offline / local, tổng hợp kiến thức chuyên sâu của **17 Chương học**, tích hợp hệ thống dẫn nguồn Slide tương tác (`[1]`, `[2]`), ngân hàng **952 câu hỏi trắc nghiệm tiếng Anh** và công cụ thi thử 50 phút bốc đề ngẫu nhiên với chấm điểm & đánh giá năng lực chi tiết.

---

## 🌟 Tính Năng Nổi Bật (Key Features)

### 1. 📖 Kho Kiến Thức Chuyên Sâu 17 Chương (Knowledge Base)
- **Cấu trúc chuẩn mực**: Phân chia theo từng chương học và các đề mục lớn, lưu giữ nguyên vẹn thuật ngữ tiếng Anh gốc của slide bài giảng (in đậm, badge, highlight).
- **Hệ thống dẫn nguồn Slide tương tác (Interactive Citations)**: Mọi kiến thức trọng tâm đều gắn tag dẫn nguồn `[1]`, `[2]`, ... Khi bấm vào sẽ tự động cuộn mượt và làm phát sáng thẻ tham chiếu tương ứng ở mục **References & Slide Citations** cuối trang (chỉ rõ số slide, tên mục và tên file PPTX gốc).
- **Công thức & Code mẫu**: Tích hợp KaTeX hiển thị công thức toán xác suất IR, BM25, PageRank, Cosine Similarity, HITS, NDCG, v.v., kèm code minh họa thuật toán.

### 2. ✍️ Chế Độ Luyện Tập Theo Từng Chương (Chapter Practice)
- Mỗi chương gồm **50 câu hỏi trắc nghiệm tiếng Anh** (4-5 lựa chọn) xoay quanh lý thuyết, công thức tính toán, bài toán thực tế và code.
- **Phản hồi tức thì (Instant Feedback)**: Bấm chọn đáp án sẽ hiển thị ngay màu xanh (đúng) hoặc đỏ (sai) kèm hộp giải thích học thuật (Academic Explanation) chi tiết.
- Thống kê thời gian thực: Số câu đúng/sai, tỷ lệ chính xác (%) và thanh tiến độ.

### 3. ⏱️ Chế Độ Thi Thử 50 Phút (Timed Exam Engine)
- **Bốc đề ngẫu nhiên (Random Sampling)**: Tự động bốc **50 câu hỏi** từ ngân hàng **952 câu** (phủ khắp 17 chương học + 102 câu tổng hợp cross-chapter).
- **Đồng hồ đếm ngược (Countdown Timer)**: 50:00 hiển thị nổi bật, tự động cảnh báo đổi màu vàng (<10 phút) và nhấp nháy đỏ (<2 phút), tự động nộp bài khi hết giờ.
- **Bảng trạng thái câu hỏi (Question Palette)**: Bảng ma trận 50 ô thể hiện trực quan trạng thái: Đã làm (Xanh), Chưa làm (Xám), Đang chọn (Viền tím), Cắm cờ xem lại (Chấm vàng 🔖).
- **Bảng điểm & Đánh giá năng lực theo chương (Chapter Mastery Breakdown)**:
  - Phân loại độ thành thạo: **Thành thạo (≥80%)**, **Khá (50-79%)**, **Cần ôn tập (<50%)**.
  - Tự động đưa ra **Khuyến nghị học tập** nhắm thẳng vào các chương yếu kèm nút bấm mở ngay lý thuyết chương đó.
  - Chế độ xem lại bài thi (Review Mode) với bộ lọc: Tất cả, Câu sai, Câu đúng, Câu đã cắm cờ.

### 4. 🗂️ Ngân Hàng Câu Hỏi Toàn Diện (Question Bank Explorer - 952 Câu)
- Tra cứu, tìm kiếm và lọc toàn bộ 952 câu hỏi theo từng chương hoặc từ khóa.
- Nút bấm bật/tắt hiển thị toàn bộ đáp án và giải thích để tra cứu nhanh.

### 5. 📚 Từ Điển Thuật Ngữ Chuyên Ngành (Glossary - 83 Thuật Ngữ)
- 83 thuật ngữ cốt lõi của Search Engines (Crawler, Inverted Index, TF-IDF, BM25, PageRank, HITS, MAP, NDCG, LTR, HNSW, RAG,...) song ngữ Anh - Việt.
- Hộp tìm kiếm tức thời và phân loại theo chương.

### 6. ⚡ Tìm Kiếm Toàn Cục (Global Search Modal - `Ctrl + K`)
- Mở nhanh bảng tìm kiếm bằng tổ hợp phím `Ctrl + K` để nhảy ngay đến chương học, thuật ngữ hoặc câu hỏi mong muốn.

### 7. 🌓 Hỗ Trợ Giao Diện Dark / Light Mode & Không Phụ Thuộc Mạng (Zero-CORS)
- Giao diện Dark theme mặc định hiện đại, mượt mà, bảo vệ mắt khi ôn thi đêm.
- Dữ liệu đóng gói trực tiếp dưới dạng file `.js` (`data/*.js`) giúp chạy trơn tru cả khi mở trực tiếp file `index.html` qua giao thức `file:///` hoặc qua Local Web Server.

---

## 📂 Danh Sách 17 Chương Học (Syllabus Coverage)

| Ch | Tiêu Đề Tiếng Anh (English) | Tiêu Đề Tiếng Việt | Slide Nguồn Gốc |
|:---|:---|:---|:---|
| **01** | Information Retrieval & Search Engines | Tổng quan Thu hồi Thông tin & Công cụ Tìm kiếm | `1. Information Retieval and Search Engines.pptx` |
| **02** | Architecture of a Search Engine | Kiến trúc Tổng thể của Công cụ Tìm kiếm | `2. Architecture of A Search Engine.pptx` |
| **03** | Crawls and Feeds | Thu thập Dữ liệu Web & Nguồn cấp Dữ liệu | `3. Crawls and Feeds.pptx` |
| **04** | Processing Text | Xử lý & Tiền xử lý Văn bản | `4. Processing Text.pptx` |
| **05** | Ranking with Indexes | Xếp hạng với Chỉ mục & Cấu trúc Inverted Index | `5. Ranking with Indexes.pptx` |
| **06** | Queries and Interfaces | Truy vấn & Giao diện Tương tác Tìm kiếm | `6. Queries and Interfaces.pptx` |
| **07** | Retrieval Models | Các Mô hình Thu hồi Thông tin (VSM, BM25, LM) | `7. Retrieval Models.pptx` |
| **08** | Search Engine Optimization (SEO) | Tối ưu hóa Công cụ Tìm kiếm & Core Web Vitals | `8 Search Engine Optimization (SEO).pptx` |
| **09** | Evaluating Search Engines | Đánh giá Hiệu năng Tìm kiếm (Precision, Recall, MAP, NDCG) | `9. Evaluating Search Engines.pptx` |
| **10** | Classification and Clustering | Phân loại & Gom cụm Tài liệu (Naive Bayes, K-Means) | `10. Classification and Clustering.pptx` |
| **11** | Social Search | Tìm kiếm Mạng xã hội & Lọc cộng tác (Collaborative Filtering) | `11. Social search.pptx` |
| **12** | Beyond Bag of Words | Vượt qua Mô hình Túi từ (Knowledge Graph, Entity Linking) | `12. Beyond bag of words.pptx` |
| **13** | Web Spam Detection & Adversarial IR | Phát hiện Web Spam & IR Đối kháng (Link Farms, Cloaking, TrustRank) | `13. Web Spam Detection and Adversarial IR.pptx` |
| **14** | Link Analysis & Web Graph Algorithms | Phân tích Liên kết & Thuật toán Đồ thị Web (PageRank, HITS) | `14. Link Analysis and Web Graph Algorithms.pptx` |
| **15** | Distributed Search & Indexing at Scale | Tìm kiếm Phân tán & Đánh chỉ mục Quy mô lớn (Sharding, MapReduce) | `15. Distributed Search and Indexing at Scale.pptx` |
| **16** | Learning to Rank & Deep Relevance Matching | Học Xếp hạng (LTR) & So khớp Sự liên quan bằng Học sâu | `16. Learning to Rank and Deep Relevance Matching.pptx` |
| **17** | Neural IR, Dense Semantic Search & RAG | Tìm kiếm Ngữ nghĩa Dense, Vector ANN & RAG Hội thoại | `17. Neural Semantic Search and RAG.pptx` |
| **Comp** | Comprehensive Exam Synthesis | Ngân hàng 102 câu hỏi tổng hợp liên chương | *Tổng hợp toàn bộ chương trình* |

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Cục Bộ (Getting Started)

### Cách 1: Khởi động 1-Click bằng Batch Script (Khuyên dùng trên Windows)
1. Mở thư mục `D:\Vscode-luyện code\SEG301-Term5`.
2. Nhấp đúp chuột vào file **`start_server.bat`**.
3. Cửa sổ dòng lệnh sẽ chạy máy chủ Python và **tự động mở trình duyệt web** tại:
   ```text
   http://localhost:8001
   ```

### Cách 2: Chạy qua lệnh Terminal / VS Code
Mở terminal tại thư mục dự án và chạy:
```powershell
python server.py
```

### Cách 3: Chạy trực tiếp không cần Server (Direct File Access)
Nhấp đúp chuột trực tiếp vào file **`index.html`** để mở trên trình duyệt (Chrome, Edge, Firefox, Brave,...). Hệ thống đã đóng gói toàn bộ dữ liệu offline vào các tệp `.js` nên hoạt động hoàn hảo không bị lỗi CORS policy.

---

## 🛠️ Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
SEG301-Term5/
├── css/
│   └── style.css            # Toàn bộ design system hiện đại, dark/light mode, exam palette
├── js/
│   └── app.js               # Điều khiển logic ứng dụng, thi thử, chấm điểm, trắc nghiệm, tìm kiếm
├── data/
│   ├── chapters.json / .js  # Thông tin metadata 17 chương học
│   ├── knowledge.json / .js # Nội dung lý thuyết chi tiết 17 chương có dẫn nguồn [1], [2]
│   ├── questions.json / .js # Ngân hàng 952 câu hỏi trắc nghiệm tiếng Anh có đáp án & giải thích
│   └── glossary.json / .js  # Từ điển 83 thuật ngữ chuyên ngành Anh - Việt
├── lib/
│   └── katex/               # Thư viện KaTeX offline hiển thị công thức toán mượt mà
├── index.html               # Giao diện web portal chính
├── server.py                # Máy chủ HTTP cục bộ tự động mở trình duyệt
├── start_server.bat         # File thực thi 1-click trên Windows
└── README.md                # Tài liệu hướng dẫn sử dụng và thông tin môn học
```

---

## 📊 Thống Kê Dữ Liệu (Data Statistics)
- **Số chương học**: 17 Chương + 1 Phần Tổng hợp Toàn diện.
- **Tổng số câu hỏi trắc nghiệm**: **952 câu hỏi** (50 câu × 17 chương = 850 câu + 102 câu tổng hợp).
- **Thuật ngữ chuyên ngành**: 83 thuật ngữ.
- **Thời gian thi thử chuẩn**: 50 phút / 50 câu bốc ngẫu nhiên.
- **Dẫn nguồn slide chi tiết**: 100% các chương đều có danh mục tài liệu tham khảo ghi rõ trang slide và tệp nguồn PPTX.

---
*Chúc bạn ôn tập hiệu quả và đạt điểm A+ môn Search Engines (SEG301)!*
