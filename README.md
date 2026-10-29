# English 7 – Mid-term Revision (Streamlit + Google Sheets)

Ứng dụng ôn tập trực tuyến dựa trên `REVISION giữa hk1.docx`.

## Nội dung
- 49 câu trắc nghiệm.
- 16 câu viết/sắp xếp câu.
- Chấm điểm tự động và hiển thị đáp án sau khi nộp.
- Học sinh nhập họ tên và lớp.
- Cho phép làm lại nhiều lần; mỗi lần nộp có mã lượt riêng.
- Lưu từng lượt vào Google Sheets. Nếu chưa cấu hình Sheets hoặc kết nối lỗi, ứng dụng lưu CSV dự phòng (trên Streamlit Cloud, CSV không bền vững qua các lần khởi động lại).

## A. Đưa mã nguồn lên GitHub
1. Tải và giải nén `english7_streamlit_complete.zip`.
2. Tạo repository mới trên GitHub, ví dụ `english7-midterm-revision`.
3. Upload các file `app.py`, `requirements.txt`, `README.md`, `secrets.toml.example`.
4. Không upload khóa Service Account thật hoặc file `secrets.toml` có thông tin bí mật.

## B. Tạo Google Sheet
1. Tạo Google Sheet mới, ví dụ `Ket qua English 7`.
2. Lấy ID từ URL:
   `https://docs.google.com/spreadsheets/d/ID_NAM_O_DAY/edit`
3. Để trống trang tính cũng được; ứng dụng tự tạo tab `KetQua` và dòng tiêu đề.

## C. Tạo Service Account (tóm tắt)
1. Mở Google Cloud Console: https://console.cloud.google.com/
2. Tạo/chọn một project.
3. Trong APIs & Services → Library, bật **Google Sheets API** và **Google Drive API**.
4. Mở IAM & Admin → Service Accounts → Create service account.
5. Tạo key dạng JSON và tải về máy. Giữ file này riêng tư.
6. Mở JSON, sẽ cần các trường như `project_id`, `private_key_id`, `private_key`, `client_email`, `client_id`, `client_x509_cert_url`.
7. Chia sẻ Google Sheet với giá trị `client_email`, cấp quyền **Editor**.

## D. Triển khai trên Streamlit Community Cloud
1. Mở https://share.streamlit.io/ và đăng nhập bằng GitHub.
2. Chọn **Create app**.
3. Chọn repository, branch (thường là `main`) và main file path `app.py`.
4. Nhấn **Deploy**.
5. Khi app đã tạo, vào menu **Manage app / Settings → Secrets** (tên mục có thể thay đổi theo giao diện).
6. Sao chép cấu trúc từ `secrets.toml.example` vào ô Secrets và thay mọi giá trị mẫu bằng giá trị thật từ Google Sheet và Service Account JSON.
7. Lưu Secrets và khởi động lại app.

Ví dụ cấu hình (không sử dụng các giá trị giả dưới đây làm thông tin thật):
```toml
spreadsheet_id = "ID_GOOGLE_SHEET_CUA_BAN"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

**Bảo mật:** không đưa khóa JSON/Secrets vào repository công khai hoặc gửi cho học sinh.

## E. Kiểm tra sau khi triển khai
1. Mở link website như một học sinh.
2. Nhập họ tên và lớp.
3. Làm thử vài câu và nộp bài.
4. Kiểm tra màn hình có điểm và trạng thái “Đã lưu lượt làm vào Google Sheets”.
5. Mở Google Sheet → tab `KetQua`, kiểm tra có một dòng mới.
6. Thử nộp lần thứ hai; cần xuất hiện thêm dòng mới.

## Lưu ý về đáp án
- Câu trắc nghiệm được nhập theo nội dung Word. Câu phát âm số 17 của Revision 1 được đánh dấu cần rà soát vì định dạng gạch chân trong file gốc có thể không được thể hiện đầy đủ qua trích xuất văn bản.
- Phần viết được chấm bằng so khớp đáp án mẫu sau khi chuẩn hóa chữ hoa/thường, khoảng trắng và dấu câu. Câu đúng nhưng có cách diễn đạt khác có thể bị tính sai; giáo viên nên xem đáp án mẫu và có thể bổ sung biến thể trong danh sách `answers` ở `app.py`.
- Ứng dụng lưu đáp án chi tiết dưới dạng JSON trong Google Sheets, cùng điểm và thời gian mỗi lượt làm.
