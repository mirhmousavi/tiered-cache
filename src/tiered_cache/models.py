from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
import time


@dataclass
class CacheItem:
    key: str
    value: Any
    expires_at: datetime | None = None
    expires_in: int | None = None

    def __post_init__(self):
        if self.expires_at and self.expires_in:
            raise ValueError("Can not set both expires_at and expires_in")
        if self.expires_in is not None:
            self.expires_at = datetime.now() + timedelta(seconds=self.expires_in)

    def get_ttl(self) -> int | None:
        """Returns the amount of seconds till the item becomes stale or `None` if it's not expirable."""
        if self.expires_in is None and self.expires_at is None:
            return None
        now = datetime.now()
        if self.expires_at <= now:
            return 0
        return (self.expires_at - now).total_seconds()

    def is_fresh(self):
        return bool(self.get_ttl())

    def is_expirable(self):
        return self.get_ttl() is not None
