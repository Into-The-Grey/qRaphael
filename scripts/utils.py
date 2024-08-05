# scripts/utils.py

import logging


def setup_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    return logger
