import logging

logger = logging.getLogger("tiered-cache")
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.WARNING)
