import pytest

from teachers import add_teacher, can_take_student, find_teacher


def test_can_take_student():
    assert can_take_student(3, 5) is True
    assert can_take_student(5, 5) is False


def test_add_and_find_teacher():
    teachers = {}
    teacher = add_teacher(teachers, "Волков С. П.", "Кафедра ИС", "", 3)
    assert teacher["id"] == 1
    assert find_teacher(teachers, 1) is teacher
    assert find_teacher(teachers, 2) is None


def test_teacher_limit_must_be_positive():
    with pytest.raises(ValueError):
        add_teacher({}, "Волков С. П.", "Кафедра ИС", "", 0)
