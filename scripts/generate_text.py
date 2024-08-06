import argparse
import logging
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
from logic.text_chat_logic import get_followup_message
from logic.model_memory_logic import (
    connect_db,
    fetch_user_memory,
    save_user_memory,
    fetch_user_details,
    fetch_user_preferences,
    fetch_medical_conditions,
    fetch_medications,
    fetch_immunizations,
    fetch_doctor_visits,
    fetch_insurance_info,
    fetch_health_metrics,
    fetch_investments,
    fetch_retirement_accounts,
    fetch_tax_information,
    fetch_expense_tracking,
    fetch_cards,
    fetch_bank_accounts,
    fetch_loans,
    fetch_salaries,
    fetch_debts,
    fetch_professional_info,
    fetch_educational_data,
    fetch_preferences_interests,
    fetch_social_connections,
    fetch_security_info,
    fetch_miscellaneous_info,
    fetch_user_name,
    update_user_name,
    get_raphael_identity,
    get_suggestions,
)

# Suppress TensorFlow warnings and errors
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

tf.get_logger().setLevel("ERROR")

# Load environment variables from .env file
load_dotenv()

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
    "--user_id",
    type=str,
    required=True,
    help="Unique identifier for the user to maintain session memory.",
)
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


def generate_text(
    prompt,
    model,
    tokenizer,
    config,
    user_memory,
    user_details,
    user_preferences,
    user_medical,
    user_financial,
    user_professional,
    user_education,
    user_social,
    user_security,
    user_miscellaneous,
    user_interests,
):
    """
    Generate text based on the provided prompt, user memory, and user details.

    Args:
    - prompt (str): The prompt to generate text from.
    - model: The model used for text generation.
    - tokenizer: The tokenizer used for text generation.
    - config (dict): The generation configuration parameters.
    - user_memory (str): The user's conversation history.
    - user_details (dict): The user's personal details.
    - user_preferences (dict): The user's preferences.
    - user_medical (dict): The user's medical details.
    - user_financial (dict): The user's financial details.
    - user_professional (dict): The user's professional details.
    - user_education (dict): The user's educational details.
    - user_social (dict): The user's social details.
    - user_security (dict): The user's security details.
    - user_miscellaneous (dict): The user's miscellaneous details.
    - user_interests (dict): The user's preferences and interests.

    Returns:
    - str: The generated text.
    """
    combined_prompt = (
        user_memory
        + "\n"
        + prompt
        + "\n"
        + "User Details: "
        + json.dumps(user_details)
        + "\n"
        + "User Preferences: "
        + json.dumps(user_preferences)
        + "\n"
        + "User Medical: "
        + json.dumps(user_medical)
        + "\n"
        + "User Financial: "
        + json.dumps(user_financial)
        + "\n"
        + "User Professional: "
        + json.dumps(user_professional)
        + "\n"
        + "User Education: "
        + json.dumps(user_education)
        + "\n"
        + "User Social: "
        + json.dumps(user_social)
        + "\n"
        + "User Security: "
        + json.dumps(user_security)
        + "\n"
        + "User Miscellaneous: "
        + json.dumps(user_miscellaneous)
        + "\n"
        + "User Interests: "
        + json.dumps(user_interests)
    )

    inputs = tokenizer(combined_prompt, return_tensors="pt").to(
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


def handle_raphael_identity():
    """
    Handle questions about Raphael's identity and capabilities.

    Returns:
    - str: Raphael's identity and capabilities.
    """
    identity = get_raphael_identity()
    response = f"My name is {identity['name']}, and I am {identity['role']}. Here are some things I can do:\n"
    for capability in identity["capabilities"]:
        response += f"- {capability}\n"
    return response


def handle_suggestions(user_preferences):
    """
    Handle requests for suggestions based on user preferences.

    Args:
    - user_preferences (dict): The user's preferences.

    Returns:
    - str: Suggestions for the user.
    """
    suggestions = get_suggestions(user_preferences)
    response = "Here are some suggestions for you:\n"
    for suggestion in suggestions:
        response += f"- {suggestion}\n"
    return response


def main():
    """
    Main function to generate text based on a provided prompt or run in loop mode.
    """
    logger.info("Starting text generation...")
    tokenizer, model = load_model_and_tokenizer(MODEL_SAVE_DIR)
    config = load_config(CONFIG_FILE)
    conn = connect_db()

    user_id = args.user_id
    user_memory = fetch_user_memory(user_id, conn)
    user_details = fetch_user_details(user_id, conn)
    user_preferences = fetch_user_preferences(user_id, conn)
    user_medical = {
        "conditions": fetch_medical_conditions(user_id, conn),
        "medications": fetch_medications(user_id, conn),
        "immunizations": fetch_immunizations(user_id, conn),
        "doctor_visits": fetch_doctor_visits(user_id, conn),
        "insurance_info": fetch_insurance_info(user_id, conn),
        "health_metrics": fetch_health_metrics(user_id, conn),
    }
    user_financial = {
        "investments": fetch_investments(user_id, conn),
        "retirement_accounts": fetch_retirement_accounts(user_id, conn),
        "tax_information": fetch_tax_information(user_id, conn),
        "expense_tracking": fetch_expense_tracking(user_id, conn),
        "cards": fetch_cards(user_id, conn),
        "bank_accounts": fetch_bank_accounts(user_id, conn),
        "loans": fetch_loans(user_id, conn),
        "salaries": fetch_salaries(user_id, conn),
        "debts": fetch_debts(user_id, conn),
    }
    user_professional = fetch_professional_info(user_id, conn)
    user_education = fetch_educational_data(user_id, conn)
    user_social = fetch_social_connections(user_id, conn)
    user_security = fetch_security_info(user_id, conn)
    user_miscellaneous = fetch_miscellaneous_info(user_id, conn)
    user_interests = fetch_preferences_interests(user_id, conn)

    user_name = fetch_user_name(user_id, conn)

    if args.loop:
        try:
            while True:
                prompt = input("Enter a prompt: ")
                if not prompt.strip():
                    continue

                if "what is your name" in prompt.lower():
                    print(handle_raphael_identity())
                    continue

                if "what can you do" in prompt.lower() or "help" in prompt.lower():
                    print(handle_raphael_identity())
                    continue

                if "suggest" in prompt.lower() or "what should I do" in prompt.lower():
                    print(handle_suggestions(user_preferences))
                    continue

                if "my name is" in prompt.lower():
                    user_name = prompt.split("is")[-1].strip()
                    update_user_name(user_id, user_name, conn)
                    print(f"Nice to meet you, {user_name}!")
                    continue

                if user_name:
                    prompt = f"{user_name}, {prompt}"

                generated_text = generate_text(
                    prompt,
                    model,
                    tokenizer,
                    config,
                    user_memory,
                    user_details,
                    user_preferences,
                    user_medical,
                    user_financial,
                    user_professional,
                    user_education,
                    user_social,
                    user_security,
                    user_miscellaneous,
                    user_interests,
                )
                print(generated_text)
                logger.info(f"Generated text for prompt '{prompt}': {generated_text}")

                # Update user memory
                user_memory += "\n" + prompt + "\n" + generated_text
                save_user_memory(user_id, prompt + "\n" + generated_text, conn)

                # Get the follow-up message
                followup_message = get_followup_message(prompt, generated_text)
                print(followup_message)
        except KeyboardInterrupt:
            print("\nExiting loop mode.")
            logger.info("Exiting loop mode.")
    else:
        if args.prompt:
            if "what is your name" in args.prompt.lower():
                print(handle_raphael_identity())
                return

            if (
                "what can you do" in args.prompt.lower()
                or "help" in args.prompt.lower()
            ):
                print(handle_raphael_identity())
                return

            if (
                "suggest" in args.prompt.lower()
                or "what should I do" in args.prompt.lower()
            ):
                print(handle_suggestions(user_preferences))
                return

            if "my name is" in args.prompt.lower():
                user_name = args.prompt.split("is")[-1].strip()
                update_user_name(user_id, user_name, conn)
                print(f"Nice to meet you, {user_name}!")
                return

            if user_name:
                args.prompt = f"{user_name}, {args.prompt}"

            generated_text = generate_text(
                args.prompt,
                model,
                tokenizer,
                config,
                user_memory,
                user_details,
                user_preferences,
                user_medical,
                user_financial,
                user_professional,
                user_education,
                user_social,
                user_security,
                user_miscellaneous,
                user_interests,
            )
            print(generated_text)
            logger.info(f"Generated text for prompt '{args.prompt}': {generated_text}")

            # Update user memory
            user_memory += "\n" + args.prompt + "\n" + generated_text
            save_user_memory(user_id, args.prompt + "\n" + generated_text, conn)
        else:
            print(
                "Error: You must provide a prompt with --prompt or use --loop for interactive mode."
            )
            logger.error("No prompt provided and --loop not specified.")


if __name__ == "__main__":
    main()
