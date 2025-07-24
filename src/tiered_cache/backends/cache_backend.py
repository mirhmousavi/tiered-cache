from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from ..models import CacheItem


class CacheBackend(ABC):
    """The interface for cache backends."""

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
        expires_in: int | None = None,
        expires_at: datetime | None = None,
    ) -> CacheItem: ...

    """
    Notes:
        only one of `expires_in` and `expires_at` must be set.
    """

    @abstractmethod
    def get(self, key: str) -> CacheItem | None: ...

    """
    Returns an instace of `CacheItem` if found otherwise `None`
    """

    @abstractmethod
    def remove(self, key: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...
