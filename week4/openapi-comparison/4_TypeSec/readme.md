# TypeSpec - Library API

## Giới thiệu

Thư mục này chứa tài liệu API sử dụng TypeSpec (ngôn ngữ thiết kế API của Microsoft).

## File chính

- `main.tsp`: Định nghĩa API

## Cài đặt

npm install -g @typespec/compiler

## Compile

tsp compile .

## Output

Sau khi compile sẽ sinh ra:

./tsp-output/openapi.yaml

## Test API

- Dùng file OpenAPI sinh ra để:
  - Chạy Swagger UI
  - Import vào Postman
  - Generate code
