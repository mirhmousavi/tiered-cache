from .logger import logger


class ErrorHandler:
    """This class handles specified errors in the init method and emits a warning if the error raises."""

    def __init__(self, *errors_to_handle):
        self.errors_to_handle = errors_to_handle

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            for error_type in self.errors_to_handle:
                if issubclass(exc_type, error_type):
                    logger.warning(
                        f"[tiered-cache] Error suppressed: {exc_type!r}({exc_value})"
                    )
                    return True
