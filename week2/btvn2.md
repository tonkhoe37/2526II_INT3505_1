HTTP Status Code là mã số chuẩn của giao thức HTTP dùng để biểu diễn kết quả xử lý một request giữa Client và Server.

Trong Web Service (đặc biệt là RESTful API), status code đóng vai trò:

- Chuẩn hóa giao tiếp giữa Client – Server
- Truyền tải trạng thái xử lý của request
- Tách biệt rõ trạng thái xử lý (status) và dữ liệu trả về (response body)
- Giúp Client tự quyết định hành vi tiếp theo (retry, sửa request, hiển thị lỗi…)

HTTP Status Code gồm 3 chữ số: XYZ

- X: Nhóm trạng thái
- YZ: Mã cụ thể trong nhóm

Các mã thể hiện lỗi trong HTTP được chia thành 2 nhóm chính:

- Nhóm 4xx – Lỗi phía Client

Bản chất: Request không hợp lệ, Server vẫn hoạt động bình thường. Client có thể sửa và gửi lại.
Thể hiện lỗi xuất phát từ phía gửi request.

Các mã phổ biến:
+400 Bad Request: Sai cú pháp, thiếu field, dữ liệu không hợp lệ
+401 Unauthorized: Chưa xác thực
+403 Forbidden: Không đủ quyền
+404 Not Found: Không tồn tại resource
+405 Method Not Allowed: Sai HTTP method
+409 Conflict: Xung đột dữ liệu
+422 Unprocessable Entity: Sai logic nghiệp vụ

Vai trò:
+Thông báo request không hợp lệ hoặc không đủ điều kiện xử lý
+Giúp Client biết cần chỉnh sửa dữ liệu hoặc quyền truy cập
+Phân định rõ trách nhiệm lỗi thuộc về phía gửi request

- Nhóm 5xx – Lỗi phía Server

Bản chất: Server không xử lý được request. Client không thể tự sửa lỗi.
Thường do bug hệ thống hoặc service phụ trợ gặp sự cố.

Các mã phổ biến:
+500 Internal Server Error: Lỗi hệ thống nội bộ
+502 Bad Gateway: Lỗi service trung gian
+503 Service Unavailable: Server quá tải hoặc bảo trì

Vai trò:
+Thông báo sự cố nội bộ hệ thống
+Cho phép Client quyết định retry hoặc xử lý ngoại lệ
+Phân biệt rõ lỗi hệ thống với lỗi nghiệp vụ

Việc sử dụng đúng HTTP Status Code giúp thiết kế API rõ ràng, giảm coupling và tăng tính chuyên nghiệp trong giao tiếp giữa Client – Server.
