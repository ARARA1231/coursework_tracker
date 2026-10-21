import pytest

from models.teachers import Teacher, add_teacher, find_teacher


def test_teacher_has_free_slots():
    teacher = Teacher(1, "Смирнова А. С.", "Кафедра ИП", max_students=2)
    assert teacher.has_free_slots(1) is True
    assert teacher.has_free_slots(2) is False


def test_teacher_free_slots_never_negative():
    teacher = Teacher(1, "Смирнова А. С.", "Кафедра ИП", max_students=2)
    assert teacher.free_slots(0) == 2
    assert teacher.free_slots(5) == 0


def test_teacher_limit_must_be_positive():
    with pytest.raises(ValueError):
        Teacher(1, "Смирнова А. С.", "Кафедра ИП", max_students=0)


def test_add_and_find_teacher():
    teachers = []
    teacher = add_teacher(teachers, "Волков С. П.", "Кафедра ИС", "", 3)
    assert teacher.id == 1
    assert find_teacher(teachers, 1) is teacher
    assert find_teacher(teachers, 2) is None
