import cli
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

    sqlite_storage.init_db(filepath)
    sessions_list = sqlite_storage.load_sessions(filepath)

    def save_session(session: StudySession) -> None:
        sqlite_storage.add_session(session, filepath)

    cli.get_menu(sessions_list, save_session)



if __name__ == "__main__":
    main()
