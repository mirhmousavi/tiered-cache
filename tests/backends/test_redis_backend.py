import redis
from unittest.mock import Mock
from src.tiered_cache.backends import RedisBackend
import pytest
from src.tiered_cache.models import CacheItem


class TestRedisBackend:
    def setup_method(self):
        self.mock_redis = Mock()
        self.backend = RedisBackend(self.mock_redis)

    @pytest.mark.parametrize(
        "key,value",
        [
            ("key1", "value1"),
            ("key2", {"name": "test", "id": 123}),
        ],
    )
    def test_set(self, key, value):
        self.backend.set(key, value)
        self.mock_redis.hsetex.assert_called_once_with(
            "tiered-cache",
            key,
            self.backend._serialize(CacheItem(key=key, value=value)),
            None,
        )

    @pytest.mark.parametrize(
        "key,value",
        [
            ("key1", "value1"),
            ("key2", {"name": "test", "id": 123}),
        ],
    )
    def test_get(self, key, value):
        expected = CacheItem(key=key, value=value)
        self.mock_redis.hget.return_value = self.backend._serialize(expected)
        actual = self.backend.get(key)
        assert actual == expected
        self.mock_redis.hget.assert_called_once_with("tiered-cache", key)

    def test_get_nonexistent_key_returns_none(self):
        self.mock_redis.hget.return_value = None
        result = self.backend.get("nonexistent")
        assert result is None

    def test_remove_key_calls_redis_hdel(self):
        self.backend.remove("key1")
        self.mock_redis.hdel.assert_called_once_with("tiered-cache", "key1")

    def test_set_with_redis_error_suppresses_error(self):
        self.mock_redis.hset.side_effect = redis.RedisError("Connection failed")
        self.backend.set("key1", "value1")

    def test_get_with_redis_error_suppresses_error(self):
        self.mock_redis.hget.side_effect = redis.RedisError("Connection failed")
        result = self.backend.get("key1")
        assert result is None

    def test_remove_with_redis_error_suppresses_error(self):
        self.mock_redis.hdel.side_effect = redis.RedisError("Connection failed")
        self.backend.remove("key1")
