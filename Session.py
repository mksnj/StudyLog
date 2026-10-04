class StudySession:
    def __init__(self, topic, date, duration, note=""):
        if not isinstance(topic, str):
            raise TypeError("topic must be a string")
        if not topic:
            raise ValueError("topic is required")

        if not isinstance(date, str):
            raise TypeError("date must be a string")
        if not date:
            raise ValueError("date is required")

        if not isinstance(duration, int):
            raise TypeError("duration must be an integer")
        if duration <= 0:
            raise ValueError("duration must be positive")

        self.topic = topic
        self.date = date
        self.duration = duration
        self.note = note

    def to_dict(self):
        return {"topic": self.topic,
                "date": self.date,
                "duration": self.duration,
                "note": self.note}

    def __str__(self):
        return (f"{self.topic} — {self.date}, "
                f"{self.duration} min, note: {self.note}")

    def __repr__(self):
        return (
            f"StudySession("
            f"topic={self.topic!r}, "
            f"date={self.date!r}, "
            f"duration={self.duration!r}, "
            f"note={self.note!r})"
        )