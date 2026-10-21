import pytest

from students import add_student, find_student, sort_students


def test_add_student_gives_next_id():
    students = {1: {"id": 1, "name": "Иван", "group": "А", "email": ""}}
    student = add_student(students, "Мария", "Б")
    assert student["id"] == 2
    assert 2 in students


def test_add_student_with_empty_name_fails():
    with pytest.raises(ValueError):
        add_student({}, "   ", "ИКБО-01-24")


def test_find_student():
    students = {}
    add_student(students, "Иван Петров", "ИКБО-01-24")
    assert find_student(students, 1)["name"] == "Иван Петров"
    assert find_student(students, 99) is None


def test_sort_students_by_group_and_name():
    students = {}
    add_student(students, "Яна", "ИКБО-02")
    add_student(students, "Борис", "ИКБО-01")
    add_student(students, "Анна", "ИКБО-02")
    names = [student["name"] for student in sort_students(students)]
    assert names == ["Борис", "Анна", "Яна"]
