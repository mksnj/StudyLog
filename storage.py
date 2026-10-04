import json
from pathlib import Path
from Session import StudySession


default_path = "sessions.json"


def load_sessions(path = default_path):
    sessions_list = []
    raw_sessions_list = []
    if Path(path).is_file():
        try:
            with open(path, 'r') as file:
                raw_sessions_list = json.load(file)
        except json.decoder.JSONDecodeError:
            return None
        else:
            for raw_session in raw_sessions_list:
                topic = raw_session.get("topic")
                date = raw_session.get("date")
                duration = raw_session.get("duration")
                note = raw_session.get("note", "")

                try:
                    session = StudySession(topic, date, duration, note)
                except (TypeError, ValueError) as error:
                    print(f"Skipped invalid session: {raw_session}")
                    print(f"Reason: {error}")
                else:
                    sessions_list.append(session)

    return sessions_list


def save_sessions(sessions_list, path = default_path):
    output_sessions_list = []
    for session in sessions_list:
        output_sessions_list.append(session.to_dict())
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(
            output_sessions_list,
            file,
            indent=2,
            ensure_ascii=False
        )



