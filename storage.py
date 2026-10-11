import json
from pathlib import Path
from Session import StudySession
import logging


logger = logging.getLogger(__name__)
default_path = "sessions.json"


def load_sessions(path: str | Path = default_path) -> list[StudySession] | None:
    sessions_list: list[StudySession] = []
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
                except (TypeError, ValueError) as error_reason:
                    logger.warning(
                        "Skipped invalid session: %s; reason: %s",
                        raw_session,
                        error_reason,
                    )
                else:
                    sessions_list.append(session)

    return sessions_list


def save_sessions(sessions_list: list[StudySession], path: str | Path = default_path) -> None:
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

