# scripts/model_loader.py

import logging
import os
import signal
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

# Suppress TensorFlow warnings and errors
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Load environment variables from .env file
load_dotenv()

# Define constants
MODEL_SAVE_DIR = "/home/ncacord/qRaphael/models/qRaphael-2b-it"
LOG_DIR = "/home/ncacord/qRaphael/logs/standard/"
LOG_FILE = os.path.join(LOG_DIR, "model_loader_logs.log")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def load_model_and_tokenizer(model_dir):
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    logger.info("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_dir)

    return tokenizer, model


def signal_handler(sig, frame):
    logger.info("Received termination signal. Shutting down gracefully...")
    # Perform any necessary cleanup here
    sys.exit(0)


if __name__ == "__main__":
    logger.info("Starting model loader...")
    tokenizer, model = load_model_and_tokenizer(MODEL_SAVE_DIR)
    logger.info("Model and tokenizer loaded successfully.")

    # Setting up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Keeping the script running to keep the model loaded
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Model loader script stopped.")
