import redis
from unittest.mock import Mock
from src.tiered_cache.backends import RedisBackend


class TestRedisBackend:
    def setup_method(self):
        self.mock_redis = Mock()
        self.backend = RedisBackend(self.mock_redis)

    def test_set_string_input_calls_redis_hset(self):
        self.backend.set("key1", "value1")
        self.mock_redis.hset.assert_called_once_with("tiered-cache", "key1", '"value1"')

    def test_set_dictionary_input_calls_redis_hset(self):
        data = {"name": "test", "id": 123}
        self.backend.set("key2", data)
        self.mock_redis.hset.assert_called_once_with(
            "tiered-cache", "key2", '{"name": "test", "id": 123}'
        )

    def test_get_string_input_returns_deserialized_value(self):
        self.mock_redis.hget.return_value = '"value1"'
        result = self.backend.get("key1")
        assert result == "value1"
        self.mock_redis.hget.assert_called_once_with("tiered-cache", "key1")

    def test_get_dictionary_input_returns_deserialized_value(self):
        self.mock_redis.hget.return_value = '{"name": "test", "id": 123}'
        result = self.backend.get("key2")
        assert result == {"name": "test", "id": 123}
        self.mock_redis.hget.assert_called_once_with("tiered-cache", "key2")

    def test_get_nonexistent_key_returns_none(self):
        self.mock_redis.hget.return_value = None
        result = self.backend.get("nonexistent")
        assert result is None

    def test_remove_string_key_calls_redis_hdel(self):
        self.backend.remove("key1")
        self.mock_redis.hdel.assert_called_once_with("tiered-cache", "key1")

    def test_remove_dictionary_key_calls_redis_hdel(self):
        self.backend.remove("key2")
        self.mock_redis.hdel.assert_called_once_with("tiered-cache", "key2")

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
