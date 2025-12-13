---
title: "Kafka in Plain English"
level: beginner
tags: [kafka, streaming, backend]
readTime: 6
updated: 2025-01-13
---

## What it is

Kafka is a system for moving and storing "events" (messages) so many services can read them reliably.

## Why it exists

Because calling every service directly doesn't scale well. Kafka lets you publish once and many things can react.

## Mental model

A topic is a named stream like `orders`. Kafka stores events in order (per partition) so consumers can process them now or replay later.

## Key terms

- **Producer**: writes events to a topic
- **Consumer**: reads events from a topic
- **Topic**: the stream name (e.g., `payments`)
- **Partition**: a shard of a topic (for scaling + ordering per shard)
- **Consumer group**: a team of consumers sharing the work

## Example

- Checkout service produces `OrderCreated` → topic `orders`
- Shipping consumes `orders` → produces `ShipmentCreated` → topic `shipments`
- Analytics consumes both topics

## Common mistakes

- Thinking Kafka "sees all API calls" (it doesn't — services publish intentionally)
- Not using a key when you need ordering (e.g., `orderId`)
- Not handling duplicates (consumers should be idempotent)

## Quick quiz

1. What's the difference between a topic and a partition?
2. Why do consumer groups exist?
3. Why might you want to replay events?

## Next to learn

"Partitions & consumer groups" and "Exactly-once vs at-least-once (in simple terms)"

