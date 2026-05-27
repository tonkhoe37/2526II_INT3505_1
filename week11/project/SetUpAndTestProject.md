# 📘 API Design Patterns Demo (FastAPI + GraphQL + Event Bus + Webhook)

---

## 📌 1. Chạy project

```bash
pip install fastapi uvicorn graphene starlette-graphene3
```

```bash
uvicorn main:app --reload
```

---

## 🌐 BASE URL

```
http://127.0.0.1:8000
```

---

# 🟢 2. REST API – CRUD Pattern

## 📌 Create Course

```
POST /courses
```

URL:

```
http://127.0.0.1:8000/courses
```

Body:

```json
{
  "title": "Python API"
}
```

---

## 📌 Get All Courses

```
GET /courses
```

URL:

```
http://127.0.0.1:8000/courses
```

---

## 📌 Query Pattern (Search)

```
GET /courses?search=python
```

---

## 📌 HATEOAS Pattern

```
GET /courses/1
```

Response:

```json
{
  "data": {
    "id": 1,
    "title": "Python API"
  },
  "_links": {
    "self": "/courses/1",
    "enroll": "/enroll/1"
  }
}
```

---

## 📌 Update Course

```
PUT /courses/1
```

---

## 📌 Delete Course

```
DELETE /courses/1
```

---

# 🟡 3. Event-Driven Architecture

## 📌 Enroll Course

```
POST /enroll/1
```

Flow:

```
publish("USER_ENROLLED") → Event Bus → Notification Service
```

Console:

```
[EVENT]: USER_ENROLLED
[NOTIFICATION]
User enrolled in course 1
```

---

# 🔵 4. Webhook Pattern

## 📌 Payment Webhook

```
POST /webhook/payment
```

Body:

```json
{
  "event": "payment.success",
  "course_id": 1
}
```

Flow:

```
External System → Webhook → publish(PAYMENT_SUCCESS)
```

Console:

```
[WEBHOOK RECEIVED]
[EVENT]: PAYMENT_SUCCESS
[NOTIFICATION]
Payment successful for course 1
```

---

# 🟣 5. GraphQL API

## Endpoint

```
/graphql
```

## Query

```graphql
{
  courses {
    id
    title
  }
}
```

## Response

```json
{
  "data": {
    "courses": [
      {
        "id": 1,
        "title": "Python API"
      }
    ]
  }
}
```

---

# ⚙️ 6. Patterns đã demo

| Pattern      | Endpoint         |
| ------------ | ---------------- |
| CRUD         | /courses         |
| Query        | /courses?search= |
| HATEOAS      | /courses/{id}    |
| Event-Driven | /enroll/{id}     |
| Webhook      | /webhook/payment |
| GraphQL      | /graphql         |

---

# 🧠 7. Kiến trúc tổng thể

```
REST API
   ├── CRUD Courses
   ├── Event Bus
   ├── Webhook
   └── Notification Service

GraphQL API
   └── Flexible Query System
```

---
