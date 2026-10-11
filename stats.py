from Session import StudySession


def get_duration(sessions_list: list[StudySession]) -> int:
    total_duration = 0
    for session in sessions_list:
        total_duration += session.duration

    return total_duration


def get_duration_by_date(sessions_list: list[StudySession]) -> dict[str, int]:
    duration_by_date = {}
    for session in sessions_list:
        duration_by_date[session.date] = duration_by_date.get(session.date, 0) + session.duration
    return duration_by_date
