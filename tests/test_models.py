from src.tiered_cache.models import CacheItem
from datetime import datetime
import pytest
import time


class TestCacheItem:
    def test_valid(self):
        assert CacheItem(key="test", value="test", expires_in=1)

    # def test_not_set_expires_in_expires_at(self):
    #     with pytest.raises(ValueError) as exc:
    #         _ = CacheItem(key='test', value='test')
    #     assert str(exc.value) == 'Either expires_at or expires_in must be set'
    def test_set_both_expires_in_expires_at(self):
        with pytest.raises(ValueError) as exc:
            _ = CacheItem(
                key="test", value="test", expires_in=1, expires_at=datetime.now()
            )
        assert str(exc.value) == "Can not set both expires_at and expires_in"

    def test_get_ttl(self):
        cache_item = CacheItem(key="test", value="test", expires_in=100)
        assert cache_item.get_ttl() == pytest.approx(100)
        time.sleep(2)
        assert cache_item.get_ttl() == pytest.approx(98, abs=1)

    def test_is_fresh_when_is_fresh(self):
        cache_item = CacheItem(key="test", value="test", expires_in=100)
        assert cache_item.is_fresh()

    def test_is_fresh_when_is_stale(self):
        cache_item = CacheItem(key="test", value="test", expires_in=0)
        assert cache_item.is_fresh() is False
