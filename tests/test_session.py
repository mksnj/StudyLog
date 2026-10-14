import pytest

from Session import StudySession
from stats import get_duration
from stats import get_duration_by_date
from cli import filter_sessions
from utils import validate_duration
from legacy.storage import load_sessions
from legacy.storage import save_sessions


def test_session():
    new_session = StudySession("Python", "2026-10-06", 60,)
    assert new_session.topic == "Python"



@pytest.mark.parametrize("duration", [x for x in range(-5, 1)])
def test_invalid_duration(duration):
    with pytest.raises(ValueError, match="duration must be positive"):
        StudySession("Python", "2026-10-07", duration)


@pytest.mark.parametrize("duration", [x for x in range(1, 5)])
def test_valid_duration(duration):
    session = StudySession("Python", "2026-10-07", duration)
    assert session.duration == duration


@pytest.mark.parametrize("topic", [""])
def test_empty_topic(topic):
    with pytest.raises(ValueError):
        StudySession(topic, "2026-10-07", 60)


@pytest.mark.parametrize("topic", [123, None, []])
def test_invalid_topic_type(topic):
    with pytest.raises(TypeError, match="topic must be a string"):
        StudySession(topic, "2026-10-07", 60)

def test_get_duration_right_return():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    time_sum = get_duration(session)
    assert time_sum == (60+40+45+20)


def test_get_duration_empty_list():
    result = get_duration([])
    assert result == 0


def test_get_duration_by_date_right_return():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    time_sum = get_duration_by_date(session)
    assert time_sum == {
        "2026-10-08": 100,
        "2026-10-07": 45,
        "2026-10-06": 20,
    }


def test_get_duration_by_date_empty_list():
    assert get_duration_by_date([]) == {}


def test_filter_sessions_by_topic():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    expected_sessions = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python", "2026-10-06", 20)
    ]
    result = filter_sessions(session, "topic", "python")
    assert result == expected_sessions



def test_filter_sessions_by_date():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    expected_sessions = [
        StudySession("tests", "2026-10-07", 45),
    ]
    result = filter_sessions(session, "date", "2026-10-07")
    assert result == expected_sessions


def test_filter_sessions_by_duration():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    expected_sessions = [
        StudySession("tests", "2026-10-07", 45),
    ]
    result = filter_sessions(session, "duration", 45)
    assert result == expected_sessions


def test_filter_sessions_empty_list():
    session = []
    assert filter_sessions(session, "duration", 45) == []


def test_filter_sessions_empty_result():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    result = filter_sessions(session, "duration", 50)
    assert result == []


def test_filter_sessions_invalid_choice():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    with pytest.raises(ValueError):
        filter_sessions(session, "bobik", "python")


def test_filter_sessions_invalid_duration():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    with pytest.raises(ValueError):
        filter_sessions(session, "duration", "abc")


def test_filter_sessions_invalid_topic():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    with pytest.raises(TypeError):
        filter_sessions(session, "topic", 123)


def test_filter_sessions_invalid_date():
    session = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    with pytest.raises(TypeError):
        filter_sessions(session, "date", 123)



@pytest.mark.parametrize(
    "duration, expected",
    [
        ("45", 45),
        (45, 45),
        ("abc", None),
        (0, None),
        (-10, None),
        ([], None),
        (None, None),
    ],
)
def test_validate_duration(duration, expected):
    result = validate_duration(duration)

    assert result == expected


def test_save_and_load_sessions_round_trip(tmp_path):
    sessions = [
        StudySession("python", "2026-10-08", 60),
        StudySession("python2", "2026-10-08", 40),
        StudySession("tests", "2026-10-07", 45),
        StudySession("python", "2026-10-06", 20)
    ]
    test_file = tmp_path / "test_sessions.json"
    save_sessions(sessions, test_file)
    new_sessions = load_sessions(test_file)
    assert new_sessions == sessions


def test_load_broken_json(tmp_path):
    broken_file = tmp_path / "broken.json"
    with open(broken_file, 'w', encoding="utf-8") as file:
        file.write(
            """
            [
                {
                    "topic": "Python",
                    "date": "2026-08-20"
                    "duration": 80,
                    "note": ""
                },
                {
                    "topic": "",
                    "date": "2026-10-04",
                    "duration": 10,
                    "note": "no"
                }
            ]
            """
        )
    result = load_sessions(broken_file)
    assert result is None


def test_load_invalid_sessions(tmp_path):
    broken_file = tmp_path / "invalid.json"
    with open(broken_file, 'w', encoding="utf-8") as file:
        file.write(
            """
            [
                {
                    "topic": "Python",
                    "date": "2026-08-20",
                    "duration": 80,
                    "note": ""
                },
                {
                    "topic": "",
                    "date": "2026-10-04",
                    "duration": 10,
                    "note": "no"
                }
            ]
            """
        )
    result = load_sessions(broken_file)
    assert result == [StudySession("Python", "2026-08-20", 80)]
