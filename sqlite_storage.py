from pathlib import Path
import sqlite3
from Session import StudySession


default_path = "study_log.db"


def init_db(path: str | Path = default_path) -> None:
    connection = sqlite3.connect(path)

    try:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY,
            topic TEXT NOT NULL,
            date TEXT NOT NULL,
            duration INTEGER NOT NULL CHECK (duration>0),
            note TEXT NOT NULL DEFAULT ''
            )
            """
        )


        connection.commit()

    finally:
        connection.close()


def add_session(session: StudySession,
                path : str | Path = default_path) -> None:
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            INSERT INTO study_sessions (topic, date, duration, note)
            VALUES (?, ?, ?, ?)
            """,
            (session.topic, session.date, session.duration, session.note)
        )
        connection.commit()

    finally:
        connection.close()


def load_sessions(path: str | Path = default_path) -> list[StudySession]:
    connection = sqlite3.connect(path)
    try:
        cursor = connection.execute("SELECT topic, date, duration, note "
                                    "FROM study_sessions "
                                    "ORDER BY id")
        sessions = cursor.fetchall()
        res_sessions: list[StudySession] = []
        for session in sessions:
            new_session = StudySession(*session)
            res_sessions.append(new_session)

        return res_sessions

    finally:
        connection.close()