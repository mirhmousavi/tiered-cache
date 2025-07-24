from ..error_handler import ErrorHandler
from typing import Any
from .cache_backend import CacheBackend
from collections import OrderedDict
from datetime import datetime
from ..models import CacheItem


class InMemoryBackend(CacheBackend):
    """Implements in-memory cache using LRU eviction policy."""

    _cache = OrderedDict()

    def __init__(self, max_size: int = 1_000):
        self.max_size = max_size

    def set(
        self,
        key: str,
        value: Any,
        expires_in: int | None = None,
        expires_at: datetime | None = None,
    ) -> None | CacheItem:
        cache_item = CacheItem(
            key=key, value=value, expires_in=expires_in, expires_at=expires_at
        )
        try:
            # Update and move to end to follow LRU policy for eviction.
            self._cache[key] = cache_item
            self._cache.move_to_end(key)
            return cache_item
        finally:
            if self.max_size and len(self._cache) > self.max_size:
                self._cache.popitem(last=False)

    def get(self, key: str) -> CacheItem | None:
        if key not in self._cache:
            return None
        cache_item = self._cache[key]
        # Check if item is expired
        if cache_item.is_expirable() and not cache_item.is_fresh():
            self._cache.popitem(key)
            return None

        # Move key to end to show that it was recently used
        self._cache.move_to_end(key)
        return cache_item

    def remove(self, key: str) -> None:
        with ErrorHandler(KeyError):
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()
