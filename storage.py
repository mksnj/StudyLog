import json
from pathlib import Path


default_path = "sessions.json"


def load_sessions(path = default_path):
    sessions_list = []
    if Path(path).is_file():
        try:
            with open(path, 'r') as file:
                sessions_list = json.load(file)
        except json.decoder.JSONDecodeError:
            return None

    return sessions_list


def save_sessions(sessions_list, path = default_path):
    with open(path, 'w') as file:
        json.dump(sessions_list, file)



