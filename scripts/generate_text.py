import argparse
import logging
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Suppress TensorFlow warnings and errors
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

tf.get_logger().setLevel("ERROR")

# Import the follow-up message logic
from logic.text_chat_logic import get_followup_message

# Load generation parameters from the configuration file
CONFIG_FILE = "/home/ncacord/qRaphael/config/text_gen_config.json"

# Define constants
MODEL_SAVE_DIR = "/home/ncacord/qRaphael/models/qRaphael-2b-it"
LOG_DIR = "/home/ncacord/qRaphael/logs/standard/"
LOG_FILE = os.path.join(LOG_DIR, "text_generation_logs.log")

# Argument parser setup
parser = argparse.ArgumentParser(description="Generate text using a quantized model.")
parser.add_argument("--prompt", type=str, help="The prompt to generate text from.")
parser.add_argument(
    "--max_length",
    type=int,
    default=50,
    help="The maximum length of the generated text.",
)
parser.add_argument(
    "--log_level",
    type=str,
    default="INFO",
    help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
)
parser.add_argument(
    "--loop",
    action="store_true",
    help="Run in loop mode for interactive text generation.",
)
args = parser.parse_args()

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
log_level = getattr(logging, args.log_level.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def load_model_and_tokenizer(model_dir):
    """
    Load the model and tokenizer from the specified directory.

    Args:
    - model_dir (str): The directory where the model and tokenizer are saved.

    Returns:
    - tokenizer: The tokenizer associated with the model.
    - model: The loaded model.
    """
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    logger.info("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_dir)

    return tokenizer, model


def load_config(config_file):
    """
    Load the configuration parameters from a JSON file.

    Args:
    - config_file (str): Path to the configuration file.

    Returns:
    - dict: The configuration parameters.
    """
    with open(config_file, "r") as file:
        config = json.load(file)
    return config


def generate_text(prompt, model, tokenizer, config):
    """
    Generate text based on the provided prompt.

    Args:
    - prompt (str): The prompt to generate text from.
    - model: The model used for text generation.
    - tokenizer: The tokenizer used for text generation.
    - config (dict): The generation configuration parameters.

    Returns:
    - str: The generated text.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(
        "cuda" if torch.cuda.is_available() else "cpu"
    )
    outputs = model.generate(
        inputs.input_ids,
        max_length=config["max_length"],
        do_sample=config["do_sample"],
        temperature=config["temperature"],
        top_k=config["top_k"],
        top_p=config["top_p"],
        repetition_penalty=config["repetition_penalty"],
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-process the text to ensure it ends at a sensible point
    end_punctuation = [".", "!", "?"]
    for punct in end_punctuation:
        if punct in generated_text:
            generated_text = generated_text[: generated_text.rfind(punct) + 1]
            break

    return generated_text


def main():
    """
    Main function to generate text based on a provided prompt or run in loop mode.
    """
    logger.info("Starting text generation...")
    tokenizer, model = load_model_and_tokenizer(MODEL_SAVE_DIR)
    config = load_config(CONFIG_FILE)

    if args.loop:
        try:
            while True:
                prompt = input("Enter a prompt: ")
                if not prompt.strip():
                    continue
                generated_text = generate_text(prompt, model, tokenizer, config)
                print(generated_text)
                logger.info(f"Generated text for prompt '{prompt}': {generated_text}")

                # Get the follow-up message
                followup_message = get_followup_message(prompt, generated_text)
                print(followup_message)
        except KeyboardInterrupt:
            print("\nExiting loop mode.")
            logger.info("Exiting loop mode.")
    else:
        if args.prompt:
            generated_text = generate_text(args.prompt, model, tokenizer, config)
            print(generated_text)
            logger.info(f"Generated text for prompt '{args.prompt}': {generated_text}")
        else:
            print(
                "Error: You must provide a prompt with --prompt or use --loop for interactive mode."
            )
            logger.error("No prompt provided and --loop not specified.")


if __name__ == "__main__":
    main()
