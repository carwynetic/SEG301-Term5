# Script to enrich knowledge base with visual diagrams, pedagogical calculation examples, and comparison tables
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_enrichments():
    enrichments = {}
    
    # -------------------------------------------------------------
    # CHAPTER 1 ENRICHMENT
    # -------------------------------------------------------------
    ch1_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch1_ex = '''<div class="example-box reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-lightbulb"></i> VÍ DỤ THỰC TẾ SO SÁNH TRUY VẤN</span>
    <span class="figure-subtext">Minh họa trực quan sự khác biệt cốt lõi giữa IR và DBMS</span>
  </div>
  <div class="example-title">Tình huống: Người dùng tìm kiếm sản phẩm "giày thể thao đi bộ êm chân giá rẻ dưới 1 triệu"</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Xử lý trong Hệ quản trị Cơ sở dữ liệu (DBMS - SQL):</strong>
      <p>Truy vấn SQL dạng khớp chính xác: <code class="inline-code">SELECT * FROM Products WHERE Description LIKE '%giày thể thao%' AND Price < 1000000;</code></p>
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
    ch2_ex = '''<div class="example-box math-example reveal-on-scroll">
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
        <li>Tài liệu $D_1$: có trong cả 2 list $\to \text{Score}(D_1) = 2.0 + 1.0 = 3.0$. Đưa vào Min-Heap kích thước $K=2$.</li>
        <li>Tài liệu $D_2$: chỉ có trong "cloud" $\to \text{Score}(D_2) = 1.5$.</li>
        <li>Tài liệu $D_3$: chỉ có trong "security" $\to \text{Score}(D_3) = 2.5$.</li>
        <li>Tài liệu $D_4$: có trong cả 2 list $\to \text{Score}(D_4) = 3.0 + 2.0 = 5.0$. Đưa vào Heap.</li>
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
    ch3_ex = '''<div class="example-box math-example reveal-on-scroll">
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
      <div class="math-block">$$F(t) = e^{-\lambda t} = e^{-0.2 \times t}$$</div>
      <p>Nếu crawler quét lại sau $t = 5$ ngày: $F(5) = e^{-0.2 \times 5} = e^{-1} \approx 0.368$ (chỉ còn $36.8\%$ xác suất dữ liệu còn mới).</p>
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
    ch4_ex = '''<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN ĐỊNH LUẬT NGÔN NGỮ</span>
    <span class="figure-subtext">Áp dụng Định luật Zipf và Định luật Heaps trong Thiết kế Hệ thống</span>
  </div>
  <div class="example-title">Bài toán: Dự toán dung lượng từ vựng và tần suất từ trong tập ngữ liệu 1.000.000 từ</div>
  <div class="example-body">
    <div class="example-step">
      <strong>1. Tính tần số xuất hiện theo Định luật Zipf ($r \times f(r) \approx C$):</strong>
      <p>Giả sử từ phổ biến nhất ở hạng $r = 1$ (từ "the") xuất hiện với tần suất $f(1) = 80.000$ lần. Hằng số $C = 1 \times 80.000 = 80.000$.</p>
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
      <div class="math-block">$$V = 30 \times (1.000.000)^{0.5} = 30 \times 1.000 = 30.000\text{ (từ vựng phân biệt)}$$</div>
      <p>Khi kho dữ liệu tăng gấp 4 lần lên $n = 4.000.000$ từ: $V = 30 \times (4.000.000)^{0.5} = 30 \times 2.000 = 60.000$ từ. Từ điển chỉ tăng gấp đôi chứ không tăng tuyến tính theo số tài liệu.</p>
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
    ch5_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    subgraph Postings["Danh sách Postings (Inverted Lists) với Skip Lists (k=sqrt(L))"]
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

    ch5_ex = '''<div class="example-box math-example reveal-on-scroll">
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
        <li>Số $5$ (nhỏ hơn 128): nhị phân $7$-bit là <code class="inline-code">0000101</code>. Thêm bit dẫn đầu $1 \to$ Byte: <code class="inline-code">10000101</code> (1 byte duy nhất).</li>
        <li>Số $15$: nhị phân $7$-bit là <code class="inline-code">0001111</code>. Thêm bit dẫn đầu $1 \to$ Byte: <code class="inline-code">10001111</code> (1 byte duy nhất).</li>
        <li>Số $830$: do $830 \ge 128$, ta chia theo cơ số 128: $830 = 6 \times 128 + 62$. Byte 1 lưu số $6$ (bit dẫn $0 \to$ <code class="inline-code">00000110</code>), Byte 2 lưu số $62$ (bit dẫn $1 \to$ <code class="inline-code">10111110</code>). Cần 2 bytes.</li>
      </ul>
      <p><em>Hiệu quả nén:</em> Lưu 4 số nguyên không nén (32-bit integer) mất $4 \times 4 = 16$ bytes. Khi dùng v-byte nén d-gaps chỉ mất $1 + 1 + 1 + 2 = 5$ bytes (<strong>tiết kiệm $68.75\%$ dung lượng lưu trữ</strong>).</p>
    </div>
  </div>
</div>'''
    enrichments['5'] = (ch5_diag, ch5_ex)

    # -------------------------------------------------------------
    # CHAPTER 6 ENRICHMENT
    # -------------------------------------------------------------
    ch6_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch6_ex = '''<div class="example-box math-example reveal-on-scroll">
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
        <li>Thành phần gốc: $\alpha \vec{q}_0 = 1.0 \times (1.0, 0.0) = (1.0, 0.0)$</li>
        <li>Thành phần tài liệu liên quan: $\frac{\beta}{|D_r|} d_1 = 0.75 \times (2.0, 2.0) = (1.5, 1.5)$</li>
        <li>Thành phần tài liệu không liên quan: $\frac{\gamma}{|D_{nr}|} d_2 = 0.25 \times (0.0, 4.0) = (0.0, 1.0)$</li>
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
    ch7_ex = '''<div class="example-box math-example reveal-on-scroll">
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
      <p><em>Nhận xét:</em> Do tài liệu $D_1$ ngắn hơn mức trung bình ($80 < 100$), hệ số $K = 1.02 < 1.2$ giúp giảm mẫu số, tạo ra sự thưởng điểm nhẹ cho văn bản ngắn cô đọng.</p>
    </div>
  </div>
</div>'''
    enrichments['7'] = (None, ch7_ex)

    # -------------------------------------------------------------
    # CHAPTER 8 ENRICHMENT
    # -------------------------------------------------------------
    ch8_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch8_ex = '''<div class="example-box code-example reveal-on-scroll">
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
    ch9_ex = '''<div class="example-box math-example reveal-on-scroll">
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
    ch10_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch10_ex = '''<div class="example-box math-example reveal-on-scroll">
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
      <div class="math-block">$$P(\text{Spam} | d) \propto P(\text{Spam}) \times P(\text{"free"}| \text{Spam}) \times P(\text{"gift"}| \text{Spam}) = 0.6 \times 0.084 \times 0.044 \approx 0.002217$$</div>
      <div class="math-block">$$P(\text{Ham} | d) \propto P(\text{Ham}) \times P(\text{"free"}| \text{Ham}) \times P(\text{"gift"}| \text{Ham}) = 0.4 \times 0.0057 \times 0.00286 \approx 0.0000065$$</div>
      <p><em>Kết luận:</em> Do $P(\text{Spam} | d) \gg P(\text{Ham} | d)$ (gấp hơn 340 lần), bộ phân loại đưa ra quyết định xếp email này vào nhãn <strong>Spam</strong> với độ tin cậy tuyệt đối.</p>
    </div>
  </div>
</div>'''
    enrichments['10'] = (ch10_diag, ch10_ex)

    # -------------------------------------------------------------
    # CHAPTER 11 ENRICHMENT
    # -------------------------------------------------------------
    ch11_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch11_ex = '''<div class="example-box reveal-on-scroll">
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
    ch12_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch12_ex = '''<div class="example-box math-example reveal-on-scroll">
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
    ch13_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ LUỒNG DỮ LIỆU MAPREDUCE</span>
    <span class="mermaid-subtext">Xây dựng Chỉ mục Ngược Phân tán (Distributed Inverted Index Construction)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Docs["Tập dữ liệu đầu vào (Input Documents)"] --> Split["Chia nhỏ thành các khối (Splits)"]
    Split --> M1["Map Task 1 (Node 1)"]
    Split --> M2["Map Task 2 (Node 2)"]

    M1 -->|"Cặp &lt;term, docID&gt;"| SS["Shuffle & Sort Phase (Gom nhóm theo khóa từ vựng)"]
    M2 -->|"Cặp &lt;term, docID&gt;"| SS

    SS -->|"Danh sách docIDs của term A-M"| R1["Reduce Task 1 (Xây dựng Posting List A-M)"]
    SS -->|"Danh sách docIDs của term N-Z"| R2["Reduce Task 2 (Xây dựng Posting List N-Z)"]

    R1 --> Out[("Inverted Index Hoàn chỉnh Phân tán")]
    R2 --> Out
  </pre>
</div>'''

    ch13_ex = '''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Tiêu chí Đánh giá</th>
        <th>Phân vùng theo Tài liệu (Document Partitioning)</th>
        <th>Phân vùng theo Từ khóa (Term Partitioning)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Cơ chế phân chia</strong></td>
        <td>Mỗi node nắm giữ một tập tài liệu hoàn chỉnh (sub-collection) và toàn bộ từ khóa của các tài liệu đó.</td>
        <td>Mỗi node nắm giữ toàn bộ posting list của một dải từ vựng nhất định (ví dụ Node 1 giữ từ A-M, Node 2 giữ từ N-Z).</td>
      </tr>
      <tr>
        <td><strong>Xử lý truy vấn</strong></td>
        <td>Gửi query tới <strong>tất cả các node</strong>, mỗi node tính Top-K cục bộ, sau đó Broker hợp nhất (Merge).</td>
        <td>Chỉ gửi query tới những node chịu trách nhiệm cho các từ khóa có trong truy vấn.</td>
      </tr>
      <tr>
        <td><strong>Điểm thắt cổ chai (Bottleneck)</strong></td>
        <td>Tải phân bổ đều, chịu lỗi rất tốt (nếu 1 node chết chỉ mất 1 phần tài liệu, hệ thống vẫn phục vụ bình thường).</td>
        <td>Dễ bị nghẽn cổ chai nghiêm trọng tại các node chứa từ khóa phổ biến (Hotspotting - e.g. "tin tức", "bóng đá").</td>
      </tr>
      <tr>
        <td><strong>Ứng dụng thực tế</strong></td>
        <td><strong>Chiếm 95% thực tế</strong> (được Google, Elasticsearch, Solr áp dụng làm chuẩn mặc định).</td>
        <td>Ít dùng đơn lẻ, chỉ kết hợp trong hệ thống đặc thù cần tối ưu băng thông.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box code-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-terminal"></i> VÍ DỤ TRACE DỮ LIỆU MAPREDUCE TỪNG BƯỚC</span>
    <span class="figure-subtext">Truy vết dữ liệu qua các giai đoạn Map, Shuffle và Reduce</span>
  </div>
  <div class="example-title">Tình huống: Tạo index cho 2 tài liệu $D_1: \text{"search engine"}$ và $D_2: \text{"search query"}$</div>
  <div class="example-body">
    <ul>
      <li><strong>Đầu ra hàm Map:</strong>
        <br/><code class="inline-code">Map(D1) -> [("search", 1), ("engine", 1)]</code>
        <br/><code class="inline-code">Map(D2) -> [("search", 2), ("query", 2)]</code>
      </li>
      <li><strong>Giai đoạn Shuffle & Sort:</strong> Gom các giá trị docID có chung key term:
        <br/><code class="inline-code">"engine" -> [1]</code>
        <br/><code class="inline-code">"query"  -> [2]</code>
        <br/><code class="inline-code">"search" -> [1, 2]</code>
      </li>
      <li><strong>Đầu ra hàm Reduce:</strong> Tạo và nén posting list:
        <br/><code class="inline-code">Reduce("search", [1, 2]) -> InvertedList("search", df=2, postings=[(1, tf=1), (2, tf=1)])</code>
      </li>
    </ul>
  </div>
</div>'''
    enrichments['13'] = (ch13_diag, ch13_ex)

    # -------------------------------------------------------------
    # CHAPTER 14 ENRICHMENT
    # -------------------------------------------------------------
    ch14_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

    ch14_ex = '''<div class="example-box math-example reveal-on-scroll">
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
      <p><em>Kết luận sau vòng 1:</em> Thứ hạng uy tín là $C (0.4750) > A (0.3333) > B (0.1917)$. Trang $C$ xếp cao nhất vì được nhận dòng giá trị liên kết từ cả $A$ và $B$.</p>
    </div>
  </div>
</div>'''
    enrichments['14'] = (ch14_diag, ch14_ex)

    # -------------------------------------------------------------
    # CHAPTER 15 ENRICHMENT
    # -------------------------------------------------------------
    ch15_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ CÔNG NGHỆ GỢI Ý</span>
    <span class="mermaid-subtext">Cây Phân loại Hệ thống Gợi ý (Recommender Systems Taxonomy)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Rec["HỆ THỐNG GỢI Ý (RECOMMENDER SYSTEMS)"] --> CF["1. Lọc Cộng Tác (Collaborative Filtering)"]
    Rec --> CB["2. Lọc Theo Nội Dung (Content-Based Filtering)"]
    Rec --> Hybrid["3. Hệ Thống Lai (Hybrid Recommender)"]

    CF --> CF1["User-Based CF: Tìm người dùng có gu tương tự (Peers)"]
    CF --> CF2["Item-Based CF: Tìm sản phẩm thường được mua kèm"]
    CF --> CF3["Matrix Factorization (SVD / Phân rã Ma trận Tiềm ẩn)"]

    CB --> CB1["Hồ sơ sản phẩm (Item Profiles: Đạo diễn, Thể loại, Tác giả)"]
    CB --> CB2["Hồ sơ sở thích người dùng (User Profile Learning)"]

    Hybrid --> H1["Kết hợp trọng số (Weighted / Stacking)"]
  </pre>
</div>'''

    ch15_ex = '''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Người Dùng (User)</th>
        <th>Phim A (Avatar)</th>
        <th>Phim B (Titanic)</th>
        <th>Phim C (Inception)</th>
        <th>Phim D (Interstellar)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>User 1 (Cần gợi ý)</strong></td>
        <td>5 ⭐</td>
        <td>4 ⭐</td>
        <td>5 ⭐</td>
        <td><strong style="color: var(--accent-amber);">? (Cần dự đoán)</strong></td>
      </tr>
      <tr>
        <td><strong>User 2</strong></td>
        <td>5 ⭐</td>
        <td>4 ⭐</td>
        <td>4 ⭐</td>
        <td>5 ⭐</td>
      </tr>
      <tr>
        <td><strong>User 3</strong></td>
        <td>1 ⭐</td>
        <td>2 ⭐</td>
        <td>1 ⭐</td>
        <td>2 ⭐</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box math-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-calculator"></i> BÀI TOÁN TÍNH TOÁN GỢI Ý</span>
    <span class="figure-subtext">Dự đoán Điểm Đánh giá bằng User-Based Collaborative Filtering</span>
  </div>
  <div class="example-title">Bài toán: Dự đoán xem User 1 có thích phim Interstellar (Phim D) không?</div>
  <div class="example-body">
    <div class="example-step">
      <strong>Bước 1: Tính độ tương đồng Cosine giữa User 1 và các User khác trên các phim chung (A, B, C):</strong>
      <p>Vector đánh giá của User 1: $\vec{u}_1 = [5, 4, 5]$</p>
      <p>Vector đánh giá của User 2: $\vec{u}_2 = [5, 4, 4]$</p>
      <div class="math-block">$$\text{Sim}(u_1, u_2) = \frac{5\times 5 + 4\times 4 + 5\times 4}{\sqrt{5^2+4^2+5^2} \times \sqrt{5^2+4^2+4^2}} = \frac{25 + 16 + 20}{\sqrt{66} \times \sqrt{57}} = \frac{61}{8.124 \times 7.550} = \frac{61}{61.33} \approx 0.995$$</div>
      <p>Tương tự với User 3: $\vec{u}_3 = [1, 2, 1] \implies \text{Sim}(u_1, u_3) = \frac{5\times 1 + 4\times 2 + 5\times 1}{\sqrt{66} \times \sqrt{6}} = \frac{18}{8.124 \times 2.449} = \frac{18}{19.90} \approx 0.904$ nhưng User 3 có điểm rating đối lập hoàn toàn.</p>
    </div>
    <div class="example-step">
      <strong>Bước 2: Dự đoán điểm số của User 1 cho Phim D dựa trên User 2 (người có độ tương đồng cực cao 0.995):</strong>
      <p>Vì User 2 cho phim Interstellar 5 ⭐ và có gu xem phim gần như giống hệt User 1 ($\text{Sim} = 0.995$), hệ thống dự đoán User 1 sẽ đánh giá phim Interstellar $\approx 4.9$ ⭐ $\implies$ <strong>Hệ thống tự động hiển thị gợi ý phim Interstellar lên đầu trang chủ của User 1</strong>.</p>
    </div>
  </div>
</div>'''
    enrichments['15'] = (ch15_diag, ch15_ex)

    # -------------------------------------------------------------
    # CHAPTER 16 ENRICHMENT
    # -------------------------------------------------------------
    ch16_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ BẢO MẬT TÌM KIẾM DOANH NGHIỆP</span>
    <span class="mermaid-subtext">Kiến trúc Federated Search với Cơ chế Thực thi Kiểm soát Truy cập (Security ACL Filtering)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    User["Nhân viên gửi truy vấn nội bộ"] --> Auth["Xác thực Danh tính (IAM / LDAP / Active Directory)"]
    Auth --> Broker["Enterprise Query Broker (Bộ điều phối Liên kết)"]

    Broker --> S1["Kho Tài liệu SharePoint"]
    Broker --> S2["Hệ thống Vé Jira / Confluence"]
    Broker --> S3["Cơ sở Dữ liệu Nhân sự / ERP"]

    S1 --> ACL["Bộ Lọc Danh sách Kiểm soát Truy cập (Security ACL Filter)"]
    S2 --> ACL
    S3 --> ACL

    ACL -->|"Loại bỏ tài liệu nhạy cảm nhân viên không được phép xem"| Filtered["Kết quả Đã Lọc Quyền (Authorized Top-K)"]
    Filtered --> User
  </pre>
</div>'''

    ch16_ex = '''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Tiêu chí Phân biệt</th>
        <th>Tìm kiếm Doanh nghiệp (Enterprise Search)</th>
        <th>Tìm kiếm Web Toàn cầu (Web Search)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Bảo mật & Quyền riêng tư</strong></td>
        <td><strong>Cực kỳ nghiêm ngặt (ACL / RBAC)</strong>: Người tìm kiếm chỉ được thấy tài liệu mình được cấp quyền truy cập.</td>
        <td>Hầu hết là công khai, mọi người dùng đều thấy kết quả giống nhau với cùng 1 query.</td>
      </tr>
      <tr>
        <td><strong>Cấu trúc Liên kết (Hyperlinks)</strong></td>
        <td>Hầu như không có siêu liên kết; <strong>không thể áp dụng thuật toán PageRank</strong>.</td>
        <td>Đồ thị liên kết web phong phú; PageRank là yếu tố xếp hạng cốt lõi.</td>
      </tr>
      <tr>
        <td><strong>Định dạng Tài liệu</strong></td>
        <td>Đa dạng và phức tạp: PDF, Word, Excel, Email, AutoCAD, bản ghi Database.</td>
        <td>Chủ yếu là HTML chuẩn hóa, một phần nhỏ PDF và văn bản.</td>
      </tr>
      <tr>
        <td><strong>Hậu quả khi sai sót (Cost of Error)</strong></td>
        <td>Rất cao (lộ bảng lương, bí mật kinh doanh, hoặc không tìm ra hợp đồng pháp lý).</td>
        <td>Thấp hơn; nếu kết quả top 1 chưa trúng, người dùng duyệt tiếp top 2, 3.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box code-example reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-file-code"></i> VÍ DỤ CẤU TRÚC VÀ TRUY VẤN XML/NEXI</span>
    <span class="figure-subtext">Truy vấn Trích xuất Chính xác Cấp độ Phần tử (Element-level Retrieval)</span>
  </div>
  <div class="example-title">Ví dụ cấu trúc bài báo khoa học XML và câu truy vấn theo cấu trúc</div>
  <div class="example-body">
    <pre class="code-block">&lt;article id="art-2026"&gt;
  &lt;title&gt;Machine Learning for Enterprise Search Systems&lt;/title&gt;
  &lt;author&gt;&lt;name&gt;Nguyen Van A&lt;/name&gt;&lt;/author&gt;
  &lt;section name="methods"&gt;
    &lt;p&gt;We apply BM25 and neural reranking over internal knowledge bases...&lt;/p&gt;
  &lt;/section&gt;
&lt;/article&gt;</pre>
    <div class="example-step">
      <strong>Truy vấn XPath / NEXI:</strong> <code class="inline-code">//article[about(., "Enterprise Search")]//section[about(@name, "methods")]</code>
      <p><em>Ý nghĩa:</em> Hệ thống chỉ trả về đúng đoạn văn bản nằm trong thẻ <code class="inline-code">&lt;section name="methods"&gt;</code> thay vì tải về cả tệp tài liệu dài 50 trang, giúp người dùng tiết kiệm tối đa thời gian đọc tài liệu.</p>
    </div>
  </div>
</div>'''
    enrichments['16'] = (ch16_diag, ch16_ex)

    # -------------------------------------------------------------
    # CHAPTER 17 ENRICHMENT
    # -------------------------------------------------------------
    ch17_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
  <div class="mermaid-header">
    <span class="mermaid-badge"><i class="fas fa-project-diagram"></i> SƠ ĐỒ HỆ THỐNG HỎI ĐÁP HIỆN ĐẠI</span>
    <span class="mermaid-subtext">Kiến trúc Hỏi Đáp Tạo Sinh Tăng cường Truy xuất (RAG - Retrieval-Augmented Generation)</span>
  </div>
  <pre class="mermaid">
flowchart TD
    Q["Câu hỏi của người dùng (User Question)"] --> Emb["Embedding Model (Biến câu hỏi thành Vector)"]
    Emb --> VDB[("Cơ sở Dữ liệu Vector (Vector DB / Dense Retrieval)")]
    VDB --> TopK["Trích xuất Top-K đoạn văn ngữ cảnh liên quan nhất (Passages)"]

    Q --> Prompt["Ghép Prompt: Context (Đoạn trích) + Question (Câu hỏi)"]
    TopK --> Prompt

    Prompt --> LLM["Mô hình Ngôn ngữ Lớn (LLM / Generative Model)"]
    LLM --> Answer["Câu trả lời chính xác kèm Nguồn trích dẫn (Grounded Answer with Citations)"]
  </pre>
</div>'''

    ch17_ex = '''<div class="table-responsive reveal-on-scroll">
  <table class="content-table">
    <thead>
      <tr>
        <th>Thế hệ Hệ thống Hỏi Đáp</th>
        <th>Loại Câu hỏi Phù hợp</th>
        <th>Phương pháp Xử lý Cốt lõi</th>
        <th>Đặc điểm Câu trả lời</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Factoid QA (Truyền thống)</strong></td>
        <td>Câu hỏi sự thật ngắn: Ai? Ở đâu? Năm nào?</td>
        <td>Phân loại thực thể mong muốn (Entity Extraction) và trích xuất chuỗi ký tự khớp mẫu.</td>
        <td>Là một từ hoặc cụm thực thể ngắn gọn (e.g. "Hà Nội", "Năm 1998").</td>
      </tr>
      <tr>
        <td><strong>Non-Factoid QA (Giải thích / Hướng dẫn)</strong></td>
        <td>Câu hỏi phức tạp: Tại sao? Làm thế nào?</td>
        <td>Tìm kiếm và xếp hạng đoạn văn (Passage Retrieval) bằng BM25 hoặc Dense Semantic Search.</td>
        <td>Là một đoạn văn bản hoàn chỉnh được trích xuất nguyên văn từ tài liệu gốc.</td>
      </tr>
      <tr>
        <td><strong>RAG (AI Tạo sinh Đương đại)</strong></td>
        <td>Mọi loại câu hỏi, từ tra cứu đến phân tích tổng hợp đa nguồn.</td>
        <td>Truy xuất ngữ cảnh chính xác từ Vector DB rồi dùng LLM tổng hợp và sinh lời thoại tự nhiên.</td>
        <td>Câu trả lời văn phong mạch lạc, chính xác cao, hạn chế tối đa hiện tượng "ảo giác" (Hallucination).</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="example-box reveal-on-scroll">
  <div class="example-header">
    <span class="example-badge"><i class="fas fa-question-circle"></i> VÍ DỤ MINH HỌA TIẾN TRÌNH FACTOID QA</span>
    <span class="figure-subtext">Luồng 3 Bước Trích xuất Câu trả lời Sự thật Kinh điển</span>
  </div>
  <div class="example-title">Câu hỏi: "Thủ đô của nước Úc là thành phố nào?"</div>
  <div class="example-body">
    <div class="example-step">
      <strong>Bước 1: Question Processing & Entity Classification:</strong>
      <p>Phân tích từ nghi vấn: "thành phố nào" $\implies$ Mục tiêu cần trích xuất thuộc kiểu thực thể <code class="inline-code">LOCATION: CITY (Thủ đô)</code>. Từ khóa tìm kiếm: <code class="inline-code">["Thủ đô", "Úc"]</code>.</p>
    </div>
    <div class="example-step">
      <strong>Bước 2: Passage Retrieval (Tìm đoạn văn bản ứng viên):</strong>
      <p>Truy xuất đoạn văn từ Wikipedia: <em>"...Canberra được chọn làm thủ đô của Úc vào năm 1908 như một sự thỏa hiệp giữa hai thành phố lớn nhất là Sydney và Melbourne..."</em></p>
    </div>
    <div class="example-step">
      <strong>Bước 3: Candidate Extraction & Answer Selection:</strong>
      <p>Nhận dạng 3 thực thể thành phố trong đoạn trích: "Canberra", "Sydney", "Melbourne". Dựa vào quan hệ ngữ pháp với từ "thủ đô", hệ thống chọn <strong>Canberra</strong> làm câu trả lời chính xác duy nhất.</p>
    </div>
  </div>
</div>'''
    enrichments['17'] = (ch17_diag, ch17_ex)

    return enrichments

if __name__ == '__main__':
    print("Enrichment definitions loaded successfully!")
