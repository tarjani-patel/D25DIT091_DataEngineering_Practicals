# Dataset Schema

## Overview

The mock enterprise e-commerce platform generates structured, semi-structured, and unstructured data from multiple business systems.

---

# Structured Data

## Customers

| Field | Type |
|--------|------|
| CustomerID | Integer |
| Name | String |
| Email | String |
| Phone | String |
| Address | String |

---

## Products

| Field | Type |
|--------|------|
| ProductID | Integer |
| ProductName | String |
| Category | String |
| Price | Decimal |
| Stock | Integer |

---

## Orders

| Field | Type |
|--------|------|
| OrderID | Integer |
| CustomerID | Integer |
| ProductID | Integer |
| Quantity | Integer |
| TotalAmount | Decimal |
| OrderDate | Date |
| Status | String |

---

## Payments

| Field | Type |
|--------|------|
| PaymentID | Integer |
| OrderID | Integer |
| Method | String |
| Amount | Decimal |
| Status | String |

---

# Semi-Structured Data

## Clickstream JSON

```json
{
  "event":"ProductView",
  "user_id":"U1023",
  "product_id":"P123",
  "device":"Mobile",
  "browser":"Chrome",
  "timestamp":"2026-07-10T10:30:22Z"
}
```

Contains:

- User Activity
- Page Views
- Search Events
- Cart Events
- Checkout Events

---

# Inventory Log Stream

Example:

```
Timestamp,Warehouse,ProductID,Stock
2026-07-10,Delhi,P101,320
2026-07-10,Mumbai,P102,250
```

Contains:

- Stock Updates
- Warehouse Events
- Restocking
- Inventory Changes

---

# Data Types

| Data Type | Example |
|-----------|----------|
| Structured | SQL Tables |
| Semi-Structured | JSON |
| Unstructured | Server Logs |

---

# Data Sources

- Customer Website
- Mobile App
- Payment Gateway
- Inventory System
- Third-party APIs
- Clickstream Tracking
- Admin Portal