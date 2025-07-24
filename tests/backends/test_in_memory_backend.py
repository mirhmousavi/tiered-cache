from src.tiered_cache.backends import InMemoryBackend
import pytest


class TestInMemoryBackend:
    def setup_method(self):
        self.backend = InMemoryBackend()
        self.backend.clear()

    @pytest.mark.parametrize(
        "key,value", [("key1", "value1"), ("key2", {"name": "test", "id": 123})]
    )
    def test_set(self, key, value):
        self.backend.set(key, value)
        assert self.backend.get(key).value == value

    def test_get_nonexistent_key_returns_none(self):
        result = self.backend.get("nonexistent")
        assert result is None

    def test_remove(self):
        self.backend.set("key1", "value1")
        self.backend.remove("key1")
        assert self.backend.get("key1") is None

    def test_remove_nonexistent_key_does_not_raise_error(self):
        self.backend.remove("nonexistent")

    def test_clear(self):
        self.backend.set("key1", "value1")
        self.backend.set("key2", "value2")
        self.backend.clear()
        assert self.backend.get("key1") is None
        assert self.backend.get("key2") is None
