from src.tiered_cache.backends import InMemoryBackend


class TestInMemoryBackend:
    def setup_method(self):
        self.backend = InMemoryBackend()

    def test_set_string_input_stores_value(self):
        self.backend.set("key1", "value1")
        assert InMemoryBackend.cache["key1"] == "value1"

    def test_set_dictionary_input_stores_value(self):
        data = {"name": "test", "id": 123}
        self.backend.set("key2", data)
        assert InMemoryBackend.cache["key2"] == data

    def test_get_string_input_returns_value(self):
        InMemoryBackend.cache["key1"] = "value1"
        result = self.backend.get("key1")
        assert result == "value1"

    def test_get_dictionary_input_returns_value(self):
        data = {"name": "test", "id": 123}
        InMemoryBackend.cache["key2"] = data
        result = self.backend.get("key2")
        assert result == data

    def test_get_nonexistent_key_returns_none(self):
        result = self.backend.get("nonexistent")
        assert result is None

    def test_remove_string_key_deletes_value(self):
        InMemoryBackend.cache["key1"] = "value1"
        self.backend.remove("key1")
        assert "key1" not in InMemoryBackend.cache

    def test_remove_dictionary_key_deletes_value(self):
        data = {"name": "test", "id": 123}
        InMemoryBackend.cache["key2"] = data
        self.backend.remove("key2")
        assert "key2" not in InMemoryBackend.cache

    def test_remove_nonexistent_key_does_not_raise_error(self):
        self.backend.remove("nonexistent")
