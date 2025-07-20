from ..error_handler import ErrorHandler
from typing import Any
from .cache_backend import CacheBackend


class InMemoryBackend(CacheBackend):
    cache = {}

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size

    def set(self, key: str, value: Any):
        if self.max_size and len(self.cache) > self.max_size:
            self.cache.popitem()
        self.cache[key] = value

    def get(self, key: str):
        with ErrorHandler(KeyError):
            return self.cache[key]

    def remove(self, key: str):
        with ErrorHandler(KeyError):
            del self.cache[key]
