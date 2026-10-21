from datetime import date

import pytest

from models.courseworks import (
    STATUS_DEFENDED,
    STATUS_ON_REVIEW,
    Coursework,
    count_active_for_teacher,
    create_coursework,
    get_deadline_message,
)
from models.students import Student
from models.teachers import Teacher


@pytest.fixture
def student():
    return Student(1, "Иван Петров", "ИКБО-01-24")


@pytest.fixture
def teacher():
    return Teacher(1, "Смирнова А. С.", "Кафедра ИП", max_students=1)


def test_coursework_links_objects(student, teacher):
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))
    assert coursework.student is student
    assert coursework.teacher is teacher
    assert coursework.is_active is True


def test_full_status_cycle(student, teacher):
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))
    coursework.submit()
    assert coursework.status == STATUS_ON_REVIEW
    coursework.defend(5)
    assert coursework.status == STATUS_DEFENDED
    assert coursework.grade == 5
    assert coursework.is_active is False


def test_cannot_defend_without_review(student, teacher):
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))
    with pytest.raises(ValueError):
        coursework.defend(5)


def test_grade_out_of_range(student, teacher):
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))
    coursework.submit()
    with pytest.raises(ValueError):
        coursework.defend(7)


def test_days_left(student, teacher):
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))
    assert coursework.days_left(date(2026, 12, 10)) == 10


def test_deadline_messages():
    assert get_deadline_message(-3) == "Срок сдачи прошёл 3 дн. назад"
    assert get_deadline_message(0) == "Сегодня последний день сдачи"
    assert "срок близко" in get_deadline_message(5)


def test_student_can_have_only_one_active_work(student):
    teacher = Teacher(1, "Смирнова А. С.", "Кафедра ИП", max_students=5)
    courseworks = []
    create_coursework(courseworks, "Тема 1", student, teacher, date.today())
    with pytest.raises(ValueError):
        create_coursework(
            courseworks, "Тема 2", student, teacher, date.today()
        )


def test_teacher_limit_is_respected(student, teacher):
    other = Student(2, "Мария Соколова", "ИКБО-01-24")
    courseworks = []
    create_coursework(courseworks, "Тема 1", student, teacher, date.today())
    assert count_active_for_teacher(courseworks, teacher) == 1
    with pytest.raises(ValueError):
        create_coursework(courseworks, "Тема 2", other, teacher, date.today())


def test_defended_work_frees_teacher_slot(student, teacher):
    other = Student(2, "Мария Соколова", "ИКБО-01-24")
    courseworks = []
    first = create_coursework(
        courseworks, "Тема 1", student, teacher, date.today()
    )
    first.submit()
    first.defend(4)
    second = create_coursework(
        courseworks, "Тема 2", other, teacher, date.today()
    )
    assert second.id == 2
