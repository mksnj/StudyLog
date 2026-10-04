def get_duration(sessions_list):
    total_duration = 0
    for session in sessions_list:
        total_duration += session["duration"]

    return total_duration


def get_duration_by_date(sessions_list):
    duration_by_date = {}
    for session in sessions_list:
        if session["date"] not in duration_by_date:
            duration_by_date[session["date"]] = session["duration"]
        else:
            duration_by_date[session["date"]] += session["duration"]
    return duration_by_date