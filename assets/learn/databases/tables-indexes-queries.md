---
title: "Databases: Tables, Indexes, and Why Queries Get Slow"
level: beginner
tags: [databases, sql, indexes, performance]
readTime: 7
updated: 2025-01-13
---

## What it is

Databases store data in tables (like spreadsheets). Indexes are like a book's index - they help the database find data quickly without scanning everything.

## Why it exists

Without indexes, finding a specific row means checking every single row (full table scan). With millions of rows, this becomes painfully slow. Indexes create shortcuts to find data fast.

## Mental model

Think of a database table like a phone book:
- **Table**: The entire phone book with all entries
- **Index**: The alphabetical index at the front that tells you "Smith starts at page 450"
- **Query**: Looking up "John Smith" - with index you jump to page 450, without index you read every page

## Key terms

- **Table**: A collection of rows (records) and columns (fields)
- **Index**: A data structure that speeds up lookups (like a hash map or B-tree)
- **Primary Key**: A unique identifier for each row (automatically indexed)
- **Full Table Scan**: Reading every row to find matches (slow!)
- **Query Plan**: How the database decides to execute your query

## Example

```sql
-- Without index: scans all 1 million rows (slow!)
SELECT * FROM users WHERE email = 'alice@example.com';

-- With index on email: jumps directly to the row (fast!)
CREATE INDEX idx_email ON users(email);
SELECT * FROM users WHERE email = 'alice@example.com';
```

## Common mistakes

- Not indexing frequently queried columns (email, user_id, etc.)
- Creating too many indexes (slows down writes)
- Using `SELECT *` when you only need specific columns
- Not understanding that `WHERE` clauses need indexes to be fast
- Forgetting that `LIKE '%term%'` can't use indexes efficiently
- Not analyzing slow queries to find bottlenecks

## Quick quiz

1. What is an index and why does it make queries faster?
2. Why might having too many indexes be a problem?
3. What's a "full table scan" and when does it happen?

## Next to learn

"Event Streaming: Kafka in Plain English" - Learn how modern systems handle real-time data streams

