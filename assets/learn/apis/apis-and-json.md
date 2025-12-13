---
title: "APIs & JSON"
level: beginner
tags: [rest, json, apis, backend]
readTime: 6
updated: 2025-01-13
---

## What it is

APIs (Application Programming Interfaces) let different applications talk to each other. JSON (JavaScript Object Notation) is the most common format for exchanging data.

## Why it exists

Applications need to share data. APIs provide a standard way to request and receive information without needing to know how the other system works internally.

## Mental model

Think of an API like a restaurant menu:
- **Endpoints**: Different dishes you can order (e.g., `/users`, `/orders`)
- **Methods**: How you order (GET = view menu, POST = place order, PUT = modify order)
- **JSON**: The format your order comes in (structured data)
- **Query params**: Special instructions (e.g., `?page=2` for pagination)

## Key terms

- **REST**: A style of API design using HTTP methods (GET, POST, PUT, DELETE)
- **JSON**: A text format for structured data (like XML but simpler)
- **Request Body**: Data sent with POST/PUT requests (in JSON format)
- **Query Parameters**: Extra info in the URL (e.g., `?search=term&page=1`)
- **Pagination**: Breaking large results into smaller pages

## Example

```json
// Request: GET /api/users?page=1&limit=10
// Response:
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "pagination": {
    "page": 1,
    "totalPages": 5
  }
}
```

## Common mistakes

- Confusing request body (POST/PUT) with query params (GET)
- Not handling pagination (assuming you'll get all results at once)
- Forgetting that JSON keys must be strings
- Not checking HTTP status codes (200 = success, 400 = bad request)

## Quick quiz

1. When should you use query parameters vs request body?
2. What's the difference between GET and POST?
3. Why is pagination important for APIs?

## Next to learn

"Auth Basics: Cookies vs JWT" - Learn how APIs handle authentication

