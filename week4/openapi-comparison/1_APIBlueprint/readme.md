# 📘 README - API Blueprint (Library API)

## 1. Giới thiệu

API Blueprint là một định dạng mô tả API REST dựa trên Markdown, giúp:

- Mô tả API rõ ràng, dễ đọc
- Dễ viết và maintain
- Tích hợp test tự động
- Sinh tài liệu nhanh chóng

API Blueprint phù hợp với các project nhỏ đến trung bình hoặc khi bạn muốn viết tài liệu API nhanh mà không cần cấu hình phức tạp như OpenAPI.

---

## 2. File chính

- `api.apib`: File tài liệu API (định dạng Markdown)

---

## 3. Yêu cầu môi trường

### Cài đặt Aglio (hiển thị tài liệu)

```bash
npm install -g aglio
```

### Cài đặt Dredd (test API)

```bash
npm install -g dredd
```

### (Optional) Convert sang OpenAPI

```bash
npm install -g apib2swagger
npm install -g @openapitools/openapi-generator-cli
```

---

## 4. Cách chạy tài liệu API

Kiểm tra xem còn tiến trình nào chạy cổng 3000 :

```bash
netstat -ano | findstr :3000
```

Nếu có tiến trình đang sử dụng thì kill nó :

````bash
npx kill-port 3000
```

```bash
aglio -i api.apib -s
````

---

## 5. Truy cập tài liệu

Mở trình duyệt:

```
http://localhost:3000
```

---

## 6. Cách test API

### 🧪 Dùng Postman

- Copy endpoint từ tài liệu
- Import thủ công vào Postman
- Test từng API

---

## 7. Cách generate code

⚠️ API Blueprint không hỗ trợ generate code trực tiếp mạnh như OpenAPI.

### Bước 1: Convert sang OpenAPI

```bash
apib2swagger -i api.apib -o openapi.json
```

---

### Bước 2: Generate server

```bash
npx @openapitools/openapi-generator-cli generate ^
-i openapi.json ^
-g nodejs-express-server ^
-o ./server
```

---

## 8. Tổng kết

### Test API

- ✅ Dredd (tự động)
- ✅ Postman
- ✅ curl

### Generate code

- ❗ Convert sang OpenAPI
- ❗ Sau đó dùng OpenAPI Generator

---

## 9. Gợi ý sử dụng

- Dùng API Blueprint khi cần viết tài liệu nhanh
- Dùng OpenAPI khi cần hệ sinh thái mạnh (generate code, validation, tooling)

---

## 📌 Ghi chú

- Backend phải chạy trước khi test với Dredd
- Đảm bảo API trả đúng format như mô tả trong `api.apib`
