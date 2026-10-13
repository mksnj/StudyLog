import sqlite3

from pathlib import Path

print("Рабочая директория:", Path.cwd())
print("Путь к базе данных:", Path("practice.db").resolve())

connection = sqlite3.connect("practice.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY,
        topic TEXT NOT NULL,
        duration INTEGER NOT NULL
    )
""")

# connection.commit()

# result = connection.execute(
#     "SELECT name FROM sqlite_master WHERE type = 'table'"
# )
# print(result.fetchall())

# connection.execute(
#     "INSERT INTO study_sessions (topic, duration) VALUES ('Python', 60);"
# )
#
# connection.execute(
#     "INSERT INTO study_sessions (topic, duration) VALUES (?, ?)",
#     ("SQL", 90)
# )

connection.execute(
    """
    INSERT INTO study_sessions (topic, duration) VALUES (?, ?)
    """,
    ("RollbackTest", 15)
)

# connection.commit()

result = connection.execute("SELECT * FROM study_sessions")
sessions = result.fetchall()
print(sessions)

connection.rollback()

result = connection.execute("SELECT * FROM study_sessions")
sessions = result.fetchall()
print(sessions)

connection.close()