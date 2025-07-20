
# Tiered Cache

Tiered Cache is a utility library designed to improve service throughput and availability by caching data across multiple storage layers (a.k.a. cache backends).

It allows applications to reduce latency and external dependencies by organizing caches in a prioritized tier. For example, it can be configured fast in-memory storage first, then falls back to shared solutions like Redis. When a cache hit occurs in a lower tier (e.g., memory), higher tiers (e.g., Redis) are updated to keep future lookups fast.

This is especially useful in highly available environments where multiple service instances are running. Instead of always querying Redis, each instance first checks its own memory. On a Redis hit, the instance updates its local memory, reducing load and improving response time.

```python
import redis
from tiered_cache import TieredCache
from tiered_cache.backends import InMemoryBackend, RedisBackend


redis_connection = redis.Redis(host='localhost', port=6380, decode_responses=True)

tiered_cache = TieredCache(
    [
        InMemoryBackend(),
        RedisBackend(redis_connection),
    ]
)

tiered_cache.set('test', 1)
print(tiered_cache.get('test'))
```
