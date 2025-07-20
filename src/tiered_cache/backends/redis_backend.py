import redis
import json
from ..error_handler import ErrorHandler
from typing import Protocol, Any
from .cache_backend import CacheBackend


class RedisConnection(Protocol):
    def hset(self, name: str, key: str, value: Any) -> None: ...

    def hget(self, name: str, key: str) -> str | None: ...

    def hdel(self, name: str, key: str) -> None: ...


class RedisBackend(CacheBackend):
    redis_hash_name = "tiered-cache"

    def __init__(self, redis_connection: RedisConnection):
        self.redis_connection = redis_connection

    def _serialize(self, value: Any):
        if value is None:
            return None
        return json.dumps(value)

    def _deserialize(self, value: str | None):
        if value is None:
            return None
        return json.loads(value)

    def set(self, key: str, value: Any):
        with ErrorHandler(redis.RedisError):
            return self.redis_connection.hset(
                self.redis_hash_name, key, self._serialize(value)
            )

    def get(self, key: str):
        with ErrorHandler(redis.RedisError):
            ret = self.redis_connection.hget(self.redis_hash_name, key)
            return self._deserialize(ret)

    def remove(self, key: str):
        with ErrorHandler(redis.RedisError):
            self.redis_connection.hdel(self.redis_hash_name, key)
