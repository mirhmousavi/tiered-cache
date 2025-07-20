from .backends import CacheBackend
from typing import Any


class TieredCache:
    def __init__(self, backends: list[CacheBackend]):
        self.backends = backends

    def set(self, key: str, value: Any):
        for backend in self.backends:
            backend.set(key, value)

    def get(self, key: str):
        for index, backend in enumerate(self.backends):
            value = backend.get(key)
            if value is not None:
                try:
                    return value
                finally:
                    for cache_miss_backend in self.backends[:index]:
                        cache_miss_backend.set(key, value)

    def remove(self, key: str):
        for backend in self.backends:
            backend.remove(key)
