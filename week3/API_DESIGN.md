# Kiến thức cơ bản về Thiết kế API (RESTful)

Thiết kế API theo chuẩn RESTful giúp hệ thống **dễ sử dụng, dễ bảo trì
và dễ mở rộng**.\
Ba nguyên tắc quan trọng cần đảm bảo là:

- **Nhất quán (Consistency)** → Cách thiết kế phải đồng bộ trong toàn
  bộ hệ thống.\
- **Dễ hiểu (Clarity)** → Người sử dụng API có thể hiểu chức năng chỉ
  bằng cách nhìn vào URL và HTTP method.\
- **Dễ mở rộng (Extensibility)** → API có thể phát triển thêm chức
  năng trong tương lai mà không làm ảnh hưởng đến hệ thống hiện tại.

---

# 1. Naming Conventions (Quy tắc đặt tên)

Quy tắc đặt tên endpoint giúp API **dễ đọc, dễ hiểu và dễ sử dụng cho
các developer khác**.

## Sử dụng danh từ số nhiều (Plural Nouns)

Trong RESTful API, URL đại diện cho **tài nguyên (resource)**.\
Các tài nguyên thường được biểu diễn dưới dạng **tập hợp (collection)**
nên nên sử dụng **danh từ số nhiều**.

Ví dụ đúng:

    /users
    /products
    /orders

Ví dụ không nên dùng:

    /user
    /product
    /order

Khi cần truy cập một tài nguyên cụ thể:

    /users/1
    /products/10

---

## Chữ thường và gạch nối (Lowercase & Hyphens)

Endpoint nên:

- viết **chữ thường hoàn toàn**
- sử dụng **dấu gạch nối (-)** nếu có nhiều từ

Ví dụ tốt:

    /order-items
    /user-addresses
    /product-categories

Ví dụ không nên dùng:

    /orderItems
    /UserAddresses
    /productCategories

---

## Phân tầng tài nguyên (Resource Hierarchy)

Trong REST API, các tài nguyên có thể có **mối quan hệ với nhau**.\
Ta thể hiện mối quan hệ này thông qua **cấu trúc phân tầng của URL**.

Ví dụ:

    /users/1/orders

Ý nghĩa: Lấy **các đơn hàng của user có id = 1**.

Ví dụ khác:

    /orders/10/items

Ý nghĩa: Lấy **các sản phẩm trong đơn hàng số 10**.

---

## Không bao giờ bao gồm động từ trong URI

Trong RESTful API:

- **URI đại diện cho tài nguyên**
- **HTTP Method đại diện cho hành động**

Ví dụ sai:

    /get-users
    /create-order
    /delete-product

Ví dụ đúng:

    GET /users
    POST /users
    PUT /users/1
    DELETE /users/1

Method Endpoint Chức năng

---

GET /users Lấy danh sách user
POST /users Tạo user mới
PUT /users/1 Cập nhật user
DELETE /users/1 Xóa user

---

# 2. API Versioning (Quản lý phiên bản)

Khi hệ thống phát triển, API có thể cần **thay đổi cấu trúc hoặc chức
năng**.\
Nếu không quản lý phiên bản, các ứng dụng đang sử dụng API cũ có thể bị
lỗi.

Vì vậy cần **định nghĩa version cho API ngay từ đầu**.

Ví dụ:

    /api/v1/products
    /api/v1/users
    /api/v2/products

Ví dụ sử dụng:

    GET /api/v1/products

Sau khi nâng cấp hệ thống:

    GET /api/v2/products

**Lợi ích của versioning:**

- Tránh phá vỡ hệ thống cũ\
- Cho phép nâng cấp API dễ dàng\
- Hỗ trợ nhiều client khác nhau

---

# 3. Best Practices (Quy tắc vàng)

## Tính nhất quán (Consistency)

Toàn bộ API phải sử dụng **cùng một kiểu thiết kế**.

Ví dụ tốt:

    /api/v1/users
    /api/v1/products
    /api/v1/orders

Ví dụ không nhất quán:

    /api/v1/users
    /products-api
    /getOrders

Consistency cần áp dụng cho:

- cấu trúc URL
- cách đặt tên
- format response
- HTTP methods

---

## Dễ hiểu (Clarity)

API nên được thiết kế sao cho **developer chỉ cần nhìn vào endpoint là
hiểu chức năng**.

Ví dụ:

    GET /users
    POST /users
    GET /users/10
    DELETE /users/10

Ví dụ khó hiểu:

    /getUserList
    /createUserData
    /removeUserAccount

---

## Lọc dữ liệu (Filtering)

Khi dữ liệu lớn, API nên cho phép **lọc hoặc tìm kiếm dữ liệu bằng query
parameters**.

Ví dụ:

    /products?category=electronics

Ví dụ khác:

    /products?price=1000

Kết hợp nhiều điều kiện:

    /products?category=phone&brand=apple

Không nên:

    /products/electronics

---

## Tóm tắt

Một RESTful API tốt cần đảm bảo:

- Naming conventions rõ ràng
- URI đại diện cho tài nguyên
- HTTP methods thể hiện hành động
- API có version
- Endpoint dễ hiểu
- Hỗ trợ filtering bằng query parameters
