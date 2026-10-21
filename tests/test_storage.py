from datetime import date

import pytest

from models.courseworks import Coursework
from models.students import Student
from models.teachers import Teacher
from storage import (
    load_courseworks,
    load_students,
    load_teachers,
    read_json,
    save_courseworks,
    save_students,
    save_teachers,
)


def test_missing_file_gives_empty_list(tmp_path):
    assert read_json(tmp_path / "nothing.json") == []


def test_broken_file_raises_value_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{ не json", encoding="utf-8")
    with pytest.raises(ValueError):
        read_json(path)


def test_save_and_load_roundtrip(tmp_path):
    student = Student(1, "Иван Петров", "ИКБО-01-24", "petrov@edu.ru")
    teacher = Teacher(1, "Смирнова А. С.", "Кафедра ИП", "", 3)
    coursework = Coursework(1, "Тема", student, teacher, date(2026, 12, 20))

    save_students([student], tmp_path / "students.json")
    save_teachers([teacher], tmp_path / "teachers.json")
    save_courseworks([coursework], tmp_path / "courseworks.json")

    students = load_students(tmp_path / "students.json")
    teachers = load_teachers(tmp_path / "teachers.json")
    courseworks = load_courseworks(
        students, teachers, tmp_path / "courseworks.json"
    )

    loaded = courseworks[0]
    assert loaded.title == "Тема"
    assert loaded.deadline == date(2026, 12, 20)
    assert loaded.student is students[0]
    assert loaded.teacher is teachers[0]


def test_project_data_loads():
    students = load_students()
    teachers = load_teachers()
    courseworks = load_courseworks(students, teachers)
    assert len(students) > 0
    assert len(teachers) > 0
    assert len(courseworks) > 0
