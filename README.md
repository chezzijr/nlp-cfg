# Xử lý ngôn ngữ tự nhiên - Văn phạm phi ngữ cảnh
Tính năng:
- Ngữ pháp tiếng Việt
- Sinh câu ngẫu nhiên
- Phân tích cấu trúc câu của câu dựa trên ngữ pháp cho trước

### Thư mục
- `data/`: chứa dữ liệu
    + `corpus.txt`: các câu ví dụ, dùng để tạo bigram model
    + `data.yaml`: từ điển, lấy từ [underthesea](https://github.com/undertheseanlp/underthesea)
    + `dict_obj.pkl`: dictionary object được serialized, phục vụ việc load từ điển nhanh hơn
- `input/`: dữ liệu đầu vào
    + `sentences.txt`: mỗi dòng chứa 1 câu để phân tích thành cây văn phạm
- `models/`:
    + `bigram.pkl`: model bigram
- `output/`:
    + `grammar.txt`: văn phạm mặc định
    + `parsed-result.txt`: cây văn phạm được phân tích từ `input/`
    + `samples.txt`: câu ngẫu nhiên, lên đến 10_000 câu

### Ngữ pháp tiếng Việt
Ngữ pháp tiếng Việt được tạo từ các thành phần đơn giản, ví dụ như:
- Trạng ngữ
- Chủ ngữ
- Vị ngữ
- Danh ngữ: là danh từ, cụm danh từ
- Đối tượng (của một hành động): có thể là danh ngữ, đại từ thay thế
- Hành động: là động từ, cụm động từ

Ngoài ra ta có các từ loại:
- noun: danh từ
- verb: động từ
- adjective: tính từ
- adverb: trạng từ
- preposition: giới từ
- numeral: số từ
- determiner: lượng từ
- conjunction: liên từ

### Sinh câu ngẫu nhiên
Giải thuật:
- Dựa trên văn phạm, ta sinh ra cấu trúc câu
    + Biểu diễn văn phạm bằng đồ thị có hướng và có chu trình (Cyclic directed graph)
    + Các node trong graph chia làm hai loại, có thể phân tách ra symbol khác (có edge đi ra, gọi là loại 1) và không thể (không có edge đi ra, gọi là loại 2)
    + Cấu trúc câu là danh sách các từ loại, là loại 2
    + Do có chu trình nên khi sinh câu sẽ có tham số depth, phòng việc bị đệ quy vô tận
    + Trong depth cho phép, ta sẽ phân tách node ngẫu nhiên
    + Khi đã đạt đến depth nhất định, ta sẽ phân tách các node loại 1 còn lại thành loại 2
- Sau khi có cấu trúc câu, ta sẽ sinh câu dựa trên mô hình bigram:
    + Ta phân tích các câu trong dataset (bao gồm định nghĩa từ điển, ví dụ từ điển và corpus cho trước) để tạo mô hình bigram
    + Mô hình bigram sẽ chứa 2 danh sách xác suất: xác suất từ xuất hiện trong dataset và xác suất từ xuất hiện dựa trên từ ở trước
    + Trong trường hợp này, xác suất lần lượt là $P(w)$ và $P(w_{i} | w_{i-1})$
    + Đối với từ đầu tiên, ta sẽ dựa trên xác suất từ xuất hiện mà chọn ngẫu nhiên dựa trên trọng số $w = P(w)$
    + Đối với các từ sau, ta sẽ lọc ra các từ mà có từ loại đúng theo cấu trúc đã sinh ra trước đó, tính lại xác suất: $P'(w_{j} | w_{i - 1}) = \frac{P(w_{j} | w_{i - 1})}{\sum_{j=1}^{} P(w_{j} | w_{i - 1})}$
    + Trong đó, $w_{i}$ là từ ở vị trí $i$, $w_{j}$ là từ đã được phân tích trong corpus đứng sau $w_{i}$ và có tỉ lệ $P(w_{j} | w_{i - 1}) \gt 0$
    + Ta chọn ngẫu nhiên dựa trên trọng số $w = P'(w_{j} | w_{i - 1})$

### Phân tích cấu trúc câu
- Ta phân tích cấu trúc câu dựa trên Top Down Chart Parsing algorithm
- Trong hiện thực ta sử dụng thư viện có sẵn [nltk](https://www.nltk.org/)
