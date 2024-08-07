import model_loader
import argparse
import json
import logging
import os
import torch
import tensorflow as tf
from dotenv import load_dotenv
from transformers import AutoTokenizer
from logic.text_chat_logic import get_followup_message
from logic.utils import load_config, handle_raphael_identity, handle_suggestions
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
)

# Suppress TensorFlow warnings and errors
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.get_logger().setLevel("ERROR")

# Load environment variables from .env file
load_dotenv()

# Load generation parameters from the configuration file
CONFIG_FILE = "/home/ncacord/qRaphael/config/text_gen_config.json"
PARSE_CONFIG_FILE = "/home/ncacord/qRaphael/config/parse_config.json"
LOG_DIR = "/home/ncacord/qRaphael/logs/standard/"
LOG_FILE = os.path.join(LOG_DIR, "text_generation_logs.log")


def load_parse_config(parse_config_file):
    type_mapping = {"str": str, "int": int, "float": float, "bool": bool}
    with open(parse_config_file, "r") as f:
        parse_config = json.load(f)
    parser = argparse.ArgumentParser(description=parse_config["description"])
    for arg in parse_config["arguments"]:
        if "action" in arg and arg["action"] == "store_true":
            parser.add_argument(arg["name"], action=arg["action"], help=arg["help"])
        else:
            arg_type = type_mapping.get(arg.get("type", "str"), str)
            kwargs = {k: v for k, v in arg.items() if k != "name" and k != "type"}
            parser.add_argument(arg["name"], type=arg_type, **kwargs)
    return parser.parse_args()


args = load_parse_config(PARSE_CONFIG_FILE)

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
log_level = getattr(logging, args.log_level.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levellevel)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def fetch_user_data(user_id, conn):
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
    return (
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
    combined_prompt = (
        f"{user_memory}\n{prompt}\nUser Details: {json.dumps(user_details)}\n"
        f"User Preferences: {json.dumps(user_preferences)}\nUser Medical: {json.dumps(user_medical)}\n"
        f"User Financial: {json.dumps(user_financial)}\nUser Professional: {json.dumps(user_professional)}\n"
        f"User Education: {json.dumps(user_education)}\nUser Social: {json.dumps(user_social)}\n"
        f"User Security: {json.dumps(user_security)}\nUser Miscellaneous: {json.dumps(user_miscellaneous)}\n"
        f"User Interests: {json.dumps(user_interests)}"
    )
    inputs = tokenizer(combined_prompt, return_tensors="pt").to(
        "cuda" if torch.cuda.is_available() else "cpu"
    )
    outputs = model.generate(
        inputs.input_ids,
        max_length=config["max_length"],
        max_time=config["max_time"],
        do_sample=config["do_sample"],
        temperature=config["temperature"],
        top_k=config["top_k"],
        top_p=config["top_p"],
        repetition_penalty=config["repetition_penalty"],
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    end_punctuation = [".", "!", "?"]
    for punct in end_punctuation:
        if punct in generated_text:
            generated_text = generated_text[: generated_text.rfind(punct) + 1]
            break
    return generated_text


def main():
    logger.info("Starting text generation...")
    tokenizer = model_loader.tokenizer
    model = model_loader.model
    config = load_config(CONFIG_FILE)
    conn = connect_db()
    user_id = args.user_id
    (
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
    ) = fetch_user_data(user_id, conn)
    user_name = fetch_user_name(user_id, conn)

    if args.loop:
        try:
            while True:
                prompt = input("Enter a prompt: ")
                if not prompt.strip():
                    continue
                if (
                    "what is your name" in prompt.lower()
                    or "what can you do" in prompt.lower()
                    or "help" in prompt.lower()
                ):
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
                user_memory += "\n" + prompt + "\n" + generated_text
                save_user_memory(user_id, prompt + "\n" + generated_text, conn)
                followup_message = get_followup_message(prompt, generated_text)
                print(followup_message)
        except KeyboardInterrupt:
            print("\nExiting loop mode.")
            logger.info("Exiting loop mode.")
    else:
        if args.prompt:
            if (
                "what is your name" in args.prompt.lower()
                or "what can you do" in args.prompt.lower()
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
            user_memory += "\n" + args.prompt + "\n" + generated_text
            save_user_memory(user_id, args.prompt + "\n" + generated_text, conn)
        else:
            print(
                "Error: You must provide a prompt with --prompt or use --loop for interactive mode."
            )
            logger.error("No prompt provided and --loop not specified.")


if __name__ == "__main__":
    main()
