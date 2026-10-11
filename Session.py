from dataclasses import dataclass


@dataclass
class StudySession:
    topic: str
    date: str
    duration: int
    note: str = ""

    def __post_init__(self):
        if not isinstance(self.topic, str):
            raise TypeError("topic must be a string")
        if not self.topic:
            raise ValueError("topic is required")

        if not isinstance(self.date, str):
            raise TypeError("date must be a string")
        if not self.date:
            raise ValueError("date is required")

        if not isinstance(self.duration, int):
            raise TypeError("duration must be an integer")
        if self.duration <= 0:
            raise ValueError("duration must be positive")


    def to_dict(self) -> dict[str, str | int]:
        return {"topic": self.topic,
                "date": self.date,
                "duration": self.duration,
                "note": self.note}

