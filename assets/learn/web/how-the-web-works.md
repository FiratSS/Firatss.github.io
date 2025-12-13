---
title: "How the Web Works in 7 Minutes"
level: beginner
tags: [http, web, basics, protocols]
readTime: 7
updated: 2025-01-13
---

## What it is

The web works through HTTP (HyperText Transfer Protocol) - a request/response system where your browser asks for resources and servers send them back.

## Why it exists

Before HTTP, there was no standard way for computers to request and share documents over networks. HTTP provides a simple, universal language for web communication.

## Mental model

Think of HTTP like ordering at a restaurant:
- **Request**: You (browser) place an order (request a webpage)
- **Response**: The kitchen (server) prepares and delivers your meal (HTML/CSS/JS files)
- **Status codes**: Like "order received" (200), "not on menu" (404), "kitchen closed" (503)

## Key terms

- **HTTP Request**: A message sent from browser to server asking for something
- **HTTP Response**: The server's reply with the requested resource
- **Status Code**: A number indicating success (200), error (404), or redirect (301)
- **Headers**: Metadata about the request/response (content type, cookies, etc.)
- **Latency**: The time it takes for a request to travel and get a response back

## Example

```
Browser → GET /index.html HTTP/1.1
         Host: example.com

Server → HTTP/1.1 200 OK
         Content-Type: text/html
         <html>...</html>
```

## Common mistakes

- Confusing HTTP with HTTPS (HTTPS adds encryption)
- Not understanding status codes (404 = not found, 500 = server error)
- Ignoring latency (distance and network speed matter)
- Forgetting that headers exist (they carry important metadata)

## Quick quiz

1. What does a 404 status code mean?
2. What's the difference between HTTP and HTTPS?
3. Why does latency increase when servers are far away?

## Next to learn

"APIs & JSON" - Learn how modern web applications exchange data

