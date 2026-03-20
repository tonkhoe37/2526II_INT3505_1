# OpenAPI Code Generation & Testing Demo (Python)

## Giới thiệu

Project này minh họa:

- Định nghĩa API bằng OpenAPI
- Test API bằng mock server (không cần backend)
- Sinh Python client để gọi API

---

## Cấu trúc

codegen-demo/
│
├── openapi.yaml
├── client-python/
├── test_api.py
└── README.md

---

## 1. Chạy Mock Server

npx prism mock openapi.yaml

Base URL:
http://localhost:4010

---

## 2. Xem API

GET http://localhost:4010/api/books

---

## 3. Sinh Python Client

npx @openapitools/openapi-generator-cli generate \
 -i openapi.yaml \
 -g python \
 -o client-python

---

## 4. Cài đặt client

cd client-python
pip install -r requirements.txt
pip install .

---

## 5. Test API bằng Python

cd ..
python test_api.py

---

## Kết luận

Project sử dụng phương pháp Contract-first API:

- Định nghĩa API trước
- Test bằng mock server
- Sinh client tự động
