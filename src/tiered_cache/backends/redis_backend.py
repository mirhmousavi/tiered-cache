import redis
import json
from ..error_handler import ErrorHandler
from typing import Protocol, Any
from .cache_backend import CacheBackend
from ..models import CacheItem
from datetime import datetime
from dataclasses import asdict


class RedisConnection(Protocol):
    def hsetx(self, name: str, key: str, value: Any, ex: int | None = None) -> None: ...

    def hget(self, name: str, key: str) -> str | None: ...

    def hdel(self, name: str, key: str) -> None: ...


class RedisBackend(CacheBackend):
    _redis_hash_name = "tiered-cache"

    def __init__(self, redis_connection: RedisConnection):
        self.redis_connection = redis_connection

    def _serialize(self, cache_item: CacheItem):
        ret = asdict(cache_item)

        del ret["expires_in"]
        del ret["key"]

        if ret["expires_at"]:
            ret["expires_at"] = ret["expires_at"].isoformat()

        return json.dumps(ret)

    def _deserialize(self, data: str | None):
        if data is None:
            return None
        return json.loads(data)

    def set(
        self,
        key: str,
        value: Any,
        expires_in: int | None = None,
        expires_at: datetime | None = None,
    ) -> CacheItem:
        cache_item = CacheItem(
            key=key, value=value, expires_in=expires_in, expires_at=expires_at
        )
        with ErrorHandler(redis.RedisError):
            self.redis_connection.hsetex(
                self._redis_hash_name,
                key,
                self._serialize(cache_item),
                cache_item.expires_in,
            )
        return cache_item

    def get(self, key: str) -> CacheItem | None:
        with ErrorHandler(redis.RedisError):
            ret = self.redis_connection.hget(self._redis_hash_name, key)
            if ret is None:
                return None
            cache_item = CacheItem(key=key, **self._deserialize(ret))
            return cache_item

    def remove(self, key: str):
        with ErrorHandler(redis.RedisError):
            self.redis_connection.hdel(self._redis_hash_name, key)

    def clear(self):
        self.redis_connection.hdel(self._redis_hash_name, "*")
