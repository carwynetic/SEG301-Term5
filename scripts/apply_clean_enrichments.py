import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Build all enrichments using strictly raw strings (r'''...''')
enrichments = {}

# -------------------------------------------------------------
# CHAPTER 1 ENRICHMENT
# -------------------------------------------------------------
ch1_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ QUY TRÌNH HỆ THỐNG</span>
    <span class="mermaid-subtext">Vòng lặp Thu hồi Thông tin Kinh điển (Classic IR Loop)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    User["Người dùng (User) có Nhu cầu thông tin (Information Need)"] --> Q["Diễn đạt thành Truy vấn (Query Formulation)"]
    Q --> IR["Hệ thống Thu hồi Thông tin (IR System / Search Engine)"]
    Docs[("Tập tài liệu số (Document Collection)")] --> IR
    IR --> Match["Mô hình So khớp & Xếp hạng (Matching & Ranking Model)"]
    Match --> Results["Danh sách tài liệu xếp hạng (Ranked Results)"]
    Results --> Eval["Người dùng đánh giá kết quả (Relevance Judgment)"]
    Eval -->|"Thỏa mãn nhu cầu"| Done["Hoàn thành phiên tìm kiếm"]
    Eval -->|"Chưa thỏa mãn: Điều chỉnh câu truy vấn"| Q
  </pre>
</div>'''

ch1_ex = r'''<div class="example-box reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-lightbulb"></i> VÍ DỤ THỰC TẾ SO SÁNH TRUY VẤN</span>
    <span class="figure-subtext">Minh họa trực quan sự khác biệt cốt lõi giữa IR và DBMS</span>
  </div>
  <div class="example-title">Tình huống: Người dùng tìm kiếm sản phẩm "giày thể thao đi bộ êm chân giá rẻ dưới 1 triệu"</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Xử lý trong Hệ quản trị Cơ sở dữ liệu (DBMS - SQL):</strong>
      <p>Truy vấn SQL dạng khớp chính xác: <code class="inline-code">SELECT * FROM Products WHERE Description LIKE '%giày thể thao%' AND Price &lt; 1000000;</code></p>
      <p><em>Hạn chế của DBMS:</em> Nếu người bán đăng mô tả là "sneaker dạo phố siêu nhẹ êm ái", câu lệnh SQL sẽ trả về <strong>0 kết quả (Zero match)</strong> vì không chứa đúng cụm từ "giày thể thao". DBMS không hiểu từ đồng nghĩa và không xếp hạng độ liên quan ngữ nghĩa.</p>
    </div>
    <div class="example-step">
      <strong>2. Xử lý trong Hệ thống Thu hồi Thông tin (IR / Search Engine):</strong>
      <p>Truy vấn tự nhiên: <code class="inline-code">giày thể thao đi bộ êm chân giá rẻ</code></p>
      <p><em>Ưu thế vượt trội của IR:</em> Hệ thống phân tích từ vựng, loại bỏ từ dừng, mở rộng từ đồng nghĩa ("giày" $\approx$ "sneaker", "êm chân" $\approx$ "đệm khí / foam"). Áp dụng mô hình BM25/VSM tính điểm liên quan, trả về danh sách 10 sản phẩm tốt nhất được xếp từ cao xuống thấp kèm đoạn trích tóm tắt (snippet) làm nổi bật từ khóa.</p>
    </div>
  </div>
</div>'''
enrichments['1'] = (ch1_diag, ch1_ex)

# -------------------------------------------------------------
# CHAPTER 2 ENRICHMENT
# -------------------------------------------------------------
ch2_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> VÍ DỤ TÍNH TOÁN & SO SÁNH CƠ CHẾ</span>
    <span class="figure-subtext">Minh họa chi tiết cơ chế duyệt Posting List: DAAT vs TAAT</span>
  </div>
  <div class="example-title">Bài toán: Xử lý truy vấn kết hợp 2 từ khóa $Q = \{\text{cloud}, \text{security}\}$ trên 4 văn bản $D_1, D_2, D_3, D_4$</div>
  <div class="example-body">
    <p>Giả sử danh sách chỉ mục ngược (Posting Lists) có cấu trúc:</p>
    <div class="example-step">
      <code class="inline-code">cloud:</code> $[(D_1, \text{score}=2.0), (D_2, \text{score}=1.5), (D_4, \text{score}=3.0)]$
      <br/><code class="inline-code">security:</code> $[(D_1, \text{score}=1.0), (D_3, \text{score}=2.5), (D_4, \text{score}=2.0)]$
    </div>
    <div class="example-step">
      <strong>Cách xử lý của DAAT (Document-At-A-Time):</strong>
      <p>Mở đồng thời con trỏ trên cả 2 posting lists. Duyệt song song theo thứ tự docID tăng dần:</p>
      <ul>
        <li>Tài liệu $D_1$: có trong cả 2 list $\implies \text{Score}(D_1) = 2.0 + 1.0 = 3.0$. Đưa vào Min-Heap kích thước $K=2$.</li>
        <li>Tài liệu $D_2$: chỉ có trong "cloud" $\implies \text{Score}(D_2) = 1.5$.</li>
        <li>Tài liệu $D_3$: chỉ có trong "security" $\implies \text{Score}(D_3) = 2.5$.</li>
        <li>Tài liệu $D_4$: có trong cả 2 list $\implies \text{Score}(D_4) = 3.0 + 2.0 = 5.0$. Đưa vào Heap.</li>
      </ul>
      <p><em>Bộ nhớ RAM:</em> Chỉ cần lưu một Min-Heap kích thước $K$ (rất nhỏ, ví dụ $K=10$), không phụ thuộc vào số lượng văn bản của kho dữ liệu.</p>
    </div>
    <div class="example-step">
      <strong>Cách xử lý của TAAT (Term-At-A-Time):</strong>
      <p>Duyệt tuần tự từng term: Đầu tiên duyệt hết list "cloud", ghi điểm tạm thời vào mảng Accumulator: <code class="inline-code">A[1]=2.0, A[2]=1.5, A[4]=3.0</code>. Sau đó duyệt tiếp list "security", cộng dồn: <code class="inline-code">A[1]+=1.0=3.0, A[3]+=2.5, A[4]+=2.0=5.0</code>.</p>
      <p><em>Bộ nhớ RAM:</em> Cần một mảng Accumulator có thể chứa hàng triệu document IDs, tiêu tốn RAM gấp hàng ngàn lần so với DAAT khi kho dữ liệu lớn.</p>
    </div>
  </div>
</div>'''
enrichments['2'] = (None, ch2_ex)

# -------------------------------------------------------------
# CHAPTER 3 ENRICHMENT
# -------------------------------------------------------------
ch3_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN MINH HỌA</span>
    <span class="figure-subtext">Đo lường Độ tươi mới (Freshness) và Tuổi thọ (Age) của Crawler</span>
  </div>
  <div class="example-title">Bài toán: Lập lịch thu thập dữ liệu cho trang tin tức điện tử</div>
  <div class="example-body">
    <p>Một trang web tin tức $S$ cập nhật các bài viết mới theo chu kỳ ngẫu nhiên với tần suất trung bình $\lambda = 0.2$ lần/ngày (tức trung bình 5 ngày có 1 bài cập nhật mới).</p>
    <div class="example-step">
      <strong>1. Tính toán Độ tươi mới (Freshness $F(t)$):</strong>
      <p>Sau khi thu thập, xác suất bản sao lưu trữ tại ngày thứ $t$ vẫn còn trùng khớp với trang gốc được mô hình hóa theo phân phối Poisson:</p>
      <div class="math-block">$$F(t) = e^{-\lambda t} = e^{-0.2 \cdot t}$$</div>
      <p>Nếu crawler quét lại sau $t = 5$ ngày: $F(5) = e^{-0.2 \cdot 5} = e^{-1} \approx 0.368$ (chỉ còn $36.8\%$ xác suất dữ liệu còn mới).</p>
    </div>
    <div class="example-step">
      <strong>2. Giải pháp tối ưu hóa bằng HTTP HEAD Request:</strong>
      <p>Thay vì tải toàn bộ mã HTML (dung lượng trung bình 2 MB), crawler gửi một request nhẹ <code class="inline-code">HEAD /news/article-101.html</code> (chỉ khoảng 300 bytes) để kiểm tra trường header <code class="inline-code">If-Modified-Since</code>. Nếu web server phản hồi mã trạng thái <code class="inline-code">HTTP 304 Not Modified</code>, crawler lập tức bỏ qua và tiết kiệm $99.98\%$ băng thông mạng.</p>
    </div>
  </div>
</div>'''
enrichments['3'] = (None, ch3_ex)

# -------------------------------------------------------------
# CHAPTER 4 ENRICHMENT
# -------------------------------------------------------------
ch4_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN ĐỊNH LUẬT NGÔN NGỮ</span>
    <span class="figure-subtext">Áp dụng Định luật Zipf và Định luật Heaps trong Thiết kế Hệ thống</span>
  </div>
  <div class="example-title">Bài toán: Dự toán dung lượng từ vựng và tần suất từ trong tập ngữ liệu 1.000.000 từ</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Tính tần số xuất hiện theo Định luật Zipf ($r \cdot f(r) \approx C$):</strong>
      <p>Giả sử từ phổ biến nhất ở hạng $r = 1$ (từ "the") xuất hiện với tần suất $f(1) = 80.000$ lần. Hằng số $C = 1 \cdot 80.000 = 80.000$.</p>
      <ul>
        <li>Tần số của từ xếp hạng $r = 2$ ("of"): $f(2) = \frac{80.000}{2} = 40.000$ lần.</li>
        <li>Tần số của từ xếp hạng $r = 10$: $f(10) = \frac{80.000}{10} = 8.000$ lần.</li>
        <li>Tần số của từ xếp hạng $r = 100$: $f(100) = \frac{80.000}{100} = 800$ lần.</li>
      </ul>
      <p><em>Ý nghĩa kỹ thuật:</em> Top $100$ từ phổ biến nhất chiếm hơn $50\%$ tổng số từ xuất hiện trong toàn bộ văn bản (Stopwords). Việc loại bỏ hoặc xử lý riêng stopwords sẽ giúp giảm kích thước index đáng kể.</p>
    </div>
    <div class="example-step">
      <strong>2. Dự toán quy mô từ điển theo Định luật Heaps ($V = k \cdot n^\beta$):</strong>
      <p>Với hệ số thực nghiệm tiếng Anh chuẩn $k = 30$ và $\beta = 0.5$:</p>
      <div class="math-block">$$V = 30 \cdot (1.000.000)^{0.5} = 30 \cdot 1.000 = 30.000\text{ (từ vựng phân biệt)}$$</div>
      <p>Khi kho dữ liệu tăng gấp 4 lần lên $n = 4.000.000$ từ: $V = 30 \cdot (4.000.000)^{0.5} = 30 \cdot 2.000 = 60.000$ từ. Từ điển chỉ tăng gấp đôi chứ không tăng tuyến tính theo số tài liệu.</p>
    </div>
  </div>
</div>

<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Hiện tượng Cắt Gốc Từ (Stemming)</th>
        <th>Ví dụ Cụ thể</th>
        <th>Hậu quả Thực tế trong Tìm kiếm</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Over-stemming</strong> (Cắt quá mức - Gộp nhầm từ khác nghĩa)</td>
        <td><code class="inline-code">"universe"</code> và <code class="inline-code">"university"</code> cùng bị cắt về <code class="inline-code">"univers"</code></td>
        <td>Người tìm kiếm bài báo về "vũ trụ" bị trả về các trang thông tin "trường đại học" (Làm giảm Precision nghiêm trọng).</td>
      </tr>
      <tr>
        <td><strong>Under-stemming</strong> (Cắt chưa tới - Bỏ sót biến thể từ)</td>
        <td><code class="inline-code">"cylinder"</code> và <code class="inline-code">"cylindrical"</code> bị cắt thành 2 gốc khác nhau <code class="inline-code">"cylind"</code> vs <code class="inline-code">"cylindric"</code></td>
        <td>Người tìm kiếm "hình trụ" sẽ bỏ sót các tài liệu chứa tính từ "thuộc về hình trụ" (Làm giảm Recall).</td>
      </tr>
    </tbody>
  </table>
</div>'''
enrichments['4'] = (None, ch4_ex)

# -------------------------------------------------------------
# CHAPTER 5 ENRICHMENT
# -------------------------------------------------------------
ch5_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ CẤU TRÚC CHỈ MỤC</span>
    <span class="mermaid-subtext">Cấu trúc Inverted Index với Danh sách Postings và Con trỏ Skip Pointers</span>
  </div>
  <pre class="mermaid">
flowchart LR
    subgraph Dict["Từ điển Từ khóa (Vocabulary Dictionary)"]
        T1["algorithm (df=3)"]
        T2["search (df=4)"]
    end

    subgraph Postings["Danh sách Postings (Inverted Lists) với Skip Lists"]
        P1["Doc 1: [pos 5]"] --> P2["Doc 4: [pos 12]"]
        P2 --> P3["Doc 9: [pos 1]"]
        
        S1["Doc 2: [pos 3]"] --> S2["Doc 5: [pos 8]"]
        S2 --> S3["Doc 7: [pos 14]"]
        S3 --> S4["Doc 11: [pos 2]"]
    end

    T1 -.-> P1
    T2 -.-> S1
    S1 == "Skip Pointer (+2)" ==> S3
  </pre>
</div>'''

ch5_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN NÉN CHỈ MỤC</span>
    <span class="figure-subtext">Kỹ thuật Nén Khoảng cách (d-gaps) bằng Mã hóa Variable Byte (v-byte)</span>
  </div>
  <div class="example-title">Bài toán: Mã hóa danh sách Document IDs $[100, 105, 120, 950]$ để tiết kiệm bộ nhớ</div>
  <div class="example-body">
    <div class="example-step">
      <strong>Bước 1: Chuyển đổi sang hiệu số khoảng cách (d-gaps):</strong>
      <p>Danh sách docID ban đầu: $[100, 105, 120, 950]$</p>
      <p>Dãy d-gaps (hiệu số liên tiếp): $gap_1 = 100$, $gap_2 = 105 - 100 = 5$, $gap_3 = 120 - 105 = 15$, $gap_4 = 950 - 120 = 830$.</p>
    </div>
    <div class="example-step">
      <strong>Bước 2: Áp dụng thuật toán Variable Byte (v-byte):</strong>
      <p>Mỗi byte gồm 7 bit lưu giá trị và 1 bit dẫn đầu (Continuation bit): bit 1 nghĩa là byte cuối của số, bit 0 nghĩa là còn tiếp tục byte sau.</p>
      <ul>
        <li>Số $5$ (nhỏ hơn 128): nhị phân $7$-bit là <code class="inline-code">0000101</code>. Thêm bit dẫn đầu $1 \implies$ Byte: <code class="inline-code">10000101</code> (1 byte duy nhất).</li>
        <li>Số $15$: nhị phân $7$-bit là <code class="inline-code">0001111</code>. Thêm bit dẫn đầu $1 \implies$ Byte: <code class="inline-code">10001111</code> (1 byte duy nhất).</li>
        <li>Số $830$: do $830 \ge 128$, ta chia theo cơ số 128: $830 = 6 \cdot 128 + 62$. Byte 1 lưu số $6$ (bit dẫn $0 \implies$ <code class="inline-code">00000110</code>), Byte 2 lưu số $62$ (bit dẫn $1 \implies$ <code class="inline-code">10111110</code>). Cần 2 bytes.</li>
      </ul>
      <p><em>Hiệu quả nén:</em> Lưu 4 số nguyên không nén (32-bit integer) mất $4 \cdot 4 = 16$ bytes. Khi dùng v-byte nén d-gaps chỉ mất $1 + 1 + 1 + 2 = 5$ bytes (<strong>tiết kiệm $68.75\%$ dung lượng lưu trữ</strong>).</p>
    </div>
  </div>
</div>'''
enrichments['5'] = (ch5_diag, ch5_ex)

# -------------------------------------------------------------
# CHAPTER 6 ENRICHMENT
# -------------------------------------------------------------
ch6_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ QUY TRÌNH TRUY VẤN</span>
    <span class="mermaid-subtext">Vòng đời Tinh chỉnh Truy vấn và Phản hồi Tương tác (Interactive Query Lifecycle)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    UserQ["Câu truy vấn thô của người dùng (Raw Query)"] --> Pre["Tiền xử lý: Tokenization & Sửa lỗi chính tả (Spell Checking)"]
    Pre --> Exp["Mở rộng truy vấn (Query Expansion: WordNet / Từ đồng nghĩa)"]
    Exp --> Engine["Lõi tìm kiếm xếp hạng (Ranking Engine)"]
    Engine --> Snippet["Trích xuất đoạn trích nổi bật (Dynamic Snippets & Highlighting)"]
    Snippet --> SERP["Trang kết quả tìm kiếm (SERP Display)"]
    SERP --> Feedback["Người dùng nhấp chuột & Đánh giá (Relevance Feedback)"]
    Feedback -->|"Thuật toán Rocchio"| Exp
  </pre>
</div>'''

ch6_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN SỐ HỌC</span>
    <span class="figure-subtext">Thuật toán Phản hồi Độ liên quan Rocchio (Rocchio Relevance Feedback)</span>
  </div>
  <div class="example-title">Bài toán: Cập nhật vector truy vấn dựa trên tài liệu liên quan ($D_r$) và không liên quan ($D_{nr}$)</div>
  <div class="example-body">
    <p>Công thức cập nhật vector truy vấn của Rocchio:</p>
    <div class="math-block">$$\vec{q}_m = \alpha \vec{q}_0 + \frac{\beta}{|D_r|} \sum_{d \in D_r} \vec{d} - \frac{\gamma}{|D_{nr}|} \sum_{d \in D_{nr}} \vec{d}$$</div>
    <div class="example-step">
      <strong>Giả thiết bài toán trong không gian 2 chiều (từ khóa "data", "science"):</strong>
      <ul>
        <li>Vector truy vấn ban đầu: $\vec{q}_0 = (1.0, 0.0)$</li>
        <li>Tập tài liệu được người dùng đánh dấu liên quan ($|D_r| = 1$): $d_1 = (2.0, 2.0)$</li>
        <li>Tập tài liệu không liên quan ($|D_{nr}| = 1$): $d_2 = (0.0, 4.0)$</li>
        <li>Trọng số chuẩn của chuẩn SMART: $\alpha = 1.0$, $\beta = 0.75$, $\gamma = 0.25$</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>Các bước tính toán vector truy vấn mới $\vec{q}_m$:</strong>
      <ul>
        <li>Thành phần gốc: $\alpha \vec{q}_0 = 1.0 \cdot (1.0, 0.0) = (1.0, 0.0)$</li>
        <li>Thành phần tài liệu liên quan: $\frac{\beta}{|D_r|} d_1 = 0.75 \cdot (2.0, 2.0) = (1.5, 1.5)$</li>
        <li>Thành phần tài liệu không liên quan: $\frac{\gamma}{|D_{nr}|} d_2 = 0.25 \cdot (0.0, 4.0) = (0.0, 1.0)$</li>
      </ul>
      <div class="math-block">$$\vec{q}_m = (1.0 + 1.5 - 0.0, 0.0 + 1.5 - 1.0) = (2.5, 0.5)$$</div>
      <p><em>Kết luận:</em> Trọng số của từ "data" tăng vọt từ $1.0$ lên $2.5$, đồng thời từ "science" trước đây chưa có trong query nay được tự động bổ sung với trọng số $0.5$ giúp tìm thêm tài liệu chuẩn xác.</p>
    </div>
  </div>
</div>'''
enrichments['6'] = (ch6_diag, ch6_ex)

# -------------------------------------------------------------
# CHAPTER 7 ENRICHMENT
# -------------------------------------------------------------
ch7_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN ĐIỂM SỐ XẾP HẠNG</span>
    <span class="figure-subtext">Tính toán Chi tiết Điểm Okapi BM25 từng bước</span>
  </div>
  <div class="example-title">Bài toán: Tính điểm BM25 cho tài liệu $D_1$ với câu truy vấn $Q = \{\text{deep}, \text{learning}\}$</div>
  <div class="example-body">
    <p>Công thức BM25 chuẩn:</p>
    <div class="math-block">$$\text{BM25}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D) \cdot (k_1 + 1)}{f(t, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{\text{avgdl}})}$$</div>
    <div class="example-step">
      <strong>Thông số giả định của hệ thống:</strong>
      <ul>
        <li>Tham số tinh chỉnh kinh điển: $k_1 = 1.2$, $b = 0.75$</li>
        <li>Độ dài trung bình văn bản trong kho: $\text{avgdl} = 100$ từ</li>
        <li>Độ dài tài liệu cần chấm điểm: $|D_1| = 80$ từ</li>
        <li>Tần số từ trong $D_1$: $f(\text{"deep"}, D_1) = 3$, $f(\text{"learning"}, D_1) = 1$</li>
        <li>Trọng số nghịch đảo văn bản: $\text{IDF}(\text{"deep"}) = 1.5$, $\text{IDF}(\text{"learning"}) = 2.0$</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>Bước 1: Tính toán hệ số co giãn độ dài mẫu số $K$:</strong>
      <div class="math-block">$$K = k_1 \cdot \left(1 - b + b \cdot \frac{|D_1|}{\text{avgdl}}\right) = 1.2 \cdot \left(1 - 0.75 + 0.75 \cdot \frac{80}{100}\right) = 1.2 \cdot (0.25 + 0.60) = 1.2 \cdot 0.85 = 1.02$$</div>
    </div>
    <div class="example-step">
      <strong>Bước 2: Tính điểm thành phần của từng từ khóa:</strong>
      <ul>
        <li>Với từ "deep": $\text{Score}_{\text{deep}} = 1.5 \cdot \frac{3 \cdot (1.2 + 1)}{3 + 1.02} = 1.5 \cdot \frac{6.6}{4.02} \approx 1.5 \cdot 1.6418 = 2.463$</li>
        <li>Với từ "learning": $\text{Score}_{\text{learning}} = 2.0 \cdot \frac{1 \cdot (1.2 + 1)}{1 + 1.02} = 2.0 \cdot \frac{2.2}{2.02} \approx 2.0 \cdot 1.0891 = 2.178$</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>Bước 3: Tổng điểm BM25 của tài liệu $D_1$:</strong>
      <div class="math-block">$$\text{BM25}(D_1, Q) = 2.463 + 2.178 = 4.641$$</div>
      <p><em>Nhận xét:</em> Do tài liệu $D_1$ ngắn hơn mức trung bình ($80 &lt; 100$), hệ số $K = 1.02 &lt; 1.2$ giúp giảm mẫu số, tạo ra sự thưởng điểm nhẹ cho văn bản ngắn cô đọng.</p>
    </div>
  </div>
</div>'''
enrichments['7'] = (None, ch7_ex)

# -------------------------------------------------------------
# CHAPTER 8 ENRICHMENT
# -------------------------------------------------------------
ch8_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ CHIẾN LƯỢC TỐI ƯU HÓA</span>
    <span class="mermaid-subtext">Tam giác Chiến lược SEO Bền vững (White Hat SEO Architecture)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    SEO["CHIẾN LƯỢC TỔNG THỂ SEO BỀN VỮNG"] --> Tech["1. Technical SEO (Kỹ thuật Nền tảng)"]
    SEO --> OnPage["2. On-Page SEO (Nội dung & Cấu trúc Trang)"]
    SEO --> OffPage["3. Off-Page SEO (Uy tín & Đồ thị Liên kết)"]

    Tech --> T1["Crawlability (robots.txt, XML sitemap)"]
    Tech --> T2["Core Web Vitals & Tốc độ tải trang"]
    Tech --> T3["HTTPS & Thân thiện Di động (Mobile-First)"]

    OnPage --> O1["Tiêu đề thẻ &lt;title&gt; và &lt;meta description&gt;"]
    OnPage --> O2["Phân cấp thẻ đề mục &lt;h1&gt;, &lt;h2&gt;, &lt;h3&gt;"]
    OnPage --> O3["Chất lượng nội dung & Mật độ từ khóa tự nhiên"]

    OffPage --> P1["Backlinks tự nhiên từ tên miền uy tín (Authority)"]
    OffPage --> P2["Đa dạng hóa văn bản neo (Anchor Text Diversity)"]
    OffPage --> P3["Tín hiệu thương hiệu & Trích dẫn xã hội"]
  </pre>
</div>'''

ch8_ex = r'''<div class="example-box code-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-code"></i> VÍ DỤ MÃ NGUỒN SO SÁNH THỰC TẾ</span>
    <span class="figure-subtext">Cấu trúc HTML Chuẩn White Hat SEO vs Hành vi Spam Black Hat Bị Phạt</span>
  </div>
  <div class="example-title">So sánh cấu trúc trang bài viết chuẩn SEO và trang cố tình vi phạm nguyên tắc Google</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Mã nguồn Chuẩn White Hat SEO (Thân thiện với Crawler & Người dùng):</strong>
      <pre class="code-block">&lt;head&gt;
  &lt;title&gt;Khóa Học Lập Trình Python Cơ Bản Cho Người Mới Bắt Đầu | TechEdu&lt;/title&gt;
  &lt;meta name="description" content="Hướng dẫn tự học Python từ con số 0 với bài tập thực hành chi tiết, ví dụ trực quan và lộ trình rõ ràng."&gt;
  &lt;link rel="canonical" href="https://techedu.vn/khoa-hoc-python"&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Lộ Trình Học Python Cơ Bản 2026&lt;/h1&gt;
  &lt;img src="python-flow.png" alt="Sơ đồ tư duy các bước học Python cơ bản"&gt;
&lt;/body&gt;</pre>
    </div>
    <div class="example-step">
      <strong>2. Thủ thuật Black Hat SEO (Keyword Stuffing & Hidden Text) - Google Phạt Nặng:</strong>
      <pre class="code-block">&lt;!-- Nhồi nhét từ khóa ẩn vô hình với người dùng nhưng cố tình lừa bot --&gt;
&lt;div style="display: none; color: #ffffff; background: #ffffff;"&gt;
  học python học python giá rẻ python hay nhất python tốt nhất python uy tín python học python...
&lt;/div&gt;
&lt;!-- Cloaking: Trả về nội dung khoa học cho bot nhưng hiển thị web cờ bạc cho người dùng --&gt;</pre>
      <p><em>Hậu quả:</em> Thuật toán Penguin và SpamBrain của Google tự động phát hiện văn bản ẩn và hạ chỉ số PageRank xuống 0 hoặc xóa hoàn toàn trang khỏi chỉ mục tìm kiếm (De-indexed).</p>
    </div>
  </div>
</div>'''
enrichments['8'] = (ch8_diag, ch8_ex)

# -------------------------------------------------------------
# CHAPTER 9 ENRICHMENT
# -------------------------------------------------------------
ch9_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN ĐỘ CHUẨN XÁC</span>
    <span class="figure-subtext">Tính toán Số học Từng bước Chi tiết: MAP và NDCG</span>
  </div>
  <div class="example-title">Bài toán: Đánh giá chất lượng của thuật toán tìm kiếm trên 2 truy vấn mẫu</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Tính toán Mean Average Precision (MAP):</strong>
      <p>Xét truy vấn $Q_1$ trả về danh sách 5 kết quả với nhãn liên quan (R = Relevant, N = Non-relevant): <code class="inline-code">[R, N, R, N, R]</code></p>
      <ul>
        <li>Vị trí 1 (R): $P@1 = \frac{1}{1} = 1.00$</li>
        <li>Vị trí 3 (R): $P@3 = \frac{2}{3} \approx 0.67$</li>
        <li>Vị trí 5 (R): $P@5 = \frac{3}{5} = 0.60$</li>
        <li>Điểm trung bình $\text{AP}(Q_1) = \frac{1.00 + 0.67 + 0.60}{3} = \frac{2.27}{3} \approx 0.757$</li>
      </ul>
      <p>Xét truy vấn $Q_2$ trả về kết quả: <code class="inline-code">[N, R, N, R, N]</code> (vị trí đúng tại rank 2 và 4):</p>
      <ul>
        <li>Vị trí 2 (R): $P@2 = \frac{1}{2} = 0.50$</li>
        <li>Vị trí 4 (R): $P@4 = \frac{2}{4} = 0.50$</li>
        <li>Điểm $\text{AP}(Q_2) = \frac{0.50 + 0.50}{2} = 0.50$</li>
      </ul>
      <div class="math-block">$$\text{MAP} = \frac{\text{AP}(Q_1) + \text{AP}(Q_2)}{2} = \frac{0.757 + 0.50}{2} = 0.6285\text{ (tức } 62.85\%)$$</div>
    </div>
    <div class="example-step">
      <strong>2. Tính toán Normalized Discounted Cumulative Gain (NDCG@3):</strong>
      <p>Hệ thống trả về 3 tài liệu đầu tiên với điểm liên quan nhiều mức: $r_1 = 3$ (rất liên quan), $r_2 = 2$ (liên quan vừa), $r_3 = 0$ (không liên quan).</p>
      <div class="math-block">$$\text{DCG}@3 = r_1 + \frac{r_2}{\log_2(2)} + \frac{r_3}{\log_2(3)} = 3 + \frac{2}{1} + \frac{0}{1.585} = 3 + 2 = 5.0$$</div>
      <p>Xếp hạng lý tưởng (Ideal DCG - sắp xếp giảm dần theo điểm: $3, 2, 1$):</p>
      <div class="math-block">$$\text{IDCG}@3 = 3 + \frac{2}{\log_2(2)} + \frac{1}{\log_2(3)} = 3 + 2 + \frac{1}{1.585} = 5 + 0.631 = 5.631$$</div>
      <div class="math-block">$$\text{NDCG}@3 = \frac{\text{DCG}@3}{\text{IDCG}@3} = \frac{5.0}{5.631} \approx 0.888\text{ (tức } 88.8\%)$$</div>
    </div>
  </div>
</div>'''
enrichments['9'] = (None, ch9_ex)

# -------------------------------------------------------------
# CHAPTER 10 ENRICHMENT
# -------------------------------------------------------------
ch10_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ THUẬT TOÁN HỌC MÁY</span>
    <span class="mermaid-subtext">Quy trình Vòng lặp Phân cụm K-Means (K-Means Clustering Iteration)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Start["Khởi tạo: Chọn ngẫu nhiên K tâm cụm ban đầu (Centroids mu_1, ..., mu_k)"] --> Dist["Bước 1: Tính khoảng cách Euclidean từ mỗi tài liệu tới K tâm cụm"]
    Dist --> Assign["Bước 2: Gán mỗi tài liệu vào cụm có tâm gần nhất"]
    Assign --> Recompute["Bước 3: Tính toán lại tọa độ trọng tâm mới (Mean coordinates) của từng cụm"]
    Recompute --> Check{"Kiểm tra điều kiện dừng: Tâm cụm có thay đổi không?"}
    Check -->|"Còn thay đổi & Chưa đạt max_iter"| Dist
    Check -->|"Tâm cụm hội tụ (Ổn định)"| Finish["Hoàn thành: Trả về K cụm tài liệu"]
  </pre>
</div>'''

ch10_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN PHÂN LỚP VĂN BẢN</span>
    <span class="figure-subtext">Thuật toán Phân loại Naive Bayes Đầy đủ với Laplace Smoothing</span>
  </div>
  <div class="example-title">Bài toán: Phân loại email mới $d = \text{"free gift"}$ vào lớp $c_1 = \text{Spam}$ hay $c_2 = \text{Ham}$ (Bình thường)</div>
  <div class="example-body">
    <div class="example-step">
      <strong>Tập dữ liệu huấn luyện (Training Set):</strong>
      <ul>
        <li>Số lượng tài liệu: $6$ email Spam ($P(\text{Spam}) = 0.6$), $4$ email Ham ($P(\text{Ham}) = 0.4$)</li>
        <li>Kích thước từ điển toàn hệ thống: $|V| = 50$ từ</li>
        <li>Trong lớp Spam: Tổng số từ là $200$, từ "free" xuất hiện $20$ lần, từ "gift" xuất hiện $10$ lần</li>
        <li>Trong lớp Ham: Tổng số từ là $300$, từ "free" xuất hiện $1$ lần, từ "gift" xuất hiện $0$ lần</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>Áp dụng làm mịn Laplace ($+1$ Smoothing):</strong>
      <div class="math-block">$$P(t | c) = \frac{\text{count}(t, c) + 1}{\sum_{t'} \text{count}(t', c) + |V|}$$</div>
      <ul>
        <li>$P(\text{"free"} | \text{Spam}) = \frac{20 + 1}{200 + 50} = \frac{21}{250} = 0.084$</li>
        <li>$P(\text{"gift"} | \text{Spam}) = \frac{10 + 1}{200 + 50} = \frac{11}{250} = 0.044$</li>
        <li>$P(\text{"free"} | \text{Ham}) = \frac{1 + 1}{300 + 50} = \frac{2}{350} \approx 0.0057$</li>
        <li>$P(\text{"gift"} | \text{Ham}) = \frac{0 + 1}{300 + 50} = \frac{1}{350} \approx 0.00286$</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>So sánh xác suất hậu nghiệm (Posterior Probabilities):</strong>
      <div class="math-block">$$P(\text{Spam} | d) \propto P(\text{Spam}) \cdot P(\text{"free"}| \text{Spam}) \cdot P(\text{"gift"}| \text{Spam}) = 0.6 \cdot 0.084 \cdot 0.044 \approx 0.002217$$</div>
      <div class="math-block">$$P(\text{Ham} | d) \propto P(\text{Ham}) \cdot P(\text{"free"}| \text{Ham}) \cdot P(\text{"gift"}| \text{Ham}) = 0.4 \cdot 0.0057 \cdot 0.00286 \approx 0.0000065$$</div>
      <p><em>Kết luận:</em> Do $P(\text{Spam} | d) \gg P(\text{Ham} | d)$ (gấp hơn 340 lần), bộ phân loại đưa ra quyết định xếp email này vào nhãn <strong>Spam</strong> với độ tin cậy tuyệt đối.</p>
    </div>
  </div>
</div>'''
enrichments['10'] = (ch10_diag, ch10_ex)

# -------------------------------------------------------------
# CHAPTER 11 ENRICHMENT
# -------------------------------------------------------------
ch11_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ SO SÁNH KIẾN TRÚC MẠNG</span>
    <span class="mermaid-subtext">Kiến trúc Tìm kiếm Siêu công cụ (Metasearch) vs Mạng Phân tán Ngang hàng (P2P)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    subgraph Meta["Hệ thống Metasearch (Centralized Broker)"]
        User1["Client"] --> Broker["Query Broker (Bộ điều phối trung tâm)"]
        Broker --> S1["Search Engine A (Google)"]
        Broker --> S2["Search Engine B (Bing)"]
        Broker --> S3["Search Engine C (Yahoo)"]
        S1 --> Merge["Hợp nhất, Lọc trùng & Tái xếp hạng (Merge & Rerank)"]
        S2 --> Merge
        S3 --> Merge
        Merge --> User1
    end

    subgraph P2P["Hệ thống P2P Search (Decentralized Peer-to-Peer)"]
        NodeA["Peer Node A"] <--> NodeB["Peer Node B"]
        NodeB <--> NodeC["Peer Node C"]
        NodeC <--> NodeD["Peer Node D"]
        NodeA <--> NodeD
    end
  </pre>
</div>'''

ch11_ex = r'''<div class="example-box reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-tags"></i> VÍ DỤ THỰC TẾ GẮN THẺ XÃ HỘI</span>
    <span class="figure-subtext">Minh họa 5 Chức năng Gắn thẻ (Tagging Functions) của Golder & Huberman</span>
  </div>
  <div class="example-title">Tình huống: Người dùng đánh dấu trang (bookmark) một bài viết về thuật toán PageRank trên mạng xã hội</div>
  <div class="example-body">
    <p>Người dùng gán các tags: <code class="inline-code">["search-engine", "algorithm", "google", "to-read", "cool", "my-thesis"]</code>. Phân tích chức năng:</p>
    <ul>
      <li><strong>1. Xác định chủ đề (Identifying Topic):</strong> <code class="inline-code">search-engine</code>, <code class="inline-code">algorithm</code> (mô tả nội dung bài viết nói về cái gì).</li>
      <li><strong>2. Xác định loại hình tài nguyên (Identifying What It Is):</strong> <code class="inline-code">article</code>, <code class="inline-code">pdf</code>, <code class="inline-code">tutorial</code> (dạng thức tài liệu).</li>
      <li><strong>3. Xác định quyền sở hữu/tác giả (Identifying Who Owns It):</strong> <code class="inline-code">google</code>, <code class="inline-code">larry-page</code> (nguồn gốc phát hành).</li>
      <li><strong>4. Đánh giá phẩm chất cá nhân (Opinion/Quality):</strong> <code class="inline-code">cool</code>, <code class="inline-code">masterpiece</code>, <code class="inline-code">hard-to-understand</code> (cảm xúc chủ quan).</li>
      <li><strong>5. Quản lý tác vụ bản thân (Self-Reference & Task Organization):</strong> <code class="inline-code">to-read</code>, <code class="inline-code">my-thesis</code>, <code class="inline-code">exam-prep</code> (chỉ có ý nghĩa cá nhân với người gắn thẻ).</li>
    </ul>
  </div>
</div>'''
enrichments['11'] = (ch11_diag, ch11_ex)

# -------------------------------------------------------------
# CHAPTER 12 ENRICHMENT
# -------------------------------------------------------------
ch12_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ MÔ HÌNH NHÚNG TỪ</span>
    <span class="mermaid-subtext">So sánh Kiến trúc Mạng Nơ-ron Word2Vec: CBOW vs Skip-Gram</span>
  </div>
  <pre class="mermaid">
flowchart LR
    subgraph CBOW["Continuous Bag of Words (CBOW)"]
        C1["Từ ngữ cảnh w(t-2)"] --> Sum["Tầng ẩn tổng hợp (Projection Sum)"]
        C2["Từ ngữ cảnh w(t-1)"] --> Sum
        C3["Từ ngữ cảnh w(t+1)"] --> Sum
        C4["Từ ngữ cảnh w(t+2)"] --> Sum
        Sum --> Target["Dự đoán Từ mục tiêu w(t)"]
    end

    subgraph SkipGram["Skip-Gram Model"]
        InputW["Từ trung tâm mục tiêu w(t)"] --> Proj["Tầng ẩn (Projection)"]
        Proj --> Out1["Dự đoán ngữ cảnh w(t-1)"]
        Proj --> Out2["Dự đoán ngữ cảnh w(t+1)"]
    end
  </pre>
</div>'''

ch12_ex = r'''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> VÍ DỤ ĐẠI SỐ VECTOR NGỮ NGHĨA</span>
    <span class="figure-subtext">Phép toán Vector Ngữ nghĩa trong Không gian Nhúng Word Embeddings</span>
  </div>
  <div class="example-title">Minh họa quan hệ đẳng cấu ngữ nghĩa: $\vec{v}(\text{"King"}) - \vec{v}(\text{"Man"}) + \vec{v}(\text{"Woman"}) \approx \vec{v}(\text{"Queen"})$</div>
  <div class="example-body">
    <p>Giả sử các từ được biểu diễn qua vector nhúng 4 chiều tượng trưng cho các thuộc tính tiềm ẩn: <code class="inline-code">[Hoàng tộc, Giới tính Nam, Nữ tính, Quyền lực]</code></p>
    <ul>
      <li>$\vec{v}(\text{"King"}) = [0.95, 0.90, 0.05, 0.90]$</li>
      <li>$\vec{v}(\text{"Man"}) = [0.05, 0.92, 0.08, 0.10]$</li>
      <li>$\vec{v}(\text{"Woman"}) = [0.05, 0.08, 0.92, 0.10]$</li>
    </ul>
    <div class="example-step">
      <strong>Thực hiện phép trừ và cộng vector:</strong>
      <div class="math-block">$$\vec{v}_{\text{result}} = \vec{v}(\text{"King"}) - \vec{v}(\text{"Man"}) + \vec{v}(\text{"Woman"})$$</div>
      <div class="math-block">$$\vec{v}_{\text{result}} = [0.95 - 0.05 + 0.05, 0.90 - 0.92 + 0.08, 0.05 - 0.08 + 0.92, 0.90 - 0.10 + 0.10] = [0.95, 0.06, 0.89, 0.90]$$</div>
      <p>Khi so sánh độ tương đồng Cosine của $\vec{v}_{\text{result}}$ với toàn bộ từ vựng, từ có độ tương đồng cao nhất đạt $98\%$ chính là vector $\vec{v}(\text{"Queen"}) = [0.94, 0.05, 0.91, 0.89]$.</p>
    </div>
  </div>
</div>'''
enrichments['12'] = (ch12_diag, ch12_ex)

# -------------------------------------------------------------
# CHAPTER 13 ENRICHMENT
# -------------------------------------------------------------
ch13_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ PHÂN LOẠI & PHÁT HIỆN WEB SPAM</span>
    <span class="mermaid-subtext">Cơ chế Phân loại Web Spam và Thuật toán TrustRank</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Spam["CÁC HÌNH THỨC WEB SPAM (SPAMDEXING)"] --> Content["1. Content Spam (Spam Nội dung)"]
    Spam --> Link["2. Link Spam (Spam Đồ thị Liên kết)"]
    Spam --> Hiding["3. Kỹ thuật Ẩn giấu (Hiding Techniques)"]

    Content --> C1["Keyword Stuffing & Text vô hình"]
    Content --> C2["Scraped Content (Cào trộm xào xáo nội dung)"]

    Link --> L1["Link Farms (Trang trại liên kết tương hỗ)"]
    Link --> L2["Spam bình luận Blog / Diễn đàn tự động"]

    Hiding --> H1["Cloaking (Tráo đổi nội dung theo User-Agent / IP)"]
    H2["Chuyển hướng lén lút (Sneaky JavaScript / Meta Refresh)"] --> Hiding

    Trust["Thuật toán TrustRank: Lan truyền điểm tin cậy từ tập hạt giống Seed uy tín (.edu, .gov)"] -.->|"Phát hiện và hạ phạt"| Link
  </pre>
</div>'''

ch13_ex = r'''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Kỹ thuật Spam Web</th>
        <th>Hành vi Kỹ thuật Chi tiết</th>
        <th>Cơ chế Phát hiện & Xử phạt của Search Engine</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Keyword Stuffing</strong></td>
        <td>Lặp lại từ khóa mục tiêu hàng trăm lần ở footer hoặc trong thẻ ẩn với kích thước chữ 0px, màu chữ trùng màu nền.</td>
        <td>Phân tích tần suất từ bất thường so với phân phối ngôn ngữ tự nhiên (vượt ngưỡng thông thường của Zipf's Law).</td>
      </tr>
      <tr>
        <td><strong>Link Farms (Trại liên kết)</strong></td>
        <td>Một mạng lưới hàng ngàn website rác tự động trỏ liên kết chéo lẫn nhau nhằm thao túng điểm PageRank.</td>
        <td>Thuật toán TrustRank: Điểm tin cậy từ các hạt giống chất lượng (.edu, .gov) không thể truyền tới mạng lưới rác này.</td>
      </tr>
      <tr>
        <td><strong>Cloaking</strong></td>
        <td>Máy chủ web kiểm tra IP hoặc HTTP User-Agent: Trả về nội dung khoa học chuẩn cho Googlebot, nhưng trả về trang cá cược cho người dùng thật.</td>
        <td>Search Engine dùng nhiều User-Agent giả danh người dùng thông thường từ các dải IP dân cư để so sánh mã nguồn đối chiếu.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-shield-alt"></i> VÍ DỤ PHÂN TÍCH KỸ THUẬT</span>
    <span class="figure-subtext">Cơ chế Hoạt động của Thuật toán TrustRank Chống Link Farm</span>
  </div>
  <div class="example-title">Tình huống: Mạng lưới 500 trang web rác tự trỏ link cho nhau để đẩy PageRank của trang đích $S$</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Lỗ hổng của PageRank truyền thống:</strong>
      <p>Do có 500 trang web vệ tinh liên tục trỏ về, trang đích $S$ nhận được số lượng in-links rất lớn, khiến điểm $PageRank(S)$ bị thổi phồng giả tạo.</p>
    </div>
    <div class="example-step">
      <strong>2. Cách TrustRank vô hiệu hóa Link Farm:</strong>
      <ul>
        <li>Chuyên gia con người chọn ra tập hạt giống gồm 200 tên miền uy tín tuyệt đối (Seed Sites: Harvard.edu, Wikipedia.org, Gov.vn) và gán điểm $Trust = 1.0$.</li>
        <li>Điểm $Trust$ chỉ được truyền đi qua các liên kết ra ngoài kèm hệ số tiêu hao (Damping Factor $\alpha = 0.85$). Càng xa tập hạt giống uy tín, điểm $Trust$ càng tiệm cận 0.</li>
        <li>Do các trang web uy tín không bao giờ trỏ link tới Link Farm, điểm $Trust(S) \approx 0.0$.</li>
      </ul>
      <p><em>Kết luận:</em> Search Engine tính tỷ số $\frac{Trust(S)}{PageRank(S)}$. Nhận thấy tỷ số này cực thấp (PageRank cao nhưng Trust bằng 0), hệ thống tự động gán nhãn <strong>Web Spam</strong> và loại bỏ trang $S$ khỏi kết quả tìm kiếm.</p>
    </div>
  </div>
</div>'''
enrichments['13'] = (ch13_diag, ch13_ex)

# -------------------------------------------------------------
# CHAPTER 14 ENRICHMENT
# -------------------------------------------------------------
ch14_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ ĐỒ THỊ LIÊN KẾT WEB</span>
    <span class="mermaid-subtext">Mô hình Random Surfer và Hiện tượng Dead End / Spider Trap trong PageRank</span>
  </div>
  <pre class="mermaid">
flowchart LR
    A["Trang A"] -->|"L(A)=2"| B["Trang B"]
    A -->|"L(A)=2"| C["Trang C"]
    B -->|"L(B)=1"| C
    C -->|"L(C)=1"| A
    C -.->|"Link ngoài"| D["Trang D (Dead End / Spider Trap)"]
    D -->|"Vòng lặp tự thân"| D

    Teleport["Xác suất Nhảy ngẫu nhiên (Teleportation 1 - d = 0.15)"] -.-> A
    Teleport -.-> B
    Teleport -.-> C
  </pre>
</div>'''

ch14_ex = r'''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Tiêu chí So sánh</th>
        <th>Thuật toán PageRank (Brin & Page, 1998)</th>
        <th>Thuật toán HITS (Jon Kleinberg, 1999)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Thời điểm tính toán</strong></td>
        <td><strong>Query-Independent (Offline):</strong> Tính toán trước trên toàn bộ đồ thị Web, lưu sẵn điểm uy tín của từng trang.</td>
        <td><strong>Query-Dependent (Online):</strong> Chỉ tính toán tại thời điểm người dùng nhập truy vấn trên tập đồ thị mở rộng (Base Set).</td>
      </tr>
      <tr>
        <td><strong>Điểm số đánh giá</strong></td>
        <td><strong>1 điểm số duy nhất:</strong> Thể hiện mức độ quan trọng / uy tín toàn cầu của trang web.</td>
        <td><strong>Cặp điểm số song hành:</strong> Điểm Hub (Trang danh bạ dẫn link tốt) và Điểm Authority (Trang nội dung chuyên môn uy tín).</td>
      </tr>
      <tr>
        <td><strong>Quan hệ củng cố</strong></td>
        <td>Trang web quan trọng nếu được nhiều trang web quan trọng khác trỏ liên kết tới.</td>
        <td>Một trang là Authority tốt nếu được nhiều Hub tốt trỏ tới; một trang là Hub tốt nếu trỏ tới nhiều Authority uy tín.</td>
      </tr>
      <tr>
        <td><strong>Khả năng ứng dụng</strong></td>
        <td>Rất cao, phục vụ hàng chục ngàn truy vấn/giây nhờ tính sẵn offline (Lõi của Google).</td>
        <td>Chậm hơn do phải xây dựng đồ thị con và lặp ma trận online tại thời điểm truy vấn.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN LIÊN KẾT ĐỒ THỊ</span>
    <span class="figure-subtext">Tính toán Số học Vòng lặp PageRank với Hệ số Suy giảm Damping Factor</span>
  </div>
  <div class="example-title">Bài toán: Tính điểm PageRank cho 3 trang web $A, B, C$ sau 1 vòng lặp</div>
  <div class="example-body">
    <p>Công thức tính điểm PageRank với hệ số suy giảm $d = 0.85$ trên mạng gồm $N = 3$ trang web:</p>
    <div class="math-block">$$PR(u) = \frac{1 - d}{N} + d \sum_{v \in B(u)} \frac{PR(v)}{L(v)}$$</div>
    <div class="example-step">
      <strong>Cấu trúc liên kết:</strong>
      <ul>
        <li>Trang $A$ trỏ đến $B$ và $C$ ($L(A) = 2$)</li>
        <li>Trang $B$ chỉ trỏ đến $C$ ($L(B) = 1$)</li>
        <li>Trang $C$ chỉ trỏ về $A$ ($L(C) = 1$)</li>
        <li>Khởi tạo ban đầu: $PR_0(A) = PR_0(B) = PR_0(C) = \frac{1}{3} \approx 0.3333$</li>
        <li>Hệ số ngẫu nhiên tối thiểu: $\frac{1 - 0.85}{3} = \frac{0.15}{3} = 0.05$</li>
      </ul>
    </div>
    <div class="example-step">
      <strong>Vòng lặp 1 ($PR_1$):</strong>
      <ul>
        <li>$PR_1(A) = 0.05 + 0.85 \cdot \left(\frac{PR_0(C)}{L(C)}\right) = 0.05 + 0.85 \cdot \frac{0.3333}{1} = 0.05 + 0.2833 = 0.3333$</li>
        <li>$PR_1(B) = 0.05 + 0.85 \cdot \left(\frac{PR_0(A)}{L(A)}\right) = 0.05 + 0.85 \cdot \frac{0.3333}{2} = 0.05 + 0.1417 = 0.1917$</li>
        <li>$PR_1(C) = 0.05 + 0.85 \cdot \left(\frac{PR_0(A)}{L(A)} + \frac{PR_0(B)}{L(B)}\right) = 0.05 + 0.85 \cdot (0.1667 + 0.3333) = 0.05 + 0.4250 = 0.4750$</li>
      </ul>
      <p><em>Kết luận sau vòng 1:</em> Thứ hạng uy tín là $C (0.4750) &gt; A (0.3333) &gt; B (0.1917)$. Trang $C$ xếp cao nhất vì được nhận dòng giá trị liên kết từ cả $A$ và $B$.</p>
    </div>
  </div>
</div>'''
enrichments['14'] = (ch14_diag, ch14_ex)

# -------------------------------------------------------------
# CHAPTER 15 ENRICHMENT
# -------------------------------------------------------------
ch15_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ HỆ THỐNG TÌM KIẾM PHÂN TÁN</span>
    <span class="mermaid-subtext">Kiến trúc Broker-Worker và Mô hình Document Sharding ở Quy mô Lớn</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Client["Client gửi truy vấn"] --> Broker["Query Broker / Ingestion Node"]
    Broker --> Caching{"Kiểm tra Result Cache?"}
    Caching -->|"Hit (Có sẵn)"| ReturnCached["Trả về kết quả ngay (< 5ms)"]
    Caching -->|"Miss (Chưa có)"| Scatter["Scatter: Phân phối query đồng thời tới các Shards"]

    Scatter --> Shard1["Shard 1 (Docs 1 - 1.000.000)"]
    Scatter --> Shard2["Shard 2 (Docs 1.000.001 - 2.000.000)"]
    Scatter --> Shard3["Shard 3 (Docs 2.000.001 - 3.000.000)"]

    Shard1 -->|"Top-10 cục bộ"| Gather["Gather & Merge: Hợp nhất và Xếp hạng Top-10 Toàn cục"]
    Shard2 -->|"Top-10 cục bộ"| Gather
    Shard3 -->|"Top-10 cục bộ"| Gather

    Gather --> Client
  </pre>
</div>'''

ch15_ex = r'''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Tiêu chí Kỹ thuật</th>
        <th>Phân vùng theo Tài liệu (Document Partitioning / Sharding)</th>
        <th>Phân vùng theo Từ khóa (Term Partitioning)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Cơ chế phân bổ</strong></td>
        <td>Mỗi máy chủ (node) lưu trữ một tập văn bản độc lập và toàn bộ chỉ mục của tập đó.</td>
        <td>Mỗi máy chủ lưu giữ toàn bộ posting list của một nhóm từ vựng cụ thể (e.g. Node 1: A-M, Node 2: N-Z).</td>
      </tr>
      <tr>
        <td><strong>Cơ chế phân tán truy vấn</strong></td>
        <td><strong>Scatter-Gather:</strong> Gửi truy vấn tới tất cả các node song song, mỗi node trả về Top-K cục bộ.</td>
        <td>Chỉ gửi truy vấn tới node phụ trách các từ vựng xuất hiện trong truy vấn.</td>
      </tr>
      <tr>
        <td><strong>Khả năng chịu lỗi (Fault Tolerance)</strong></td>
        <td><strong>Rất cao:</strong> Nếu một node gặp sự cố, hệ thống chỉ mất 1 phần tài liệu, vẫn trả về kết quả bình thường.</td>
        <td><strong>Rủi ro cao:</strong> Nếu node phụ trách từ vựng phổ biến bị sập, toàn bộ các truy vấn chứa từ đó bị lỗi.</td>
      </tr>
      <tr>
        <td><strong>Hiện tượng nghẽn mạng (Hotspots)</strong></td>
        <td>Tải phân bổ đều trên toàn cụm.</td>
        <td>Dễ bị nghẽn mạng nghiêm trọng tại các node chứa từ khóa "hot" (Breaking news, Celebrity).</td>
      </tr>
      <tr>
        <td><strong>Thực tiễn ngành công nghiệp</strong></td>
        <td>Được lựa chọn làm chuẩn mực cho hầu hết các search engine lớn (Google, Elasticsearch, Solr).</td>
        <td>Ít khi sử dụng độc lập, chỉ dùng trong một số bộ nhớ đệm cache tầng thấp.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box code-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-terminal"></i> VÍ DỤ MINH HỌA DÒNG DỮ LIỆU MAPREDUCE</span>
    <span class="figure-subtext">Quá trình Tạo Chỉ mục Ngược qua Map, Shuffle & Sort và Reduce</span>
  </div>
  <div class="example-title">Xử lý 2 tài liệu $D_1: \text{"search engine"}$ và $D_2: \text{"search query"}$</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Giai đoạn Map:</strong>
      <p>Mỗi worker quét văn bản và phát ra các cặp khóa - giá trị $\langle \text{term}, \text{docID} \rangle$:</p>
      <pre class="code-block">Map(docID=1, "search engine") -> [("search", 1), ("engine", 1)]
Map(docID=2, "search query")  -> [("search", 2), ("query", 2)]</pre>
    </div>
    <div class="example-step">
      <strong>2. Giai đoạn Shuffle & Sort:</strong>
      <p>Hệ thống tự động gom các docID có chung term lại thành một danh sách có thứ tự:</p>
      <pre class="code-block">"engine" -> [1]
"query"  -> [2]
"search" -> [1, 2]</pre>
    </div>
    <div class="example-step">
      <strong>3. Giai đoạn Reduce:</strong>
      <p>Hàm Reduce ghi ra đĩa cấu trúc Inverted Index nén hoàn chỉnh:</p>
      <pre class="code-block">Reduce("search", [1, 2]) -> PostingList: term="search", df=2, postings=[(1, tf=1), (2, tf=1)]</pre>
    </div>
  </div>
</div>'''
enrichments['15'] = (ch15_diag, ch15_ex)

# -------------------------------------------------------------
# CHAPTER 16 ENRICHMENT
# -------------------------------------------------------------
ch16_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ BA TRƯỜNG PHÁI LTR</span>
    <span class="mermaid-subtext">Tiến hóa Kiến trúc Học máy Xếp hạng (Learning to Rank Paradigms)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    LTR["LEARNING TO RANK (LTR)"] --> Pointwise["1. Pointwise Approach"]
    LTR --> Pairwise["2. Pairwise Approach"]
    LTR --> Listwise["3. Listwise Approach"]

    Pointwise --> PwDesc["Đầu vào: Từng tài liệu riêng lẻ d_i<br/>Mục tiêu: Hồi quy điểm số / Phân loại nhãn độc lập<br/>Mô hình: PRank, Regression Tree<br/>Hạn chế: Bỏ qua vị trí tương đối giữa các kết quả"]

    Pairwise --> PrDesc["Đầu vào: Cặp 2 tài liệu (d_i, d_j)<br/>Mục tiêu: Tối ưu hóa thứ tự ưu tiên d_i tốt hơn d_j<br/>Mô hình: RankNet, LambdaMART<br/>Ưu điểm: Tương đồng trực tiếp với bài toán xếp hạng"]

    Listwise --> LwDesc["Đầu vào: Toàn bộ danh sách tài liệu cho query Q<br/>Mục tiêu: Tối ưu trực tiếp các chỉ số IR (MAP, NDCG)<br/>Mô hình: ListNet, LambdaRank, SoftRank<br/>Ưu điểm: Phản ánh trung thực nhất trải nghiệm người dùng"]
  </pre>
</div>'''

ch16_ex = r'''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Trường phái LTR</th>
        <th>Đơn vị Dữ liệu Đầu vào</th>
        <th>Hàm Mất mát (Loss Function)</th>
        <th>Thuật toán & Mô hình Tiêu biểu</th>
        <th>Ưu điểm & Nhược điểm Cốt lõi</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Pointwise</strong></td>
        <td>Một văn bản đơn lẻ $(q, d_i)$ cùng nhãn điểm</td>
        <td>Mean Squared Error (MSE), Cross-Entropy</td>
        <td>Linear Regression, PRank, McRank</td>
        <td>Dễ triển khai nhưng không học được thứ tự tương đối giữa các văn bản.</td>
      </tr>
      <tr>
        <td><strong>Pairwise</strong></td>
        <td>Một cặp hai văn bản $(d_i, d_j)$ cho cùng query</td>
        <td>Pairwise Cross-Entropy Loss, Hinge Loss</td>
        <td><strong>RankNet, LambdaMART, RankSVM</strong></td>
        <td>Rất mạnh mẽ trong công nghiệp; giảm bài toán xếp hạng về phân loại nhị phân cặp đôi.</td>
      </tr>
      <tr>
        <td><strong>Listwise</strong></td>
        <td>Toàn bộ danh sách văn bản $D_q$ của một truy vấn</td>
        <td>ListMLE, SoftNDCG, Cross-Entropy trên phân phối xác suất</td>
        <td><strong>ListNet, LambdaRank, AdaRank</strong></td>
        <td>Tối ưu trực tiếp chỉ số NDCG và MAP; độ phức tạp tính toán cao nhất.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN HÀM MẤT MÁT LTR</span>
    <span class="figure-subtext">Tính toán Xác suất Ưu tiên và Hàm mất mát RankNet Pairwise Loss</span>
  </div>
  <div class="example-title">Bài toán: Đánh giá cặp tài liệu $(d_i, d_j)$ với $d_i$ có độ liên quan cao hơn $d_j$ ($d_i \succ d_j$)</div>
  <div class="example-body">
    <div class="example-step">
      <strong>Công thức xác suất mô hình gán $d_i$ xếp trên $d_j$:</strong>
      <p>Giả sử mạng nơ-ron hoặc mô hình cây dự đoán điểm số của 2 tài liệu lần lượt là $s_i = 1.8$ và $s_j = 0.6$. Xác suất theo hàm Logistic Sigmoid:</p>
      <div class="math-block">$$P_{ij} = \frac{1}{1 + e^{-\sigma(s_i - s_j)}}$$</div>
      <p>Với hệ số $\sigma = 1.0$, hiệu số điểm $s_i - s_j = 1.8 - 0.6 = 1.2$:</p>
      <div class="math-block">$$P_{ij} = \frac{1}{1 + e^{-1.2}} = \frac{1}{1 + 0.3012} = \frac{1}{1.3012} \approx 0.7685\text{ (tức } 76.85\%)$$</div>
    </div>
    <div class="example-step">
      <strong>Hàm mất mát Cross-Entropy của cặp:</strong>
      <p>Vì trên thực tế $d_i \succ d_j$ (nhãn chuẩn $\bar{P}_{ij} = 1$):</p>
      <div class="math-block">$$C_{ij} = -\ln(P_{ij}) = -\ln(0.7685) \approx 0.263$$</div>
      <p><em>Ý nghĩa:</em> Đạo hàm Gradient $\lambda_{ij} = \frac{\partial C_{ij}}{\partial s_i} = P_{ij} - 1 = 0.7685 - 1 = -0.2315$ sẽ kéo tăng điểm số $s_i$ lên và dìm giảm điểm số $s_j$ xuống trong bước lan truyền ngược (Backpropagation) để đảm bảo $d_i$ luôn đứng trên $d_j$.</p>
    </div>
  </div>
</div>'''
enrichments['16'] = (ch16_diag, ch16_ex)

# -------------------------------------------------------------
# CHAPTER 17 ENRICHMENT
# -------------------------------------------------------------
ch17_diag = r'''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ KIẾN TRÚC NEURAL IR</span>
    <span class="mermaid-subtext">So sánh Ba Mô hình Bi-Encoder (DPR), Cross-Encoder và ColBERT Late Interaction</span>
  </div>
  <pre class="mermaid">
flowchart TD
    subgraph BiEncoder["1. Bi-Encoder (Dense Passage Retrieval - DPR)"]
        Q1["Query"] --> B1["BERT Query Encoder"] --> VQ["Vector 768d"]
        D1["Document"] --> B2["BERT Doc Encoder"] --> VD["Vector 768d"]
        VQ --> Dot["Dot Product / Cosine (MIPS Index cực nhanh)"]
        VD --> Dot
    end

    subgraph CrossEncoder["2. Cross-Encoder (Reranker Toàn diện)"]
        QD["[CLS] Query [SEP] Document"] --> FullBERT["Full Cross-Attention BERT"]
        FullBERT --> Score["Điểm liên quan trực tiếp (Rất chính xác, tính toán nặng)"]
    end

    subgraph ColBERT_diag["3. ColBERT (Contextualized Late Interaction)"]
        Q3["Query Tokens"] --> BQ3["BERT"] --> TQ["Token Embeddings E_q"]
        D3["Doc Tokens"] --> BD3["BERT"] --> TD["Token Embeddings E_d"]
        TQ --> MaxSim["MaxSim: Mỗi token query lấy max tương đồng rồi cộng tổng"]
        TD --> MaxSim
    end
  </pre>
</div>'''

ch17_ex = r'''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Tiêu chí So sánh</th>
        <th>Truy xuất Từ khóa (Lexical - BM25)</th>
        <th>Truy xuất Vector Mật độ cao (Dense - DPR)</th>
        <th>Hệ thống RAG (Retrieval-Augmented Generation)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Cơ chế biểu diễn</strong></td>
        <td>Sparse Vector (Hàng chục ngàn chiều, dựa trên tần suất từ vựng).</td>
        <td>Dense Vector (Biểu diễn ngữ nghĩa tiềm ẩn, 768 hoặc 1536 chiều).</td>
        <td>Kết hợp Dense Retrieval với Mô hình Ngôn ngữ Lớn (LLM).</td>
      </tr>
      <tr>
        <td><strong>Vấn đề Lệch Từ vựng (Vocabulary Mismatch)</strong></td>
        <td><strong>Bị ảnh hưởng nặng</strong>: Nếu từ đồng nghĩa khác chữ, BM25 chấm 0 điểm.</td>
        <td><strong>Khắc phục triệt để</strong>: "xe hơi" và "ô tô" có vector rất gần nhau.</td>
        <td>Khắc phục hoàn toàn và có khả năng suy luận ngữ cảnh sâu sắc.</td>
      </tr>
      <tr>
        <td><strong>Tốc độ và Tài nguyên</strong></td>
        <td>Cực nhanh (vài ms trên CPU), tốn rất ít RAM/Disk.</td>
        <td>Đòi hỏi Vector DB (Faiss, Milvus, Qdrant) và GPU cho Inference.</td>
        <td>Cần thời gian sinh văn bản của LLM (200ms - 1s).</td>
      </tr>
      <tr>
        <td><strong>Đầu ra trả về</strong></td>
        <td>Danh sách tài liệu / URL xếp hạng.</td>
        <td>Danh sách đoạn văn (Passages) có ngữ nghĩa gần nhất.</td>
        <td>Câu trả lời hoàn chỉnh được tổng hợp mạch lạc kèm nguồn trích dẫn.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> VÍ DỤ MINH HỌA CƠ CHẾ MAXSIM CỦA COLBERT</span>
    <span class="figure-subtext">Cơ chế Tương tác Muộn (Late Interaction) Tối ưu hóa Giữa Tốc độ và Độ chuẩn xác</span>
  </div>
  <div class="example-title">Tình huống: Tính điểm phù hợp giữa câu hỏi $Q$ gồm 2 tokens và đoạn văn $D$ gồm 3 tokens</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Mã hóa độc lập các token embeddings:</strong>
      <p>Query có 2 vector token: $E_q = \{q_1, q_2\}$. Document có 3 vector token: $E_d = \{d_1, d_2, d_3\}$.</p>
    </div>
    <div class="example-step">
      <strong>2. Bảng ma trận độ tương đồng Cosine giữa các cặp token:</strong>
      <div class="table-responsive">
        <table class="content-table" style="margin: 0.5rem 0;">
          <thead>
            <tr>
              <th>Query Token</th>
              <th>Cosine với $d_1$</th>
              <th>Cosine với $d_2$</th>
              <th>Cosine với $d_3$</th>
              <th>MaxSim của Token</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>$q_1$ ("search")</td>
              <td>0.45</td>
              <td><strong>0.88</strong></td>
              <td>0.30</td>
              <td>$\max(0.45, 0.88, 0.30) = \mathbf{0.88}$</td>
            </tr>
            <tr>
              <td>$q_2$ ("engines")</td>
              <td>0.20</td>
              <td>0.35</td>
              <td><strong>0.82</strong></td>
              <td>$\max(0.20, 0.35, 0.82) = \mathbf{0.82}$</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="example-step">
      <strong>3. Điểm số tương tác muộn ColBERT:</strong>
      <div class="math-block">$$\text{Score}(Q, D) = \sum_{i \in Q} \max_{j \in D} (q_i \cdot d_j) = 0.88 + 0.82 = 1.70$$</div>
      <p><em>Ưu điểm vượt trội:</em> Thay vì nén toàn bộ văn bản vào 1 vector duy nhất (làm mất chi tiết như Bi-Encoder), ColBERT giữ lại từng token vector và tính MaxSim cực nhanh trên GPU, đạt độ chính xác tương đương Cross-Encoder với độ trễ thấp hơn hàng chục lần.</p>
    </div>
  </div>
</div>'''
enrichments['17'] = (ch17_diag, ch17_ex)

# Load knowledge.json
with open('data/knowledge.json', 'r', encoding='utf-8') as f:
    kdata = json.load(f)

for ch_num, (diag, ex) in enrichments.items():
    html = kdata[ch_num]['content_html']
    
    # 1. Insert diagram if present
    if diag and ('mermaid' in diag):
        if '<h2 class="chapter-h2">1.' in html:
            target = '<h2 class="chapter-h2">1.'
            html = html.replace(target, diag + '\n' + target, 1)
        elif '<h2 class="chapter-h2">' in html:
            target = '<h2 class="chapter-h2">'
            html = html.replace(target, diag + '\n' + target, 1)
        else:
            html = html + '\n' + diag

    # 2. Insert example/table
    if ex:
        if '<div class="references-section' in html:
            target = '<div class="references-section'
            html = html.replace(target, ex + '\n' + target, 1)
        elif '<h2 class="chapter-h2">Tài liệu tham khảo' in html:
            target = '<h2 class="chapter-h2">Tài liệu tham khảo'
            html = html.replace(target, ex + '\n' + target, 1)
        else:
            html = html + '\n' + ex

    kdata[ch_num]['content_html'] = html
    print(f"Chapter {ch_num} clean enriched. New length: {len(html)}")

# Write updated knowledge.json
with open('data/knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(kdata, f, ensure_ascii=False, indent=2)

# Write updated knowledge.js
with open('data/knowledge.js', 'w', encoding='utf-8') as f:
    f.write('// Auto-generated knowledge database for SEG301 Exam Prep Portal\n')
    f.write('window.SEG_KNOWLEDGE = ')
    json.dump(kdata, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("All chapters successfully cleanly enriched in knowledge.json and knowledge.js!")

