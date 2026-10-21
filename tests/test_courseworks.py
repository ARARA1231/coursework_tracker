from datetime import date

import pytest

from courseworks import (
    STATUS_DEFENDED,
    STATUS_ON_REVIEW,
    change_status,
    create_coursework,
    days_until_deadline,
    get_deadline_message,
)


@pytest.fixture
def teacher():
    return {"id": 1, "name": "Смирнова А. С.", "max_students": 1}


def test_days_until_deadline():
    assert days_until_deadline(date(2026, 12, 20), date(2026, 12, 10)) == 10


def test_deadline_messages():
    assert get_deadline_message(-3) == "Срок сдачи прошёл 3 дн. назад"
    assert get_deadline_message(0) == "Сегодня последний день сдачи"
    assert "срок близко" in get_deadline_message(5)


def test_student_can_have_only_one_active_work():
    teacher = {"id": 1, "name": "Смирнова А. С.", "max_students": 5}
    courseworks = []
    create_coursework(courseworks, teacher, 1, "Тема 1", date.today())
    with pytest.raises(ValueError):
        create_coursework(courseworks, teacher, 1, "Тема 2", date.today())


def test_teacher_limit_is_respected(teacher):
    courseworks = []
    create_coursework(courseworks, teacher, 1, "Тема 1", date.today())
    with pytest.raises(ValueError):
        create_coursework(courseworks, teacher, 2, "Тема 2", date.today())


def test_status_cycle_and_grade(teacher):
    courseworks = []
    coursework = create_coursework(
        courseworks, teacher, 1, "Тема", date.today()
    )
    change_status(coursework, STATUS_ON_REVIEW)
    change_status(coursework, STATUS_DEFENDED, grade=5)
    assert coursework["status"] == STATUS_DEFENDED
    assert coursework["grade"] == 5


def test_cannot_skip_review(teacher):
    coursework = create_coursework([], teacher, 1, "Тема", date.today())
    with pytest.raises(ValueError):
        change_status(coursework, STATUS_DEFENDED, grade=5)
