# English 7 – Mid-term Revision (Streamlit + Supabase)

Ứng dụng ôn tập trực tuyến dựa trên `REVISION giữa hk1.docx`.

## Nội dung
- 49 câu trắc nghiệm và 16 câu viết/sắp xếp câu.
- Chấm điểm tự động, hiển thị đáp án sau khi nộp.
- Học sinh nhập họ tên và lớp.
- Có thể làm nhiều lần; mỗi lần nộp được lưu thành một lượt riêng trên cơ sở dữ liệu trực tuyến Supabase.
- Không cần tạo Service Account hoặc khóa JSON của Google Cloud.

## 1. Đưa mã nguồn lên GitHub
1. Tải và giải nén `english7_streamlit_complete.zip`.
2. Tạo repository mới trên GitHub, ví dụ `english7-midterm-revision`.
3. Upload các file `app.py`, `requirements.txt`, `README.md`, `secrets.toml.example`, `supabase_setup.sql`.
4. Không upload khóa bí mật thật hoặc file Secrets có thông tin thật.

## 2. Tạo cơ sở dữ liệu Supabase
1. Mở https://supabase.com/ và đăng ký/đăng nhập. Có thể đăng nhập bằng GitHub.
2. Chọn **New project**, đặt tên ví dụ `english7-results`, tạo mật khẩu database mạnh và lưu ở nơi an toàn.
3. Chờ dự án được tạo xong.
4. Trong dự án, mở **SQL Editor** → **New query**.
5. Mở file `supabase_setup.sql` trong gói tải về, sao chép toàn bộ nội dung vào SQL Editor rồi nhấn **Run**. Thao tác này tạo bảng `english7_results` để lưu kết quả.
6. Vào **Project Settings** → **API** (hoặc mục **Connect/API Keys**, tùy giao diện hiện tại). Sao chép **Project URL**.
7. Lấy khóa bí mật phía máy chủ (**Secret key**, hoặc `service_role` trong giao diện khóa cũ). Chỉ dùng khóa này ở phía máy chủ Streamlit; tuyệt đối không đưa vào mã nguồn công khai, không gửi cho học sinh và không đăng ảnh chụp chứa khóa. Khóa này có quyền cao, nên chỉ lưu trong Streamlit Secrets.

## 3. Triển khai trên Streamlit Community Cloud
1. Mở https://share.streamlit.io/ và đăng nhập bằng GitHub.
2. Chọn **Create app**, chọn repository, branch `main` và main file path `app.py`, rồi nhấn **Deploy**.
3. Khi ứng dụng đã tạo, mở **App settings / Settings → Secrets**.
4. Dán cấu trúc dưới đây và thay bằng thông tin thật từ Supabase:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_SECRET_KEY"
```

5. Nhấn **Save**; khởi động lại ứng dụng nếu được yêu cầu.

## 4. Kiểm tra lưu điểm
1. Mở website của ứng dụng.
2. Nhập họ tên và lớp, làm thử vài câu rồi nhấn **NỘP BÀI VÀ CHẤM ĐIỂM**.
3. Màn hình cần báo đã lưu lượt làm vào cơ sở dữ liệu trực tuyến.
4. Trở lại Supabase → **Table Editor** → `english7_results`. Kiểm tra có dòng mới với tên học sinh, lớp, điểm và thời gian.
5. Thử nộp lần thứ hai; hệ thống sẽ lưu thêm một dòng mới.

## Bảo mật quan trọng
- Không commit `SUPABASE_KEY` vào GitHub.
- Không chia sẻ khóa bí mật hoặc ảnh chụp có khóa.
- Bảng có bật Row Level Security. Ứng dụng ghi dữ liệu từ phía máy chủ bằng khóa bí mật được cất trong Streamlit Secrets. Không sử dụng khóa bí mật trong mã chạy ở trình duyệt.
- Chỉ thu thập thông tin học sinh cần thiết (họ tên, lớp và kết quả); giới hạn quyền truy cập dự án cho người có trách nhiệm.

## Lưu ý về đáp án
- Câu phát âm số 17 của Revision 1 được đánh dấu cần rà soát vì định dạng gạch chân trong file gốc có thể không được thể hiện đầy đủ qua trích xuất văn bản.
- Phần viết được chấm bằng so khớp đáp án mẫu sau khi chuẩn hóa chữ hoa/thường, khoảng trắng và dấu câu. Câu đúng nhưng có cách diễn đạt khác có thể bị tính sai; giáo viên nên rà soát trước khi dùng chính thức.