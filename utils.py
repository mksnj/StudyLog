def validate_duration(duration: str| int| None) -> int | None:
    try:
        validated_duration = int(duration)
    except (ValueError, TypeError):
        return None
    else:
        if validated_duration > 0:
            return validated_duration
        else:
            return None

