import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Import enrichments from enrichment_defs
from enrichment_defs import build_enrichments

enrichments = build_enrichments()

# Add enrichments for Ch 13, 14, 15, 16, 17 tailored to exact curriculum
ch13_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

ch13_ex = '''<div class="table-responsive reveal-on-scroll">
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

ch14_ex = '''<div class="table-responsive reveal-on-scroll">
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
      <p><em>Kết luận sau vòng 1:</em> Thứ hạng uy tín là $C (0.4750) > A (0.3333) > B (0.1917)$. Trang $C$ xếp cao nhất vì được nhận dòng giá trị liên kết từ cả $A$ và $B$.</p>
    </div>
  </div>
</div>'''
enrichments['14'] = (ch14_diag, ch14_ex)

ch15_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

ch15_ex = '''<div class="table-responsive reveal-on-scroll">
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

ch16_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

ch16_ex = '''<div class="table-responsive reveal-on-scroll">
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
      <div class="math-block">$$C_{ij} = -\log(P_{ij}) = -\ln(0.7685) \approx 0.263$$</div>
      <p><em>Ý nghĩa:</em> Đạo hàm Gradient $\lambda_{ij} = \frac{\partial C_{ij}}{\partial s_i} = P_{ij} - 1 = 0.7685 - 1 = -0.2315$ sẽ kéo tăng điểm số $s_i$ lên và dìm giảm điểm số $s_j$ xuống trong bước lan truyền ngược (Backpropagation) để đảm bảo $d_i$ luôn đứng trên $d_j$.</p>
    </div>
  </div>
</div>'''
enrichments['16'] = (ch16_diag, ch16_ex)

ch17_diag = '''<div class="mermaid-diagram-wrap reveal-on-scroll">
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

ch17_ex = '''<div class="table-responsive reveal-on-scroll">
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

print(f"Total chapters with enrichments: {len(enrichments)}")

# Load knowledge.json
with open('data/knowledge.json', 'r', encoding='utf-8') as f:
    kdata = json.load(f)

for ch_num, (diag, ex) in enrichments.items():
    html = kdata[ch_num]['content_html']
    
    # 1. Insert diagram if present and not already there
    if diag and ('mermaid' in diag):
        # Check if already added
        clean_check = diag.splitlines()[2]
        if clean_check not in html:
            # Insert right after the first <hr class="content-divider" /> or right before section 1
            if '<h2 class="chapter-h2">1.' in html:
                target = '<h2 class="chapter-h2">1.'
                html = html.replace(target, diag + '\n' + target, 1)
            elif '<h2 class="chapter-h2">' in html:
                target = '<h2 class="chapter-h2">'
                html = html.replace(target, diag + '\n' + target, 1)
            else:
                html = html + '\n' + diag

    # 2. Insert example/table before References/References Heading or at the end
    if ex:
        # Check if already added
        clean_ex_check = ex.splitlines()[2]
        if clean_ex_check not in html:
            if '<div class="references-section' in html:
                target = '<div class="references-section'
                html = html.replace(target, ex + '\n' + target, 1)
            elif '<h2 class="chapter-h2">Tài liệu tham khảo' in html:
                target = '<h2 class="chapter-h2">Tài liệu tham khảo'
                html = html.replace(target, ex + '\n' + target, 1)
            else:
                html = html + '\n' + ex

    kdata[ch_num]['content_html'] = html
    print(f"Chapter {ch_num} enriched. New length: {len(html)}")

# Write updated knowledge.json
with open('data/knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(kdata, f, ensure_ascii=False, indent=2)

# Write updated knowledge.js
with open('data/knowledge.js', 'w', encoding='utf-8') as f:
    f.write('// Auto-generated knowledge database for SEG301 Exam Prep Portal\n')
    f.write('window.SEG_KNOWLEDGE = ')
    json.dump(kdata, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("All chapters successfully enriched in knowledge.json and knowledge.js!")
