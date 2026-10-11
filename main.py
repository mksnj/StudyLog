import cli
import storage
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

def main():

    filepath = input("enter the file path:").strip()
    if not filepath:
        filepath = storage.default_path
    sessions_list = storage.load_sessions(filepath)
    if sessions_list is None:
        print("file is wrong")
        return
    cli.get_menu(sessions_list)
    storage.save_sessions(sessions_list, filepath)


if __name__ == "__main__":
    main()
