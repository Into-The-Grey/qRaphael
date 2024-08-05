# tests/test_environment.py

import sys
import os
import logging
from scripts.utils import setup_logging


def test_python_version():
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 12


def test_logging_configuration(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logging(log_file)

    test_message = "This is a test log message."
    logger.info(test_message)

    # Ensure all handlers are flushed
    for handler in logger.handlers:
        handler.flush()

    with open(log_file, "r") as file:
        log_contents = file.read()

    assert test_message in log_contents
