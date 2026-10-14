import sqlite3
from pathlib import Path

import pytest

import sqlite_storage
from Session import StudySession


def test_init_db(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"

    sqlite_storage.init_db(db_path)
    sqlite_storage.init_db(db_path)

    assert db_path.is_file()

    sessions = sqlite_storage.load_sessions(db_path)
    assert sessions == []


def test_add_and_load_session(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"

    sqlite_storage.init_db(db_path)
    sqlite_storage.add_session(StudySession("python", "2026-10-14", 80, "maks2"), db_path)
    sessions = sqlite_storage.load_sessions(db_path)

    assert sessions == [StudySession("python", "2026-10-14", 80, "maks2")]


def test_invalid_duration(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    sqlite_storage.init_db(db_path)
    connection = sqlite3.connect(db_path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO study_sessions (topic, date, duration, note)
                VALUES (?, ?, ?, ?)
                """,
                ("python", "2026-10-14", -80, "maks2")
            )

        cursor = connection.execute(
            "SELECT COUNT(*) FROM study_sessions"
        )
        count = cursor.fetchone()[0]

        assert count == 0
    finally:
        connection.close()

def test_save_three_valid_sessions(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    sqlite_storage.init_db(db_path)
    expected_sessions = [
        StudySession("python", "2026-10-14", 80, "croak"),
        StudySession("sqlite", "2026-10-14", 120, ""),
        StudySession("1c", "2026-10-14", 160, "meow"),
    ]
    for session in expected_sessions:
        sqlite_storage.add_session(session, db_path)

    assert sqlite_storage.load_sessions(db_path) == expected_sessions
