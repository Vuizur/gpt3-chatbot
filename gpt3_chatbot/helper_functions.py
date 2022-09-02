# Loads a json file with the settings for the conversation
import json


def load_config_json(file_path: str = None, DEFAULT_JSON_PATH = "characters/default.json") -> dict[str, any]:
    # Load the default settings into a dictionary
    json_dict: dict[str, any] = {}
    with open(DEFAULT_JSON_PATH, "r", encoding="utf-8") as f:
        json_dict = json.load(f)

    # If a file path is given, load the settings from the file
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            json_dict.update(json.load(f))

    return json_dict


def load_key():
    with open("openai-key.txt", "r", encoding="utf-8") as f:
        return f.readline()