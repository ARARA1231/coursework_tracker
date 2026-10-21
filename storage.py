"""Загрузка и сохранение данных в JSON: JSON -> объекты и объекты -> JSON."""

import json
from datetime import date
from pathlib import Path

from models.courseworks import Coursework
from models.students import Student, find_student
from models.teachers import Teacher, find_teacher

DATA_DIR = Path(__file__).resolve().parent / "data"
STUDENTS_FILE = DATA_DIR / "students.json"
TEACHERS_FILE = DATA_DIR / "teachers.json"
COURSEWORKS_FILE = DATA_DIR / "courseworks.json"


def read_json(path: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет — возвращается пустой список.
    Если файл повреждён — выбрасывается ValueError с понятным сообщением.
    """
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Файл {path.name} повреждён: {error}") from error


def write_json(path: Path, records: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_students(path: Path = STUDENTS_FILE) -> list[Student]:
    """Загрузить студентов и превратить записи в объекты Student."""
    return [
        Student(
            student_id=record["id"],
            name=record["name"],
            group=record["group"],
            email=record.get("email", ""),
        )
        for record in read_json(path)
    ]


def save_students(
    students: list[Student], path: Path = STUDENTS_FILE
) -> None:
    """Сохранить объекты Student в JSON."""
    records = [
        {
            "id": student.id,
            "name": student.name,
            "group": student.group,
            "email": student.email,
        }
        for student in students
    ]
    write_json(path, records)


def load_teachers(path: Path = TEACHERS_FILE) -> list[Teacher]:
    """Загрузить преподавателей и превратить записи в объекты Teacher."""
    return [
        Teacher(
            teacher_id=record["id"],
            name=record["name"],
            department=record["department"],
            email=record.get("email", ""),
            max_students=record.get("max_students", 5),
        )
        for record in read_json(path)
    ]


def save_teachers(
    teachers: list[Teacher], path: Path = TEACHERS_FILE
) -> None:
    """Сохранить объекты Teacher в JSON."""
    records = [
        {
            "id": teacher.id,
            "name": teacher.name,
            "department": teacher.department,
            "email": teacher.email,
            "max_students": teacher.max_students,
        }
        for teacher in teachers
    ]
    write_json(path, records)


def load_courseworks(
    students: list[Student],
    teachers: list[Teacher],
    path: Path = COURSEWORKS_FILE,
) -> list[Coursework]:
    """Загрузить курсовые работы.

    В JSON хранятся student_id и teacher_id, а в объекте Coursework —
    ссылки на сами объекты Student и Teacher.
    """
    courseworks = []
    for record in read_json(path):
        student = find_student(students, record["student_id"])
        teacher = find_teacher(teachers, record["teacher_id"])
        if student is None or teacher is None:
            raise ValueError(
                f"Курсовая работа {record['id']} ссылается "
                "на несуществующего студента или преподавателя"
            )
        courseworks.append(
            Coursework(
                coursework_id=record["id"],
                title=record["title"],
                student=student,
                teacher=teacher,
                deadline=date.fromisoformat(record["deadline"]),
                status=record["status"],
                grade=record.get("grade"),
            )
        )
    return courseworks


def save_courseworks(
    courseworks: list[Coursework], path: Path = COURSEWORKS_FILE
) -> None:
    """Сохранить объекты Coursework в JSON (ссылки -> id)."""
    records = [
        {
            "id": coursework.id,
            "title": coursework.title,
            "student_id": coursework.student.id,
            "teacher_id": coursework.teacher.id,
            "deadline": coursework.deadline.isoformat(),
            "status": coursework.status,
            "grade": coursework.grade,
        }
        for coursework in courseworks
    ]
    write_json(path, records)


def load_all() -> tuple[list[Student], list[Teacher], list[Coursework]]:
    """Загрузить все данные проекта одним вызовом."""
    students = load_students()
    teachers = load_teachers()
    courseworks = load_courseworks(students, teachers)
    return students, teachers, courseworks
