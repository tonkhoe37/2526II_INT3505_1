# Deprecation Notice - Payment API v1

## Overview

Payment API v1 has been officially deprecated.

Developers are encouraged to migrate to Payment API v2.

---

# Deprecated Endpoint

POST /api/v1/payments

---

# New Endpoint

POST /api/v2/payments

---

# Deprecation Timeline

| Event                  | Date       |
| ---------------------- | ---------- |
| API v2 Release Date    | May 2026   |
| API v1 Deprecated Date | May 2026   |
| API v1 Sunset Date     | 2026-12-31 |

---

# Why migrate to v2?

Payment API v2 introduces:

- Improved request validation
- Payment method support
- Token field support
- Transaction ID response

---

# Request Changes

## API v1 Request

```json
{
  "amount": 100,
  "currency": "USD"
}
```

## API v2 Request

```json
{
  "amount": 100,
  "currency": "USD",
  "payment_method": "VISA",
  "token": "secure-token"
}
```

---

# Validation Differences

## API v1

API v1 accepts:

- amount
- currency

without additional validation.

---

## API v2

API v2 requires:

- amount
- currency
- payment_method
- token

If any field is missing, API v2 returns:

```json
{
  "status": "error",
  "message": "Missing required fields"
}
```

---

# Response Changes

## API v1 Response

```json
{
  "api_version": "v1",
  "status": "success",
  "message": "Payment processed using API v1",
  "amount": 100,
  "currency": "USD",
  "warning": "API v1 is deprecated. Please migrate to v2."
}
```

---

## API v2 Response

```json
{
  "api_version": "v2",
  "status": "success",
  "message": "Payment processed using API v2",
  "transaction_id": "TXN-999999",
  "payment_method": "VISA"
}
```

---

# Deprecation Headers

API v1 responses include the following headers:

```text
Deprecation: true
Sunset: 2026-12-31
```

These headers indicate that API v1 is deprecated and scheduled for removal.

---

# Required Developer Actions

Developers should:

1. Update API endpoint from:

   /api/v1/payments

   to:

   /api/v2/payments

2. Add required request fields:
   - payment_method
   - token

3. Update client-side response handling for:
   - transaction_id
   - payment_method

4. Complete migration before the sunset date.

---

# Example Requests

## API v1

```bash
curl -X POST http://localhost:5000/api/v1/payments \
-H "Content-Type: application/json" \
-d '{
  "amount": 100,
  "currency": "USD"
}'
```

---

## API v2

```bash
curl -X POST http://localhost:5000/api/v2/payments \
-H "Content-Type: application/json" \
-d '{
  "amount": 100,
  "currency": "USD",
  "payment_method": "VISA",
  "token": "secure-token"
}'
```

---

# Notes

- API v1 remains temporarily available for backward compatibility.
- Developers are strongly encouraged to migrate as soon as possible.
- API v1 may be removed after the sunset date.
