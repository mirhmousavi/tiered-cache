import pytest
from unittest.mock import patch
from src.tiered_cache.error_handler import ErrorHandler


class TestErrorHandler:
    def test_suppresses_specified_error_type(self):
        with ErrorHandler(ValueError):
            raise ValueError("Test error")

    def test_suppresses_multiple_specified_error_types(self):
        with ErrorHandler(ValueError, TypeError):
            raise ValueError("Test error")

        with ErrorHandler(ValueError, TypeError):
            raise TypeError("Test error")

    def test_suppresses_subclass_of_specified_error_type(self):
        class CustomError(ValueError):
            pass

        with ErrorHandler(ValueError):
            raise CustomError("Test error")

    def test_allows_unspecified_error_to_propagate(self):
        with pytest.raises(RuntimeError):
            with ErrorHandler(ValueError):
                raise RuntimeError("Test error")

    def test_allows_unspecified_error_among_multiple_to_propagate(self):
        with pytest.raises(RuntimeError):
            with ErrorHandler(ValueError, TypeError):
                raise RuntimeError("Test error")

    def test_no_error_raised_executes_normally(self):
        result = None
        with ErrorHandler(ValueError):
            result = "success"
        assert result == "success"

    @patch("src.tiered_cache.error_handler.logger")
    def test_logs_warning_when_suppressing_error(self, mock_logger):
        with ErrorHandler(ValueError):
            raise ValueError("Test error message")

        mock_logger.warning.assert_called_once_with(
            "[tiered-cache] Error suppressed: <class 'ValueError'>(Test error message)"
        )

    @patch("src.tiered_cache.error_handler.logger")
    def test_logs_warning_with_correct_error_details(self, mock_logger):
        with ErrorHandler(TypeError):
            raise TypeError("Custom type error")

        mock_logger.warning.assert_called_once_with(
            "[tiered-cache] Error suppressed: <class 'TypeError'>(Custom type error)"
        )

    @patch("src.tiered_cache.error_handler.logger")
    def test_does_not_log_when_no_error_raised(self, mock_logger):
        with ErrorHandler(ValueError):
            pass

        mock_logger.warning.assert_not_called()

    @patch("src.tiered_cache.error_handler.logger")
    def test_does_not_log_when_unhandled_error_propagates(self, mock_logger):
        with pytest.raises(RuntimeError):
            with ErrorHandler(ValueError):
                raise RuntimeError("Test error")

        mock_logger.warning.assert_not_called()

    def test_context_manager_returns_self(self):
        error_handler = ErrorHandler(ValueError)
        with error_handler as handler:
            assert handler is error_handler

    def test_handles_multiple_error_instances_in_sequence(self):
        with ErrorHandler(ValueError):
            raise ValueError("First error")

        with ErrorHandler(ValueError):
            raise ValueError("Second error")

    @patch("src.tiered_cache.error_handler.logger")
    def test_suppresses_error_with_no_message(self, mock_logger):
        with ErrorHandler(ValueError):
            raise ValueError()

        mock_logger.warning.assert_called_once_with(
            "[tiered-cache] Error suppressed: <class 'ValueError'>()"
        )
