from ..error_handler import ErrorHandler
from typing import Any
from .cache_backend import CacheBackend
from collections import OrderedDict


class InMemoryBackend(CacheBackend):
    """Implements in-memory cache using LRU eviction policy."""

    cache = OrderedDict()

    def __init__(self, max_size: int = 1_000):
        self.max_size = max_size

    def set(self, key: str, value: Any):
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        try:
            self.cache[key] = value
        finally:
            if self.max_size and len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
            self.cache[key] = value

    def get(self, key: str):
        if key in self.cache:
            # Move key to end to show that it was recently used
            self.cache.move_to_end(key)
            return self.cache[key]

    def remove(self, key: str):
        with ErrorHandler(KeyError):
            del self.cache[key]
