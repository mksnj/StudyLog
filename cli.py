import stats
import utils
from Session import StudySession

def get_menu(sessions_list: list[StudySession]) -> None:
    valid_actions = {
        "1": check_sessions,
        "2": add_session,
        "3": get_info,
        "4": filter_sessions,
        "5": sort_sessions,

    }

    flag = True
    while flag:
        print("\n--- Study Log ---\n")
        print("1.\tCheck sessions")
        print("2.\tAdd new session")
        print("3.\tGet info")
        print("4.\tGet filtered sessions")
        print("5.\tGet sorted sessions")
        print("6.\tExit\n")

        choice = input("Enter your choice: ")
        if choice in valid_actions:
            action = valid_actions.get(choice)
            action(sessions_list)
        elif choice == "6":
            flag = False
        else:
            print("Invalid choice\n")


def check_sessions(sessions_list: list[StudySession]) -> None:
    print("\n--- Checking sessions: ---")
    if not sessions_list:
        print("There are no sessions")
    else:
        for session in sessions_list:
            print(f"topic:\t{session.topic};\t"
                  f"date:\t{session.date};\t"
                  f"duration:\t{session.duration};\t"
                  f"note:\t{session.note}")


def add_session(sessions_list: list[StudySession]) -> None:
    topic = input("Enter topic: ")
    date = input("Enter date: ")
    duration = input("Enter duration: ")
    duration = utils.validate_duration(duration)

    if duration is None:
        print("Invalid duration\n")
        return

    note = input("Enter note: ")

    try:
        session = StudySession(topic, date, duration, note)
    except (TypeError, ValueError) as error:
        print(f"Skipped invalid session; Reason: {error}")
        return

    sessions_list.append(session)


def get_info(sessions_list: list[StudySession]) -> None:
    total_duration = stats.get_duration(sessions_list)
    print("there are ", len(sessions_list), " sessions")
    if sessions_list:
        print("total duration:\t", total_duration, "mins" 
              " = ", total_duration // 60, "h ", total_duration % 60, "mins")
        print(stats.get_duration_by_date(sessions_list))
    print("btw this prog was made by frog 0_o")


def filter_sessions(
        sessions_list: list[StudySession],
        choice: str | None = None,
        chosen_topic: str | int | None = None
) -> list[StudySession]:

    if choice is None:
        choice = input("Enter parameter you need to filter by: ")
    choice = choice.strip().lower()
    valid_choices = ["topic", "date", "duration"]

    if choice in valid_choices:
        if chosen_topic is None:
            chosen_topic = input(f"Enter {choice} you need to filter by: ")


        if choice != "duration":
            if not isinstance(chosen_topic, str):
                raise TypeError("Invalid type: value must be a string")

            chosen_topic = chosen_topic.strip().lower()
            filtered_sessions = [session for session in sessions_list if getattr(session, choice).strip().lower() == chosen_topic]
        else:
            validated_duration = utils.validate_duration(chosen_topic)
            if validated_duration is None:
                raise ValueError("Invalid duration")
            filtered_sessions = [session for session in sessions_list if getattr(session, choice) == validated_duration]
        if filtered_sessions:
            filtered_duration = stats.get_duration(filtered_sessions)

            print(filtered_sessions)
            print("duration of this sessions = ", filtered_duration, "mins")
            return filtered_sessions
        else:
            print("No sessions found\n")
            return []
    else:
        raise ValueError("Invalid choice of topic")


def sort_sessions(sessions_list: list[StudySession]) -> None:
    choice = input("Enter parameter you need to sort by: ").lower()
    valid_choices = ["topic", "date", "duration"]

    if choice in valid_choices:
        sorted_sessions = sorted(sessions_list, key = lambda x: getattr(x, choice))
        if sorted_sessions:
            for index, session in enumerate(sorted_sessions):
                print(f"#{index}, {session}\t")
        else:
            print("No sessions found\n")
    else:
        print("Invalid choice")
        return
