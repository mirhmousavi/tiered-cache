from unittest.mock import Mock
from src.tiered_cache.tiered_cache import TieredCache


class TestTieredCache:
    def setup_method(self):
        self.backend1 = Mock()
        self.backend2 = Mock()
        self.tiered_cache = TieredCache([self.backend1, self.backend2])

    def test_set_string_input_calls_all_backends(self):
        self.tiered_cache.set("key1", "value1")
        self.backend1.set.assert_called_once_with("key1", "value1")
        self.backend2.set.assert_called_once_with("key1", "value1")

    def test_set_dictionary_input_calls_all_backends(self):
        data = {"name": "test", "id": 123}
        self.tiered_cache.set("key2", data)
        self.backend1.set.assert_called_once_with("key2", data)
        self.backend2.set.assert_called_once_with("key2", data)

    def test_get_string_input_returns_value_from_first_backend(self):
        self.backend1.get.return_value = "value1"
        result = self.tiered_cache.get("key1")
        assert result == "value1"
        self.backend1.get.assert_called_once_with("key1")
        self.backend2.get.assert_not_called()

    def test_get_dictionary_input_returns_value_from_first_backend(self):
        data = {"name": "test", "id": 123}
        self.backend1.get.return_value = data
        result = self.tiered_cache.get("key2")
        assert result == data
        self.backend1.get.assert_called_once_with("key2")
        self.backend2.get.assert_not_called()

    def test_get_string_input_propagates_from_second_backend_to_first(self):
        self.backend1.get.return_value = None
        self.backend2.get.return_value = "value1"
        result = self.tiered_cache.get("key1")
        assert result == "value1"
        self.backend1.get.assert_called_once_with("key1")
        self.backend2.get.assert_called_once_with("key1")
        self.backend1.set.assert_called_once_with("key1", "value1")

    def test_get_dictionary_input_propagates_from_second_backend_to_first(self):
        data = {"name": "test", "id": 123}
        self.backend1.get.return_value = None
        self.backend2.get.return_value = data
        result = self.tiered_cache.get("key2")
        assert result == data
        self.backend1.get.assert_called_once_with("key2")
        self.backend2.get.assert_called_once_with("key2")
        self.backend1.set.assert_called_once_with("key2", data)

    def test_get_nonexistent_key_returns_none(self):
        self.backend1.get.return_value = None
        self.backend2.get.return_value = None
        result = self.tiered_cache.get("nonexistent")
        assert result is None

    def test_remove_string_key_calls_all_backends(self):
        self.tiered_cache.remove("key1")
        self.backend1.remove.assert_called_once_with("key1")
        self.backend2.remove.assert_called_once_with("key1")

    def test_remove_dictionary_key_calls_all_backends(self):
        self.tiered_cache.remove("key2")
        self.backend1.remove.assert_called_once_with("key2")
        self.backend2.remove.assert_called_once_with("key2")

    def test_get_with_three_backends_propagates_to_earlier_backends(self):
        backend3 = Mock()
        tiered_cache = TieredCache([self.backend1, self.backend2, backend3])

        self.backend1.get.return_value = None
        self.backend2.get.return_value = None
        backend3.get.return_value = "value1"

        result = tiered_cache.get("key1")
        assert result == "value1"

        self.backend1.set.assert_called_once_with("key1", "value1")
        self.backend2.set.assert_called_once_with("key1", "value1")
        backend3.set.assert_not_called()
