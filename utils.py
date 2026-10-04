def validate_duration(duration):
    try:
        duration = int(duration)
    except ValueError:
        return None
    else:
        if duration > 0:
            return duration
        else:
            return None

