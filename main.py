import cli
import storage
import sqlite_storage
import logging

from Session import StudySession

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

def main():



    filepath = input("enter the file path:").strip()
    if not filepath:
        filepath = sqlite_storage.default_path

    # sqlite_storage.add_session(
    #     StudySession("Databases",
    #                  "2026-10-13",
    #                  90,
    #                  "sqlite3"),
    #     filepath)

    sessions_list = sqlite_storage.load_sessions(filepath)
    if sessions_list is None:
        print("file is wrong")
        return
    cli.get_menu(sessions_list)
    storage.save_sessions(sessions_list, filepath)


if __name__ == "__main__":
    main()
