# 📚 Tài liệu API - Libarry management system

## 1. Giới thiệu cơ bản và Lý thuyết

**OpenAPI Specification (trước đây gọi là Swagger)** là một tiêu chuẩn mạnh mẽ và phổ biến nhất hiện nay dùng để mô tả các RESTful API.

Thay vì viết tài liệu bằng Word hay Excel dễ gây nhầm lẫn và khó đồng bộ, OpenAPI cho phép bạn định nghĩa toàn bộ cấu trúc API (bao gồm các endpoint, request parameters, response body, mã lỗi HTTP) vào một file duy nhất (`.json` hoặc `.yaml`).

**Lợi ích mang lại:**

- **Tài liệu sống:** Giao diện tài liệu trực quan, có thể thao tác gọi nghiệm thu (test) ngay trên trình duyệt.
- **Đồng bộ hóa:** Là "hợp đồng" thống nhất giữa team Frontend và Backend.
- **Tự động hóa:** Từ một bản đặc tả có thể sinh ra code (frontend SDK, backend stub) và tạo server giả lập (mock server).

---

## 2. Yêu cầu môi trường và Cài đặt

Để sử dụng đầy đủ các công cụ quản lý API này, máy tính của bạn cần đáp ứng các yêu cầu sau:

### Yêu cầu hệ thống:

- **Node.js & npm:** Bắt buộc (Dùng để chạy các thư viện giao diện và mock server).
- **Java Runtime Environment (JRE):** Bắt buộc (Chỉ dùng nếu bạn muốn thực hiện tính năng tự động sinh code).

### Các lệnh cài đặt công cụ:

Mở Terminal/Command Prompt và chạy các lệnh sau để cài đặt các công cụ cần thiết trên toàn hệ thống (global):

```bash
# 1. Cài đặt công cụ xem giao diện tài liệu (Swagger UI)
npm install -g swagger-ui-cli

# 2. Cài đặt công cụ tự động sinh code (OpenAPI Generator)
npm install -g @openapitools/openapi-generator-cli
```
