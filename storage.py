"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
STUDENTS_FILE = DATA_DIR / "students.json"
TEACHERS_FILE = DATA_DIR / "teachers.json"
COURSEWORKS_FILE = DATA_DIR / "courseworks.json"


def read_json(path: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет — возвращается пустой список.
    Если файл повреждён — выбрасывается ValueError.
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


def load_students(path: Path = STUDENTS_FILE) -> dict[int, dict]:
    """Загрузить студентов в словарь {id: данные}."""
    return {record["id"]: record for record in read_json(path)}


def save_students(
    students: dict[int, dict], path: Path = STUDENTS_FILE
) -> None:
    """Сохранить словарь студентов."""
    write_json(path, list(students.values()))


def load_teachers(path: Path = TEACHERS_FILE) -> dict[int, dict]:
    """Загрузить преподавателей в словарь {id: данные}."""
    return {record["id"]: record for record in read_json(path)}


def save_teachers(
    teachers: dict[int, dict], path: Path = TEACHERS_FILE
) -> None:
    """Сохранить словарь преподавателей."""
    write_json(path, list(teachers.values()))


def load_courseworks(path: Path = COURSEWORKS_FILE) -> list[dict]:
    """Загрузить курсовые работы. Дата срока превращается в date."""
    courseworks = read_json(path)
    for coursework in courseworks:
        coursework["deadline"] = date.fromisoformat(coursework["deadline"])
    return courseworks


def save_courseworks(
    courseworks: list[dict], path: Path = COURSEWORKS_FILE
) -> None:
    """Сохранить курсовые работы. Дата записывается строкой."""
    records = [
        {**coursework, "deadline": coursework["deadline"].isoformat()}
        for coursework in courseworks
    ]
    write_json(path, records)
