import json


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


def handle_raphael_identity():
    """
    Handle questions about Raphael's identity and capabilities.

    Returns:
    - str: Raphael's identity and capabilities.
    """
    from logic.model_memory_logic import get_raphael_identity

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
    from logic.model_memory_logic import get_suggestions

    suggestions = get_suggestions(user_preferences)
    response = "Here are some suggestions for you:\n"
    for suggestion in suggestions:
        response += f"- {suggestion}\n"
    return response
