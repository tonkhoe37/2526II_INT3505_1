# So sánh các API Specification với nhau

| Tiêu chí                           | OpenAPI (Swagger)                               | API Blueprint                     | RAML                             | TypeSpec                                  |
| :--------------------------------- | :---------------------------------------------- | :-------------------------------- | :------------------------------- | :---------------------------------------- |
| **Triết lý thiết kế**              | Tập trung vào sự đầy đủ và khả năng tương thích | Ưu tiên sự đơn giản và dễ đọc     | Tập trung vào tái sử dụng        | Sử dụng tư duy lập trình để sinh tài liệu |
| **Định dạng file**                 | JSON hoặc YAML                                  | Markdown (APIB)                   | YAML                             | DSL giống TypeScript                      |
| **Độ phổ biến**                    | Rất cao                                         | Trung bình                        | Trung bình                       | Đang tăng                                 |
| **Khả năng đọc (Human-readable)**  | Trung bình                                      | Rất cao                           | Cao                              | Cao (đối với developer)                   |
| **Khả năng tái sử dụng**           | Trung bình (components, $ref)                   | Trung bình                        | Rất cao (traits, resource types) | Rất cao (kế thừa, generic)                |
| **Công cụ (Tooling)**              | Rất mạnh (Swagger UI, Postman, Codegen)         | Trung bình (Aglio, Apiary)        | Trung bình                       | Khá mạnh (tsp compiler, VS Code)          |
| **Code Generation**                | Rất mạnh (sinh server/client đa ngôn ngữ)       | Rất yếu                           | Trung bình                       | Mạnh (thông qua OpenAPI)                  |
| **Mock Server**                    | Rất mạnh                                        | Yếu                               | Trung bình                       | Mạnh                                      |
| **Contract-first (API-first)**     | Rất mạnh                                        | Yếu                               | Mạnh                             | Rất mạnh                                  |
| **Độ khó học (Learning curve)**    | Trung bình                                      | Dễ                                | Trung bình                       | Trung bình                                |
| **Khả năng dùng trong production** | Rất cao                                         | Thấp                              | Trung bình                       | Khá                                       |
| **Khả năng tích hợp framework**    | Rất mạnh                                        | Rất thấp                          | Thấp                             | Mạnh                                      |
| **Khả năng mở rộng & maintain**    | Trung bình                                      | Thấp                              | Cao                              | Rất cao                                   |
| **Đối tượng phù hợp**              | Backend / Fullstack dev                         | Technical writer / tài liệu nhanh | Enterprise system                | Developer thích type-safe                 |
