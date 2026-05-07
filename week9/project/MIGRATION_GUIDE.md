# Payment API Migration Guide

Version: v1 -> v2

---

# Overview

Payment API v1 has been deprecated and will be removed in the future.

Developers should migrate to Payment API v2.

---

# Endpoint Changes

## Old Endpoint

POST /api/v1/payments

## New Endpoint

POST /api/v2/payments

---

# Why Migrate to v2?

API v2 provides:

- Better validation
- Improved security
- Token-based payment processing
- Transaction ID support
- Better scalability

---

# Request Changes

## v1 Request

```json
{
  "amount": 100,
  "currency": "USD"
}
```
