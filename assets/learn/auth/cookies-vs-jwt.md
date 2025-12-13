---
title: "Auth Basics: Cookies vs JWT"
level: beginner
tags: [authentication, cookies, jwt, security, sessions]
readTime: 8
updated: 2025-01-13
---

## What it is

Authentication is how systems know "who you are." Cookies and JWTs are two common ways to maintain your logged-in state across requests.

## Why it exists

HTTP is stateless - each request is independent. Without cookies or tokens, you'd have to log in for every single request. These mechanisms let you prove your identity once and reuse it.

## Mental model

- **Cookies**: Like a membership card the server gives you. You show it each time, and the server looks up your account.
- **JWT (JSON Web Token)**: Like a self-contained ID badge. It has your info encoded inside, so the server doesn't need to look it up.

## Key terms

- **Session**: Server-side storage of your login state (used with cookies)
- **Cookie**: Small piece of data stored by your browser, sent with every request
- **JWT**: A token containing your identity info, usually stored in localStorage or sent in headers
- **Stateless**: JWTs don't require server-side storage (unlike sessions)
- **CSRF**: Attack where malicious site uses your cookies (cookies are vulnerable to this)

## Example

**Cookies (Session-based):**
```
Login → Server creates session → Sends cookie → Browser stores cookie
Next request → Browser sends cookie → Server looks up session → Authenticated
```

**JWT:**
```
Login → Server creates JWT → Sends token → Client stores token
Next request → Client sends token in header → Server verifies signature → Authenticated
```

## Common mistakes

- Storing JWTs in cookies (defeats the stateless benefit)
- Not setting `HttpOnly` flag on cookies (allows XSS attacks)
- Not validating JWT signatures (anyone could forge tokens)
- Using JWTs for sessions when you need to revoke access (JWTs can't be easily revoked)
- Not understanding CSRF attacks with cookies

## Quick quiz

1. What's the main difference between cookies and JWTs?
2. Why might you choose JWT over cookies?
3. What security risk do cookies have that JWTs don't?

## Next to learn

"Databases: Tables, Indexes, and Why Queries Get Slow" - Learn how data is stored and retrieved efficiently

