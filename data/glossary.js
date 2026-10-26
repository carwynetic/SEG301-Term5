/* SEG301 Comprehensive Bilingual Search Engine Glossary */
window.SEG_GLOSSARY = [
  {
    "term": "Information Retrieval (IR)",
    "term_vn": "Thu hồi thông tin",
    "chapter": 1,
    "category": "Foundations",
    "definition": "Ngành khoa học máy tính nghiên cứu về cấu trúc, phân tích, tổ chức, lưu trữ, tìm kiếm và truy xuất thông tin từ các tập hợp văn bản."
  },
  {
    "term": "Information Need",
    "term_vn": "Nhu cầu thông tin",
    "chapter": 1,
    "category": "Foundations",
    "definition": "Ước muốn hoặc lỗ hổng tri thức thúc đẩy người dùng đi tìm kiếm thông tin."
  },
  {
    "term": "Query",
    "term_vn": "Câu truy vấn",
    "chapter": 1,
    "category": "Foundations",
    "definition": "Biểu diễn bằng ngôn ngữ tự nhiên hoặc ký hiệu mà người dùng gửi tới hệ thống IR để diễn đạt nhu cầu thông tin."
  },
  {
    "term": "Web Search Engine",
    "term_vn": "Công cụ tìm kiếm web",
    "chapter": 1,
    "category": "Foundations",
    "definition": "Hệ thống IR quy mô lớn thu thập và lập chỉ mục hàng tỷ trang web mở trên toàn cầu."
  },
  {
    "term": "Enterprise Search",
    "term_vn": "Tìm kiếm doanh nghiệp",
    "chapter": 1,
    "category": "Foundations",
    "definition": "Hệ thống tìm kiếm trong phạm vi mạng nội bộ công ty, đáp ứng các tiêu chuẩn khắt khe về bảo mật và tuân thủ pháp lý."
  },
  {
    "term": "Selective Dissemination of Information (SDI)",
    "term_vn": "Phổ biến thông tin chọn lọc",
    "chapter": 1,
    "category": "Applications",
    "definition": "Hệ thống định tuyến/lọc tài liệu tự động đẩy thông tin mới phù hợp tới hồ sơ đăng ký của người dùng."
  },
  {
    "term": "Text Acquisition",
    "term_vn": "Thu nhận văn bản",
    "chapter": 2,
    "category": "Architecture",
    "definition": "Giai đoạn đầu tiên của tiến trình lập chỉ mục: thu thập tài liệu qua crawler, feeds và chuyển đổi sang định dạng chuẩn."
  },
  {
    "term": "Text Transformation",
    "term_vn": "Biến đổi văn bản",
    "chapter": 2,
    "category": "Architecture",
    "definition": "Giai đoạn phân tích cú pháp, tách từ (tokenization), loại từ dừng (stopping), và đưa về gốc từ (stemming)."
  },
  {
    "term": "Index Creation",
    "term_vn": "Tạo lập chỉ mục",
    "chapter": 2,
    "category": "Architecture",
    "definition": "Tổ chức các term thành cấu trúc chỉ mục ngược (Inverted Index) và nén dữ liệu để tối ưu tốc độ truy xuất."
  },
  {
    "term": "Query Process",
    "term_vn": "Tiến trình truy vấn",
    "chapter": 2,
    "category": "Architecture",
    "definition": "Tiến trình xử lý thời gian thực: tiếp nhận truy vấn, tính điểm xếp hạng các tài liệu liên quan và hiển thị trang kết quả."
  },
  {
    "term": "Throughput",
    "term_vn": "Thông lượng",
    "chapter": 2,
    "category": "Performance",
    "definition": "Số lượng truy vấn hệ thống có thể xử lý thành công trong một đơn vị thời gian (thường tính bằng QPS - Queries Per Second)."
  },
  {
    "term": "Latency",
    "term_vn": "Độ trễ",
    "chapter": 2,
    "category": "Performance",
    "definition": "Khoảng thời gian từ lúc người dùng gửi truy vấn đến khi nhận được toàn bộ trang kết quả SERP."
  },
  {
    "term": "Web Crawler (Spider / Bot)",
    "term_vn": "Bộ thu thập dữ liệu web",
    "chapter": 3,
    "category": "Crawling",
    "definition": "Chương trình tự động duyệt qua World Wide Web bằng cách bắt đầu từ tập hạt giống (Seeds) và lần theo các siêu liên kết."
  },
  {
    "term": "URL Frontier",
    "term_vn": "Hàng đợi URL",
    "chapter": 3,
    "category": "Crawling",
    "definition": "Cấu trúc dữ liệu hàng đợi quản lý danh sách các liên kết đã phát hiện nhưng chưa được tải về, điều phối thứ tự và độ lịch sự (politeness)."
  },
  {
    "term": "Robots Exclusion Protocol (robots.txt)",
    "term_vn": "Quy ước loại trừ robot",
    "chapter": 3,
    "category": "Crawling",
    "definition": "Tệp văn bản đặt tại gốc website chỉ định các phân vùng thư mục mà crawler được phép hoặc bị cấm truy cập."
  },
  {
    "term": "Spider Trap",
    "term_vn": "Bẫy nhện",
    "chapter": 3,
    "category": "Crawling",
    "definition": "Cấu trúc website vô tận (như lịch tạo động, liên kết vòng tròn) khiến crawler bị kẹt trong vòng lặp tải vô hạn."
  },
  {
    "term": "SimHash / MinHash",
    "term_vn": "Băm tương đồng / Băm cực tiểu",
    "chapter": 3,
    "category": "Preprocessing",
    "definition": "Kỹ thuật Locality-Sensitive Hashing (LSH) cho phép phát hiện các trang web trùng lặp gần (near-duplicate) với chi phí tính toán thấp."
  },
  {
    "term": "Zipf's Law",
    "term_vn": "Định luật Zipf",
    "chapter": 4,
    "category": "Text Statistics",
    "definition": "Quy luật thực nghiệm khẳng định tần suất xuất hiện của từ tỉ lệ nghịch với thứ hạng tần suất của nó: f(r) ~ 1/r."
  },
  {
    "term": "Heaps' Law",
    "term_vn": "Định luật Heaps",
    "chapter": 4,
    "category": "Text Statistics",
    "definition": "Quy luật ước lượng tốc độ tăng trưởng kích thước từ vựng (V) theo tổng số từ trong kho ngữ liệu (N): V = k * N^beta."
  },
  {
    "term": "Tokenization",
    "term_vn": "Tách từ",
    "chapter": 4,
    "category": "Preprocessing",
    "definition": "Quá trình phân chia chuỗi văn bản liên tục thành các đơn vị ngữ pháp cơ sở gọi là tokens."
  },
  {
    "term": "Stemming",
    "term_vn": "Đưa về gốc từ (theo quy tắc)",
    "chapter": 4,
    "category": "Preprocessing",
    "definition": "Kỹ thuật lược bỏ hậu tố/tiền tố ngữ pháp dựa trên tập luật giải thuật (như Porter Stemmer) để đưa từ về dạng gốc thô."
  },
  {
    "term": "Lemmatization",
    "term_vn": "Đưa về từ nguyên (từ điển)",
    "chapter": 4,
    "category": "Preprocessing",
    "definition": "Kỹ thuật sử dụng từ điển và phân tích hình thái học để đưa từ về đúng dạng từ nguyên hợp lệ (Lemma)."
  },
  {
    "term": "Anchor Text",
    "term_vn": "Văn bản neo",
    "chapter": 4,
    "category": "Preprocessing",
    "definition": "Đoạn văn bản có thể nhấp chuột của siêu liên kết, cung cấp mô tả ngắn gọn và khách quan về nội dung trang đích."
  },
  {
    "term": "Inverted Index",
    "term_vn": "Chỉ mục ngược",
    "chapter": 5,
    "category": "Indexing",
    "definition": "Cấu trúc dữ liệu nền tảng của Search Engine, ánh xạ từ mỗi từ vựng (term) tới danh sách các tài liệu (postings) chứa từ đó."
  },
  {
    "term": "Posting List",
    "term_vn": "Danh sách posting",
    "chapter": 5,
    "category": "Indexing",
    "definition": "Danh sách các phần tử ghi nhận docID, term frequency, và vị trí từ (positions) của một term trong toàn kho tài liệu."
  },
  {
    "term": "d-gaps (Document Gaps)",
    "term_vn": "Khoảng cách docID",
    "chapter": 5,
    "category": "Compression",
    "definition": "Kỹ thuật lưu trữ hiệu số chênh lệch giữa hai docID liên tiếp thay vì giá trị tuyệt đối, giúp các số nguyên trở nên nhỏ hơn để dễ nén."
  },
  {
    "term": "Variable Byte (V-Byte) Encoding",
    "term_vn": "Mã hóa byte biến thiên",
    "chapter": 5,
    "category": "Compression",
    "definition": "Phương pháp nén số nguyên sử dụng 7 bit cho dữ liệu và 1 bit tiếp tục (continuation bit) để xác định byte kết thúc."
  },
  {
    "term": "Document-At-A-Time (DAAT)",
    "term_vn": "Xử lý từng tài liệu",
    "chapter": 5,
    "category": "Query Processing",
    "definition": "Chiến lược duyệt đồng thời các danh sách postings của tất cả từ khóa truy vấn để hoàn thành tính điểm trọn vẹn cho từng tài liệu một."
  },
  {
    "term": "Term-At-A-Time (TAAT)",
    "term_vn": "Xử lý từng thuật ngữ",
    "chapter": 5,
    "category": "Query Processing",
    "definition": "Chiến lược xử lý tuần tự từng danh sách posting và cộng dồn điểm số vào các biến tích lũy (accumulators) trong bộ nhớ."
  },
  {
    "term": "WAND (Weak AND)",
    "term_vn": "Thuật toán WAND cắt tỉa động",
    "chapter": 5,
    "category": "Query Processing",
    "definition": "Thuật toán cắt tỉa động hiệu năng cao giúp bỏ qua hàng triệu tài liệu không có cơ hội lọt vào Top-K điểm cao nhất."
  },
  {
    "term": "Pseudo-Relevance Feedback (PRF)",
    "term_vn": "Phản hồi độ liên quan giả định",
    "chapter": 6,
    "category": "Queries",
    "definition": "Kỹ thuật mở rộng truy vấn tự động bằng cách giả định k tài liệu đầu tiên trả về là đúng, trích xuất các từ quan trọng nhất từ chúng để bổ sung vào truy vấn."
  },
  {
    "term": "Rocchio Algorithm",
    "term_vn": "Thuật toán Rocchio",
    "chapter": 6,
    "category": "Queries",
    "definition": "Thuật toán phản hồi độ liên quan trong không gian vector điều chỉnh vector truy vấn dịch gần về phía các tài liệu liên quan."
  },
  {
    "term": "Levenshtein Distance",
    "term_vn": "Khoảng cách biên tập Levenshtein",
    "chapter": 6,
    "category": "Spelling Correction",
    "definition": "Số lượng phép biến đổi tối thiểu (Chèn, Xóa, Thay thế) để chuyển đổi từ một chuỗi ký tự này sang chuỗi ký tự khác."
  },
  {
    "term": "Soundex",
    "term_vn": "Mã hóa phát âm Soundex",
    "chapter": 6,
    "category": "Spelling Correction",
    "definition": "Thuật toán ngữ âm mã hóa từ ngữ dựa trên cách phát âm trong tiếng Anh, giúp tìm kiếm từ đồng âm khác chính tả."
  },
  {
    "term": "SERP (Search Engine Result Page)",
    "term_vn": "Trang kết quả tìm kiếm",
    "chapter": 6,
    "category": "Interfaces",
    "definition": "Giao diện hiển thị danh sách các kết quả tìm kiếm bao gồm tiêu đề, URL, đoạn trích (snippet) và các tính năng nâng cao."
  },
  {
    "term": "Vector Space Model (VSM)",
    "term_vn": "Mô hình không gian vector",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Mô hình IR biểu diễn văn bản và truy vấn dưới dạng các vector đa chiều và đo độ tương đồng bằng hàm Cosine."
  },
  {
    "term": "TF-IDF",
    "term_vn": "Tần suất từ - Nghịch đảo tần suất văn bản",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Công thức gán trọng số từ vựng kết hợp giữa tần suất xuất hiện trong tài liệu (TF) và mức độ hiếm của từ trong toàn bộ kho dữ liệu (IDF)."
  },
  {
    "term": "Okapi BM25",
    "term_vn": "Mô hình xác suất BM25",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Hàm xếp hạng xác suất phi tuyến tính hàng đầu trong IR truyền thống, tích hợp bão hòa tần suất từ (k1) và chuẩn hóa độ dài tài liệu (b)."
  },
  {
    "term": "Query Likelihood Model",
    "term_vn": "Mô hình hợp lý của truy vấn",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Mô hình xác suất đánh giá độ liên quan bằng xác suất mà mô hình ngôn ngữ của tài liệu sinh ra được câu truy vấn: P(Q|D)."
  },
  {
    "term": "Jelinek-Mercer Smoothing",
    "term_vn": "Làm mượt tuyến tính Jelinek-Mercer",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Kỹ thuật làm mượt ngôn ngữ nội suy tuyến tính giữa xác suất từ trong tài liệu với xác suất từ trong toàn bộ kho tài liệu."
  },
  {
    "term": "Dirichlet Prior Smoothing",
    "term_vn": "Làm mượt tiên nghiệm Dirichlet",
    "chapter": 7,
    "category": "Retrieval Models",
    "definition": "Kỹ thuật làm mượt Bayes với tham số mu phụ thuộc vào độ dài thực tế của tài liệu."
  },
  {
    "term": "On-Page SEO",
    "term_vn": "Tối ưu hóa trên trang",
    "chapter": 8,
    "category": "SEO",
    "definition": "Các biện pháp tối ưu trực tiếp trên nội dung và mã nguồn HTML của trang web (Title, Meta, Headers, Keywords, Schema markup)."
  },
  {
    "term": "Off-Page SEO",
    "term_vn": "Tối ưu hóa ngoài trang",
    "chapter": 8,
    "category": "SEO",
    "definition": "Các hoạt động xây dựng uy tín website bên ngoài trang chủ yếu thông qua hệ thống liên kết ngược (Backlinks) chất lượng."
  },
  {
    "term": "Technical SEO",
    "term_vn": "Tối ưu hóa kỹ thuật",
    "chapter": 8,
    "category": "SEO",
    "definition": "Tối ưu cấu trúc kỹ thuật đảm bảo bot tìm kiếm có thể crawl, render và index dễ dàng (tốc độ tải, HTTPS, sitemap, robots.txt)."
  },
  {
    "term": "Core Web Vitals",
    "term_vn": "Chỉ số trải nghiệm trang cốt lõi",
    "chapter": 8,
    "category": "SEO",
    "definition": "Bộ 3 chỉ số đo lường trải nghiệm người dùng thực tế của Google: LCP (tốc độ tải), INP (tính tương tác), và CLS (độ ổn định thị giác)."
  },
  {
    "term": "Precision@k (P@k)",
    "term_vn": "Độ chính xác tại k",
    "chapter": 9,
    "category": "Evaluation",
    "definition": "Tỷ lệ phần trăm tài liệu thực sự liên quan nằm trong Top-k kết quả đầu tiên được trả về."
  },
  {
    "term": "Mean Average Precision (MAP)",
    "term_vn": "Độ chính xác trung bình trung bình",
    "chapter": 9,
    "category": "Evaluation",
    "definition": "Chỉ số đánh giá độ hiệu quả toàn diện tính trung bình của Average Precision (AP) trên toàn bộ tập các truy vấn thử nghiệm."
  },
  {
    "term": "Mean Reciprocal Rank (MRR)",
    "term_vn": "Nghịch đảo thứ hạng trung bình",
    "chapter": 9,
    "category": "Evaluation",
    "definition": "Độ đo tập trung vào vị trí xuất hiện của tài liệu liên quan ĐẦU TIÊN trong danh sách kết quả, rất quan trọng cho Navigational search và QA."
  },
  {
    "term": "Normalized Discounted Cumulative Gain (NDCG@k)",
    "term_vn": "Độ lợi tích lũy giảm dần chuẩn hóa tại k",
    "chapter": 9,
    "category": "Evaluation",
    "definition": "Độ đo xếp hạng đa mức độ liên quan (Graded Relevance), áp dụng hàm suy giảm logarithm theo vị trí thứ hạng."
  },
  {
    "term": "Naive Bayes Classifier",
    "term_vn": "Bộ phân loại Naive Bayes",
    "chapter": 10,
    "category": "Machine Learning",
    "definition": "Mô hình sinh phân loại có giám sát dựa trên định lý Bayes với giả định ngây thơ rằng các từ xuất hiện độc lập với nhau có điều kiện theo lớp."
  },
  {
    "term": "Support Vector Machine (SVM)",
    "term_vn": "Máy vector hỗ trợ",
    "chapter": 10,
    "category": "Machine Learning",
    "definition": "Mô hình phân biệt tìm siêu phẳng phân cách tối đa hóa lề (Margin) giữa các lớp dữ liệu trong không gian nhiều chiều."
  },
  {
    "term": "K-Means Clustering",
    "term_vn": "Gom cụm K-Means",
    "chapter": 10,
    "category": "Clustering",
    "definition": "Thuật toán phân cụm không giám sát phân hoạch tập dữ liệu thành K cụm bằng cách gán điểm dữ liệu tới tâm cụm gần nhất và cập nhật lại tâm."
  },
  {
    "term": "Hierarchical Agglomerative Clustering (HAC)",
    "term_vn": "Gom cụm phân cấp tích tụ",
    "chapter": 10,
    "category": "Clustering",
    "definition": "Chiến lược gom cụm từ dưới lên (Bottom-up), khởi đầu mỗi tài liệu là 1 cụm riêng và liên tục hợp nhất các cặp cụm gần nhau nhất."
  },
  {
    "term": "Social Search",
    "term_vn": "Tìm kiếm xã hội",
    "chapter": 11,
    "category": "Social IR",
    "definition": "Hình thức tìm kiếm khai thác mạng lưới quan hệ xã hội, dữ liệu tương tác người dùng, đánh giá, chia sẻ và gắn thẻ cộng đồng."
  },
  {
    "term": "Folksonomy",
    "term_vn": "Phân loại học dân gian",
    "chapter": 11,
    "category": "Social IR",
    "definition": "Hệ thống phân loại nội dung hợp tác mở tạo ra bởi người dùng thông qua việc tự do gắn các thẻ từ khóa (User Tags)."
  },
  {
    "term": "Collaborative Filtering",
    "term_vn": "Lọc cộng tác",
    "chapter": 11,
    "category": "Recommendation",
    "definition": "Phương pháp dự đoán sở thích của người dùng dựa trên việc thu thập sở thích và hành vi của nhiều người dùng tương đồng khác."
  },
  {
    "term": "Term Dependence Model",
    "term_vn": "Mô hình phụ thuộc từ",
    "chapter": 12,
    "category": "Advanced IR",
    "definition": "Mô hình IR vượt qua giả định độc lập từ bằng cách tính điểm cho các cụm từ liền kề (phrases) và các từ xuất hiện gần nhau trong cửa sổ ngữ cảnh."
  },
  {
    "term": "Sequential Dependence Model (SDM)",
    "term_vn": "Mô hình phụ thuộc tuần tự",
    "chapter": 12,
    "category": "Advanced IR",
    "definition": "Biến thể của Markov Random Field kết hợp trọng số giữa: từ đơn lẻ (Single terms), cụm từ chính xác (Exact phrases), và tập từ không theo thứ tự (Unordered windows)."
  },
  {
    "term": "Multimedia IR",
    "term_vn": "Thu hồi thông tin đa phương tiện",
    "chapter": 12,
    "category": "Advanced IR",
    "definition": "Tìm kiếm và truy xuất các dạng dữ liệu phi văn bản như hình ảnh, âm thanh, video bằng các đặc trưng thị giác và âm thanh đa phương thức."
  },
  {
    "term": "Web Spam (Spamdexing)",
    "term_vn": "Thư rác web",
    "chapter": 13,
    "category": "Security",
    "definition": "Hành vi cố ý đánh lừa thuật toán của Search Engine nhằm đưa các trang web chất lượng thấp hoặc lừa đảo lên thứ hạng cao."
  },
  {
    "term": "Cloaking",
    "term_vn": "Che giấu nội dung",
    "chapter": 13,
    "category": "Security",
    "definition": "Kỹ thuật spam web trả về nội dung tối ưu cho robot của Search Engine nhưng hiển thị nội dung hoàn toàn khác cho người dùng thực."
  },
  {
    "term": "Link Farm",
    "term_vn": "Trang trại liên kết",
    "chapter": 13,
    "category": "Security",
    "definition": "Mạng lưới các website nhân tạo liên kết chéo chằng chịt nhằm thao túng điểm PageRank của Search Engine."
  },
  {
    "term": "TrustRank",
    "term_vn": "Thuật toán độ tin cậy TrustRank",
    "chapter": 13,
    "category": "Security",
    "definition": "Thuật toán lan truyền độ tin cậy từ tập hạt giống được kiểm duyệt thủ công nhằm phân biệt giữa website uy tín và trang web spam."
  },
  {
    "term": "Spam Mass",
    "term_vn": "Khối lượng spam liên kết",
    "chapter": 13,
    "category": "Security",
    "definition": "Độ đo tỷ lệ điểm PageRank của một trang được đóng góp bất hợp pháp từ các trang web rác không đáng tin cậy."
  },
  {
    "term": "PageRank",
    "term_vn": "Thuật toán PageRank",
    "chapter": 14,
    "category": "Link Analysis",
    "definition": "Thuật toán phân tích liên kết của Google tính toán tầm quan trọng khách quan của trang web dựa trên cấu trúc liên kết toàn cầu của Web."
  },
  {
    "term": "Damping Factor (d)",
    "term_vn": "Hệ số suy giảm / cản",
    "chapter": 14,
    "category": "Link Analysis",
    "definition": "Xác suất người lướt web ngẫu nhiên tiếp tục nhấp vào liên kết trên trang hiện tại thay vì nhảy ngẫu nhiên sang trang khác (thường chọn d = 0.85)."
  },
  {
    "term": "HITS (Hubs and Authorities)",
    "term_vn": "Thuật toán HITS",
    "chapter": 14,
    "category": "Link Analysis",
    "definition": "Thuật toán phân tích liên kết phụ thuộc truy vấn của Kleinberg phân biệt giữa trang tổng hợp liên kết (Hub) và trang chuyên gia (Authority)."
  },
  {
    "term": "Bow-tie Structure",
    "term_vn": "Cấu trúc nơ bướm của Web",
    "chapter": 14,
    "category": "Link Analysis",
    "definition": "Mô hình cấu trúc vĩ mô của đồ thị Web phân chia thành: SCC (lõi trung tâm), thành phần IN, thành phần OUT, Tubes, Tendrils, và Disconnected."
  },
  {
    "term": "Document Partitioning (Sharding)",
    "term_vn": "Phân hoạch theo tài liệu",
    "chapter": 15,
    "category": "Distributed Systems",
    "definition": "Kiến trúc phân tán chia nhỏ kho tài liệu ra các máy chủ Shard, mỗi Shard duy trì một Local Inverted Index hoàn chỉnh."
  },
  {
    "term": "Term Partitioning",
    "term_vn": "Phân hoạch theo thuật ngữ",
    "chapter": 15,
    "category": "Distributed Systems",
    "definition": "Kiến trúc phân tán chia nhỏ từ điển thuật ngữ ra các máy chủ, mỗi máy chủ quản lý toàn bộ danh sách posting của các từ được phân công."
  },
  {
    "term": "MapReduce for Indexing",
    "term_vn": "MapReduce cho lập chỉ mục",
    "chapter": 15,
    "category": "Distributed Systems",
    "definition": "Mô hình lập trình phân tán xử lý song song khổng lồ chia thành Map (tách từ và sinh cặp khóa-giá trị) và Reduce (đảo và nén postings)."
  },
  {
    "term": "Multi-tier Caching",
    "term_vn": "Bộ đệm nhiều tầng",
    "chapter": 15,
    "category": "Distributed Systems",
    "definition": "Hệ thống lưu trữ đệm phân cấp kết hợp Result Cache, Postings List Cache và Document Score Cache để giảm tải I/O và giảm độ trễ truy vấn."
  },
  {
    "term": "Learning to Rank (LTR)",
    "term_vn": "Học để xếp hạng",
    "chapter": 16,
    "category": "Machine Learning",
    "definition": "Ứng dụng các thuật toán Machine Learning có giám sát để tự động tối ưu hóa hàm tính điểm xếp hạng từ vector đặc trưng phong phú."
  },
  {
    "term": "Pairwise Ranking",
    "term_vn": "Xếp hạng theo cặp",
    "chapter": 16,
    "category": "Machine Learning",
    "definition": "Tiếp cận LTR mô hình hóa bài toán thành phân loại nhị phân trên từng cặp tài liệu để xác định tài liệu nào có độ liên quan cao hơn."
  },
  {
    "term": "LambdaMART",
    "term_vn": "Thuật toán LambdaMART",
    "chapter": 16,
    "category": "Machine Learning",
    "definition": "Thuật toán LTR đỉnh cao kết hợp cây quyết định tăng cường độ dốc (GBDT) với các gradient lambda tối ưu trực tiếp chỉ số NDCG."
  },
  {
    "term": "Deep Relevance Matching Model (DRMM)",
    "term_vn": "Mô hình khớp độ liên quan sâu",
    "chapter": 16,
    "category": "Deep Learning",
    "definition": "Kiến trúc mạng nơ-ron học sâu tập trung vào tương tác trực tiếp giữa các từ trong truy vấn và tài liệu thông qua ma trận tương tác và histogram."
  },
  {
    "term": "Dense Retrieval",
    "term_vn": "Truy xuất vector mật độ cao",
    "chapter": 17,
    "category": "Neural IR",
    "definition": "Phương pháp tìm kiếm biểu diễn truy vấn và văn bản dưới dạng các vector nhúng liên tục dày đặc và tìm kiếm dựa trên độ tương đồng không gian vector."
  },
  {
    "term": "Bi-Encoder (Dual Encoder / DPR)",
    "term_vn": "Mô hình hai nhánh mã hóa",
    "chapter": 17,
    "category": "Neural IR",
    "definition": "Kiến trúc mã hóa độc lập truy vấn và tài liệu thành 2 vector riêng biệt, cho phép đánh chỉ mục trước offline và tìm kiếm cực nhanh."
  },
  {
    "term": "Cross-Encoder Reranker",
    "term_vn": "Mô hình tái xếp hạng chéo",
    "chapter": 17,
    "category": "Neural IR",
    "definition": "Mô hình đưa đồng thời cả truy vấn và tài liệu qua toàn bộ các lớp Transformer Self-Attention để đạt độ chính xác tối đa tại tầng tái xếp hạng."
  },
  {
    "term": "ColBERT (Late Interaction)",
    "term_vn": "Tương tác muộn ColBERT",
    "chapter": 17,
    "category": "Neural IR",
    "definition": "Kiến trúc nơ-ron bảo lưu vector nhúng của từng token và áp dụng toán tử MaxSim ở bước cuối cùng để vừa đạt độ chính xác cao vừa có tốc độ vượt trội."
  },
  {
    "term": "Hierarchical Navigable Small World (HNSW)",
    "term_vn": "Đồ thị thế giới nhỏ nhiều tầng HNSW",
    "chapter": 17,
    "category": "Vector Search",
    "definition": "Cấu trúc dữ liệu đồ thị phân tầng dùng cho tìm kiếm vector láng giềng gần nhất xấp xỉ (ANN) nhanh nhất hiện nay trong các Vector DB."
  },
  {
    "term": "Reciprocal Rank Fusion (RRF)",
    "term_vn": "Hợp nhất nghịch đảo thứ hạng RRF",
    "chapter": 17,
    "category": "Hybrid Search",
    "definition": "Thuật toán kết hợp các danh sách kết quả từ tìm kiếm từ khóa truyền thống (BM25) và tìm kiếm vector (Dense Search) mà không cần chuẩn hóa điểm."
  },
  {
    "term": "Retrieval-Augmented Generation (RAG)",
    "term_vn": "Sinh nội dung tăng cường bằng truy xuất",
    "chapter": 17,
    "category": "Conversational IR",
    "definition": "Kiến trúc kết hợp công cụ tìm kiếm với mô hình ngôn ngữ lớn (LLM) để tổng hợp câu trả lời chính xác, cập nhật và có trích dẫn nguồn gốc tin cậy."
  }
];
