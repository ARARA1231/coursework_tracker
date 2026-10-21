import pytest

from models.students import Student, add_student, find_student, sort_students


def test_student_str():
    student = Student(1, "Иван Петров", "ИКБО-01-24")
    assert str(student) == "Иван Петров (ИКБО-01-24)"


def test_add_student_gives_next_id():
    students = [Student(1, "Иван Петров", "ИКБО-01-24")]
    student = add_student(students, "Мария Соколова", "ИКБО-02-24")
    assert student.id == 2
    assert len(students) == 2


def test_add_student_with_empty_name_fails():
    with pytest.raises(ValueError):
        add_student([], "   ", "ИКБО-01-24")


def test_find_student():
    students = [Student(1, "Иван", "А"), Student(2, "Мария", "Б")]
    assert find_student(students, 2).name == "Мария"
    assert find_student(students, 99) is None


def test_sort_students_by_group_and_name():
    students = [
        Student(1, "Яна", "ИКБО-02"),
        Student(2, "Борис", "ИКБО-01"),
        Student(3, "Анна", "ИКБО-02"),
    ]
    names = [student.name for student in sort_students(students)]
    assert names == ["Борис", "Анна", "Яна"]
